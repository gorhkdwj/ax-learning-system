#!/usr/bin/env python
"""AX 학습 메타데이터 카탈로그를 검증합니다.

JSON Schema가 개별 파일의 구조를 검사하고, 이 검증기는 여러 파일 사이의
참조·버전·소유관계·DAG·로컬 경로와 생명주기 규칙을 검사합니다.
검증기는 메타데이터를 수정하지 않으며 읽기 전용으로 동작합니다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


SCHEMA_FILES = {
    "unit": "learning-unit.schema.json",
    "resource": "learning-resource.schema.json",
    "set": "learning-set.schema.json",
    "study": "learning-study.schema.json",
    "signal": "trend-signal.schema.json",
    "candidate": "capability-candidate.schema.json",
    "handoff": "phase2-handoff.schema.json",
    "taxonomy": "capability-taxonomy.schema.json",
}

METADATA_FILENAMES = {
    "unit.json": "unit",
    "resource.json": "resource",
    "set.json": "set",
    "study.json": "study",
    "signal.json": "signal",
    "candidate.json": "candidate",
    "handoff.json": "handoff",
    "taxonomy.json": "taxonomy",
}

# `examples/valid`는 검증기 자체를 확인하는 가상 표본이며 기본 검증 범위에
# 포함됩니다. 실제 카탈로그 규모와 구분해 보고하기 위한 접두 경로입니다.
EXAMPLES_PREFIX = ("examples", "valid")

LEVEL_ORDER = {
    "D0": 0,
    "D1": 1,
    "D2": 2,
    "D3": 3,
    "D4": 4,
}

ERROR = "ERROR"
WARNING = "WARNING"


@dataclass(frozen=True)
class Issue:
    """사람과 자동화가 함께 읽을 수 있는 검증 결과 한 건입니다."""

    severity: str
    code: str
    path: Path
    message: str

    def render(self, workspace_root: Path) -> str:
        try:
            display_path = self.path.resolve().relative_to(workspace_root.resolve())
        except ValueError:
            display_path = self.path
        return f"{self.severity}|{self.code}|{display_path.as_posix()}|{self.message}"


@dataclass
class Record:
    """파싱된 메타데이터와 원본 파일을 연결합니다."""

    kind: str
    path: Path
    data: dict[str, Any]

    @property
    def id(self) -> str | None:
        value = self.data.get("id")
        return value if isinstance(value, str) else None

    @property
    def version(self) -> str | None:
        value = self.data.get("version")
        return value if isinstance(value, str) else None

    @property
    def key(self) -> tuple[str, str] | None:
        if self.id is None or self.version is None:
            return None
        return (self.id, self.version)


def _empty_counts() -> dict[str, int]:
    return {kind: 0 for kind in METADATA_FILENAMES.values()}


@dataclass
class ValidationReport:
    """검증 결과와 처리한 파일 수를 보관합니다.

    `counts`는 검사한 모든 파일이고 `example_counts`는 그중 `examples/valid`의
    가상 표본입니다. 표본은 검증기 자체를 확인하려고 기본 검증 범위에 넣은
    것이므로 실제 카탈로그 규모와 구분해서 보고합니다.
    """

    issues: list[Issue] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=_empty_counts)
    example_counts: dict[str, int] = field(default_factory=_empty_counts)

    def real_counts(self) -> dict[str, int]:
        """예제를 제외한 실제 카탈로그 집계입니다."""
        return {
            kind: value - self.example_counts.get(kind, 0)
            for kind, value in self.counts.items()
        }

    @property
    def error_count(self) -> int:
        return sum(issue.severity == ERROR for issue in self.issues)

    @property
    def warning_count(self) -> int:
        return sum(issue.severity == WARNING for issue in self.issues)

    @property
    def is_valid(self) -> bool:
        return self.error_count == 0


class CatalogValidator:
    """AX 카탈로그, Trend Signal과 조사 Candidate를 함께 검증합니다."""

    def __init__(
        self,
        workspace_root: Path,
        schema_dir: Path,
        today: date | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.schema_dir = schema_dir.resolve()
        self.today = today or date.today()
        self.schemas = self._load_schemas()

    def _load_schemas(self) -> dict[str, dict[str, Any]]:
        schemas: dict[str, dict[str, Any]] = {}
        for kind, filename in SCHEMA_FILES.items():
            path = self.schema_dir / filename
            with path.open("r", encoding="utf-8") as stream:
                schema = json.load(stream)
            Draft202012Validator.check_schema(schema)
            schemas[kind] = schema
        return schemas

    def validate(self, roots: Iterable[Path]) -> ValidationReport:
        report = ValidationReport()
        records = self._discover_and_validate_files(roots, report)

        indexes: dict[str, dict[tuple[str, str], Record]] = {
            "unit": {},
            "resource": {},
            "set": {},
            "study": {},
            "signal": {},
            "candidate": {},
            "handoff": {},
            "taxonomy": {},
        }
        self._build_indexes(records, indexes, report)
        self._validate_lifecycle(records, report)
        self._validate_references(records, indexes, report)
        self._validate_supersession(indexes, report)
        self._validate_unit_dag(indexes["unit"], report)
        self._validate_set_dags_and_prerequisites(indexes, report)
        self._validate_taxonomy_registry(indexes, report)
        self._validate_signal_registry(indexes, report)
        self._validate_candidate_registry(indexes, report)
        self._validate_candidate_relation_dag(indexes["candidate"], report)
        self._validate_handoff_registry(indexes, report)

        return report

    def _discover_and_validate_files(
        self,
        roots: Iterable[Path],
        report: ValidationReport,
    ) -> list[Record]:
        paths: set[Path] = set()
        for root in roots:
            resolved = root if root.is_absolute() else self.workspace_root / root
            resolved = resolved.resolve()
            if not resolved.exists():
                report.issues.append(
                    Issue(ERROR, "ROOT_NOT_FOUND", resolved, "검증 대상 경로가 없습니다.")
                )
                continue
            if resolved.is_file():
                if resolved.name in METADATA_FILENAMES:
                    paths.add(resolved)
                else:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "UNSUPPORTED_METADATA_FILE",
                            resolved,
                            (
                                "파일명은 unit.json, resource.json, set.json, study.json, "
                                "signal.json, candidate.json, handoff.json 또는 "
                                "taxonomy.json이어야 합니다."
                            ),
                        )
                    )
                continue
            for filename in METADATA_FILENAMES:
                paths.update(resolved.rglob(filename))

        if not paths and not report.issues:
            report.issues.append(
                Issue(
                    ERROR,
                    "NO_METADATA",
                    self.workspace_root,
                    "검증할 메타데이터 파일을 찾지 못했습니다.",
                )
            )

        records: list[Record] = []
        for path in sorted(paths):
            kind = METADATA_FILENAMES[path.name]
            try:
                with path.open("r", encoding="utf-8") as stream:
                    data = json.load(stream)
            except (OSError, json.JSONDecodeError) as exc:
                report.issues.append(
                    Issue(ERROR, "JSON_PARSE_ERROR", path, str(exc))
                )
                continue

            if not isinstance(data, dict):
                report.issues.append(
                    Issue(
                        ERROR,
                        "ROOT_NOT_OBJECT",
                        path,
                        "메타데이터의 최상위 값은 JSON 객체여야 합니다.",
                    )
                )
                continue

            validator = Draft202012Validator(
                self.schemas[kind],
                format_checker=FormatChecker(),
            )
            schema_errors = sorted(
                validator.iter_errors(data),
                key=lambda error: [str(part) for part in error.absolute_path],
            )
            for error in schema_errors:
                location = "$" + "".join(
                    f"[{part}]" if isinstance(part, int) else f".{part}"
                    for part in error.absolute_path
                )
                report.issues.append(
                    Issue(
                        ERROR,
                        "SCHEMA_ERROR",
                        path,
                        f"{location}: {error.message}",
                    )
                )

            records.append(Record(kind=kind, path=path, data=data))
            report.counts[kind] += 1
            if self._is_example(path):
                report.example_counts[kind] += 1

        return records

    def _is_example(self, path: Path) -> bool:
        """가상 표본 디렉터리 안의 파일인지 판별합니다."""
        try:
            relative = path.resolve().relative_to(self.workspace_root)
        except ValueError:
            return False
        return relative.parts[: len(EXAMPLES_PREFIX)] == EXAMPLES_PREFIX

    def _build_indexes(
        self,
        records: Iterable[Record],
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        for record in records:
            if record.key is None:
                continue
            existing = indexes[record.kind].get(record.key)
            if existing is not None:
                report.issues.append(
                    Issue(
                        ERROR,
                        "DUPLICATE_ID_VERSION",
                        record.path,
                        (
                            f"{record.id}@{record.version}가 중복되었습니다. "
                            f"기존 파일: {self._display_path(existing.path)}"
                        ),
                    )
                )
                continue
            indexes[record.kind][record.key] = record

    def _validate_lifecycle(
        self,
        records: Iterable[Record],
        report: ValidationReport,
    ) -> None:
        for record in records:
            lifecycle = record.data.get("lifecycle")
            if not isinstance(lifecycle, dict):
                continue
            review_due = lifecycle.get("review_due_at")
            if isinstance(review_due, str):
                try:
                    due_date = date.fromisoformat(review_due)
                except ValueError:
                    continue
                if due_date < self.today:
                    report.issues.append(
                        Issue(
                            WARNING,
                            "REVIEW_OVERDUE",
                            record.path,
                            f"검토 예정일 {review_due}가 지났습니다.",
                        )
                    )

    def _validate_references(
        self,
        records: Iterable[Record],
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        for record in records:
            if record.kind == "unit":
                self._validate_unit_references(record, indexes, report)
            elif record.kind == "resource":
                self._validate_resource_references(record, indexes, report)
            elif record.kind == "set":
                self._validate_set_references(record, indexes, report)
            elif record.kind == "study":
                self._validate_study_references(record, indexes, report)
            elif record.kind == "signal":
                self._validate_signal_references(record, indexes, report)
            elif record.kind == "candidate":
                self._validate_candidate_references(record, indexes, report)
            elif record.kind == "handoff":
                self._validate_handoff_references(record, indexes, report)

    def _validate_unit_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        outcomes = self._list(record.data.get("learning", {}), "outcomes")
        outcome_ids = [outcome.get("id") for outcome in outcomes]
        self._report_duplicates(
            outcome_ids,
            record,
            "DUPLICATE_OUTCOME_ID",
            "학습성과 ID",
            report,
        )

        relations = self._list(record.data, "relations")
        relation_keys: list[tuple[Any, Any, Any]] = []
        for relation in relations:
            target = relation.get("target")
            target_key = self._reference_key(target)
            self._resolve("unit", target, record, "UNIT_RELATION", indexes, report)
            relation_keys.append(
                (relation.get("type"), target_key, relation.get("required_level"))
            )
            if (
                relation.get("type") == "prerequisite"
                and relation.get("required_level") not in LEVEL_ORDER
            ):
                report.issues.append(
                    Issue(
                        ERROR,
                        "PREREQUISITE_LEVEL_REQUIRED",
                        record.path,
                        "prerequisite 관계에는 명시적인 required_level이 필요합니다.",
                    )
                )
            if (
                relation.get("type") == "prerequisite"
                and target_key is not None
                and target_key[0] == record.id
            ):
                report.issues.append(
                    Issue(
                        ERROR,
                        "SELF_PREREQUISITE",
                        record.path,
                        "동일한 Unit ID의 다른 버전을 포함한 자기 선수조건은 허용하지 않습니다.",
                    )
                )
        self._report_duplicates(
            relation_keys,
            record,
            "DUPLICATE_UNIT_RELATION",
            "Unit 관계",
            report,
        )

        resource_links = self._list(record.data, "resource_refs")
        resource_keys: list[tuple[str, str] | None] = []
        resource_outcomes: set[str] = set()
        for resource_link in resource_links:
            resource_keys.append(self._reference_key(resource_link.get("resource")))
            resource = self._resolve(
                "resource",
                resource_link.get("resource"),
                record,
                "UNIT_RESOURCE",
                indexes,
                report,
            )
            if resource is not None:
                owner = resource.data.get("owner", {})
                if (
                    owner.get("kind") != "unit"
                    or owner.get("id") != record.id
                    or owner.get("version") != record.version
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "RESOURCE_OWNER_MISMATCH",
                            record.path,
                            (
                                f"{resource.id}@{resource.version}의 owner가 "
                                f"{record.id}@{record.version}가 아닙니다."
                            ),
                        )
                    )
                resource_outcomes.update(
                    outcome_id
                    for outcome_id in self._list(
                        resource.data, "learning_outcome_ids"
                    )
                    if isinstance(outcome_id, str)
                )
        self._report_duplicates(
            resource_keys,
            record,
            "DUPLICATE_UNIT_RESOURCE",
            "Unit Resource 참조",
            report,
        )

        validation = record.data.get("validation", {})
        checks = self._list(validation, "checks")
        self._report_duplicates(
            [check.get("id") for check in checks],
            record,
            "DUPLICATE_VALIDATION_CHECK",
            "검증 항목 ID",
            report,
        )
        checked_outcomes: set[str] = set()
        for check in checks:
            for outcome_id in self._list(check, "learning_outcome_ids"):
                if outcome_id not in outcome_ids:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "VALIDATION_OUTCOME_NOT_FOUND",
                            record.path,
                            f"검증 항목 {check.get('id')}의 {outcome_id}가 Unit에 없습니다.",
                        )
                    )
                elif check.get("required") is True:
                    checked_outcomes.add(outcome_id)
            if check.get("type") == "resource":
                validation_resource = self._resolve(
                    "resource",
                    check.get("resource_ref"),
                    record,
                    "VALIDATION_RESOURCE",
                    indexes,
                    report,
                )
                if validation_resource is not None:
                    owner = validation_resource.data.get("owner", {})
                    if (
                        owner.get("kind") != "unit"
                        or owner.get("id") != record.id
                        or owner.get("version") != record.version
                    ):
                        report.issues.append(
                            Issue(
                                ERROR,
                                "VALIDATION_RESOURCE_OWNER_MISMATCH",
                                record.path,
                                f"검증 Resource {validation_resource.id}@{validation_resource.version}의 owner가 현재 Unit이 아닙니다.",
                            )
                        )

        for outcome_id in outcome_ids:
            if outcome_id not in resource_outcomes:
                report.issues.append(
                    Issue(
                        ERROR,
                        "OUTCOME_WITHOUT_RESOURCE",
                        record.path,
                        f"{outcome_id}를 다루는 Resource가 없습니다.",
                    )
                )
            if outcome_id not in checked_outcomes:
                report.issues.append(
                    Issue(
                        ERROR,
                        "OUTCOME_WITHOUT_REQUIRED_CHECK",
                        record.path,
                        f"{outcome_id}를 판정하는 필수 검증 항목이 없습니다.",
                    )
                )

        status = record.data.get("lifecycle", {}).get("status")
        if status in {"active", "operational", "pilot", "scale"}:
            if not resource_links or not checks:
                report.issues.append(
                    Issue(
                        ERROR,
                        "ACTIVE_UNIT_INCOMPLETE",
                        record.path,
                        f"{status} Unit에는 Resource와 검증 항목이 모두 필요합니다.",
                    )
                )

    def _validate_resource_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        owner = record.data.get("owner")
        if isinstance(owner, dict):
            owner_kind = owner.get("kind")
            if owner_kind in {"unit", "set"}:
                owner_record = self._resolve(
                    owner_kind,
                    owner,
                    record,
                    "RESOURCE_OWNER",
                    indexes,
                    report,
                )
                if owner_record is not None:
                    owner_references: set[tuple[str, str]] = set()
                    outcome_counts: dict[str, int] = {}
                    if owner_kind == "unit":
                        owner_references.update(
                            key
                            for key in (
                                self._reference_key(link.get("resource"))
                                for link in self._list(
                                    owner_record.data, "resource_refs"
                                )
                            )
                            if key is not None
                        )
                        owner_references.update(
                            key
                            for key in (
                                self._reference_key(check.get("resource_ref"))
                                for check in self._list(
                                    owner_record.data.get("validation", {}), "checks"
                                )
                                if check.get("type") == "resource"
                            )
                            if key is not None
                        )
                        for outcome in self._list(
                            owner_record.data.get("learning", {}), "outcomes"
                        ):
                            outcome_id = outcome.get("id")
                            if isinstance(outcome_id, str):
                                outcome_counts[outcome_id] = 1
                    else:
                        owner_references.update(
                            key
                            for step in self._list(owner_record.data, "steps")
                            for key in (
                                self._reference_key(reference)
                                for reference in self._list(step, "resource_refs")
                            )
                            if key is not None
                        )
                        owner_references.update(
                            key
                            for key in (
                                self._reference_key(reference)
                                for reference in self._list(
                                    owner_record.data, "capstone_resource_refs"
                                )
                            )
                            if key is not None
                        )
                        unit_references = [
                            requirement.get("unit")
                            for requirement in self._list(
                                owner_record.data, "entry_requirements"
                            )
                        ] + [
                            step.get("unit_ref")
                            for step in self._list(owner_record.data, "steps")
                        ]
                        for unit_reference in unit_references:
                            unit_key = self._reference_key(unit_reference)
                            unit = indexes["unit"].get(unit_key)
                            if unit is None:
                                continue
                            for outcome in self._list(
                                unit.data.get("learning", {}), "outcomes"
                            ):
                                outcome_id = outcome.get("id")
                                if isinstance(outcome_id, str):
                                    outcome_counts[outcome_id] = (
                                        outcome_counts.get(outcome_id, 0) + 1
                                    )

                    if record.key not in owner_references:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "OWNER_BACKREFERENCE_MISSING",
                                record.path,
                                f"owner {owner_record.id}@{owner_record.version}가 이 Resource를 참조하지 않습니다.",
                            )
                        )
                    for outcome_id in self._list(
                        record.data, "learning_outcome_ids"
                    ):
                        count = outcome_counts.get(outcome_id, 0)
                        if count == 0:
                            report.issues.append(
                                Issue(
                                    ERROR,
                                    "UNKNOWN_OUTCOME",
                                    record.path,
                                    f"{outcome_id}가 owner 범위에 없습니다.",
                                )
                            )
                        elif count > 1:
                            report.issues.append(
                                Issue(
                                    ERROR,
                                    "AMBIGUOUS_OUTCOME",
                                    record.path,
                                    f"{outcome_id}가 owner Set의 여러 Unit에 중복됩니다.",
                                )
                            )

        accessibility = record.data.get("accessibility", {})
        for reference in self._list(accessibility, "alternative_resource_refs"):
            alternative = self._resolve(
                "resource",
                reference,
                record,
                "ACCESSIBILITY_ALTERNATIVE",
                indexes,
                report,
            )
            if alternative is not None and alternative.key == record.key:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SELF_ACCESSIBILITY_ALTERNATIVE",
                        record.path,
                        "Resource가 자기 자신을 접근성 대체자료로 참조합니다.",
                    )
                )

        location = record.data.get("location")
        if isinstance(location, dict) and location.get("kind") == "local":
            self._validate_local_path(
                location.get("path"),
                record,
                "RESOURCE_PATH",
                report,
            )

        verification = record.data.get("verification", {})
        for evidence_path in self._list(verification, "evidence_paths"):
            self._validate_local_path(
                evidence_path,
                record,
                "EVIDENCE_PATH",
                report,
            )
        if verification.get("status") == "verified":
            if not verification.get("checked_at"):
                report.issues.append(
                    Issue(
                        ERROR,
                        "VERIFICATION_DATE_REQUIRED",
                        record.path,
                        "verified Resource에는 verification.checked_at이 필요합니다.",
                    )
                )
            if not self._list(verification, "evidence_paths") and not self._list(
                verification, "commands"
            ):
                report.issues.append(
                    Issue(
                        WARNING,
                        "VERIFICATION_EVIDENCE_MISSING",
                        record.path,
                        "verified 상태이지만 증거 경로나 실행 명령이 없습니다.",
                    )
                )

    def _validate_set_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        entry_requirements = self._list(record.data, "entry_requirements")
        entry_keys = [
            self._reference_key(requirement.get("unit"))
            for requirement in entry_requirements
        ]
        self._report_duplicates(
            entry_keys,
            record,
            "DUPLICATE_ENTRY_REQUIREMENT",
            "진입 요구 Unit",
            report,
        )
        versions_by_entry_id: dict[str, set[str]] = {}
        for key in entry_keys:
            if key is not None:
                versions_by_entry_id.setdefault(key[0], set()).add(key[1])
        for unit_id, versions in versions_by_entry_id.items():
            if len(versions) > 1:
                report.issues.append(
                    Issue(
                        ERROR,
                        "CONFLICTING_ENTRY_VERSIONS",
                        record.path,
                        f"{unit_id}의 여러 버전을 동시에 진입 요구사항으로 사용합니다.",
                    )
                )

        for requirement in entry_requirements:
            self._resolve(
                "unit",
                requirement.get("unit"),
                record,
                "SET_ENTRY_UNIT",
                indexes,
                report,
            )

        for step in self._list(record.data, "steps"):
            unit = self._resolve(
                "unit",
                step.get("unit_ref"),
                record,
                "SET_STEP_UNIT",
                indexes,
                report,
            )
            step_resource_keys: list[tuple[str, str] | None] = []
            for reference in self._list(step, "resource_refs"):
                step_resource_keys.append(self._reference_key(reference))
                resource = self._resolve(
                    "resource",
                    reference,
                    record,
                    "SET_STEP_RESOURCE",
                    indexes,
                    report,
                )
                if resource is not None and unit is not None:
                    owner = resource.data.get("owner", {})
                    valid_unit_owner = (
                        owner.get("kind") == "unit"
                        and owner.get("id") == unit.id
                        and owner.get("version") == unit.version
                    )
                    valid_set_owner = (
                        owner.get("kind") == "set"
                        and owner.get("id") == record.id
                        and owner.get("version") == record.version
                    )
                    if not (valid_unit_owner or valid_set_owner):
                        report.issues.append(
                            Issue(
                                ERROR,
                                "STEP_RESOURCE_OWNER_MISMATCH",
                                record.path,
                                f"단계 {step.get('id')}의 Resource {resource.id}@{resource.version}는 단계 Unit 또는 현재 Set 소유가 아닙니다.",
                            )
                        )
            self._report_duplicates(
                step_resource_keys,
                record,
                "DUPLICATE_STEP_RESOURCE",
                f"단계 {step.get('id')} Resource 참조",
                report,
            )
            if unit is not None:
                known_gates = {
                    check.get("id")
                    for check in self._list(
                        unit.data.get("validation", {}), "checks"
                    )
                }
                gate_ids = self._list(step, "validation_gate_ids")
                self._report_duplicates(
                    gate_ids,
                    record,
                    "DUPLICATE_VALIDATION_GATE",
                    f"단계 {step.get('id')} 검증 게이트",
                    report,
                )
                for gate_id in gate_ids:
                    if gate_id not in known_gates:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "UNKNOWN_VALIDATION_GATE",
                                record.path,
                                (
                                    f"단계 {step.get('id')}의 gate {gate_id}가 "
                                    f"{unit.id}@{unit.version}에 없습니다."
                                ),
                            )
                        )

        capstone_references = self._list(record.data, "capstone_resource_refs")
        self._report_duplicates(
            [self._reference_key(reference) for reference in capstone_references],
            record,
            "DUPLICATE_CAPSTONE_RESOURCE",
            "capstone Resource 참조",
            report,
        )
        for reference in capstone_references:
            resource = self._resolve(
                "resource",
                reference,
                record,
                "SET_CAPSTONE_RESOURCE",
                indexes,
                report,
            )
            if resource is not None:
                owner = resource.data.get("owner", {})
                if (
                    owner.get("kind") != "set"
                    or owner.get("id") != record.id
                    or owner.get("version") != record.version
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "CAPSTONE_OWNER_MISMATCH",
                            record.path,
                            f"capstone {resource.id}@{resource.version}는 현재 Set 소유여야 합니다.",
                        )
                    )

        lifecycle_status = record.data.get("lifecycle", {}).get("status")
        if (
            record.data.get("set_type") in {"project", "deliverable"}
            and lifecycle_status in {"active", "operational", "pilot", "scale"}
            and not capstone_references
        ):
            report.issues.append(
                Issue(
                    ERROR,
                    "CAPSTONE_REQUIRED",
                    record.path,
                    "활성 project 또는 deliverable Set에는 capstone Resource가 필요합니다.",
                )
            )

        self._validate_set_semantics(record, report)

    def _validate_set_semantics(
        self,
        record: Record,
        report: ValidationReport,
    ) -> None:
        steps = self._list(record.data, "steps")
        highest_level = max(
            (
                LEVEL_ORDER.get(step.get("required_level"), -1)
                for step in steps
                if isinstance(step, dict)
            ),
            default=-1,
        )
        if highest_level >= LEVEL_ORDER["D2"] and not isinstance(
            record.data.get("transfer_evaluation"), dict
        ):
            report.issues.append(
                Issue(
                    ERROR,
                    "TRANSFER_EVALUATION_REQUIRED",
                    record.path,
                    "D2 이상을 요구하는 Set에는 transfer_evaluation이 필요합니다.",
                )
            )

        lifecycle = record.data.get("lifecycle", {})
        status = lifecycle.get("status")
        impact = record.data.get("business_impact", {})
        if status in {"pilot", "operational", "scale"}:
            baseline = self._list(impact, "baseline_metrics")
            targets = self._list(impact, "target_metrics")
            if not baseline or not targets:
                report.issues.append(
                    Issue(
                        ERROR,
                        "MEASURED_IMPACT_REQUIRED",
                        record.path,
                        f"{status} 상태의 Set에는 기준선과 목표 지표가 필요합니다.",
                    )
                )
            if any(metric.get("value") == "not_measured" for metric in baseline):
                report.issues.append(
                    Issue(
                        ERROR,
                        "BASELINE_NOT_MEASURED",
                        record.path,
                        f"{status} 상태에서는 not_measured 기준선을 사용할 수 없습니다.",
                    )
                )

        requirements = record.data.get("requirements", {})
        permissions = self._list(requirements, "permissions")
        risky_access = {"write", "delete", "admin", "financial"}
        if any(permission.get("access") in risky_access for permission in permissions):
            risk = record.data.get("risk_profile")
            if not isinstance(risk, dict):
                report.issues.append(
                    Issue(
                        ERROR,
                        "RISK_PROFILE_REQUIRED",
                        record.path,
                        "외부 쓰기·삭제·관리·재무 권한이 있는 Set에는 risk_profile이 필요합니다.",
                    )
                )
            else:
                for field_name in (
                    "human_approval_points",
                    "stop_conditions",
                    "rollback_plan",
                ):
                    value = risk.get(field_name)
                    if value in (None, "", []):
                        report.issues.append(
                            Issue(
                                ERROR,
                                "RISK_CONTROL_REQUIRED",
                                record.path,
                                f"위험 권한이 있는 Set의 risk_profile.{field_name}가 비어 있습니다.",
                            )
                        )

    def _validate_study_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """Study의 원천, 미디어 조건, 상태 승격 조건과 카탈로그 참조를 검증합니다.

        Study는 이수 대상이 아니므로 소유관계·역참조 검증에 참여하지 않으며,
        Unit 참조는 의도적으로 정확한 버전 대신 ID 존재만 확인합니다.
        """

        data = record.data
        media_source_kinds = {"video", "podcast"}

        source = data.get("source")
        source_kind = source.get("kind") if isinstance(source, dict) else None
        if isinstance(source, dict):
            has_url = isinstance(source.get("url"), str) and bool(source.get("url"))
            has_private_ref = isinstance(source.get("private_source_ref"), dict)
            if not has_url and not has_private_ref:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_SOURCE_MISSING",
                        record.path,
                        "source에는 url과 private_source_ref 중 최소 하나가 필요합니다.",
                    )
                )

        media = data.get("media")
        if media is not None and source_kind not in media_source_kinds:
            report.issues.append(
                Issue(
                    ERROR,
                    "STUDY_MEDIA_ON_NON_MEDIA",
                    record.path,
                    (
                        f"source.kind={source_kind}인 Study에는 media를 둘 수 없습니다. "
                        "media는 video 또는 podcast 자료에만 허용합니다."
                    ),
                )
            )
        if media is None and source_kind in media_source_kinds:
            report.issues.append(
                Issue(
                    ERROR,
                    "STUDY_MEDIA_MISSING",
                    record.path,
                    (
                        f"source.kind={source_kind}인 Study에는 transcript_source를 포함한 "
                        "media 기록이 필요합니다."
                    ),
                )
            )

        takeaways = self._list(data, "takeaways")
        takeaway_statuses = {
            item.get("verification", {}).get("status")
            for item in takeaways
            if isinstance(item, dict) and isinstance(item.get("verification"), dict)
        }
        has_human_confirmed = bool(
            takeaway_statuses & {"human_confirmed", "cross_checked"}
        )
        has_cross_checked = "cross_checked" in takeaway_statuses

        status = data.get("status")
        application = data.get("application")
        if status == "applied":
            if not isinstance(application, dict):
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_APPLIED_WITHOUT_APPLICATION",
                        record.path,
                        "applied 상태에는 실제 반영 내역을 담은 application이 필요합니다.",
                    )
                )
            if not has_human_confirmed:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_APPLIED_WITHOUT_CONFIRMATION",
                        record.path,
                        (
                            "applied 상태에는 human_confirmed 이상으로 검증된 takeaway가 "
                            "1건 이상 필요합니다. AI 요약만으로 업무 반영을 표시할 수 없습니다."
                        ),
                    )
                )

        if isinstance(application, dict):
            for evidence_path in self._list(application, "evidence_paths"):
                self._validate_study_evidence_path(evidence_path, record, report)

        unit_outcome_ids = {
            outcome.get("id")
            for unit in indexes["unit"].values()
            for outcome in self._list(unit.data.get("learning", {}), "outcomes")
            if isinstance(outcome.get("id"), str)
        }
        for coverage_item in self._list(data, "outcome_coverage"):
            if not isinstance(coverage_item, dict):
                continue
            outcome_id = coverage_item.get("outcome_id")
            if isinstance(outcome_id, str) and outcome_id not in unit_outcome_ids:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_OUTCOME_UNKNOWN",
                        record.path,
                        f"outcome_coverage: {outcome_id}가 어떤 Unit의 학습성과에도 없습니다.",
                    )
                )
            if coverage_item.get("coverage") == "contradicts" and not has_cross_checked:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_CONTRADICTS_WITHOUT_EVIDENCE",
                        record.path,
                        (
                            f"outcome_coverage: {outcome_id}에 contradicts를 표시하려면 "
                            "공식 출처로 cross_checked된 takeaway가 필요합니다."
                        ),
                    )
                )

        known_unit_ids = {unit_id for (unit_id, _version) in indexes["unit"]}
        for reference in self._list(data, "related_unit_refs"):
            if not isinstance(reference, dict):
                continue
            unit_id = reference.get("id")
            if isinstance(unit_id, str) and unit_id not in known_unit_ids:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_UNIT_UNKNOWN",
                        record.path,
                        f"related_unit_refs: Unit {unit_id}가 어느 버전으로도 없습니다.",
                    )
                )

        for reference in self._list(data, "discovered_signal_refs"):
            key = self._reference_key(reference)
            if key is not None and key not in indexes["signal"]:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_SIGNAL_UNKNOWN",
                        record.path,
                        f"discovered_signal_refs: Signal {key[0]}@{key[1]}를 찾을 수 없습니다.",
                    )
                )

    def _validate_study_evidence_path(
        self,
        raw_path: Any,
        record: Record,
        report: ValidationReport,
    ) -> None:
        """application 증거 경로에 기존 로컬 경로 규칙을 STUDY_INVALID_PATH로 적용합니다."""

        if not isinstance(raw_path, str):
            return
        if Path(raw_path).is_absolute() or "\\" in raw_path:
            report.issues.append(
                Issue(
                    ERROR,
                    "STUDY_INVALID_PATH",
                    record.path,
                    (
                        "application.evidence_paths: 작업공간 기준 슬래시 상대경로를 "
                        "사용해야 합니다."
                    ),
                )
            )
            return
        candidate = (self.workspace_root / raw_path).resolve()
        try:
            within_workspace = (
                os.path.commonpath([self.workspace_root, candidate])
                == str(self.workspace_root)
            )
        except ValueError:
            within_workspace = False
        if not within_workspace:
            report.issues.append(
                Issue(
                    ERROR,
                    "STUDY_INVALID_PATH",
                    record.path,
                    "application.evidence_paths: 경로가 작업공간 밖을 가리킵니다.",
                )
            )
            return
        if not candidate.exists():
            report.issues.append(
                Issue(
                    ERROR,
                    "STUDY_INVALID_PATH",
                    record.path,
                    f"application.evidence_paths: {raw_path}가 없습니다.",
                )
            )

    def _validate_candidate_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        evidence = self._list(record.data, "evidence")
        self._report_duplicates(
            [item.get("id") for item in evidence],
            record,
            "DUPLICATE_CANDIDATE_EVIDENCE_ID",
            "Candidate evidence ID",
            report,
        )

        classification = record.data.get("classification", {})
        merge_target = (
            classification.get("merge_target")
            if isinstance(classification, dict)
            else None
        )
        if isinstance(merge_target, dict):
            kind = merge_target.get("kind")
            identifier = merge_target.get("id")
            if kind in {"unit", "set", "resource", "signal"}:
                if not isinstance(identifier, str) or not identifier.startswith(
                    f"{kind}."
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "CANDIDATE_MERGE_KIND_MISMATCH",
                            record.path,
                            f"merge_target의 kind={kind}와 id={identifier}가 일치하지 않습니다.",
                        )
                    )
                self._resolve(
                    kind,
                    merge_target,
                    record,
                    "CANDIDATE_MERGE_TARGET",
                    indexes,
                    report,
                )

        relations = self._list(record.data, "relations")
        relation_keys: list[tuple[Any, Any, Any]] = []
        for relation in relations:
            target = relation.get("target")
            target_key = self._reference_key(target)
            relation_keys.append(
                (
                    relation.get("type"),
                    target_key[0] if target_key is not None else None,
                    target_key[1] if target_key is not None else None,
                )
            )
            self._resolve(
                "candidate",
                target,
                record,
                "CANDIDATE_RELATION",
                indexes,
                report,
            )
        self._report_duplicates(
            relation_keys,
            record,
            "DUPLICATE_CANDIDATE_RELATION",
            "Candidate 관계",
            report,
        )

    def _validate_candidate_registry(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        candidates = indexes["candidate"]
        authoritative_sources = {
            "standard",
            "official_spec",
            "official_docs",
            "official_source",
            "primary_research",
            "practitioner_primary",
        }
        name_owners: dict[str, list[Record]] = {}

        for record in candidates.values():
            data = record.data
            decision = data.get("decision", {})
            status = decision.get("status") if isinstance(decision, dict) else None
            classification = data.get("classification", {})
            destination = (
                classification.get("proposed_destination")
                if isinstance(classification, dict)
                else None
            )

            expected_destinations = {
                "merged": {"merge_existing"},
                "deferred": {"defer"},
                "signalized": {"trend_signal"},
                "excluded": {"exclude"},
            }
            allowed = expected_destinations.get(status)
            if allowed is not None and destination not in allowed:
                report.issues.append(
                    Issue(
                        ERROR,
                        "CANDIDATE_DECISION_MISMATCH",
                        record.path,
                        (
                            f"decision.status={status}와 "
                            f"classification.proposed_destination={destination}이 일치하지 않습니다."
                        ),
                    )
                )
            if status == "accepted" and destination in {
                "merge_existing",
                "trend_signal",
                "defer",
                "exclude",
            }:
                report.issues.append(
                    Issue(
                        ERROR,
                        "CANDIDATE_DECISION_MISMATCH",
                        record.path,
                        (
                            f"accepted 후보의 목적지로 {destination}을 사용할 수 없습니다. "
                            "병합·Signal 전환·보류·제외 상태를 사용하십시오."
                        ),
                    )
                )

            evidence = self._list(data, "evidence")
            for item in evidence:
                published_at = self._parse_date(item.get("published_at"))
                checked_at = self._parse_date(item.get("checked_at"))
                if checked_at is not None and checked_at > self.today:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "CANDIDATE_FUTURE_DATE",
                            record.path,
                            f"evidence {item.get('id')}의 checked_at이 미래입니다.",
                        )
                    )
                if (
                    published_at is not None
                    and checked_at is not None
                    and published_at > checked_at
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "CANDIDATE_EVIDENCE_DATE_ORDER",
                            record.path,
                            (
                                f"evidence {item.get('id')}의 published_at이 "
                                "checked_at보다 늦습니다."
                            ),
                        )
                    )

            researched_at = self._parse_date(
                data.get("review", {}).get("researched_at")
            )
            if researched_at is not None and researched_at > self.today:
                report.issues.append(
                    Issue(
                        ERROR,
                        "CANDIDATE_FUTURE_DATE",
                        record.path,
                        "review.researched_at은 미래 날짜일 수 없습니다.",
                    )
                )

            if status == "accepted":
                source_types = {item.get("source_type") for item in evidence}
                confidence = decision.get("confidence")
                if (
                    confidence not in {"medium", "high"}
                    or not bool(source_types & authoritative_sources)
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "CANDIDATE_NOT_ACCEPTABLE",
                            record.path,
                            (
                                "accepted 후보에는 중간 이상 신뢰도와 표준·공식·1차 "
                                "또는 원 실무자 근거가 필요합니다."
                            ),
                        )
                    )

            names = [data.get("canonical_name"), *data.get("aliases", [])]
            for name in names:
                if not isinstance(name, str):
                    continue
                normalized = self._normalize_signal_name(name)
                name_owners.setdefault(normalized, []).append(record)

        for normalized, owners in name_owners.items():
            active = [
                record
                for record in owners
                if record.data.get("decision", {}).get("status")
                not in {"merged", "excluded"}
            ]
            distinct_keys = {record.key for record in active}
            if len(distinct_keys) <= 1:
                continue
            labels = ", ".join(
                f"{record.id}@{record.version}" for record in active
            )
            for record in active:
                report.issues.append(
                    Issue(
                        WARNING,
                        "CANDIDATE_NAME_COLLISION",
                        record.path,
                        f"정규화 명칭 {normalized!r}가 여러 활성 후보에 존재합니다: {labels}",
                    )
                )

    def _validate_candidate_relation_dag(
        self,
        candidates: dict[tuple[str, str], Record],
        report: ValidationReport,
    ) -> None:
        """후보의 필수 선행관계가 순환하지 않는지 검사합니다."""

        graph: dict[tuple[str, str], list[tuple[str, str]]] = {
            key: [] for key in candidates
        }
        for key, record in candidates.items():
            for relation in self._list(record.data, "relations"):
                if relation.get("type") != "requires":
                    continue
                target_key = self._reference_key(relation.get("target"))
                if target_key in candidates:
                    graph[key].append(target_key)

        self._find_cycles(
            graph,
            "CANDIDATE_RELATION_CYCLE",
            lambda key: f"{key[0]}@{key[1]}",
            lambda key: candidates[key].path,
            report,
        )

    def _validate_handoff_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """인계 파일의 정확한 Candidate 참조와 기존 상대경로를 검증합니다."""

        decisions = self._list(record.data, "decisions")
        self._report_duplicates(
            [item.get("candidate_ref") for item in decisions],
            record,
            "DUPLICATE_HANDOFF_CANDIDATE_REF",
            "Handoff Candidate 참조",
            report,
        )
        for decision in decisions:
            self._resolve(
                "candidate",
                decision.get("candidate_ref"),
                record,
                "HANDOFF_CANDIDATE",
                indexes,
                report,
            )

        source_contract = record.data.get("source_contract", {})
        if isinstance(source_contract, dict):
            for index, path in enumerate(source_contract.get("governance_files", [])):
                self._validate_local_path(
                    path,
                    record,
                    f"source_contract.governance_files[{index}]",
                    report,
                )
            self._validate_local_path(
                source_contract.get("checkpoint_path"),
                record,
                "source_contract.checkpoint_path",
                report,
            )

        artifacts = self._list(record.data, "artifacts")
        self._report_duplicates(
            [item.get("path") for item in artifacts],
            record,
            "DUPLICATE_HANDOFF_ARTIFACT",
            "Handoff artifact 경로",
            report,
        )
        for index, artifact in enumerate(artifacts):
            self._validate_local_path(
                artifact.get("path"),
                record,
                f"artifacts[{index}].path",
                report,
            )

        resume = record.data.get("resume", {})
        if isinstance(resume, dict):
            for field_name in ("read_first", "inputs"):
                for index, path in enumerate(resume.get(field_name, [])):
                    self._validate_local_path(
                        path,
                        record,
                        f"resume.{field_name}[{index}]",
                        report,
                    )

    def _validate_handoff_registry(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """인계 요약 수치와 실제 Candidate 및 재개 가능성을 교차 검증합니다."""

        for record in indexes["handoff"].values():
            data = record.data
            execution = data.get("execution", {})
            counts = (
                execution.get("counts", {})
                if isinstance(execution, dict)
                else {}
            )
            decisions = self._list(data, "decisions")

            total = counts.get("candidates_total")
            disposition_fields = (
                "proposed",
                "needs_review",
                "accepted",
                "merged",
                "deferred",
                "signalized",
                "excluded",
            )
            disposition_total = sum(
                counts.get(field_name, 0)
                for field_name in disposition_fields
                if isinstance(counts.get(field_name), int)
            )
            if isinstance(total, int) and disposition_total != total:
                report.issues.append(
                    Issue(
                        ERROR,
                        "HANDOFF_COUNT_MISMATCH",
                        record.path,
                        (
                            f"상태별 Candidate 합계 {disposition_total}가 "
                            f"candidates_total {total}과 다릅니다."
                        ),
                    )
                )

            if isinstance(total, int) and len(decisions) != total:
                report.issues.append(
                    Issue(
                        ERROR,
                        "HANDOFF_DECISION_COUNT_MISMATCH",
                        record.path,
                        (
                            f"decisions {len(decisions)}개가 "
                            f"candidates_total {total}과 다릅니다."
                        ),
                    )
                )

            decision_counts = {field_name: 0 for field_name in disposition_fields}
            for decision in decisions:
                disposition = decision.get("disposition")
                if disposition in decision_counts:
                    decision_counts[disposition] += 1
                key = self._reference_key(decision.get("candidate_ref"))
                target = indexes["candidate"].get(key) if key is not None else None
                if target is None:
                    continue
                candidate_status = target.data.get("decision", {}).get("status")
                if candidate_status != disposition:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_CANDIDATE_STATUS_MISMATCH",
                            record.path,
                            (
                                f"{target.id}@{target.version}의 실제 상태 "
                                f"{candidate_status}와 인계 상태 {disposition}이 다릅니다."
                            ),
                        )
                    )

            for field_name, actual in decision_counts.items():
                expected = counts.get(field_name)
                if isinstance(expected, int) and expected != actual:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_DISPOSITION_COUNT_MISMATCH",
                            record.path,
                            (
                                f"{field_name} 집계 {expected}와 decisions의 실제 수 "
                                f"{actual}이 다릅니다."
                            ),
                        )
                    )

            work_packages = (
                execution.get("work_packages", [])
                if isinstance(execution, dict)
                else []
            )
            self._report_duplicates(
                [item.get("id") for item in work_packages],
                record,
                "DUPLICATE_HANDOFF_WORK_PACKAGE",
                "Handoff work package ID",
                report,
            )
            package_total = sum(
                item.get("candidate_count", 0)
                for item in work_packages
                if isinstance(item.get("candidate_count"), int)
            )
            if isinstance(total, int) and package_total != total:
                report.issues.append(
                    Issue(
                        ERROR,
                        "HANDOFF_WORK_PACKAGE_COUNT_MISMATCH",
                        record.path,
                        (
                            f"work package Candidate 합계 {package_total}가 "
                            f"candidates_total {total}과 다릅니다."
                        ),
                    )
                )

            coverage = data.get("coverage", {})
            domains = (
                coverage.get("domains", [])
                if isinstance(coverage, dict)
                else []
            )
            self._report_duplicates(
                [item.get("id") for item in domains],
                record,
                "DUPLICATE_HANDOFF_DOMAIN",
                "Handoff coverage domain ID",
                report,
            )

            scope = data.get("scope", {})
            started_at = (
                self._parse_date(scope.get("started_at"))
                if isinstance(scope, dict)
                else None
            )
            ended_at = (
                self._parse_date(scope.get("ended_at"))
                if isinstance(scope, dict)
                else None
            )
            if started_at is not None and ended_at is not None and ended_at < started_at:
                report.issues.append(
                    Issue(
                        ERROR,
                        "HANDOFF_DATE_ORDER",
                        record.path,
                        "scope.ended_at이 scope.started_at보다 빠릅니다.",
                    )
                )

            dated_fields = [
                ("created_at", data.get("created_at")),
                (
                    "scope.started_at",
                    scope.get("started_at") if isinstance(scope, dict) else None,
                ),
                (
                    "scope.ended_at",
                    scope.get("ended_at") if isinstance(scope, dict) else None,
                ),
            ]
            quality = data.get("quality", {})
            if isinstance(quality, dict):
                for field_name in ("catalog_validation", "regression_tests"):
                    result = quality.get(field_name, {})
                    dated_fields.append(
                        (
                            f"quality.{field_name}.ran_at",
                            result.get("ran_at") if isinstance(result, dict) else None,
                        )
                    )
                source_audit = quality.get("source_audit", {})
                if isinstance(source_audit, dict):
                    reviewed = source_audit.get("reviewed_count")
                    priority_total = sum(
                        source_audit.get(field_name, 0)
                        for field_name in ("p0_count", "p1_count", "p2_count")
                        if isinstance(source_audit.get(field_name), int)
                    )
                    if isinstance(reviewed, int) and reviewed != priority_total:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "HANDOFF_SOURCE_AUDIT_COUNT_MISMATCH",
                                record.path,
                                (
                                    f"source audit 우선순위 합계 {priority_total}가 "
                                    f"reviewed_count {reviewed}와 다릅니다."
                                ),
                            )
                        )

            approval = data.get("approval", {})
            if isinstance(approval, dict):
                dated_fields.extend(
                    [
                        ("approval.requested_at", approval.get("requested_at")),
                        ("approval.approved_at", approval.get("approved_at")),
                    ]
                )
                requested_at = self._parse_date(approval.get("requested_at"))
                approved_at = self._parse_date(approval.get("approved_at"))
                if (
                    requested_at is not None
                    and approved_at is not None
                    and approved_at < requested_at
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_APPROVAL_DATE_ORDER",
                            record.path,
                            "approval.approved_at이 approval.requested_at보다 빠릅니다.",
                        )
                    )

            for field_name, raw_value in dated_fields:
                parsed = self._parse_date(raw_value)
                if parsed is not None and parsed > self.today:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_FUTURE_DATE",
                            record.path,
                            f"{field_name}은 미래 날짜일 수 없습니다.",
                        )
                    )

            status = data.get("status")
            if status in {"ready_for_review", "phase_complete"}:
                for field_name in ("catalog_validation", "regression_tests"):
                    result = quality.get(field_name, {}) if isinstance(quality, dict) else {}
                    if not isinstance(result, dict) or result.get("exit_code") != 0:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "HANDOFF_VALIDATION_NOT_PASSED",
                                record.path,
                                f"{status} 상태에는 quality.{field_name} 성공이 필요합니다.",
                            )
                        )

            if status == "phase_complete":
                incomplete_domains = [
                    item.get("id")
                    for item in domains
                    if item.get("status") != "complete"
                ]
                if incomplete_domains:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_PHASE_COVERAGE_INCOMPLETE",
                            record.path,
                            (
                                "phase_complete 상태에 미완료 영역이 있습니다: "
                                + ", ".join(str(item) for item in incomplete_domains)
                            ),
                        )
                    )
                open_items = data.get("open_items", {})
                unresolved = []
                if isinstance(open_items, dict):
                    for field_name in ("questions", "conflicts", "unverified_claims"):
                        if open_items.get(field_name):
                            unresolved.append(field_name)
                if unresolved:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "HANDOFF_PHASE_OPEN_ITEMS",
                            record.path,
                            (
                                "phase_complete 상태에 미해결 항목이 있습니다: "
                                + ", ".join(unresolved)
                            ),
                        )
                    )

    def _validate_signal_references(
        self,
        record: Record,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """Trend Signal 내부 근거와 외부 참조의 정합성을 검증합니다."""

        claims = self._list(record.data, "claims")
        evidence = self._list(record.data, "evidence")
        interpretations = self._list(record.data.get("disambiguation", {}), "interpretations")

        self._report_duplicates(
            [claim.get("id") for claim in claims],
            record,
            "DUPLICATE_SIGNAL_CLAIM_ID",
            "Signal claim ID",
            report,
        )
        self._report_duplicates(
            [item.get("id") for item in evidence],
            record,
            "DUPLICATE_SIGNAL_EVIDENCE_ID",
            "Signal evidence ID",
            report,
        )
        self._report_duplicates(
            [item.get("id") for item in interpretations],
            record,
            "DUPLICATE_SIGNAL_INTERPRETATION_ID",
            "Signal interpretation ID",
            report,
        )

        evidence_by_id = {
            item.get("id"): item
            for item in evidence
            if isinstance(item.get("id"), str)
        }
        used_evidence_ids: set[str] = set()
        for claim in claims:
            stances: set[str] = set()
            for evidence_ref in self._list(claim, "evidence_refs"):
                evidence_id = evidence_ref.get("id")
                stance = evidence_ref.get("stance")
                if isinstance(stance, str):
                    stances.add(stance)
                if not isinstance(evidence_id, str):
                    continue
                used_evidence_ids.add(evidence_id)
                if evidence_id not in evidence_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_EVIDENCE_NOT_FOUND",
                            record.path,
                            f"claim {claim.get('id')}이 존재하지 않는 근거 {evidence_id}를 참조합니다.",
                        )
                    )
            claim_status = claim.get("status")
            if claim_status == "supported" and "supports" not in stances:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_CLAIM_STANCE_MISMATCH",
                        record.path,
                        f"supported claim {claim.get('id')}에는 supports 근거가 필요합니다.",
                    )
                )
            if claim_status == "rejected" and "contradicts" not in stances:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_CLAIM_STANCE_MISMATCH",
                        record.path,
                        f"rejected claim {claim.get('id')}에는 contradicts 근거가 필요합니다.",
                    )
                )

        interpretation_ids = {
            item.get("id")
            for item in interpretations
            if isinstance(item.get("id"), str)
        }
        for interpretation in interpretations:
            for evidence_id in self._list(interpretation, "evidence_ids"):
                if not isinstance(evidence_id, str):
                    continue
                used_evidence_ids.add(evidence_id)
                if evidence_id not in evidence_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_EVIDENCE_NOT_FOUND",
                            record.path,
                            (
                                f"interpretation {interpretation.get('id')}이 존재하지 않는 "
                                f"근거 {evidence_id}를 참조합니다."
                            ),
                        )
                    )

        disambiguation = record.data.get("disambiguation", {})
        selected = (
            disambiguation.get("selected_interpretation_id")
            if isinstance(disambiguation, dict)
            else None
        )
        if isinstance(selected, str) and selected not in interpretation_ids:
            report.issues.append(
                Issue(
                    ERROR,
                    "SIGNAL_INTERPRETATION_NOT_FOUND",
                    record.path,
                    f"선택된 interpretation {selected}를 찾을 수 없습니다.",
                )
            )

        for evidence_id in evidence_by_id:
            if evidence_id not in used_evidence_ids:
                report.issues.append(
                    Issue(
                        WARNING,
                        "SIGNAL_UNUSED_EVIDENCE",
                        record.path,
                        f"근거 {evidence_id}가 어떤 claim 또는 interpretation에도 연결되지 않았습니다.",
                    )
                )

        for relation in self._list(record.data, "related_signal_refs"):
            target = relation.get("target")
            target_key = self._reference_key(target)
            self._resolve(
                "signal",
                target,
                record,
                "SIGNAL_RELATION",
                indexes,
                report,
            )
            if target_key == record.key:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_SELF_REFERENCE",
                        record.path,
                        "Signal은 자기 자신을 관련 Signal로 참조할 수 없습니다.",
                    )
                )

        duplicate_of = record.data.get("duplicate_of")
        if duplicate_of is not None:
            target_key = self._reference_key(duplicate_of)
            self._resolve(
                "signal",
                duplicate_of,
                record,
                "SIGNAL_DUPLICATE_OF",
                indexes,
                report,
            )
            if target_key == record.key:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_SELF_REFERENCE",
                        record.path,
                        "Signal은 자기 자신을 중복 대상으로 지정할 수 없습니다.",
                    )
                )

        promotion = record.data.get("promotion")
        if isinstance(promotion, dict):
            for target_ref in self._list(promotion, "targets"):
                kind = target_ref.get("kind")
                identifier = target_ref.get("id")
                if kind not in {"unit", "set", "resource"}:
                    continue
                if not isinstance(identifier, str) or not identifier.startswith(
                    f"{kind}."
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_PROMOTION_KIND_MISMATCH",
                            record.path,
                            f"promotion target의 kind={kind}와 id={identifier}가 일치하지 않습니다.",
                        )
                    )
                target = self._resolve(
                    kind,
                    target_ref,
                    record,
                    "SIGNAL_PROMOTION",
                    indexes,
                    report,
                )
                if target is not None:
                    target_status = target.data.get("lifecycle", {}).get("status")
                    if target_status in {"deprecated", "archived"}:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "SIGNAL_INVALID_PROMOTION_TARGET",
                                record.path,
                                (
                                    f"promotion target {target.id}@{target.version}의 "
                                    f"상태가 {target_status}입니다."
                                ),
                            )
                        )

    def _validate_taxonomy_registry(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """분류 레지스트리 내부와 Candidate·Unit의 분류 참조를 검증합니다."""

        registries = list(indexes["taxonomy"].values())
        active_registries = [
            record
            for record in registries
            if record.data.get("status") != "deprecated"
        ]
        taxonomy_consumers = [
            *indexes["candidate"].values(),
            *indexes["unit"].values(),
            *indexes["study"].values(),
        ]

        if taxonomy_consumers and len(active_registries) != 1:
            issue_path = (
                active_registries[0].path
                if active_registries
                else self.workspace_root
            )
            report.issues.append(
                Issue(
                    ERROR,
                    "TAXONOMY_REGISTRY_COUNT",
                    issue_path,
                    (
                        "Candidate 또는 Unit을 검증하려면 활성 Taxonomy Registry가 "
                        f"정확히 하나여야 합니다. 현재 {len(active_registries)}개입니다."
                    ),
                )
            )

        for registry in registries:
            self._validate_taxonomy_registry_record(registry, report)

        if len(active_registries) != 1:
            return

        registry = active_registries[0]
        node_by_id = {
            node["id"]: node
            for node in self._list(registry.data, "nodes")
            if isinstance(node, dict) and isinstance(node.get("id"), str)
        }
        for candidate in indexes["candidate"].values():
            discovery = candidate.data.get("discovery", {})
            lens_id = (
                discovery.get("lens_id")
                if isinstance(discovery, dict)
                else None
            )
            self._validate_taxonomy_node_reference(
                lens_id,
                "domain",
                candidate,
                "discovery.lens_id",
                node_by_id,
                report,
            )
            self._validate_taxonomy_assignment(candidate, node_by_id, report)

        for unit in indexes["unit"].values():
            self._validate_taxonomy_assignment(unit, node_by_id, report)

        for study in indexes["study"].values():
            self._validate_study_taxonomy_refs(study, node_by_id, report)

    def _validate_study_taxonomy_refs(
        self,
        record: Record,
        node_by_id: dict[str, dict[str, Any]],
        report: ValidationReport,
    ) -> None:
        """Study taxonomy_refs가 활성 Registry의 유효한 node를 가리키는지 검증합니다.

        Unit의 taxonomy와 달리 domain과 subdomain을 모두 허용하며 부모 관계는
        요구하지 않습니다. 분류 없는 기록 축적을 막는 것이 목적입니다.
        """

        for node_id in self._list(record.data, "taxonomy_refs"):
            if not isinstance(node_id, str):
                continue
            node = node_by_id.get(node_id)
            if node is None:
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_TAXONOMY_UNKNOWN",
                        record.path,
                        f"taxonomy_refs: node {node_id}가 활성 Registry에 없습니다.",
                    )
                )
                continue
            if node.get("status") == "deprecated":
                report.issues.append(
                    Issue(
                        ERROR,
                        "STUDY_TAXONOMY_DEPRECATED",
                        record.path,
                        f"taxonomy_refs: 폐기된 node {node_id}를 참조합니다.",
                    )
                )

    def _validate_taxonomy_registry_record(
        self,
        registry: Record,
        report: ValidationReport,
    ) -> None:
        nodes = [
            node
            for node in self._list(registry.data, "nodes")
            if isinstance(node, dict)
        ]
        frameworks = [
            framework
            for framework in self._list(registry.data, "external_frameworks")
            if isinstance(framework, dict)
        ]
        views = [
            view
            for view in self._list(registry.data, "views")
            if isinstance(view, dict)
        ]

        node_ids = [node.get("id") for node in nodes]
        framework_ids = [framework.get("id") for framework in frameworks]
        view_ids = [view.get("id") for view in views]
        self._report_duplicates(
            node_ids,
            registry,
            "DUPLICATE_TAXONOMY_NODE_ID",
            "Taxonomy node ID",
            report,
        )
        self._report_duplicates(
            framework_ids,
            registry,
            "DUPLICATE_TAXONOMY_FRAMEWORK_ID",
            "외부 프레임워크 ID",
            report,
        )
        self._report_duplicates(
            view_ids,
            registry,
            "DUPLICATE_TAXONOMY_VIEW_ID",
            "Taxonomy view ID",
            report,
        )

        node_by_id = {
            node["id"]: node
            for node in nodes
            if isinstance(node.get("id"), str)
        }
        framework_id_set = {
            identifier
            for identifier in framework_ids
            if isinstance(identifier, str)
        }
        name_owners: dict[str, set[str]] = {}

        graph: dict[str, list[str]] = {
            identifier: [] for identifier in node_by_id
        }
        for node_id, node in node_by_id.items():
            node_type = node.get("node_type")
            parent_ids = [
                parent_id
                for parent_id in self._list(node, "parent_ids")
                if isinstance(parent_id, str)
            ]
            if node_type == "domain" and parent_ids:
                report.issues.append(
                    Issue(
                        ERROR,
                        "TAXONOMY_DOMAIN_HAS_PARENT",
                        registry.path,
                        f"domain node {node_id}에는 parent_ids를 둘 수 없습니다.",
                    )
                )
            if node_type == "subdomain" and not parent_ids:
                report.issues.append(
                    Issue(
                        ERROR,
                        "TAXONOMY_SUBDOMAIN_WITHOUT_PARENT",
                        registry.path,
                        f"subdomain node {node_id}에는 하나 이상의 parent_id가 필요합니다.",
                    )
                )

            for parent_id in parent_ids:
                if parent_id not in node_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "TAXONOMY_NODE_NOT_FOUND",
                            registry.path,
                            f"node {node_id}의 parent_id {parent_id}를 찾을 수 없습니다.",
                        )
                    )
                    continue
                graph[node_id].append(parent_id)

            for relation_name in ("related_ids",):
                for target_id in self._list(node, relation_name):
                    if not isinstance(target_id, str):
                        continue
                    if target_id == node_id:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "TAXONOMY_SELF_REFERENCE",
                                registry.path,
                                f"node {node_id}가 {relation_name}에서 자기 자신을 참조합니다.",
                            )
                        )
                    elif target_id not in node_by_id:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "TAXONOMY_NODE_NOT_FOUND",
                                registry.path,
                                f"node {node_id}의 {relation_name} {target_id}를 찾을 수 없습니다.",
                            )
                        )

            lifecycle = node.get("lifecycle", {})
            superseded_by = (
                lifecycle.get("superseded_by")
                if isinstance(lifecycle, dict)
                else None
            )
            if isinstance(superseded_by, str):
                if superseded_by == node_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "TAXONOMY_SELF_REFERENCE",
                            registry.path,
                            f"node {node_id}가 자신을 superseded_by로 참조합니다.",
                        )
                    )
                elif superseded_by not in node_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "TAXONOMY_NODE_NOT_FOUND",
                            registry.path,
                            f"node {node_id}의 superseded_by {superseded_by}를 찾을 수 없습니다.",
                        )
                    )

            for mapping in self._list(node, "external_mappings"):
                if not isinstance(mapping, dict):
                    continue
                framework_id = mapping.get("framework_id")
                if (
                    isinstance(framework_id, str)
                    and framework_id not in framework_id_set
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "TAXONOMY_FRAMEWORK_NOT_FOUND",
                            registry.path,
                            (
                                f"node {node_id}의 외부 매핑 프레임워크 "
                                f"{framework_id}를 찾을 수 없습니다."
                            ),
                        )
                    )

            names = [
                node_id,
                node.get("title_ko"),
                node.get("title_en"),
                *self._list(node, "aliases"),
            ]
            for name in names:
                if not isinstance(name, str):
                    continue
                normalized = self._normalize_signal_name(name)
                if normalized:
                    name_owners.setdefault(normalized, set()).add(node_id)

        for normalized, owners in name_owners.items():
            if len(owners) > 1:
                report.issues.append(
                    Issue(
                        ERROR,
                        "TAXONOMY_NAME_COLLISION",
                        registry.path,
                        (
                            f"정규화 명칭 {normalized!r}가 여러 node에 존재합니다: "
                            f"{', '.join(sorted(owners))}"
                        ),
                    )
                )

        for view in views:
            view_id = view.get("id", "unknown-view")
            for node_ref in self._list(view, "node_refs"):
                if isinstance(node_ref, str) and node_ref not in node_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "TAXONOMY_NODE_NOT_FOUND",
                            registry.path,
                            f"view {view_id}의 node_ref {node_ref}를 찾을 수 없습니다.",
                        )
                    )

        self._find_cycles(
            graph,
            "TAXONOMY_HIERARCHY_CYCLE",
            str,
            lambda _node_id: registry.path,
            report,
        )

    def _validate_taxonomy_assignment(
        self,
        record: Record,
        node_by_id: dict[str, dict[str, Any]],
        report: ValidationReport,
    ) -> None:
        taxonomy = record.data.get("taxonomy")
        if not isinstance(taxonomy, dict):
            return
        major_domain = taxonomy.get("major_domain")
        valid_major = self._validate_taxonomy_node_reference(
            major_domain,
            "domain",
            record,
            "taxonomy.major_domain",
            node_by_id,
            report,
        )
        for subdomain_id in self._list(taxonomy, "subdomains"):
            valid_subdomain = self._validate_taxonomy_node_reference(
                subdomain_id,
                "subdomain",
                record,
                "taxonomy.subdomains",
                node_by_id,
                report,
            )
            if (
                valid_major
                and valid_subdomain
                and isinstance(major_domain, str)
                and isinstance(subdomain_id, str)
                and major_domain
                not in self._taxonomy_ancestors(subdomain_id, node_by_id)
            ):
                report.issues.append(
                    Issue(
                        ERROR,
                        "TAXONOMY_PARENT_MISMATCH",
                        record.path,
                        (
                            f"subdomain {subdomain_id}는 major_domain "
                            f"{major_domain}의 하위 node가 아닙니다."
                        ),
                    )
                )

    def _validate_taxonomy_node_reference(
        self,
        node_id: Any,
        expected_type: str,
        record: Record,
        relation_name: str,
        node_by_id: dict[str, dict[str, Any]],
        report: ValidationReport,
    ) -> bool:
        if not isinstance(node_id, str):
            return False
        node = node_by_id.get(node_id)
        if node is None:
            report.issues.append(
                Issue(
                    ERROR,
                    "TAXONOMY_NODE_NOT_FOUND",
                    record.path,
                    f"{relation_name}: node {node_id}를 찾을 수 없습니다.",
                )
            )
            return False
        if node.get("node_type") != expected_type:
            report.issues.append(
                Issue(
                    ERROR,
                    "TAXONOMY_NODE_TYPE",
                    record.path,
                    (
                        f"{relation_name}: node {node_id}는 {expected_type}이 아니라 "
                        f"{node.get('node_type')}입니다."
                    ),
                )
            )
            return False
        if node.get("status") == "deprecated":
            report.issues.append(
                Issue(
                    ERROR,
                    "TAXONOMY_DEPRECATED_REFERENCE",
                    record.path,
                    f"{relation_name}: 폐기된 node {node_id}를 참조합니다.",
                )
            )
            return False
        return True

    @staticmethod
    def _taxonomy_ancestors(
        node_id: str,
        node_by_id: dict[str, dict[str, Any]],
    ) -> set[str]:
        ancestors: set[str] = set()
        pending = [node_id]
        while pending:
            current_id = pending.pop()
            current = node_by_id.get(current_id)
            if not isinstance(current, dict):
                continue
            for parent_id in current.get("parent_ids", []):
                if (
                    isinstance(parent_id, str)
                    and parent_id not in ancestors
                    and parent_id != node_id
                ):
                    ancestors.add(parent_id)
                    pending.append(parent_id)
        return ancestors

    def _validate_signal_registry(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        """Trend Signal 상태, 명칭, 승격 게이트와 계층 관계를 검증합니다."""

        signals = indexes["signal"]
        allowed_transitions = {
            "captured": {"triaged", "duplicate", "rejected", "archived"},
            "triaged": {
                "researching",
                "watching",
                "duplicate",
                "rejected",
                "archived",
            },
            "researching": {
                "substantiated",
                "watching",
                "duplicate",
                "rejected",
                "archived",
            },
            "substantiated": {
                "promoted",
                "watching",
                "duplicate",
                "rejected",
                "archived",
            },
            "watching": {"researching", "duplicate", "rejected", "archived"},
            "rejected": {"researching", "archived"},
            "duplicate": {"archived"},
            "promoted": {"archived"},
            "archived": set(),
        }
        authoritative_sources = {
            "standard",
            "official_spec",
            "official_docs",
            "official_source",
            "primary_research",
            "practitioner_primary",
        }
        name_owners: dict[str, list[tuple[Record, str]]] = {}

        for key, record in signals.items():
            data = record.data
            status = data.get("status")
            history = self._list(data, "status_history")
            history_statuses = [item.get("status") for item in history]
            history_dates: list[date] = []
            history_invalid = False

            if not history_statuses or history_statuses[0] != "captured":
                history_invalid = True
            if history_statuses and history_statuses[-1] != status:
                history_invalid = True
            for before, after in zip(history_statuses, history_statuses[1:]):
                if after not in allowed_transitions.get(before, set()):
                    history_invalid = True
            for item in history:
                parsed = self._parse_date(item.get("at"))
                if parsed is not None:
                    history_dates.append(parsed)
                    if parsed > self.today:
                        history_invalid = True
            if any(
                before > after
                for before, after in zip(history_dates, history_dates[1:])
            ):
                history_invalid = True
            if history_invalid:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_STATUS_HISTORY",
                        record.path,
                        "status_history가 허용된 상태 전이, 날짜 순서 또는 현재 status와 일치하지 않습니다.",
                    )
                )

            review = data.get("review", {})
            first_observed = self._parse_date(review.get("first_observed_at"))
            last_reviewed = self._parse_date(review.get("last_reviewed_at"))
            review_due = self._parse_date(review.get("review_due_at"))
            if (
                first_observed is not None
                and last_reviewed is not None
                and first_observed > last_reviewed
            ):
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_REVIEW_DATE_ORDER",
                        record.path,
                        "first_observed_at은 last_reviewed_at보다 늦을 수 없습니다.",
                    )
                )
            if last_reviewed is not None and last_reviewed > self.today:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_FUTURE_DATE",
                        record.path,
                        "last_reviewed_at은 미래 날짜일 수 없습니다.",
                    )
                )
            if (
                review_due is not None
                and review_due < self.today
                and status not in {"rejected", "duplicate", "archived"}
            ):
                report.issues.append(
                    Issue(
                        WARNING,
                        "SIGNAL_REVIEW_OVERDUE",
                        record.path,
                        f"Signal 검토 예정일 {review_due.isoformat()}이 지났습니다.",
                    )
                )

            for evidence in self._list(data, "evidence"):
                published_at = self._parse_date(evidence.get("published_at"))
                checked_at = self._parse_date(evidence.get("checked_at"))
                if checked_at is not None and checked_at > self.today:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_FUTURE_DATE",
                            record.path,
                            f"evidence {evidence.get('id')}의 checked_at이 미래입니다.",
                        )
                    )
                if (
                    published_at is not None
                    and checked_at is not None
                    and published_at > checked_at
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_EVIDENCE_DATE_ORDER",
                            record.path,
                            (
                                f"evidence {evidence.get('id')}의 published_at이 "
                                "checked_at보다 늦습니다."
                            ),
                        )
                    )

            local_names: dict[str, str] = {}
            canonical_name = data.get("canonical_name")
            if isinstance(canonical_name, str):
                normalized = self._normalize_signal_name(canonical_name)
                local_names[normalized] = canonical_name
                name_owners.setdefault(normalized, []).append(
                    (record, "canonical_name")
                )
            for alias in self._list(data, "aliases"):
                value = alias.get("value")
                if not isinstance(value, str):
                    continue
                normalized = self._normalize_signal_name(value)
                kind = alias.get("kind")
                if (
                    normalized in local_names
                    and kind in {"synonym", "translation", "spelling"}
                ):
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_ALIAS_COLLISION",
                            record.path,
                            (
                                f"alias {value!r}가 같은 Signal의 명칭 "
                                f"{local_names[normalized]!r}와 중복됩니다."
                            ),
                        )
                    )
                local_names.setdefault(normalized, value)
                name_owners.setdefault(normalized, []).append(
                    (record, f"alias:{kind}")
                )

            duplicate_of = data.get("duplicate_of")
            promotion = data.get("promotion")
            if status == "duplicate":
                if duplicate_of is None:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_DUPLICATE_TARGET_REQUIRED",
                            record.path,
                            "duplicate 상태에는 duplicate_of가 필요합니다.",
                        )
                    )
                if promotion is not None:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_INVALID_STATUS_FIELDS",
                            record.path,
                            "duplicate Signal에는 promotion을 기록할 수 없습니다.",
                        )
                    )
            elif duplicate_of is not None:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_INVALID_STATUS_FIELDS",
                        record.path,
                        "duplicate_of는 duplicate 상태에서만 사용할 수 있습니다.",
                    )
                )

            if status == "promoted":
                if promotion is None:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_PROMOTION_REQUIRED",
                            record.path,
                            "promoted 상태에는 실제 카탈로그 대상을 가리키는 promotion이 필요합니다.",
                        )
                    )
            elif promotion is not None:
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_INVALID_STATUS_FIELDS",
                        record.path,
                        "promotion은 promoted 상태에서만 사용할 수 있습니다.",
                    )
                )

            if status in {"substantiated", "promoted"}:
                claims = self._list(data, "claims")
                critical_claims = [
                    claim for claim in claims if claim.get("critical") is True
                ]
                identity_supported = any(
                    claim.get("type") in {"identity", "definition"}
                    and claim.get("critical") is True
                    and claim.get("status") == "supported"
                    for claim in claims
                )
                unresolved_critical = [
                    claim.get("id")
                    for claim in critical_claims
                    if claim.get("status") != "supported"
                ]
                source_types = {
                    item.get("source_type")
                    for item in self._list(data, "evidence")
                }
                disambiguation = data.get("disambiguation", {})
                disambiguation_status = (
                    disambiguation.get("status")
                    if isinstance(disambiguation, dict)
                    else None
                )
                confidence = data.get("verification", {}).get("confidence")
                gate_failed = (
                    data.get("relevance", {}).get("status") != "eligible"
                    or confidence not in {"medium", "high"}
                    or not identity_supported
                    or bool(unresolved_critical)
                    or not bool(source_types & authoritative_sources)
                    or disambiguation_status != "clear"
                )
                if gate_failed:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SIGNAL_NOT_SUBSTANTIATED",
                            record.path,
                            (
                                "substantiated/promoted 상태에는 업무 적합성, 중간 이상 검증 신뢰도, "
                                "지원된 핵심 정의, 권위 있는 근거, 해소된 중의성이 필요하며 "
                                f"미해결 핵심 claim은 없어야 합니다: {unresolved_critical}"
                            ),
                        )
                    )

            destination = data.get("candidate_mapping", {}).get("destination")
            if destination == "probe_set" and not isinstance(
                data.get("probe_plan"), dict
            ):
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_PROBE_PLAN_REQUIRED",
                        record.path,
                        "probe_set 후보에는 비교 가능한 probe_plan이 필요합니다.",
                    )
                )

        for normalized, owners in name_owners.items():
            active_owners = [
                owner
                for owner in owners
                if owner[0].data.get("status")
                not in {"duplicate", "rejected", "archived"}
            ]
            distinct_keys = {owner[0].key for owner in active_owners}
            if len(distinct_keys) <= 1:
                continue
            owner_labels = ", ".join(
                f"{owner.id}@{owner.version} ({field})"
                for owner, field in active_owners
            )
            for owner, _field in active_owners:
                report.issues.append(
                    Issue(
                        WARNING,
                        "SIGNAL_NAME_COLLISION",
                        owner.path,
                        f"정규화 명칭 {normalized!r}가 여러 활성 Signal에 존재합니다: {owner_labels}",
                    )
                )

        hierarchy_types = {"broader_than", "narrower_than", "split_into"}
        graph: dict[tuple[str, str], list[tuple[str, str]]] = {
            key: [] for key in signals
        }
        for key, record in signals.items():
            for relation in self._list(record.data, "related_signal_refs"):
                if relation.get("type") not in hierarchy_types:
                    continue
                target_key = self._reference_key(relation.get("target"))
                if target_key in signals:
                    graph[key].append(target_key)
        self._find_cycles(
            graph,
            "SIGNAL_HIERARCHY_CYCLE",
            lambda item: f"{item[0]}@{item[1]}",
            lambda item: signals[item].path,
            report,
        )

        for key, record in signals.items():
            if record.data.get("status") != "duplicate":
                continue
            duplicate_key = self._reference_key(record.data.get("duplicate_of"))
            target = signals.get(duplicate_key) if duplicate_key is not None else None
            if target is not None and target.data.get("status") == "duplicate":
                report.issues.append(
                    Issue(
                        ERROR,
                        "SIGNAL_DUPLICATE_CHAIN",
                        record.path,
                        (
                            f"duplicate 대상 {target.id}@{target.version}도 duplicate입니다. "
                            "최종 정규 Signal을 직접 참조하십시오."
                        ),
                    )
                )

    @staticmethod
    def _normalize_signal_name(value: str) -> str:
        normalized = unicodedata.normalize("NFKC", value).casefold().strip()
        for character in ("-", "‐", "‑", "‒", "–", "—", "_"):
            normalized = normalized.replace(character, " ")
        return " ".join(normalized.split())

    @staticmethod
    def _parse_date(value: Any) -> date | None:
        if not isinstance(value, str):
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None

    def _validate_supersession(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        for kind, records in indexes.items():
            graph: dict[tuple[str, str], list[tuple[str, str]]] = {
                key: [] for key in records
            }
            for key, record in records.items():
                lifecycle = record.data.get("lifecycle", {})
                reference = lifecycle.get("superseded_by")
                if reference is None:
                    continue
                target_key = self._reference_key(reference)
                if target_key is None:
                    continue
                target = records.get(target_key)
                if target is None:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "MISSING_SUPERSESSION_TARGET",
                            record.path,
                            f"{kind} 대체 대상 {target_key[0]}@{target_key[1]}를 찾을 수 없습니다.",
                        )
                    )
                    continue
                if target_key == key:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "SELF_SUPERSESSION",
                            record.path,
                            "자기 자신을 대체 대상으로 지정할 수 없습니다.",
                        )
                    )
                graph[key].append(target_key)
                target_status = target.data.get("lifecycle", {}).get("status")
                if target_status in {"deprecated", "archived"}:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "INVALID_SUPERSESSION_TARGET",
                            record.path,
                            f"대체 대상 {target.id}@{target.version}의 상태가 {target_status}입니다.",
                        )
                    )

            self._find_cycles(
                graph,
                "SUPERSESSION_CYCLE",
                lambda item: f"{item[0]}@{item[1]}",
                lambda item: records[item].path,
                report,
            )

    def _validate_unit_dag(
        self,
        units: dict[tuple[str, str], Record],
        report: ValidationReport,
    ) -> None:
        graph: dict[tuple[str, str], list[tuple[str, str]]] = {
            key: [] for key in units
        }
        for key, record in units.items():
            for relation in self._list(record.data, "relations"):
                if relation.get("type") != "prerequisite":
                    continue
                target_key = self._reference_key(relation.get("target"))
                if target_key in units:
                    graph[key].append(target_key)

        self._find_cycles(
            graph,
            "UNIT_PREREQUISITE_CYCLE",
            lambda key: f"{key[0]}@{key[1]}",
            lambda key: units[key].path,
            report,
        )

    def _validate_set_dags_and_prerequisites(
        self,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> None:
        for set_record in indexes["set"].values():
            steps = self._list(set_record.data, "steps")
            step_by_id: dict[str, dict[str, Any]] = {}
            for step in steps:
                step_id = step.get("id")
                if not isinstance(step_id, str):
                    continue
                if step_id in step_by_id:
                    report.issues.append(
                        Issue(
                            ERROR,
                            "DUPLICATE_STEP_ID",
                            set_record.path,
                            f"단계 ID {step_id}가 중복되었습니다.",
                        )
                    )
                    continue
                step_by_id[step_id] = step

            graph: dict[str, list[str]] = {step_id: [] for step_id in step_by_id}
            source_position = {
                step.get("id"): index
                for index, step in enumerate(steps)
                if isinstance(step.get("id"), str)
            }
            for step_id, step in step_by_id.items():
                for dependency in self._list(step, "depends_on"):
                    if dependency not in step_by_id:
                        report.issues.append(
                            Issue(
                                ERROR,
                                "UNKNOWN_STEP_DEPENDENCY",
                                set_record.path,
                                f"단계 {step_id}가 없는 단계 {dependency}에 의존합니다.",
                            )
                        )
                        continue
                    graph[step_id].append(dependency)
                    dependency_step = step_by_id[dependency]
                    if (
                        step.get("required") is True
                        and dependency_step.get("required") is False
                    ):
                        report.issues.append(
                            Issue(
                                ERROR,
                                "REQUIRED_STEP_DEPENDS_ON_OPTIONAL",
                                set_record.path,
                                f"필수 단계 {step_id}가 선택 단계 {dependency}에 의존합니다.",
                            )
                        )
                    if source_position.get(dependency, -1) > source_position.get(
                        step_id, -1
                    ):
                        report.issues.append(
                            Issue(
                                WARNING,
                                "STEP_ORDER_NOT_TOPOLOGICAL",
                                set_record.path,
                                f"단계 {dependency}를 의존 단계 {step_id}보다 앞에 배치하십시오.",
                            )
                        )

            versions_by_unit_id: dict[str, set[str]] = {}
            for step in step_by_id.values():
                key = self._reference_key(step.get("unit_ref"))
                if key is not None:
                    versions_by_unit_id.setdefault(key[0], set()).add(key[1])
            for unit_id, versions in versions_by_unit_id.items():
                if len(versions) > 1:
                    report.issues.append(
                        Issue(
                            WARNING,
                            "MIXED_UNIT_VERSIONS",
                            set_record.path,
                            f"{unit_id}의 여러 버전이 한 Set에 함께 사용됩니다.",
                        )
                    )

            has_cycle = self._find_cycles(
                graph,
                "SET_STEP_CYCLE",
                str,
                lambda _key: set_record.path,
                report,
            )
            if not has_cycle:
                self._validate_set_prerequisites(
                    set_record,
                    step_by_id,
                    graph,
                    indexes["unit"],
                    report,
                )

    def _validate_set_prerequisites(
        self,
        set_record: Record,
        step_by_id: dict[str, dict[str, Any]],
        graph: dict[str, list[str]],
        units: dict[tuple[str, str], Record],
        report: ValidationReport,
    ) -> None:
        entry_levels: dict[tuple[str, str], int] = {}
        for requirement in self._list(set_record.data, "entry_requirements"):
            key = self._reference_key(requirement.get("unit"))
            if key is not None:
                entry_levels[key] = LEVEL_ORDER.get(
                    requirement.get("required_level"), -1
                )

        ancestor_cache: dict[str, set[str]] = {}

        def ancestors(step_id: str) -> set[str]:
            cached = ancestor_cache.get(step_id)
            if cached is not None:
                return cached
            result: set[str] = set()
            for dependency in graph.get(step_id, []):
                result.add(dependency)
                result.update(ancestors(dependency))
            ancestor_cache[step_id] = result
            return result

        for step_id, step in step_by_id.items():
            unit_key = self._reference_key(step.get("unit_ref"))
            unit = units.get(unit_key) if unit_key is not None else None
            if unit is None:
                continue

            available_levels = dict(entry_levels)
            for ancestor_id in ancestors(step_id):
                ancestor_step = step_by_id[ancestor_id]
                ancestor_key = self._reference_key(ancestor_step.get("unit_ref"))
                if ancestor_key is not None:
                    available_levels[ancestor_key] = max(
                        available_levels.get(ancestor_key, -1),
                        LEVEL_ORDER.get(ancestor_step.get("required_level"), -1),
                    )

            for relation in self._list(unit.data, "relations"):
                if relation.get("type") != "prerequisite":
                    continue
                prerequisite_key = self._reference_key(relation.get("target"))
                required_level = LEVEL_ORDER.get(relation.get("required_level"), 0)
                actual_level = available_levels.get(prerequisite_key, -1)
                if actual_level < required_level:
                    prereq_label = (
                        f"{prerequisite_key[0]}@{prerequisite_key[1]}"
                        if prerequisite_key is not None
                        else "알 수 없는 Unit"
                    )
                    report.issues.append(
                        Issue(
                            ERROR,
                            "UNSATISFIED_PREREQUISITE",
                            set_record.path,
                            (
                                f"단계 {step_id} 전에 {prereq_label} "
                                f"{relation.get('required_level', 'D0')}가 충족되지 않았습니다."
                            ),
                        )
                    )

    def _resolve(
        self,
        kind: str,
        reference: Any,
        source: Record,
        relation_name: str,
        indexes: dict[str, dict[tuple[str, str], Record]],
        report: ValidationReport,
    ) -> Record | None:
        key = self._reference_key(reference)
        if key is None:
            return None
        target = indexes[kind].get(key)
        if target is None:
            report.issues.append(
                Issue(
                    ERROR,
                    "MISSING_REFERENCE",
                    source.path,
                    (
                        f"{relation_name}: {kind} {key[0]}@{key[1]}를 "
                        "찾을 수 없습니다."
                    ),
                )
            )
            return None

        lifecycle = target.data.get("lifecycle", {})
        status = lifecycle.get("status")
        source_status = source.data.get("lifecycle", {}).get("status")
        if status == "archived" and source_status != "archived":
            report.issues.append(
                Issue(
                    ERROR,
                    "ARCHIVED_REFERENCE",
                    source.path,
                    f"{relation_name}: 보관된 {target.id}@{target.version}를 참조합니다.",
                )
            )
        elif status == "deprecated" and source_status != "archived":
            report.issues.append(
                Issue(
                    WARNING,
                    "DEPRECATED_REFERENCE",
                    source.path,
                    f"{relation_name}: 폐기 예정 {target.id}@{target.version}를 참조합니다.",
                )
            )
        return target

    def _validate_local_path(
        self,
        raw_path: Any,
        record: Record,
        relation_name: str,
        report: ValidationReport,
    ) -> None:
        if not isinstance(raw_path, str):
            return
        if Path(raw_path).is_absolute() or "\\" in raw_path:
            report.issues.append(
                Issue(
                    ERROR,
                    "UNSAFE_LOCAL_PATH",
                    record.path,
                    f"{relation_name}: 작업공간 기준 슬래시 상대경로를 사용해야 합니다.",
                )
            )
            return

        candidate = (self.workspace_root / raw_path).resolve()
        try:
            within_workspace = (
                os.path.commonpath([self.workspace_root, candidate])
                == str(self.workspace_root)
            )
        except ValueError:
            within_workspace = False
        if not within_workspace:
            report.issues.append(
                Issue(
                    ERROR,
                    "PATH_ESCAPES_WORKSPACE",
                    record.path,
                    f"{relation_name}: 경로가 작업공간 밖을 가리킵니다.",
                )
            )
            return
        if not candidate.exists():
            report.issues.append(
                Issue(
                    ERROR,
                    "LOCAL_PATH_NOT_FOUND",
                    record.path,
                    f"{relation_name}: {raw_path}가 없습니다.",
                )
            )

    def _find_cycles(
        self,
        graph: dict[Any, list[Any]],
        code: str,
        label: Any,
        path_for_node: Any,
        report: ValidationReport,
    ) -> bool:
        state: dict[Any, int] = {}
        stack: list[Any] = []
        reported: set[tuple[str, ...]] = set()
        found = False

        def visit(node: Any) -> None:
            nonlocal found
            state[node] = 1
            stack.append(node)
            for target in graph.get(node, []):
                if state.get(target, 0) == 0:
                    visit(target)
                elif state.get(target) == 1:
                    found = True
                    start = stack.index(target)
                    cycle = stack[start:] + [target]
                    rendered = tuple(label(item) for item in cycle)
                    fingerprint = tuple(sorted(set(rendered)))
                    if fingerprint not in reported:
                        reported.add(fingerprint)
                        report.issues.append(
                            Issue(
                                ERROR,
                                code,
                                path_for_node(node),
                                " -> ".join(rendered),
                            )
                        )
            stack.pop()
            state[node] = 2

        for node in graph:
            if state.get(node, 0) == 0:
                visit(node)
        return found

    @staticmethod
    def _reference_key(reference: Any) -> tuple[str, str] | None:
        if not isinstance(reference, dict):
            return None
        identifier = reference.get("id")
        version = reference.get("version")
        if isinstance(identifier, str) and isinstance(version, str):
            return (identifier, version)
        return None

    @staticmethod
    def _list(mapping: Any, key: str) -> list[Any]:
        if not isinstance(mapping, dict):
            return []
        value = mapping.get(key)
        return value if isinstance(value, list) else []

    @staticmethod
    def _report_duplicates(
        values: Iterable[Any],
        record: Record,
        code: str,
        label: str,
        report: ValidationReport,
    ) -> None:
        seen: set[str] = set()
        reported: set[str] = set()
        for value in values:
            if value is None:
                continue
            fingerprint = json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )
            if fingerprint in seen and fingerprint not in reported:
                reported.add(fingerprint)
                report.issues.append(
                    Issue(
                        ERROR,
                        code,
                        record.path,
                        f"{label} {value!r}가 중복되었습니다.",
                    )
                )
            seen.add(fingerprint)

    def _display_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.workspace_root).as_posix()
        except ValueError:
            return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "AX 학습 Unit, Resource, Set, Study, Trend Signal, Capability "
            "Candidate와 Taxonomy Registry 메타데이터를 검증합니다."
        )
    )
    parser.add_argument(
        "roots",
        nargs="*",
        default=[
            "examples/valid",
            "catalog",
            "sets",
            "studies",
            "research/signals",
            "research/capability-survey",
            "taxonomy",
        ],
        help=(
            "검증할 파일 또는 디렉터리입니다. 기본값: "
            "examples/valid catalog sets studies research/signals "
            "research/capability-survey taxonomy"
        ),
    )
    parser.add_argument(
        "--workspace-root",
        default=None,
        help="상대경로 기준 작업공간입니다. 기본값: 이 스크립트의 상위 작업공간",
    )
    parser.add_argument(
        "--schema-dir",
        default="schemas",
        help="JSON Schema 디렉터리입니다. 기본값: schemas",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="성공 시 개별 메시지를 생략합니다.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    default_root = Path(__file__).resolve().parents[1]
    workspace_root = (
        Path(args.workspace_root).resolve()
        if args.workspace_root
        else default_root
    )
    schema_dir = Path(args.schema_dir)
    if not schema_dir.is_absolute():
        schema_dir = workspace_root / schema_dir

    try:
        validator = CatalogValidator(
            workspace_root=workspace_root,
            schema_dir=schema_dir,
        )
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        print(f"ERROR|SCHEMA_LOAD|{schema_dir}|{exc}")
        return 2

    report = validator.validate(Path(root) for root in args.roots)
    for issue in sorted(
        report.issues,
        key=lambda item: (
            item.severity != ERROR,
            item.code,
            str(item.path),
            item.message,
        ),
    ):
        print(issue.render(workspace_root))

    def _format(prefix: str, counts: dict[str, int], tail: str = "") -> str:
        return (
            f"{prefix}|units={counts['unit']}|"
            f"resources={counts['resource']}|"
            f"sets={counts['set']}|"
            f"studies={counts['study']}|"
            f"signals={counts['signal']}|"
            f"candidates={counts['candidate']}|"
            f"handoffs={counts['handoff']}|"
            f"taxonomies={counts['taxonomy']}"
            f"{tail}"
        )

    summary = _format(
        "SUMMARY",
        report.counts,
        f"|errors={report.error_count}|warnings={report.warning_count}",
    )
    # SUMMARY는 검사한 전체이며 `examples/valid`의 가상 표본을 포함합니다.
    # 실제 카탈로그 규모는 SUMMARY_REAL로 따로 보고합니다.
    summary_real = _format("SUMMARY_REAL", report.real_counts())
    if not args.quiet or report.issues:
        print(summary)
        print(summary_real)

    return 0 if report.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
