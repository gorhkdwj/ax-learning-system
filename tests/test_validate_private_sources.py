from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.validate_private_sources import PrivateSourceValidator


class PrivateSourceValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.vault_root = Path(self.temporary_directory.name) / "vault"
        self.package_root = (
            self.vault_root
            / "sources"
            / "documents"
            / "private-source.example"
        )
        (self.package_root / "files").mkdir(parents=True)
        self.pdf_path = self.package_root / "files" / "sample.pdf"
        self.pdf_path.write_bytes(b"synthetic-pdf-fixture")
        digest = hashlib.sha256(self.pdf_path.read_bytes()).hexdigest()
        self.manifest = {
            "schema_version": "1.0.0",
            "id": "private-source.example",
            "version": "1.0.0",
            "title": "예시 원천",
            "reviewed_at": "2026-08-02",
            "rights": {
                "status": "unverified",
                "allowed_use": "personal_learning_only",
                "redistribution": "prohibited_until_verified",
            },
            "selection": {
                "included_topics": ["예시"],
                "excluded_scope": ["나머지 자료"],
                "expected_file_count": 1,
            },
            "files": [
                {
                    "id": "private-file.example.sample",
                    "title": "예시 PDF",
                    "path": "files/sample.pdf",
                    "sha256": digest,
                    "size_bytes": self.pdf_path.stat().st_size,
                    "page_count": 2,
                }
            ],
        }
        self._write_manifest()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write_manifest(self) -> None:
        (self.package_root / "source.json").write_text(
            json.dumps(self.manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _codes(report) -> set[str]:
        return {issue.code for issue in report.issues}

    def _validate(self, pages: int = 2, *, require_files: bool = False):
        with patch(
            "tools.validate_private_sources._pdf_page_count",
            return_value=pages,
        ):
            return PrivateSourceValidator().validate(
                self.vault_root,
                require_files=require_files,
            )

    def test_missing_vault_is_successfully_skipped(self) -> None:
        report = PrivateSourceValidator().validate(
            self.vault_root / "not-created"
        )

        self.assertTrue(report.skipped)
        self.assertTrue(report.is_valid)

    def test_valid_manifest_checks_file_integrity(self) -> None:
        report = self._validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest_count, 1)
        self.assertEqual(report.file_count, 1)

    def test_manifest_only_clone_is_valid(self) -> None:
        self.pdf_path.unlink()

        report = self._validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.file_count, 0)
        self.assertEqual(report.unavailable_file_count, 1)

    def test_required_missing_file_is_rejected(self) -> None:
        self.pdf_path.unlink()

        self.assertIn(
            "FILE_NOT_FOUND",
            self._codes(self._validate(require_files=True)),
        )

    def test_partially_restored_package_is_rejected(self) -> None:
        missing = dict(self.manifest["files"][0])
        missing.update(
            {
                "id": "private-file.example.missing",
                "title": "누락 PDF",
                "path": "files/missing.pdf",
            }
        )
        self.manifest["files"].append(missing)
        self.manifest["selection"]["expected_file_count"] = 2
        self._write_manifest()

        self.assertIn("FILE_NOT_FOUND", self._codes(self._validate()))

    def test_checksum_mismatch_is_rejected(self) -> None:
        self.manifest["files"][0]["sha256"] = "0" * 64
        self._write_manifest()

        self.assertIn("CHECKSUM_MISMATCH", self._codes(self._validate()))

    def test_page_count_mismatch_is_rejected(self) -> None:
        self.assertIn("PAGE_COUNT_MISMATCH", self._codes(self._validate(3)))

    def test_expected_file_count_is_enforced(self) -> None:
        self.manifest["selection"]["expected_file_count"] = 2
        self._write_manifest()

        self.assertIn("FILE_COUNT_MISMATCH", self._codes(self._validate()))

    def test_unsafe_absolute_path_is_rejected_by_schema(self) -> None:
        self.manifest["files"][0]["path"] = "C:/private/sample.pdf"
        self._write_manifest()

        self.assertIn("SCHEMA_ERROR", self._codes(self._validate()))


if __name__ == "__main__":
    unittest.main()
