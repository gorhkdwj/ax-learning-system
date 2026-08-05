#!/usr/bin/env python
"""선택적 Vault의 private source manifest와 원본 파일을 검증합니다.

공개 저장소는 Vault가 없어도 동작해야 하므로 Vault 디렉터리가 없으면 성공으로
건너뜁니다. Vault가 있으면 sources/ 전체를 순회하며 source.json의 스키마,
상대경로, 파일 크기와 SHA-256을 읽기 전용으로 확인합니다. PDF 페이지 수는
media_kind가 document(미지정 포함)인 파일에만 확인하며, transcript·frame·
audio·video는 크기와 해시만 확인합니다. captured_at_seconds와
duration_seconds는 사람이 기록한 참고값으로 다루고 파일에서 실제 재생시간을
추출하지 않습니다. 외부 도구 의존을 늘리지 않기 위한 결정입니다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from tools.workspace_paths import resolve_vault_root
except ModuleNotFoundError:  # 직접 `python tools/...py`로 실행할 때
    from workspace_paths import resolve_vault_root


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "private-source-manifest.schema.json"
)

# media_kind별로 manifest에 반드시 기록해야 하는 참고값입니다. 스키마가 먼저
# 강제하지만, 스키마 개정으로 계약이 느슨해져도 검증기가 지키도록 이중으로
# 확인합니다.
REQUIRED_MEDIA_FIELDS = {
    "frame": "captured_at_seconds",
    "audio": "duration_seconds",
    "video": "duration_seconds",
}


@dataclass(frozen=True)
class PrivateSourceIssue:
    code: str
    path: Path
    message: str

    def render(self, vault_root: Path) -> str:
        try:
            display_path = self.path.resolve().relative_to(vault_root.resolve())
        except ValueError:
            display_path = Path("<outside-vault>")
        return f"PRIVATE_SOURCE_ERROR|{self.code}|{display_path.as_posix()}|{self.message}"


@dataclass
class PrivateSourceReport:
    skipped: bool = False
    manifest_count: int = 0
    file_count: int = 0
    unavailable_file_count: int = 0
    issues: list[PrivateSourceIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _pdf_page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency failure path
        raise RuntimeError(
            "PDF 페이지 검증에는 requirements-dev.txt의 pypdf가 필요합니다."
        ) from exc
    return len(PdfReader(path).pages)


class PrivateSourceValidator:
    def __init__(self, schema_path: Path = SCHEMA_PATH) -> None:
        with schema_path.open("r", encoding="utf-8") as stream:
            self.schema: dict[str, Any] = json.load(stream)
        Draft202012Validator.check_schema(self.schema)
        self.validator = Draft202012Validator(
            self.schema,
            format_checker=FormatChecker(),
        )

    def validate(
        self,
        vault_root: Path,
        *,
        require_files: bool = False,
    ) -> PrivateSourceReport:
        root = vault_root.resolve()
        report = PrivateSourceReport()
        if not root.is_dir():
            report.skipped = True
            return report

        # documents만 보던 범위를 sources 전체로 넓혀 media와 articles도
        # 검증 대상에 포함합니다. 기존 documents 경로는 그대로 포함됩니다.
        sources_root = root / "sources"
        manifests = (
            sorted(sources_root.rglob("source.json"))
            if sources_root.is_dir()
            else []
        )
        for manifest_path in manifests:
            report.manifest_count += 1
            self._validate_manifest(
                root,
                manifest_path,
                report,
                require_files=require_files,
            )
        return report

    def _validate_manifest(
        self,
        vault_root: Path,
        manifest_path: Path,
        report: PrivateSourceReport,
        *,
        require_files: bool,
    ) -> None:
        try:
            with manifest_path.open("r", encoding="utf-8") as stream:
                data = json.load(stream)
        except (OSError, json.JSONDecodeError) as exc:
            report.issues.append(
                PrivateSourceIssue("MANIFEST_PARSE", manifest_path, str(exc))
            )
            return

        schema_errors = sorted(
            self.validator.iter_errors(data),
            key=lambda error: [str(part) for part in error.absolute_path],
        )
        for error in schema_errors:
            location = "$" + "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}"
                for part in error.absolute_path
            )
            report.issues.append(
                PrivateSourceIssue(
                    "SCHEMA_ERROR",
                    manifest_path,
                    f"{location}: {error.message}",
                )
            )
        if schema_errors or not isinstance(data, dict):
            return

        files = data.get("files", [])
        expected_count = data.get("selection", {}).get("expected_file_count")
        if expected_count != len(files):
            report.issues.append(
                PrivateSourceIssue(
                    "FILE_COUNT_MISMATCH",
                    manifest_path,
                    f"expected={expected_count}, manifest={len(files)}",
                )
            )

        self._check_duplicates(
            [item.get("id") for item in files],
            "DUPLICATE_FILE_ID",
            manifest_path,
            report,
        )
        self._check_duplicates(
            [item.get("path") for item in files],
            "DUPLICATE_FILE_PATH",
            manifest_path,
            report,
        )

        package_root = manifest_path.parent.resolve()
        safe_declared_paths = []
        for item in files:
            relative_path = item.get("path")
            if not isinstance(relative_path, str):
                continue
            path = (package_root / relative_path).resolve()
            if path != package_root and package_root in path.parents:
                safe_declared_paths.append(path)
        manifest_only = (
            not require_files
            and bool(safe_declared_paths)
            and not any(path.is_file() for path in safe_declared_paths)
        )
        for item in files:
            self._validate_file(
                vault_root,
                package_root,
                item,
                report,
                allow_missing=manifest_only,
            )

    @staticmethod
    def _check_duplicates(
        values: list[Any],
        code: str,
        path: Path,
        report: PrivateSourceReport,
    ) -> None:
        seen: set[Any] = set()
        for value in values:
            if value in seen:
                report.issues.append(
                    PrivateSourceIssue(code, path, f"중복 값: {value}")
                )
            seen.add(value)

    def _validate_file(
        self,
        vault_root: Path,
        package_root: Path,
        item: dict[str, Any],
        report: PrivateSourceReport,
        *,
        allow_missing: bool,
    ) -> None:
        relative_path = item.get("path")
        if not isinstance(relative_path, str):
            return
        # media_kind 미지정은 기존 manifest와의 하위호환을 위해 document로
        # 해석합니다.
        media_kind = item.get("media_kind", "document")
        required_media_field = REQUIRED_MEDIA_FIELDS.get(media_kind)
        if required_media_field is not None and required_media_field not in item:
            report.issues.append(
                PrivateSourceIssue(
                    "MEDIA_FIELD_MISSING",
                    package_root / "source.json",
                    f"media_kind={media_kind} 파일에는 "
                    f"{required_media_field}가 필요합니다.",
                )
            )
        path = (package_root / relative_path).resolve()
        if path == package_root or package_root not in path.parents:
            report.issues.append(
                PrivateSourceIssue(
                    "PATH_ESCAPE",
                    package_root / "source.json",
                    "파일 경로가 원천 패키지 밖을 가리킵니다.",
                )
            )
            return
        if not path.is_file():
            if allow_missing:
                report.unavailable_file_count += 1
                return
            report.issues.append(
                PrivateSourceIssue("FILE_NOT_FOUND", path, "원천 파일이 없습니다.")
            )
            return

        report.file_count += 1
        actual_size = path.stat().st_size
        if actual_size != item.get("size_bytes"):
            report.issues.append(
                PrivateSourceIssue(
                    "SIZE_MISMATCH",
                    path,
                    f"expected={item.get('size_bytes')}, actual={actual_size}",
                )
            )

        actual_hash = _sha256(path)
        if actual_hash != item.get("sha256"):
            report.issues.append(
                PrivateSourceIssue(
                    "CHECKSUM_MISMATCH",
                    path,
                    f"expected={item.get('sha256')}, actual={actual_hash}",
                )
            )

        # 페이지 수 검증은 document에만 해당합니다. 나머지 미디어는 크기와
        # SHA-256만 확인하며 재생시간은 manifest의 참고값을 그대로 신뢰합니다.
        if media_kind != "document":
            return

        try:
            actual_pages = _pdf_page_count(path)
        except Exception as exc:  # pypdf reports malformed or encrypted PDFs here
            report.issues.append(
                PrivateSourceIssue("PAGE_COUNT_FAILED", path, str(exc))
            )
            return
        if actual_pages != item.get("page_count"):
            report.issues.append(
                PrivateSourceIssue(
                    "PAGE_COUNT_MISMATCH",
                    path,
                    f"expected={item.get('page_count')}, actual={actual_pages}",
                )
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="선택적 Vault의 private source manifest를 검증합니다."
    )
    parser.add_argument(
        "--vault-root",
        default=None,
        help="AX_VAULT_ROOT를 대체할 선택적 Vault 경로입니다.",
    )
    parser.add_argument(
        "--require-files",
        action="store_true",
        help="manifest만 있는 clone을 허용하지 않고 모든 원천 파일을 요구합니다.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        vault_root = resolve_vault_root(args.vault_root)
        report = PrivateSourceValidator().validate(
            vault_root,
            require_files=args.require_files,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"PRIVATE_SOURCE_ERROR|INITIALIZATION|<config>|{exc}")
        return 2

    if report.skipped:
        print(
            "PRIVATE_SOURCE_SUMMARY|status=skipped|reason=vault_unavailable|"
            "manifests=0|files=0|unavailable_files=0|errors=0"
        )
        return 0

    for issue in report.issues:
        print(issue.render(vault_root))
    if report.is_valid and report.unavailable_file_count:
        status = "manifest_only"
    else:
        status = "passed" if report.is_valid else "failed"
    print(
        "PRIVATE_SOURCE_SUMMARY|"
        f"status={status}|"
        f"manifests={report.manifest_count}|files={report.file_count}|"
        f"unavailable_files={report.unavailable_file_count}|"
        f"errors={len(report.issues)}"
    )
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
