"""Synthetic coverage for publication scanning; contains no real credentials."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from verify_publication import findings


SCRIPT = Path(__file__).with_name("verify_publication.py")
SYNTHETIC_EMAIL = "person" + "@" + "example.org"


class PublicationSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self):
        self.temp.cleanup()

    def add(self, name, content="ok\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", "--force", "--", name], cwd=self.root, check=True)

    def test_detects_private_paths_emails_tokens_pem_and_private_names(self):
        windows_path = "C:" + "\\" + "Users" + "\\someone\\work"
        pem = "-----BEGIN " + "PRIVATE KEY-----"
        unix_path = "/" + "home/someone/private/file"
        self.add("docs/sample.md", "path " + windows_path + "\nmail " + SYNTHETIC_EMAIL + "\nkey ghp_" + "A" * 30 + "\n" + pem + "\n" + unix_path + "\n")
        self.add("coordination/notes.txt")
        rules = {(rule, line) for _, rule, line in findings(self.root)}
        self.assertTrue({("private-path", 1), ("personal-email", 2), ("token", 3), ("pem-private-key", 4), ("private-path", 5), ("private-artifact-path", 1)} <= rules)

    def test_generic_language_and_allowed_email_pass(self):
        self.add("README.md", "OAuth tokens are refreshed securely. noreply@github.com is allowed.\n")
        self.assertEqual([], findings(self.root))

    def test_private_filename_detected(self):
        self.add("settings/.env.production", "placeholder\n")
        self.assertIn(("settings/.env.production", "credential-file", 1), findings(self.root))

    def test_untracked_files_are_ignored(self):
        self.add("tracked.md")
        (self.root / "untracked.md").write_text(SYNTHETIC_EMAIL, encoding="utf-8")
        self.assertEqual([], findings(self.root))

    def test_missing_git_and_empty_index_rejected(self):
        with tempfile.TemporaryDirectory() as plain:
            with self.assertRaises(RuntimeError):
                findings(Path(plain))
        with self.assertRaises(RuntimeError):
            findings(self.root)

    def test_cli_reports_only_path_rule_line_and_never_value(self):
        self.add("docs/sample.md", SYNTHETIC_EMAIL + "\n")
        # The CLI is rooted at its own checkout; copy it into this synthetic repo.
        shutil_script = self.root / "tests" / SCRIPT.name
        shutil_script.parent.mkdir()
        shutil_script.write_bytes(SCRIPT.read_bytes())
        completed = subprocess.run([sys.executable, str(shutil_script)], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("docs/sample.md:personal-email:1\n", completed.stdout)
        self.assertNotIn(SYNTHETIC_EMAIL, completed.stdout)
        self.assertEqual("", completed.stderr)

    def test_scans_index_instead_of_worktree(self):
        self.add("sample.md", SYNTHETIC_EMAIL)
        (self.root / "sample.md").write_text("safe", encoding="utf-8")
        self.assertIn(("sample.md", "personal-email", 1), findings(self.root))
        self.add("sample.md", "safe")
        (self.root / "sample.md").write_text(SYNTHETIC_EMAIL, encoding="utf-8")
        self.assertEqual([], findings(self.root))

    def test_invalid_utf8_and_binary_cannot_be_skipped(self):
        for name, content in [("binary.txt", bytes([0, 255])), ("invalid.txt", bytes([255]))]:
            (self.root / name).write_bytes(content)
            subprocess.run(["git", "add", "--", name], cwd=self.root, check=True)
        self.assertIn(("binary.txt", "binary-or-oversized-file", 1), findings(self.root))
        self.assertIn(("invalid.txt", "non-utf8-file", 1), findings(self.root))

    def test_private_configs_caches_media_and_backups_are_rejected(self):
        for name in ["config.toml", "token-local.json", ".codex/state.txt", "deliverables/video.txt", "skill-backups/old.md", "tests/__pycache__/cache.pyc", "asset.mp4", "data.sqlite"]:
            self.add(name)
        flagged = {name for name, _, _ in findings(self.root)}
        self.assertEqual(8, len(flagged))

    def test_symlink_index_entry_rejected_without_following_it(self):
        self.add("sample.md")
        object_id = subprocess.run(["git", "rev-parse", ":sample.md"], cwd=self.root, check=True, text=True, capture_output=True).stdout.strip()
        subprocess.run(["git", "update-index", "--add", "--cacheinfo", "120000," + object_id + ",link"], cwd=self.root, check=True)
        self.assertIn(("link", "non-regular-file", 1), findings(self.root))

    def test_scanner_and_test_source_do_not_flag_themselves(self):
        self.add("tests/verify_publication.py", SCRIPT.read_text(encoding="utf-8"))
        self.add("tests/test_publication_safety.py", Path(__file__).read_text(encoding="utf-8"))
        self.assertEqual([], findings(self.root))


if __name__ == "__main__":
    unittest.main()
