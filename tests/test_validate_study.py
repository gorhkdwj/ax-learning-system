from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.validate_catalog import CatalogValidator, build_parser


class StudyValidationTest(unittest.TestCase):
    """Study 스키마와 교차 검증 규칙을 실제 파일 단위로 검증합니다."""

    STUDY_RELATIVE_PATH = (
        Path("studies") / "study.example.grounded-eval-article" / "study.json"
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace_root = Path(__file__).resolve().parents[1]
        cls.schema_dir = cls.workspace_root / "schemas"

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "valid"
        shutil.copytree(
            self.workspace_root / "examples" / "valid",
            self.fixture_root,
        )
        # 승격된 content-provenance Resource는 정규 Unit이 소유하므로 fixture로
        # 복사하지 않습니다. 소유자가 examples/valid에만 있던 문제는 2026-08-06에
        # 정규 등록으로 해소했습니다.
        self.signal_root = Path(self.temporary_directory.name) / "signals"
        shutil.copytree(
            self.workspace_root / "research" / "signals",
            self.signal_root,
        )
        self.taxonomy_root = Path(self.temporary_directory.name) / "taxonomy"
        shutil.copytree(
            self.workspace_root / "taxonomy",
            self.taxonomy_root,
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def validate(self):
        validator = CatalogValidator(
            workspace_root=self.workspace_root,
            schema_dir=self.schema_dir,
        )
        return validator.validate(
            [
                self.fixture_root,
                self.signal_root,
                self.taxonomy_root,
            ]
        )

    def mutate_study(
        self,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = self.fixture_root / self.STUDY_RELATIVE_PATH
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def mutate_taxonomy(
        self,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = self.taxonomy_root / "taxonomy.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def codes(report) -> set[str]:
        return {issue.code for issue in report.issues}

    @staticmethod
    def make_applied(data: dict[str, Any]) -> None:
        data["status"] = "applied"
        data["application"] = {
            "task": "근거 평가 기록 형식을 팀 평가 절차서에 반영했습니다.",
            "evidence_paths": ["studies/README.md"],
            "completed_at": "2026-08-02",
        }

    def test_default_roots_include_studies(self) -> None:
        args = build_parser().parse_args([])

        self.assertIn("studies", args.roots)

    def test_valid_example_study_passes(self) -> None:
        report = self.validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)
        self.assertEqual(report.counts["study"], 1)

    def test_missing_taxonomy_refs_is_schema_error(self) -> None:
        self.mutate_study(lambda data: data.pop("taxonomy_refs"))

        self.assertIn("SCHEMA_ERROR", self.codes(self.validate()))

    def test_unknown_taxonomy_node_is_rejected(self) -> None:
        self.mutate_study(
            lambda data: data.update(taxonomy_refs=["nonexistent-node"])
        )

        self.assertIn("STUDY_TAXONOMY_UNKNOWN", self.codes(self.validate()))

    def test_deprecated_taxonomy_node_is_rejected(self) -> None:
        def deprecate_node(data: dict[str, Any]) -> None:
            for node in data["nodes"]:
                if node["id"] == "opportunity-discovery":
                    node["status"] = "deprecated"

        self.mutate_taxonomy(deprecate_node)
        self.mutate_study(
            lambda data: data.update(taxonomy_refs=["opportunity-discovery"])
        )

        self.assertIn("STUDY_TAXONOMY_DEPRECATED", self.codes(self.validate()))

    def test_source_without_url_or_private_ref_is_rejected(self) -> None:
        self.mutate_study(lambda data: data["source"].pop("url"))

        self.assertIn("STUDY_SOURCE_MISSING", self.codes(self.validate()))

    def test_applied_without_application_is_rejected(self) -> None:
        self.mutate_study(lambda data: data.update(status="applied"))

        report = self.validate()

        self.assertIn("STUDY_APPLIED_WITHOUT_APPLICATION", self.codes(report))
        self.assertNotIn("STUDY_APPLIED_WITHOUT_CONFIRMATION", self.codes(report))

    def test_applied_with_only_ai_derived_takeaways_is_rejected(self) -> None:
        def change(data: dict[str, Any]) -> None:
            self.make_applied(data)
            for takeaway in data["takeaways"]:
                takeaway["verification"]["status"] = "ai_derived"
                takeaway["verification"].pop("source_url", None)

        self.mutate_study(change)

        report = self.validate()

        self.assertIn("STUDY_APPLIED_WITHOUT_CONFIRMATION", self.codes(report))
        self.assertNotIn("STUDY_APPLIED_WITHOUT_APPLICATION", self.codes(report))

    def test_applied_with_human_confirmation_passes(self) -> None:
        self.mutate_study(self.make_applied)

        report = self.validate()

        self.assertTrue(report.is_valid)
        self.assertNotIn("STUDY_APPLIED_WITHOUT_CONFIRMATION", self.codes(report))

    def test_contradicts_without_cross_checked_is_rejected(self) -> None:
        def change(data: dict[str, Any]) -> None:
            for takeaway in data["takeaways"]:
                if takeaway["verification"]["status"] == "cross_checked":
                    takeaway["verification"]["status"] = "human_confirmed"
            data["outcome_coverage"] = [
                {
                    "outcome_id": "outcome.example.grounded-output-evaluation.apply",
                    "coverage": "contradicts",
                    "mapped_at": "2026-08-02",
                }
            ]

        self.mutate_study(change)

        self.assertIn(
            "STUDY_CONTRADICTS_WITHOUT_EVIDENCE",
            self.codes(self.validate()),
        )

    def test_contradicts_with_cross_checked_passes(self) -> None:
        self.mutate_study(
            lambda data: data.update(
                outcome_coverage=[
                    {
                        "outcome_id": "outcome.example.grounded-output-evaluation.apply",
                        "coverage": "contradicts",
                        "basis": "아티클의 평가 기록 형식이 Unit 기준과 상충합니다.",
                        "mapped_at": "2026-08-02",
                    }
                ]
            )
        )

        report = self.validate()

        self.assertTrue(report.is_valid)
        self.assertNotIn(
            "STUDY_CONTRADICTS_WITHOUT_EVIDENCE",
            self.codes(report),
        )

    def test_unknown_outcome_id_is_rejected(self) -> None:
        self.mutate_study(
            lambda data: data.update(
                outcome_coverage=[
                    {
                        "outcome_id": "outcome.example.does-not-exist",
                        "coverage": "partial",
                        "mapped_at": "2026-08-02",
                    }
                ]
            )
        )

        self.assertIn("STUDY_OUTCOME_UNKNOWN", self.codes(self.validate()))

    def test_unknown_related_unit_is_rejected(self) -> None:
        self.mutate_study(
            lambda data: data["related_unit_refs"].append(
                {"id": "unit.example.does-not-exist"}
            )
        )

        self.assertIn("STUDY_UNIT_UNKNOWN", self.codes(self.validate()))

    def test_related_unit_joins_by_id_across_versions(self) -> None:
        self.mutate_study(
            lambda data: data["related_unit_refs"][0].update(
                observed_at_version="0.9.0"
            )
        )

        report = self.validate()

        self.assertTrue(report.is_valid)
        self.assertNotIn("STUDY_UNIT_UNKNOWN", self.codes(report))

    def test_unknown_discovered_signal_is_rejected(self) -> None:
        self.mutate_study(
            lambda data: data.update(
                discovered_signal_refs=[
                    {"id": "signal.example.does-not-exist", "version": "1.0.0"},
                    {"id": "signal.agent.agent-harness", "version": "9.9.9"},
                ]
            )
        )

        report = self.validate()

        unknown_signal_issues = [
            issue
            for issue in report.issues
            if issue.code == "STUDY_SIGNAL_UNKNOWN"
        ]
        self.assertEqual(len(unknown_signal_issues), 2)

    def test_cross_checked_without_source_url_is_schema_error(self) -> None:
        def change(data: dict[str, Any]) -> None:
            for takeaway in data["takeaways"]:
                if takeaway["verification"]["status"] == "cross_checked":
                    takeaway["verification"].pop("source_url")

        self.mutate_study(change)

        self.assertIn("SCHEMA_ERROR", self.codes(self.validate()))

    def test_media_on_article_is_rejected(self) -> None:
        self.mutate_study(
            lambda data: data.update(media={"transcript_source": "none"})
        )

        self.assertIn("STUDY_MEDIA_ON_NON_MEDIA", self.codes(self.validate()))

    def test_video_without_media_is_rejected(self) -> None:
        self.mutate_study(lambda data: data["source"].update(kind="video"))

        self.assertIn("STUDY_MEDIA_MISSING", self.codes(self.validate()))

    def test_video_with_media_passes(self) -> None:
        def change(data: dict[str, Any]) -> None:
            data["source"]["kind"] = "video"
            data["media"] = {
                "duration_minutes": 25,
                "watched_segments": ["00:00-12:30"],
                "transcript_source": "auto_caption",
                "corrections": [
                    {
                        "at": "07:42",
                        "heard": "retrieval grading",
                        "confirmed": "retrieval grounding",
                        "basis": "frame",
                    }
                ],
            }

        self.mutate_study(change)

        report = self.validate()

        self.assertTrue(report.is_valid)

    def test_applied_evidence_path_with_backslash_is_rejected(self) -> None:
        def change(data: dict[str, Any]) -> None:
            self.make_applied(data)
            data["application"]["evidence_paths"] = ["studies\\README.md"]

        self.mutate_study(change)

        self.assertIn("STUDY_INVALID_PATH", self.codes(self.validate()))

    def test_duplicate_study_id_version_is_rejected(self) -> None:
        source_directory = (
            self.fixture_root / "studies" / "study.example.grounded-eval-article"
        )
        shutil.copytree(
            source_directory,
            self.fixture_root / "studies" / "study.example.duplicate-copy",
        )

        self.assertIn("DUPLICATE_ID_VERSION", self.codes(self.validate()))


if __name__ == "__main__":
    unittest.main()
