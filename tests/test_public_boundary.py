from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import check_public_boundary


class PublicBoundaryTest(unittest.TestCase):
    def test_pdf_in_public_tree_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "catalog").mkdir()
            (root / "catalog" / "private.pdf").write_bytes(b"pdf")

            with patch.object(check_public_boundary, "PUBLIC_ROOT", root):
                issues = check_public_boundary.collect_issues()

        self.assertTrue(
            any("forbidden public binary" in issue for issue in issues)
        )

    def test_absolute_path_in_public_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "docs" / "note.md").write_text(
                "local path: C:/Users/example/private.pdf",
                encoding="utf-8",
            )

            with patch.object(check_public_boundary, "PUBLIC_ROOT", root):
                issues = check_public_boundary.collect_issues()

        self.assertTrue(
            any("local absolute path" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
