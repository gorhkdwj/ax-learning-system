from __future__ import annotations

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from tools.build_domain_model_course import render_course


class _CourseHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.buttons_without_type = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.tags.append(tag)
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(str(attributes["id"]))
        if tag == "a" and attributes.get("href"):
            self.links.append(str(attributes["href"]))
        if tag == "button" and attributes.get("type") != "button":
            self.buttons_without_type += 1


class DomainModelCourseBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.course_root = (
            cls.repo_root
            / "catalog"
            / "items"
            / "unit.data-analytics-ml.domain-concept-relationship-modeling"
            / "resources"
            / "course"
        )
        cls.data = json.loads(
            (cls.course_root / "course-content.json").read_text(encoding="utf-8")
        )
        cls.rendered = render_course(cls.data)
        cls.committed = (cls.course_root / "index.html").read_text(encoding="utf-8")

    def test_committed_html_is_current(self) -> None:
        self.assertEqual(self.committed, self.rendered)

    def test_learning_path_has_six_blocks_and_expected_timebox(self) -> None:
        modules = self.data["modules"]

        self.assertEqual(len(modules), 6)
        self.assertEqual(
            sum(module["minutes"] for module in modules if module["kind"] == "core"),
            600,
        )
        self.assertEqual(
            sum(
                module["minutes"]
                for module in modules
                if module["kind"] == "linked_probe"
            ),
            120,
        )
        for module in modules:
            self.assertGreaterEqual(len(module["concepts"]), 1)
            self.assertGreaterEqual(len(module["steps"]), 4)
            self.assertTrue(module["artifact"])
            self.assertTrue(module["checkpoint"]["prompt"])
            self.assertTrue(module["checkpoint"]["guidance"])

    def test_html_exposes_accessible_text_first_contract(self) -> None:
        parser = _CourseHTMLParser()
        parser.feed(self.rendered)

        self.assertIn('<html lang="ko">', self.rendered)
        self.assertIn('class="skip-link" href="#course-content"', self.rendered)
        self.assertIn("main", parser.tags)
        self.assertIn("nav", parser.tags)
        self.assertIn("noscript", parser.tags)
        self.assertIn("course-content", parser.ids)
        self.assertEqual(parser.buttons_without_type, 0)
        self.assertIn(":focus-visible", self.rendered)
        self.assertIn("prefers-reduced-motion", self.rendered)
        self.assertIn("@media print", self.rendered)
        for module in self.data["modules"]:
            self.assertIn(module["id"], parser.ids)
            self.assertIn(
                f'href="#{module["id"]}">{module["title"]}</a>', self.rendered
            )

    def test_all_local_learning_resource_links_resolve(self) -> None:
        for module in self.data["modules"]:
            for resource in module.get("resources", []):
                self.assertFalse(resource["href"].startswith(("http://", "https://")))
                resolved = (self.course_root / resource["href"]).resolve()
                self.assertTrue(
                    resolved.is_file(),
                    f'{module["id"]}의 실습 자료가 없습니다: {resource["href"]}',
                )

    def test_progress_is_local_only_and_public_boundary_is_preserved(self) -> None:
        self.assertIn("localStorage", self.rendered)
        self.assertIn("외부로 전송되지 않습니다", self.rendered)
        self.assertNotIn("fetch(", self.rendered)
        self.assertNotIn("XMLHttpRequest", self.rendered)
        self.assertNotIn("file://", self.rendered)
        self.assertNotRegex(self.rendered, r"[A-Za-z]:\\")
        self.assertNotIn("<iframe", self.rendered)


if __name__ == "__main__":
    unittest.main()
