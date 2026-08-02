"""공개 저장소에 명백한 비공개·대용량 항목이 유입되지 않았는지 검사합니다."""

from __future__ import annotations

import re
from pathlib import Path


PUBLIC_ROOT = Path(__file__).resolve().parents[1]
MAX_PUBLIC_FILE_BYTES = 90 * 1024 * 1024
FORBIDDEN_TOP_LEVEL = {
    ".remember",
    "0.AI_Agent",
    "articles",
    "ax-learning-vault",
    "embeddings",
    "generated-private",
    "original-articles",
    "private",
    "source-materials",
}
FORBIDDEN_FILE_NAMES = {
    ".env",
    ".env.local",
    "id_rsa",
    "id_ed25519",
}
FORBIDDEN_PUBLIC_SUFFIXES = {
    ".docx",
    ".pdf",
    ".pptx",
    ".zip",
}
PUBLIC_CONTENT_ROOTS = {
    "catalog",
    "docs",
    "sets",
    "taxonomy",
}
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
}
LOCAL_ABSOLUTE_PATH = re.compile(
    r"(?i)(?:(?<![A-Za-z0-9])[A-Z]:[\\/]|file://)"
)
IGNORED_WALK_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def collect_issues() -> list[str]:
    issues: list[str] = []

    for name in sorted(FORBIDDEN_TOP_LEVEL):
        if (PUBLIC_ROOT / name).exists():
            issues.append(f"forbidden public path: {name}")

    for path in PUBLIC_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(PUBLIC_ROOT)
        if any(part in IGNORED_WALK_PARTS for part in relative.parts):
            continue
        if path.name in FORBIDDEN_FILE_NAMES:
            issues.append(f"forbidden local file: {relative.as_posix()}")
        if path.suffix.lower() in FORBIDDEN_PUBLIC_SUFFIXES:
            issues.append(f"forbidden public binary: {relative.as_posix()}")
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            issues.append(
                "oversized public file: "
                f"{relative.as_posix()} ({path.stat().st_size} bytes)"
            )
        if (
            relative.parts
            and relative.parts[0] in PUBLIC_CONTENT_ROOTS
            and path.suffix.lower() in TEXT_SUFFIXES
        ):
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if LOCAL_ABSOLUTE_PATH.search(content):
                issues.append(
                    f"local absolute path in public content: {relative.as_posix()}"
                )

    return issues


def main() -> int:
    issues = collect_issues()
    if issues:
        for issue in issues:
            print(f"PUBLIC_BOUNDARY_ERROR|{issue}")
        print(f"PUBLIC_BOUNDARY_SUMMARY|errors={len(issues)}")
        return 1

    print("PUBLIC_BOUNDARY_SUMMARY|errors=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
