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

    def _write_file_entry(
        self,
        relative_path: str,
        content: bytes,
        file_id: str,
        title: str,
        package_root: Path | None = None,
        **fields,
    ) -> dict:
        """실제 파일을 만들고 크기·해시가 일치하는 manifest 항목을 돌려줍니다."""
        root = package_root if package_root is not None else self.package_root
        file_path = root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        entry = {
            "id": file_id,
            "title": title,
            "path": relative_path,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": file_path.stat().st_size,
        }
        entry.update(fields)
        return entry

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

    def test_legacy_manifest_without_media_kind_passes(self) -> None:
        # 하위호환: media_kind 없는 기존 형식 manifest는 수정 없이 document로
        # 해석되어 그대로 통과해야 합니다.
        self.assertNotIn("media_kind", self.manifest["files"][0])

        report = self._validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest_count, 1)
        self.assertEqual(report.file_count, 1)

    def test_transcript_passes_without_page_count_and_skips_pypdf(self) -> None:
        self.manifest["files"] = [
            self._write_file_entry(
                "files/lecture.ko.vtt",
                b"WEBVTT\n",
                "private-file.example.transcript",
                "예시 트랜스크립트",
                media_kind="transcript",
            )
        ]
        self._write_manifest()

        with patch(
            "tools.validate_private_sources._pdf_page_count"
        ) as page_count_mock:
            report = PrivateSourceValidator().validate(self.vault_root)

        self.assertTrue(report.is_valid)
        self.assertEqual(report.file_count, 1)
        page_count_mock.assert_not_called()

    def test_frame_without_captured_at_seconds_is_rejected(self) -> None:
        self.manifest["files"] = [
            {
                "id": "private-file.example.frame",
                "title": "예시 프레임",
                "path": "files/t-0130.jpg",
                "media_kind": "frame",
                "sha256": "0" * 64,
                "size_bytes": 1,
            }
        ]
        self._write_manifest()

        self.assertIn("SCHEMA_ERROR", self._codes(self._validate()))

    def test_video_without_duration_seconds_is_rejected(self) -> None:
        self.manifest["files"] = [
            {
                "id": "private-file.example.video",
                "title": "예시 영상",
                "path": "files/clip.mp4",
                "media_kind": "video",
                "sha256": "0" * 64,
                "size_bytes": 1,
            }
        ]
        self._write_manifest()

        self.assertIn("SCHEMA_ERROR", self._codes(self._validate()))

    def test_document_with_non_pdf_extension_is_rejected(self) -> None:
        self.manifest["files"][0]["path"] = "files/sample.txt"
        self._write_manifest()

        self.assertIn("SCHEMA_ERROR", self._codes(self._validate()))

    def test_articles_manifest_is_discovered(self) -> None:
        article_root = (
            self.vault_root / "sources" / "articles" / "private-source.article"
        )
        article_root.mkdir(parents=True)
        article_manifest = {
            "schema_version": "1.0.0",
            "id": "private-source.article",
            "version": "1.0.0",
            "title": "예시 아티클",
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
                self._write_file_entry(
                    "files/capture.md",
                    "# 본문 갈무리\n".encode("utf-8"),
                    "private-file.article.capture",
                    "본문 갈무리",
                    package_root=article_root,
                    media_kind="transcript",
                )
            ],
        }
        (article_root / "source.json").write_text(
            json.dumps(article_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        report = self._validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest_count, 2)

    def test_media_files_check_size_and_checksum_only(self) -> None:
        media_root = (
            self.vault_root / "sources" / "media" / "private-source.media"
        )
        media_root.mkdir(parents=True)
        media_manifest = {
            "schema_version": "1.0.0",
            "id": "private-source.media",
            "version": "1.0.0",
            "title": "예시 미디어",
            "reviewed_at": "2026-08-02",
            "rights": {
                "status": "unverified",
                "allowed_use": "personal_learning_only",
                "redistribution": "prohibited_until_verified",
            },
            "selection": {
                "included_topics": ["예시"],
                "excluded_scope": ["나머지 자료"],
                "expected_file_count": 3,
            },
            "files": [
                self._write_file_entry(
                    "frames/t-0130.jpg",
                    b"synthetic-jpg-fixture",
                    "private-file.media.frame",
                    "예시 프레임",
                    package_root=media_root,
                    media_kind="frame",
                    captured_at_seconds=90,
                ),
                self._write_file_entry(
                    "audio/lecture.m4a",
                    b"synthetic-audio-fixture",
                    "private-file.media.audio",
                    "예시 오디오",
                    package_root=media_root,
                    media_kind="audio",
                    duration_seconds=1800,
                ),
                self._write_file_entry(
                    "video/lecture.mp4",
                    b"synthetic-video-fixture",
                    "private-file.media.video",
                    "예시 영상",
                    package_root=media_root,
                    media_kind="video",
                    duration_seconds=1800,
                ),
            ],
        }
        (media_root / "source.json").write_text(
            json.dumps(media_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        with patch(
            "tools.validate_private_sources._pdf_page_count",
            return_value=2,
        ) as page_count_mock:
            report = PrivateSourceValidator().validate(self.vault_root)

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest_count, 2)
        self.assertEqual(report.file_count, 4)
        # 페이지 수 확인은 setUp의 document 한 건에만 일어나야 하며,
        # 미디어 파일에서는 pypdf를 호출하지 않아야 합니다.
        page_count_mock.assert_called_once_with(self.pdf_path.resolve())


if __name__ == "__main__":
    unittest.main()
