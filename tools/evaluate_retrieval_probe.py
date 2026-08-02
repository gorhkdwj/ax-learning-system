#!/usr/bin/env python
"""고정 RAG 검색 snapshot을 채점하고 가장 단순한 충분 방식을 판정합니다."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_METHODS = {
    "text_vector",
    "metadata_relational",
    "structured_graph",
}


@dataclass(frozen=True)
class ProbeIssue:
    code: str
    message: str


def evaluate_probe(
    probe: dict[str, Any],
    decision: dict[str, Any],
) -> tuple[list[ProbeIssue], dict[str, dict[str, int | bool]]]:
    issues: list[ProbeIssue] = []
    questions = probe.get("golden_questions", [])
    if not isinstance(questions, list) or len(questions) != 12:
        issues.append(
            ProbeIssue(
                "GOLDEN_QUESTION_COUNT",
                f"골든 질문은 정확히 12개여야 합니다: actual={len(questions) if isinstance(questions, list) else 0}",
            )
        )
        questions = []
    question_ids = {
        item.get("id") for item in questions if isinstance(item, dict)
    }
    required_ids = {
        item.get("id")
        for item in questions
        if isinstance(item, dict) and item.get("required") is True
    }

    snapshots = probe.get("snapshots", {})
    if not isinstance(snapshots, dict) or set(snapshots) != EXPECTED_METHODS:
        issues.append(
            ProbeIssue(
                "METHOD_SET_MISMATCH",
                "text_vector, metadata_relational, structured_graph snapshot이 모두 필요합니다.",
            )
        )
        snapshots = {}

    scorecards: dict[str, dict[str, int | bool]] = {}
    for method, snapshot in snapshots.items():
        if not isinstance(snapshot, dict):
            continue
        results = snapshot.get("results", [])
        result_by_id = {
            item.get("question_id"): item
            for item in results
            if isinstance(item, dict)
        }
        missing = sorted(question_ids - set(result_by_id))
        if missing:
            issues.append(
                ProbeIssue(
                    "SNAPSHOT_QUESTION_MISSING",
                    f"{method}에 질문 결과가 없습니다: {missing}",
                )
            )
        required_results = [
            result_by_id[question_id]
            for question_id in required_ids
            if question_id in result_by_id
        ]
        recovered = sum(
            item.get("required_facts_recovered") is True
            for item in required_results
        )
        wrong = sum(
            int(item.get("wrong_evidence_count", 0))
            for item in required_results
        )
        freshness_failures = sum(
            item.get("freshness_pass") is not True for item in required_results
        )
        acl_failures = sum(
            item.get("acl_pass") is not True for item in required_results
        )
        trace_failures = sum(
            item.get("traceable") is not True for item in required_results
        )
        qualifies = (
            len(required_results) == len(required_ids)
            and recovered == len(required_ids)
            and wrong == 0
            and freshness_failures == 0
            and acl_failures == 0
            and trace_failures == 0
        )
        scorecards[method] = {
            "required_recovered": recovered,
            "required_total": len(required_ids),
            "wrong_evidence": wrong,
            "freshness_failures": freshness_failures,
            "acl_failures": acl_failures,
            "trace_failures": trace_failures,
            "maintenance_rank": int(snapshot.get("maintenance_rank", 99)),
            "qualifies": qualifies,
        }

    qualifying = [
        method
        for method, score in scorecards.items()
        if score.get("qualifies") is True
    ]
    recommended = (
        min(
            qualifying,
            key=lambda method: int(scorecards[method]["maintenance_rank"]),
        )
        if qualifying
        else None
    )
    selected = decision.get("selected_baseline")
    if selected != recommended:
        issues.append(
            ProbeIssue(
                "NOT_SIMPLEST_SUFFICIENT",
                f"selected={selected}, recommended={recommended}",
            )
        )
    if selected == "structured_graph":
        non_graph_qualifies = any(
            method != "structured_graph"
            and scorecards.get(method, {}).get("qualifies") is True
            for method in scorecards
        )
        unique_questions = decision.get("graph_only_required_question_ids", [])
        gates = decision.get("graph_gates", {})
        if non_graph_qualifies or not unique_questions:
            issues.append(
                ProbeIssue(
                    "UNJUSTIFIED_GRAPH_SELECTION",
                    "그래프만 해결한 필수 관계 질문이 입증되지 않았습니다.",
                )
            )
        if not isinstance(gates, dict) or not (
            gates.get("acl_pass") is True and gates.get("freshness_pass") is True
        ):
            issues.append(
                ProbeIssue(
                    "GRAPH_GATE_FAILED",
                    "그래프 방식의 ACL·최신성 Gate가 통과하지 않았습니다.",
                )
            )

    choices = decision.get("question_type_choices")
    if not isinstance(choices, list) or not choices:
        issues.append(
            ProbeIssue(
                "QUESTION_TYPE_TABLE_MISSING",
                "질문 유형별 검색 방식 선택표가 없습니다.",
            )
        )
    for field_name in ("excluded_reasons", "revisit_conditions"):
        value = decision.get(field_name)
        if not isinstance(value, list) or not value:
            issues.append(
                ProbeIssue(
                    "DECISION_RECORD_INCOMPLETE",
                    f"{field_name} 기록이 비어 있습니다.",
                )
            )

    return issues, scorecards


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probe", type=Path)
    parser.add_argument("decision", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        probe = json.loads(args.probe.read_text(encoding="utf-8"))
        decision = json.loads(args.decision.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"PROBE_ERROR|INPUT_PARSE|{exc}")
        return 2
    if not isinstance(probe, dict) or not isinstance(decision, dict):
        print("PROBE_ERROR|ROOT_NOT_OBJECT|입력 최상위 값은 객체여야 합니다.")
        return 2

    issues, scorecards = evaluate_probe(probe, decision)
    for method, score in sorted(scorecards.items()):
        print(
            "PROBE_SCORE|"
            f"method={method}|recovered={score['required_recovered']}/{score['required_total']}|"
            f"wrong={score['wrong_evidence']}|freshness_failures={score['freshness_failures']}|"
            f"acl_failures={score['acl_failures']}|trace_failures={score['trace_failures']}|"
            f"qualifies={'yes' if score['qualifies'] else 'no'}"
        )
    for issue in issues:
        print(f"PROBE_ERROR|{issue.code}|{issue.message}")
    print(f"PROBE_SUMMARY|status={'passed' if not issues else 'failed'}|errors={len(issues)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
