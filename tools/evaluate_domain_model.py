#!/usr/bin/env python
"""질문 기반 도메인 개념·관계 모델링 산출물을 결정적으로 검사합니다."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPRESENTATION_ORDER = {"json": 0, "rdbms": 1, "graph": 2}
REQUIRED_SEMANTIC_CRITERIA = {
    "question-answerability",
    "classification-semantics",
    "temporality-provenance",
    "representation-sufficiency",
    "independent-transfer",
    "oral-explanation",
}


@dataclass(frozen=True)
class ModelIssue:
    code: str
    message: str


def _items(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _duplicates(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def evaluate_model(data: dict[str, Any]) -> list[ModelIssue]:
    issues: list[ModelIssue] = []
    classes = _items(data, "classes")
    fields = _items(data, "fields")
    relations = _items(data, "relations")
    questions = _items(data, "questions")

    if not 3 <= len(classes) <= 7:
        issues.append(
            ModelIssue(
                "CLASS_COUNT_OUT_OF_RANGE",
                f"클래스 수는 3~7개여야 합니다: actual={len(classes)}",
            )
        )

    class_ids = {item.get("id") for item in classes if item.get("id")}
    for duplicate in _duplicates([item.get("id") for item in classes]):
        issues.append(ModelIssue("DUPLICATE_CLASS_ID", f"중복 클래스: {duplicate}"))
    for item in classes:
        if item.get("role") in {"value", "state"}:
            issues.append(
                ModelIssue(
                    "VALUE_OR_STATE_PROMOTED_TO_CLASS",
                    f"값 또는 상태를 클래스로 승격했습니다: {item.get('id')}",
                )
            )

    field_ids = {item.get("id") for item in fields if item.get("id")}
    for item in fields:
        if item.get("owner") not in class_ids:
            issues.append(
                ModelIssue(
                    "FIELD_OWNER_NOT_FOUND",
                    f"필드 owner가 없습니다: {item.get('id')}",
                )
            )

    relation_ids = {item.get("id") for item in relations if item.get("id")}
    for item in relations:
        if item.get("from") not in class_ids or item.get("to") not in class_ids:
            issues.append(
                ModelIssue(
                    "RELATION_ENDPOINT_NOT_FOUND",
                    f"관계 끝점이 없습니다: {item.get('id')}",
                )
            )

    field_kinds = {item.get("kind") for item in fields}
    class_roles = {item.get("role") for item in classes}
    if "state" not in field_kinds:
        issues.append(
            ModelIssue("STATE_NOT_MODELED", "시간에 따라 변하는 상태 필드가 없습니다.")
        )
    if "temporal" not in field_kinds:
        issues.append(
            ModelIssue(
                "TEMPORALITY_NOT_MODELED",
                "상태의 기준 시점 또는 유효기간 필드가 없습니다.",
            )
        )
    if "provenance" not in field_kinds and "source" not in class_roles:
        issues.append(
            ModelIssue("SOURCE_NOT_MODELED", "원천 추적 필드 또는 Source 클래스가 없습니다.")
        )
    if "version" not in field_kinds and "version" not in class_roles:
        issues.append(
            ModelIssue("VERSION_NOT_MODELED", "버전 필드 또는 Version 클래스가 없습니다.")
        )

    known_path_ids = class_ids | field_ids | relation_ids
    question_ids = {item.get("id") for item in questions if item.get("id")}
    for item in questions:
        path_ids = item.get("answer_path_ids")
        if not isinstance(path_ids, list) or not path_ids:
            issues.append(
                ModelIssue(
                    "UNANSWERABLE_QUESTION",
                    f"답변 경로가 비어 있습니다: {item.get('id')}",
                )
            )
            continue
        missing = [path_id for path_id in path_ids if path_id not in known_path_ids]
        if missing:
            issues.append(
                ModelIssue(
                    "UNANSWERABLE_QUESTION",
                    f"{item.get('id')}의 답변 경로가 모델에 없습니다: {missing}",
                )
            )

    decision = data.get("representation_decision", {})
    if not isinstance(decision, dict):
        decision = {}
    selected = decision.get("selected")
    sufficient = decision.get("sufficient_representations", [])
    if selected not in REPRESENTATION_ORDER:
        issues.append(ModelIssue("REPRESENTATION_NOT_SELECTED", "표현 기술을 선택하지 않았습니다."))
    elif selected not in sufficient:
        issues.append(
            ModelIssue(
                "SELECTED_REPRESENTATION_INSUFFICIENT",
                "선택한 표현이 질문을 충족하는 방식 목록에 없습니다.",
            )
        )
    else:
        simpler = [
            item
            for item in sufficient
            if item in REPRESENTATION_ORDER
            and REPRESENTATION_ORDER[item] < REPRESENTATION_ORDER[selected]
        ]
        if simpler:
            issues.append(
                ModelIssue(
                    "UNNECESSARY_COMPLEXITY",
                    f"더 단순한 충분 표현이 있습니다: {simpler}",
                )
            )

    graph_question_ids = decision.get("graph_required_question_ids", [])
    if selected == "graph":
        valid_graph_questions = [
            question_id
            for question_id in graph_question_ids
            if question_id in question_ids
        ]
        gates = decision.get("gates", {})
        if not valid_graph_questions:
            issues.append(
                ModelIssue(
                    "UNJUSTIFIED_GRAPH_SELECTION",
                    "다른 표현이 충족하지 못한 필수 관계 질문이 없습니다.",
                )
            )
        if not isinstance(gates, dict) or not (
            gates.get("acl_pass") is True and gates.get("freshness_pass") is True
        ):
            issues.append(
                ModelIssue(
                    "GRAPH_GATE_FAILED",
                    "그래프 선택에는 ACL과 최신성 Gate 통과가 필요합니다.",
                )
            )

    rationale = decision.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        issues.append(
            ModelIssue("REPRESENTATION_RATIONALE_MISSING", "질문과 유지비에 근거한 선택 이유가 없습니다.")
        )

    corrected_errors = data.get("corrected_errors")
    if not isinstance(corrected_errors, list) or len(corrected_errors) < 2:
        issues.append(
            ModelIssue(
                "HIDDEN_ERRORS_NOT_CORRECTED",
                "독립 전이평가에서 최소 두 가지 모델링 오류를 찾아 수정해야 합니다.",
            )
        )

    explanation = data.get("human_explanation")
    required_explanations = (
        "classification_reason",
        "representation_reason",
        "validation_evidence",
    )
    if not isinstance(explanation, dict) or any(
        not isinstance(explanation.get(key), str) or not explanation[key].strip()
        for key in required_explanations
    ):
        issues.append(
            ModelIssue(
                "HUMAN_EXPLANATION_REQUIRED",
                "최종 분류·표현 선택·검증 근거를 사용자 설명으로 남겨야 합니다.",
            )
        )

    return issues


def evaluate_semantic_review(
    data: dict[str, Any], *, model_id: str | None = None, model_ids: list[str] | None = None
) -> list[ModelIssue]:
    """사람이 수행한 의미 검토와 적응형 보충학습 계약을 검사합니다."""

    issues: list[ModelIssue] = []
    reviewed_model_ids = data.get("reviewed_model_ids")
    if not isinstance(reviewed_model_ids, list) or not all(
        isinstance(item, str) and item.strip() for item in reviewed_model_ids
    ) or len(reviewed_model_ids) < 2:
        issues.append(
            ModelIssue(
                "TWO_TRANSFER_MODELS_REQUIRED",
                "서로 다른 두 전이 모델의 ID를 의미 검토에 기록해야 합니다.",
            )
        )
        reviewed_model_ids = []
    elif len(set(reviewed_model_ids)) != len(reviewed_model_ids):
        issues.append(
            ModelIssue(
                "DUPLICATE_REVIEWED_MODEL_ID",
                "의미 검토의 전이 모델 ID는 서로 달라야 합니다.",
            )
        )

    expected_model_ids = list(model_ids or [])
    if model_id:
        expected_model_ids.append(model_id)
    for expected_model_id in expected_model_ids:
        if expected_model_id not in reviewed_model_ids:
            issues.append(
                ModelIssue(
                    "SEMANTIC_REVIEW_MODEL_MISMATCH",
                    f"현재 모델 ID가 의미 검토 대상에 없습니다: {expected_model_id}",
                )
            )

    if data.get("reviewer_type") not in {
        "learner_self_review",
        "human_peer_review",
    }:
        issues.append(
            ModelIssue(
                "HUMAN_REVIEWER_REQUIRED",
                "학습자 자기검토 또는 사람 동료검토 유형을 명시해야 합니다.",
            )
        )

    reviewed_at = data.get("reviewed_at")
    try:
        if not isinstance(reviewed_at, str):
            raise ValueError
        date.fromisoformat(reviewed_at)
    except ValueError:
        issues.append(
            ModelIssue(
                "SEMANTIC_REVIEW_DATE_INVALID",
                "의미 검토일을 YYYY-MM-DD 형식으로 기록해야 합니다.",
            )
        )

    criteria = _items(data, "criteria")
    criteria_by_id = {
        item.get("id"): item for item in criteria if isinstance(item.get("id"), str)
    }
    missing_criteria = sorted(REQUIRED_SEMANTIC_CRITERIA - criteria_by_id.keys())
    if missing_criteria:
        issues.append(
            ModelIssue(
                "SEMANTIC_CRITERIA_MISSING",
                f"필수 의미 검토 기준이 없습니다: {missing_criteria}",
            )
        )
    for criterion_id in sorted(REQUIRED_SEMANTIC_CRITERIA):
        criterion = criteria_by_id.get(criterion_id)
        if criterion is None:
            continue
        if criterion.get("status") != "pass":
            issues.append(
                ModelIssue(
                    "SEMANTIC_CRITERION_FAILED",
                    f"사람 의미 검토를 통과하지 못했습니다: {criterion_id}",
                )
            )
        evidence = criterion.get("evidence")
        if not isinstance(evidence, str) or len(evidence.strip()) < 20:
            issues.append(
                ModelIssue(
                    "SEMANTIC_EVIDENCE_INSUFFICIENT",
                    f"의미 검토 근거를 구체적으로 기록해야 합니다: {criterion_id}",
                )
            )

    if data.get("oral_explanation_confirmed") is not True:
        issues.append(
            ModelIssue(
                "ORAL_EXPLANATION_NOT_CONFIRMED",
                "사용자가 분류·표현 선택·검증 근거를 자신의 말로 설명해야 합니다.",
            )
        )

    repeated_error_codes = data.get("repeated_error_codes", [])
    if not isinstance(repeated_error_codes, list):
        repeated_error_codes = []
        issues.append(
            ModelIssue(
                "REPEATED_ERROR_CODES_INVALID",
                "반복 오류 코드는 배열로 기록해야 합니다.",
            )
        )
    remediation = data.get("remediation")
    if not isinstance(remediation, dict):
        remediation = {}
    remediation_required = remediation.get("required") is True
    remediation_minutes = remediation.get("minutes")
    retest_status = remediation.get("retest_status")
    if repeated_error_codes:
        if not remediation_required:
            issues.append(
                ModelIssue(
                    "REMEDIATION_REQUIRED",
                    "반복 오류가 있으면 보충학습을 수행해야 합니다.",
                )
            )
        if not isinstance(remediation_minutes, int) or not 1 <= remediation_minutes <= 120:
            issues.append(
                ModelIssue(
                    "REMEDIATION_TIME_OUT_OF_RANGE",
                    "반복 오류 보충학습은 1~120분 범위여야 합니다.",
                )
            )
        if retest_status != "passed":
            issues.append(
                ModelIssue(
                    "REMEDIATION_RETEST_REQUIRED",
                    "보충학습 뒤 재평가를 통과해야 합니다.",
                )
            )
    elif remediation_required or remediation_minutes not in {0, None}:
        issues.append(
            ModelIssue(
                "UNNECESSARY_REMEDIATION",
                "반복 오류가 없으면 시간을 채우기 위한 보충학습을 배정하지 않습니다.",
            )
        )

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="검사할 모델 JSON 경로")
    parser.add_argument(
        "--semantic-review",
        type=Path,
        help="두 전이 모델을 대상으로 수행한 사람 의미 검토 JSON 경로",
    )
    parser.add_argument(
        "--require-semantic-review",
        action="store_true",
        help="사람 의미 검토가 없으면 완료 판정을 실패로 처리합니다.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = json.loads(args.model.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MODEL_ERROR|INPUT_PARSE|{exc}")
        return 2
    if not isinstance(data, dict):
        print("MODEL_ERROR|ROOT_NOT_OBJECT|최상위 값은 JSON 객체여야 합니다.")
        return 2

    issues = evaluate_model(data)
    if args.semantic_review is not None:
        try:
            semantic_review = json.loads(
                args.semantic_review.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            print(f"MODEL_ERROR|SEMANTIC_REVIEW_PARSE|{exc}")
            return 2
        if not isinstance(semantic_review, dict):
            print("MODEL_ERROR|SEMANTIC_REVIEW_ROOT|의미 검토는 JSON 객체여야 합니다.")
            return 2
        issues.extend(
            evaluate_semantic_review(
                semantic_review,
                model_id=data.get("submission_id"),
            )
        )
    elif args.require_semantic_review:
        issues.append(
            ModelIssue(
                "SEMANTIC_REVIEW_REQUIRED",
                "D2 완료에는 두 전이 모델의 사람 의미 검토가 필요합니다.",
            )
        )
    for issue in issues:
        print(f"MODEL_ERROR|{issue.code}|{issue.message}")
    print(f"MODEL_SUMMARY|status={'passed' if not issues else 'failed'}|errors={len(issues)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
