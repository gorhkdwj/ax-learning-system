import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.workspace_paths import VAULT_ENV_VAR, resolve_vault_root


class WorkspacePathsTest(unittest.TestCase):
    def test_default_vault_is_public_root_sibling(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            parent = Path(temporary_directory)
            public_root = parent / "ax-learning-system"
            public_root.mkdir()

            with patch.dict(os.environ, {VAULT_ENV_VAR: ""}):
                resolved = resolve_vault_root(repository_root=public_root)

            self.assertEqual(resolved, (parent / "ax-learning-vault").resolve())

    def test_environment_vault_path_is_resolved_from_public_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            parent = Path(temporary_directory)
            public_root = parent / "ax-learning-system"
            public_root.mkdir()

            with patch.dict(
                os.environ,
                {VAULT_ENV_VAR: "../environment-vault"},
            ):
                resolved = resolve_vault_root(repository_root=public_root)

            self.assertEqual(resolved, (parent / "environment-vault").resolve())

    def test_relative_vault_path_is_resolved_from_public_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            parent = Path(temporary_directory)
            public_root = parent / "ax-learning-system"
            public_root.mkdir()

            resolved = resolve_vault_root(
                "../private-vault",
                repository_root=public_root,
            )

            self.assertEqual(resolved, (parent / "private-vault").resolve())

    def test_vault_inside_public_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            public_root = Path(temporary_directory) / "ax-learning-system"
            public_root.mkdir()

            with self.assertRaises(ValueError):
                resolve_vault_root(
                    "./private",
                    repository_root=public_root,
                )


if __name__ == "__main__":
    unittest.main()
