from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.evaluate_domain_learning import evaluate_learning


class DomainLearningEvaluatorTest(unittest.TestCase):
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

    def _load(self, name: str) -> dict:
        return json.loads(
            (self.fixture_root / name).read_text(encoding="utf-8")
        )

    def test_two_valid_transfer_models_and_review_pass(self) -> None:
        issues = evaluate_learning(
            [self._load("valid.json"), self._load("valid-transfer.json")],
            self._load("semantic-review.valid.json"),
        )

        self.assertEqual(issues, [])

    def test_duplicate_transfer_model_is_rejected(self) -> None:
        model = self._load("valid.json")
        codes = {
            issue.code
            for issue in evaluate_learning(
                [model, json.loads(json.dumps(model))],
                self._load("semantic-review.valid.json"),
            )
        }

        self.assertIn("DISTINCT_TRANSFER_MODELS_REQUIRED", codes)
        self.assertIn("DISTINCT_TRANSFER_TASKS_REQUIRED", codes)

    def test_failed_semantic_review_blocks_completion(self) -> None:
        codes = {
            issue.code
            for issue in evaluate_learning(
                [self._load("valid.json"), self._load("valid-transfer.json")],
                self._load("semantic-review.failed.json"),
            )
        }

        self.assertIn("SEMANTIC_CRITERION_FAILED", codes)
        self.assertIn("REMEDIATION_REQUIRED", codes)


if __name__ == "__main__":
    unittest.main()
