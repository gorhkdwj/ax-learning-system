#!/usr/bin/env python
"""두 독립 전이 모델과 사람 의미 검토를 하나의 D2 완료 Gate로 검사합니다."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from tools.evaluate_domain_model import (
        ModelIssue,
        evaluate_model,
        evaluate_semantic_review,
    )
except ModuleNotFoundError:  # 직접 스크립트 실행에서는 tools/가 sys.path 루트입니다.
    from evaluate_domain_model import (  # type: ignore[no-redef]
        ModelIssue,
        evaluate_model,
        evaluate_semantic_review,
    )


def evaluate_learning(
    models: list[dict[str, Any]], semantic_review: dict[str, Any]
) -> list[ModelIssue]:
    issues: list[ModelIssue] = []
    if len(models) != 2:
        return [
            ModelIssue(
                "TWO_MODEL_FILES_REQUIRED",
                "D2 완료에는 서로 다른 두 전이 모델 파일이 필요합니다.",
            )
        ]

    model_ids = [model.get("submission_id") for model in models]
    if any(not isinstance(model_id, str) or not model_id.strip() for model_id in model_ids):
        issues.append(
            ModelIssue(
                "SUBMISSION_ID_REQUIRED",
                "각 전이 모델에 안정적인 submission_id가 필요합니다.",
            )
        )
        model_ids = []
    elif len(set(model_ids)) != 2:
        issues.append(
            ModelIssue(
                "DISTINCT_TRANSFER_MODELS_REQUIRED",
                "두 전이 모델의 submission_id는 서로 달라야 합니다.",
            )
        )

    task_ids = [model.get("transfer_task_id") for model in models]
    if any(not isinstance(task_id, str) or not task_id.strip() for task_id in task_ids):
        issues.append(
            ModelIssue(
                "TRANSFER_TASK_ID_REQUIRED",
                "각 전이 모델에 transfer_task_id가 필요합니다.",
            )
        )
    elif len(set(task_ids)) != 2:
        issues.append(
            ModelIssue(
                "DISTINCT_TRANSFER_TASKS_REQUIRED",
                "서로 다른 두 전이과제를 수행해야 합니다.",
            )
        )

    for model in models:
        issues.extend(evaluate_model(model))
    issues.extend(
        evaluate_semantic_review(
            semantic_review,
            model_ids=[item for item in model_ids if isinstance(item, str)],
        )
    )
    return issues


def _read_object(path: Path, label: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{label} 최상위 값은 JSON 객체여야 합니다.")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first_model", type=Path)
    parser.add_argument("second_model", type=Path)
    parser.add_argument("semantic_review", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        models = [
            _read_object(args.first_model, "첫 모델"),
            _read_object(args.second_model, "둘째 모델"),
        ]
        semantic_review = _read_object(args.semantic_review, "의미 검토")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"LEARNING_ERROR|INPUT_PARSE|{exc}")
        return 2

    issues = evaluate_learning(models, semantic_review)
    for issue in issues:
        print(f"LEARNING_ERROR|{issue.code}|{issue.message}")
    print(
        f"LEARNING_SUMMARY|status={'passed' if not issues else 'failed'}|"
        f"models={len(models)}|errors={len(issues)}"
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
