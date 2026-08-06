from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.build_domain_model_course import render_course
from tools.validate_catalog import CatalogValidator


class StudyOwnedResourceTest(unittest.TestCase):
    """Study가 Unit을 거치지 않고 자기 학습자료를 소유할 수 있는지 검증합니다.

    Study는 자료 한 편을 그 자체로 학습하는 세션이므로 자기 outcomes와 자기
    Resource를 가질 수 있어야 합니다. Unit 학습성과에 대응시키는 것은
    outcome_coverage로 하는 선택적 교차연결이며 학습의 전제가 아닙니다.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.study_root = (
            cls.repo_root
            / "studies"
            / "study.organization-adoption.hermes-agent-slack-field-report"
        )
        cls.study = json.loads(
            (cls.study_root / "study.json").read_text(encoding="utf-8")
        )
        cls.session_root = cls.study_root / "resources" / "session"

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "studies"
        shutil.copytree(self.study_root, self.fixture_root / self.study_root.name)
        self.taxonomy_root = Path(self.temporary_directory.name) / "taxonomy"
        shutil.copytree(self.repo_root / "taxonomy", self.taxonomy_root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def validate(self):
        validator = CatalogValidator(
            workspace_root=self.repo_root,
            schema_dir=self.repo_root / "schemas",
        )
        return validator.validate([self.fixture_root, self.taxonomy_root])

    def mutate(self, change: Callable[[dict[str, Any]], None]) -> None:
        path = self.fixture_root / self.study_root.name / "study.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def codes(report) -> set[str]:
        return {issue.code for issue in report.issues}

    def test_study_owns_its_session_resource(self) -> None:
        resource = json.loads(
            (self.session_root / "resource.json").read_text(encoding="utf-8")
        )
        self.assertEqual(resource["owner"]["kind"], "study")
        self.assertEqual(resource["owner"]["id"], self.study["id"])

    def test_study_outcomes_are_independent_of_units(self) -> None:
        """Study의 학습성과는 Unit ID 공간을 쓰지 않습니다."""
        self.assertTrue(self.study["outcomes"])
        for outcome in self.study["outcomes"]:
            with self.subTest(outcome=outcome["id"]):
                self.assertTrue(outcome["id"].startswith("outcome.study."))

    def test_session_outcomes_all_covered_by_the_resource(self) -> None:
        resource = json.loads(
            (self.session_root / "resource.json").read_text(encoding="utf-8")
        )
        declared = {o["id"] for o in self.study["outcomes"]}
        self.assertEqual(set(resource["learning_outcome_ids"]), declared)

    def test_generated_session_html_matches_structured_content(self) -> None:
        data = json.loads(
            (self.session_root / "course-content.json").read_text(encoding="utf-8")
        )
        output = self.session_root / "index.html"
        self.assertTrue(output.exists())
        self.assertEqual(output.read_text(encoding="utf-8"), render_course(data))

    def test_answers_are_not_the_first_concept(self) -> None:
        """생성기가 첫 개념을 펼치므로 해설을 첫 자리에 두면 답이 보입니다."""
        data = json.loads(
            (self.session_root / "course-content.json").read_text(encoding="utf-8")
        )
        for module in data["modules"]:
            concepts = module["concepts"]
            if not any("해설" in c["title"] for c in concepts):
                continue
            with self.subTest(module=module["id"]):
                self.assertNotIn("해설", concepts[0]["title"])

    def test_declared_resource_must_exist(self) -> None:
        self.mutate(
            lambda data: data["resource_refs"].append(
                {
                    "resource": {
                        "id": "resource.study.missing-material",
                        "version": "1.0.0",
                    },
                    "role": "reference",
                }
            )
        )

        self.assertIn("MISSING_REFERENCE", self.codes(self.validate()))

    def test_owning_resources_without_outcomes_is_rejected(self) -> None:
        self.mutate(lambda data: data.update(outcomes=[]))

        self.assertIn(
            "STUDY_RESOURCE_WITHOUT_OUTCOME",
            self.codes(self.validate()),
        )

    def test_duplicate_outcome_id_is_rejected(self) -> None:
        self.mutate(
            lambda data: data["outcomes"].append(dict(data["outcomes"][0]))
        )

        self.assertIn("STUDY_DUPLICATE_OUTCOME", self.codes(self.validate()))


if __name__ == "__main__":
    unittest.main()
