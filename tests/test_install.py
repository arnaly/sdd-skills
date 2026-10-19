import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install as installer


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="sdd-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "source"
        self.source.mkdir()
        shutil.copytree(ROOT / "skills", self.source / "skills")
        shutil.copyfile(ROOT / "VERSION", self.source / "VERSION")
        self.destination = self.base / "personal skills"

    def install(self, **kwargs):
        return installer.install(self.source, self.destination, **kwargs)

    def test_fresh_install_is_complete_and_preserves_unrelated_skills(self):
        unrelated = self.destination / "another-skill" / "keep.txt"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("local", encoding="utf-8")
        result = self.install()
        self.assertEqual(set(result.installed), set(installer.SKILLS))
        for name in installer.SKILLS:
            self.assertEqual(
                installer.manifest(self.source / "skills" / name),
                installer.manifest(self.destination / name),
            )
            marker = json.loads((self.destination / name / installer.MARKER).read_text())
            self.assertEqual(marker["skill"], name)
        self.assertEqual(unrelated.read_text(), "local")

    def test_identical_reinstall_does_not_write_files(self):
        self.install()
        before = {p: p.stat().st_mtime_ns for p in self.destination.rglob("*")}
        result = self.install()
        self.assertFalse(result.installed)
        self.assertEqual(len(result.unchanged), 8)
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in self.destination.rglob("*")})

    def test_foreign_directory_blocks_the_entire_install_even_with_update(self):
        foreign = self.destination / installer.SKILLS[-1]
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("Contenido ajeno", encoding="utf-8")
        for update in (False, True):
            with self.subTest(update=update), self.assertRaises(installer.InstallError):
                self.install(update=update)
            self.assertEqual(list(self.destination.iterdir()), [foreign])
            self.assertEqual((foreign / "SKILL.md").read_text(), "Contenido ajeno")

    def test_file_destination_is_not_replaced(self):
        self.destination.mkdir()
        existing = self.destination / "sdd-plan"
        existing.write_text("keep", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            self.install(update=True)
        self.assertEqual(existing.read_text(), "keep")
        self.assertEqual(list(self.destination.iterdir()), [existing])

    def test_symlink_destination_is_not_followed_or_replaced(self):
        outside = self.base / "outside"
        outside.mkdir()
        sentinel = outside / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        self.destination.mkdir()
        link = self.destination / "sdd-context"
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(installer.InstallError):
            self.install(update=True)
        self.assertTrue(link.is_symlink())
        self.assertEqual(sentinel.read_text(), "keep")

    def test_local_edit_blocks_without_update(self):
        self.install()
        edited = self.destination / "sdd-plan" / "SKILL.md"
        edited.write_text("local edit", encoding="utf-8")
        before = {name: installer.manifest(self.destination / name) for name in installer.SKILLS}
        with self.assertRaises(installer.InstallError):
            self.install()
        self.assertEqual(before, {name: installer.manifest(self.destination / name) for name in installer.SKILLS})

    def test_update_backs_up_local_edits_and_removes_stale_files_only_from_live_copy(self):
        self.install()
        edited = self.destination / "sdd-plan" / "assets" / "plan.md"
        edited.write_text("custom plan", encoding="utf-8")
        extra = self.destination / "sdd-plan" / "local.txt"
        extra.write_text("custom note", encoding="utf-8")
        result = self.install(update=True)
        self.assertEqual(result.installed, ("sdd-plan",))
        self.assertEqual((result.backup / "sdd-plan" / "assets" / "plan.md").read_text(), "custom plan")
        self.assertEqual((result.backup / "sdd-plan" / "local.txt").read_text(), "custom note")
        self.assertFalse(extra.exists())
        self.assertEqual(installer.manifest(self.destination / "sdd-plan"), installer.manifest(self.source / "skills" / "sdd-plan"))

    def test_version_update_keeps_original_metadata_in_backup(self):
        self.install()
        old = installer.read_owner(self.destination / "sdd-specify")
        (self.source / "VERSION").write_text("0.2.0\n", encoding="utf-8")
        result = self.install(update=True)
        self.assertEqual(len(result.installed), 8)
        self.assertEqual(installer.read_owner(result.backup / "sdd-specify"), old)
        self.assertEqual(installer.read_owner(self.destination / "sdd-specify")["version"], "0.2.0")

    def test_source_and_destination_cannot_overlap(self):
        for destination in (self.source, self.source / "skills", self.source / "skills" / "nested"):
            with self.subTest(destination=destination), self.assertRaises(installer.InstallError):
                installer.install(self.source, destination, update=True)

    def test_incomplete_source_does_not_create_destination(self):
        (self.source / "skills" / installer.SKILLS[-1] / "SKILL.md").unlink()
        with self.assertRaises(installer.InstallError):
            self.install()
        self.assertFalse(self.destination.exists())

    def test_source_symlinks_are_rejected_before_installation(self):
        link = self.source / "skills" / "sdd-plan" / "linked.txt"
        link.symlink_to(self.source / "VERSION")
        with self.assertRaises(installer.InstallError):
            self.install()
        self.assertFalse(self.destination.exists())

    def test_backup_symlink_is_rejected(self):
        self.install()
        (self.destination / "sdd-plan" / "local.txt").write_text("local", encoding="utf-8")
        outside = self.base / "outside-backups"
        outside.mkdir()
        backup_root = self.destination.parent / f".{self.destination.name}-sdd-backups"
        backup_root.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(installer.InstallError):
            self.install(update=True)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertTrue((self.destination / "sdd-plan" / "local.txt").exists())

    def test_failed_update_restores_every_previous_skill(self):
        self.install()
        before = {name: installer.manifest(self.destination / name) for name in installer.SKILLS}
        (self.source / "VERSION").write_text("0.2.0\n", encoding="utf-8")
        self.run_with_deployment_failure(update=True)
        self.assertEqual(before, {name: installer.manifest(self.destination / name) for name in installer.SKILLS})
        for name in installer.SKILLS:
            self.assertNotEqual(installer.read_owner(self.destination / name)["version"], "0.2.0")
        self.assertFalse(any(p.name.startswith(".sdd-install-") for p in self.destination.parent.iterdir()))

    def test_failed_fresh_install_removes_partially_deployed_skills(self):
        self.run_with_deployment_failure(update=False)
        self.assertEqual(list(self.destination.iterdir()), [])

    def run_with_deployment_failure(self, *, update):
        original = Path.rename

        def fail_one_deployment(path, target):
            if path.parent.name.startswith(".sdd-install-") and path.name == "sdd-plan":
                raise OSError("Simulated write failure")
            return original(path, target)

        with patch.object(Path, "rename", fail_one_deployment):
            with self.assertRaisesRegex(OSError, "Simulated write failure"):
                self.install(update=update)

    def test_cli_accepts_a_custom_destination_with_spaces(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"), "--dest", str(self.destination)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Instaladas/actualizadas: 8", result.stdout)
        self.assertTrue((self.destination / "sdd-validate" / "assets" / "validation.md").is_file())

    def test_cli_installs_and_updates_in_current_project_by_default(self):
        project = self.base / "current project"
        project.mkdir()
        instructions = project / "AGENTS.md"
        instructions.write_text("Keep existing instructions.\n", encoding="utf-8")
        destination = project / "skills"
        for args, expected in (([], "Instaladas/actualizadas: 8"), ([], "sin cambios: 8")):
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install.py"), *args],
                cwd=project, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(expected, result.stdout)
        for name in installer.SKILLS:
            self.assertTrue((destination / name / "SKILL.md").is_file())
        edited = destination / "sdd-plan" / "SKILL.md"
        edited.write_text("local edit", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"), "--update"],
            cwd=project, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Instaladas/actualizadas: 1", result.stdout)
        backup, = (project / ".skills-sdd-backups").iterdir()
        self.assertEqual((backup / "sdd-plan" / "SKILL.md").read_text(), "local edit")
        self.assertEqual(instructions.read_text(), "Keep existing instructions.\n")
        self.assertFalse((project / ".agents").exists())


class PackageTests(unittest.TestCase):
    def test_exactly_eight_skills_with_matching_names_and_descriptions(self):
        folders = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(folders, set(installer.SKILLS))
        for name in installer.SKILLS:
            content = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            frontmatter = content.split("---", 2)[1]
            fields = dict(line.split(":", 1) for line in frontmatter.strip().splitlines())
            self.assertEqual(fields["name"].strip(), name)
            self.assertTrue(json.loads(fields["description"].strip()))

    def test_relative_references_work_without_the_source_repository(self):
        with tempfile.TemporaryDirectory(prefix="sdd-package-") as directory:
            destination = Path(directory) / "relocated"
            installer.install(ROOT, destination)
            for name in installer.SKILLS:
                root = destination / name
                for document in root.rglob("*.md"):
                    text = document.read_text(encoding="utf-8")
                    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                        if "://" in target or target.startswith("#"):
                            continue
                        path = (document.parent / target.split("#", 1)[0]).resolve()
                        with self.subTest(document=document.relative_to(destination), target=target):
                            self.assertTrue(path.is_relative_to(root), "Resource escapes its skill")
                            self.assertTrue(path.is_file(), "Missing packaged resource")


if __name__ == "__main__":
    unittest.main()
