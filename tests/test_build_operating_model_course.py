from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.build_domain_model_course import render_course


class OperatingModelCourseBuilderTest(unittest.TestCase):
    """운영모델 D0 교재의 생성물이 정본 콘텐츠와 일치하는지 확인합니다.

    HTML은 직접 수정하지 않고 course-content.json과 생성기를 고친 뒤
    재생성하는 것이 규칙이므로, 둘이 어긋난 상태로 커밋되는 것을 막습니다.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.course_root = (
            cls.repo_root
            / "catalog"
            / "items"
            / "unit.organization-adoption.ax-operating-model-decision-rights"
            / "resources"
            / "course"
        )
        cls.source = cls.course_root / "course-content.json"
        cls.output = cls.course_root / "index.html"
        cls.data = json.loads(cls.source.read_text(encoding="utf-8"))

    def test_generated_html_matches_structured_content(self) -> None:
        self.assertTrue(self.output.exists())
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            render_course(self.data),
        )

    def test_course_targets_the_d0_outcome_only(self) -> None:
        resource = json.loads(
            (self.course_root / "resource.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            resource["learning_outcome_ids"],
            ["outcome.organization-adoption.ax-operating-model-decision-rights.d0"],
        )
        self.assertEqual(
            resource["owner"]["id"],
            "unit.organization-adoption.ax-operating-model-decision-rights",
        )

    def test_module_minutes_sum_to_declared_core_minutes(self) -> None:
        total = sum(module["minutes"] for module in self.data["modules"])
        self.assertEqual(total, self.data["core_minutes"])

    def test_case_judgement_answers_are_collapsed(self) -> None:
        """사례 판정의 해설이 펼쳐진 채로 생성되면 회수 연습이 사라집니다.

        생성기는 각 모듈의 첫 개념을 open으로 렌더링합니다. 따라서 해설을
        첫 자리에 두면 답이 그대로 보입니다. 첫 자리에는 안내를 두고 해설은
        그 뒤에 배치해야 합니다.
        """
        module = next(
            m for m in self.data["modules"] if m["id"] == "case-judgement"
        )
        answers = [
            c for c in module["concepts"] if "판정 —" in c["title"]
        ]
        self.assertEqual(len(answers), 3)
        self.assertNotIn("판정 —", module["concepts"][0]["title"])
        for concept in answers:
            with self.subTest(concept=concept["title"]):
                self.assertIn("먼저 답을 적은 뒤", concept["title"])
                self.assertNotEqual(module["concepts"][0], concept)

    def test_every_module_has_a_checkpoint_prompt(self) -> None:
        for module in self.data["modules"]:
            with self.subTest(module=module["id"]):
                self.assertTrue(module["checkpoint"]["prompt"].strip())
                self.assertTrue(module["checkpoint"]["guidance"].strip())


if __name__ == "__main__":
    unittest.main()
