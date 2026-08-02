from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.evaluate_domain_model import evaluate_model, evaluate_semantic_review


class DomainModelEvaluatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_root = (
            Path(__file__).resolve().parents[1]
            / "catalog"
            / "items"
            / "unit.data-analytics-ml.domain-concept-relationship-modeling"
            / "resources"
            / "lab"
            / "fixtures"
        )

    def _codes(self, name: str) -> set[str]:
        data = json.loads(
            (self.fixture_root / name).read_text(encoding="utf-8")
        )
        return {issue.code for issue in evaluate_model(data)}

    def _semantic_codes(
        self,
        name: str,
        *, model_id: str = "submission.synthetic-knowledge-library.valid",
    ) -> set[str]:
        data = json.loads(
            (self.fixture_root / name).read_text(encoding="utf-8")
        )
        return {
            issue.code
            for issue in evaluate_semantic_review(data, model_id=model_id)
        }

    def test_valid_model_passes(self) -> None:
        self.assertEqual(self._codes("valid.json"), set())

    def test_too_many_classes_is_rejected(self) -> None:
        self.assertIn(
            "CLASS_COUNT_OUT_OF_RANGE",
            self._codes("too-many-classes.json"),
        )

    def test_missing_state_is_rejected(self) -> None:
        self.assertIn("STATE_NOT_MODELED", self._codes("missing-state.json"))

    def test_unanswerable_question_is_rejected(self) -> None:
        self.assertIn(
            "UNANSWERABLE_QUESTION",
            self._codes("unanswerable-question.json"),
        )

    def test_graph_requires_unique_question_and_gates(self) -> None:
        codes = self._codes("unsupported-graph.json")

        self.assertIn("UNJUSTIFIED_GRAPH_SELECTION", codes)
        self.assertIn("UNNECESSARY_COMPLEXITY", codes)

    def test_valid_semantic_review_passes(self) -> None:
        self.assertEqual(
            self._semantic_codes("semantic-review.valid.json"),
            set(),
        )

    def test_failed_semantic_review_is_rejected(self) -> None:
        codes = self._semantic_codes("semantic-review.failed.json")

        self.assertIn("TWO_TRANSFER_MODELS_REQUIRED", codes)
        self.assertIn("SEMANTIC_CRITERIA_MISSING", codes)
        self.assertIn("SEMANTIC_CRITERION_FAILED", codes)
        self.assertIn("ORAL_EXPLANATION_NOT_CONFIRMED", codes)
        self.assertIn("REMEDIATION_REQUIRED", codes)
        self.assertIn("REMEDIATION_TIME_OUT_OF_RANGE", codes)
        self.assertIn("REMEDIATION_RETEST_REQUIRED", codes)

    def test_semantic_review_must_include_current_model(self) -> None:
        self.assertIn(
            "SEMANTIC_REVIEW_MODEL_MISMATCH",
            self._semantic_codes(
                "semantic-review.valid.json",
                model_id="submission.not-reviewed",
            ),
        )

    def test_repeated_error_remediation_is_bounded(self) -> None:
        data = json.loads(
            (self.fixture_root / "semantic-review.valid.json").read_text(
                encoding="utf-8"
            )
        )
        data["repeated_error_codes"] = ["VALUE_OR_STATE_PROMOTED_TO_CLASS"]
        data["remediation"] = {
            "required": True,
            "minutes": 121,
            "retest_status": "passed",
        }

        codes = {
            issue.code
            for issue in evaluate_semantic_review(
                data,
                model_id="submission.synthetic-knowledge-library.valid",
            )
        }
        self.assertIn("REMEDIATION_TIME_OUT_OF_RANGE", codes)


if __name__ == "__main__":
    unittest.main()
