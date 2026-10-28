import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_requirements as vr  # noqa: E402

DIMS = vr.DIMENSIONS
FEATURE = """@FR-001 @P1 @pkg
Feature: Thing
  Statement.

  @FR-001-S1
  Scenario: Works
    Given a thing
    When it runs
    Then it works
    And it is quick
"""


def grill(skip: str | None = None) -> str:
    out = ["# Grill"]
    for number, dim in enumerate(DIMS, 1):
        if dim == skip:
            continue
        out += [f"## {dim}", "", f"**Q{number}. A question?**", "", "- **Recommendation:** do it", "- **Why:** because",
                "- **Status:** Recommended", "- **Feeds:** FR-001", ""]
    return "\n".join(out)


class VerifyRequirementsTests(unittest.TestCase):
    def tree(self, feature=FEATURE, grill_text=None, owns="FR-001, NFR-001", second_owner=False) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "functional-requirements.md").write_text("| FR-001 | Area | P1 |\n", encoding="utf-8")
        (root / "non-functional-requirements.md").write_text("## NFR-001 — Quality\n", encoding="utf-8")
        for name in ("pkg", "other") if second_owner else ("pkg",):
            pkg = root / name
            (pkg / "features").mkdir(parents=True)
            (pkg / "requirement.md").write_text(f"# R\n\n- **Owns:** {owns}\n", encoding="utf-8")
            (pkg / "diagrams.md").write_text("# D\n", encoding="utf-8")
            (pkg / "grill-log.md").write_text(grill_text or grill(), encoding="utf-8")
            (pkg / "features" / "a.feature").write_text(feature, encoding="utf-8")
        return root

    def test_valid_tree_passes(self):
        errors, stats = vr.verify(self.tree())
        self.assertEqual(errors, [])
        self.assertEqual(stats["scenarios"], 1)

    def test_missing_baseline_file_fails(self):
        for filename in ("functional-requirements.md", "non-functional-requirements.md"):
            with self.subTest(filename=filename):
                root = self.tree()
                (root / filename).unlink()
                errors, _ = vr.verify(root)
                self.assertTrue(any(filename in e and "missing" in e for e in errors), errors)

    def test_empty_requirement_directory_fails(self):
        root = Path(tempfile.mkdtemp())
        errors, _ = vr.verify(root)
        self.assertTrue(any("functional-requirements.md: missing" in e for e in errors), errors)
        self.assertTrue(any("non-functional-requirements.md: missing" in e for e in errors), errors)

    def test_tag_without_scenario_does_not_establish_coverage(self):
        errors, stats = vr.verify(self.tree(feature="@FR-001\nFeature: Only a heading\n"))
        self.assertEqual(stats["scenarios"], 0)
        self.assertTrue(any("no scenarios" in e for e in errors), errors)
        self.assertTrue(any("no feature file tagged @FR-001" in e for e in errors), errors)

    def test_invalid_scenario_does_not_establish_coverage(self):
        errors, _ = vr.verify(self.tree(feature="@FR-001\nFeature: Invalid\n  Scenario: Incomplete\n    Given input\n"))
        self.assertTrue(any("no Then" in e for e in errors), errors)
        self.assertTrue(any("no feature file tagged @FR-001" in e for e in errors), errors)

    def test_level_three_baselines_without_packages_report_missing_ownership(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "functional-requirements.md").write_text("### FR-001 — Goal\n", encoding="utf-8")
            (root / "non-functional-requirements.md").write_text("### NFR-001 — Quality\n", encoding="utf-8")
            errors, stats = vr.verify(root)
            self.assertEqual(stats["packages"], 0)
            self.assertIn("FR-001: not owned by any package", errors)
            self.assertIn("NFR-001: not owned by any package", errors)

    def test_baseline_headings_at_every_markdown_depth(self):
        for depth in range(1, 7):
            with self.subTest(depth=depth):
                root = self.tree()
                for filename, ident in (("functional-requirements.md", "FR-001"),
                                        ("non-functional-requirements.md", "NFR-001")):
                    (root / filename).write_text(f"{'#' * depth}\t{ident} — Title\n", encoding="utf-8")
                self.assertEqual(vr.baseline_ids(root), ({"FR-001"}, {"NFR-001"}))
                self.assertEqual(vr.verify(root)[0], [])

    def test_baseline_table_whitespace_for_both_identifier_families(self):
        for whitespace in ("", " ", "   ", "\t"):
            with self.subTest(whitespace=whitespace):
                root = self.tree()
                for filename, ident in (("functional-requirements.md", "FR-001"),
                                        ("non-functional-requirements.md", "NFR-001")):
                    (root / filename).write_text(f"  |{whitespace}{ident}{whitespace}| Title |\n", encoding="utf-8")
                self.assertEqual(vr.baseline_ids(root), ({"FR-001"}, {"NFR-001"}))
                self.assertEqual(vr.verify(root)[0], [])

    def test_prose_mentions_and_non_declaration_positions_are_ignored(self):
        root = self.tree()
        mentions = ("See FR-099 and NFR-099.\n- FR-098 is a reference.\n"
                    "### Related FR-097\n| Reference | FR-096 |\n"
                    "### FR-0010 is not a full ID\n####### FR-095 invalid depth\n")
        for filename in ("functional-requirements.md", "non-functional-requirements.md"):
            path = root / filename
            path.write_text(path.read_text(encoding="utf-8") + mentions, encoding="utf-8")
        self.assertEqual(vr.baseline_ids(root), ({"FR-001"}, {"NFR-001"}))
        self.assertEqual(vr.verify(root)[0], [])

    def test_present_baseline_without_recognized_ids_fails(self):
        for filename in ("functional-requirements.md", "non-functional-requirements.md"):
            for content in ("", "Only prose mentioning FR-001 and NFR-001.\n"):
                with self.subTest(filename=filename, content=content):
                    root = self.tree()
                    (root / filename).write_text(content, encoding="utf-8")
                    errors, _ = vr.verify(root)
                    self.assertTrue(any(filename in e and "no recognized" in e for e in errors), errors)

    def test_duplicate_baseline_declaration_fails(self):
        root = self.tree()
        (root / "functional-requirements.md").write_text(
            "### FR-001 — Goal\n| FR-001 | Duplicate |\n", encoding="utf-8")
        errors, _ = vr.verify(root)
        self.assertTrue(any("duplicate" in e and "FR-001" in e for e in errors), errors)

    def test_duplicate_id_on_owns_line_fails(self):
        errors, _ = vr.verify(self.tree(owns="FR-001, NFR-001, FR-001"))
        self.assertTrue(any("duplicate" in e and "FR-001" in e for e in errors), errors)

    def test_scenario_without_then_fails(self):
        errors, _ = vr.verify(self.tree(feature=FEATURE.replace("    Then it works\n    And it is quick\n", "")))
        self.assertTrue(any("no Then" in e for e in errors), errors)

    def test_outline_without_examples_fails(self):
        bad = FEATURE.replace("Scenario: Works", "Scenario Outline: Works").replace("a thing", "a <thing>")
        errors, _ = vr.verify(self.tree(feature=bad))
        self.assertTrue(any("no Examples" in e for e in errors), errors)

    def test_duplicate_scenario_title_fails(self):
        errors, _ = vr.verify(self.tree(feature=FEATURE + "\n  Scenario: Works\n    Given x\n    When y\n    Then z\n"))
        self.assertTrue(any("duplicate scenario title" in e for e in errors), errors)

    def test_missing_dimension_fails(self):
        errors, _ = vr.verify(self.tree(grill_text=grill(skip="Data")))
        self.assertTrue(any("missing dimension 'Data'" in e for e in errors), errors)

    def test_unowned_requirement_fails(self):
        errors, _ = vr.verify(self.tree(owns="FR-001"))
        self.assertTrue(any("NFR-001: not owned" in e for e in errors), errors)

    def test_requirement_owned_twice_fails(self):
        errors, _ = vr.verify(self.tree(second_owner=True))
        self.assertTrue(any("owned by several packages" in e for e in errors), errors)

    def test_owned_fr_needs_a_tagged_feature(self):
        errors, _ = vr.verify(self.tree(feature=FEATURE.replace("@FR-001 ", "")))
        self.assertTrue(any("no feature file tagged @FR-001" in e for e in errors), errors)

    def test_decisions_report_lists_decision_needed_only(self):
        text = grill().replace("- **Status:** Recommended", "- **Status:** Decision needed", 1)
        root = self.tree(grill_text=text)
        report = vr.decisions_markdown(root)
        self.assertIn("## pkg", report)
        self.assertEqual(sum(1 for line in report.splitlines() if line.startswith("| Q")), 2)  # header plus one decision


if __name__ == "__main__":
    unittest.main()
