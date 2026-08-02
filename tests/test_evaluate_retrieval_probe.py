from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.evaluate_retrieval_probe import evaluate_probe


class RetrievalProbeEvaluatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resource_root = (
            Path(__file__).resolve().parents[1]
            / "sets"
            / "set.workflow.retrieval-grounded-generation"
            / "resources"
            / "representation-probe"
        )
        cls.probe = json.loads(
            (cls.resource_root / "probe.json").read_text(encoding="utf-8")
        )
        cls.decision = json.loads(
            (cls.resource_root / "decision.example.json").read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def _codes(issues) -> set[str]:
        return {issue.code for issue in issues}

    def test_example_selects_simplest_sufficient_method(self) -> None:
        issues, scorecards = evaluate_probe(self.probe, self.decision)

        self.assertEqual(issues, [])
        self.assertFalse(scorecards["text_vector"]["qualifies"])
        self.assertTrue(scorecards["metadata_relational"]["qualifies"])
        self.assertTrue(scorecards["structured_graph"]["qualifies"])

    def test_unjustified_graph_choice_is_rejected(self) -> None:
        decision = copy.deepcopy(self.decision)
        decision["selected_baseline"] = "structured_graph"

        issues, _ = evaluate_probe(self.probe, decision)
        codes = self._codes(issues)

        self.assertIn("NOT_SIMPLEST_SUFFICIENT", codes)
        self.assertIn("UNJUSTIFIED_GRAPH_SELECTION", codes)

    def test_all_twelve_question_results_are_required(self) -> None:
        probe = copy.deepcopy(self.probe)
        probe["snapshots"]["metadata_relational"]["results"].pop()

        issues, _ = evaluate_probe(probe, self.decision)

        self.assertIn("SNAPSHOT_QUESTION_MISSING", self._codes(issues))


if __name__ == "__main__":
    unittest.main()
