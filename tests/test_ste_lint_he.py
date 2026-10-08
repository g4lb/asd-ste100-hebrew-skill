"""Tests for scripts/ste-lint-he.py. Run: python3 -m unittest discover -s tests -v"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ste-lint-he.py"
_spec = importlib.util.spec_from_file_location("ste_lint_he", SCRIPT)
ste = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ste)


def rules(text):
    return {f["rule"] for f in ste.lint(text)[0]}


def run_cli(*args, stdin=""):
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8")


class SelftestCases(unittest.TestCase):
    def test_every_case_triggers_and_clears(self):
        for rule, bad, good in ste.SELFTEST_CASES:
            with self.subTest(rule=rule, text=bad):
                self.assertIn(rule, rules(bad))
            with self.subTest(rule=rule, text=good):
                self.assertNotIn(rule, rules(good))

    def test_hedges_never_flagged(self):
        self.assertEqual(ste.lint(ste.HEDGES)[0], [])

    def test_selftest_flag(self):
        result = run_cli("--selftest")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("selftest OK", result.stdout)


class Markdown(unittest.TestCase):
    def test_code_is_skipped(self):
        self.assertEqual(ste.lint("```\nלבצע בדיקה; ב2025\n```")[0], [])
        self.assertEqual(ste.lint("להריץ את `a; b` עכשיו.")[0], [])

    def test_fenced_and_quoted_lists_ignored(self):
        self.assertNotIn("dangling-conjunction", rules("~~~\n- קוד או\n~~~"))
        self.assertNotIn("dangling-conjunction", rules("> - פריט או"))

    def test_table_cells_linted_separately(self):
        cell = " ".join(["מילה"] * 15) + "."
        table = f"| א | ב |\n| --- | --- |\n| {cell} | {cell} |"
        self.assertNotIn("sentence-length", rules(table))

    def test_crlf_line_endings(self):
        found = ste.lint("- פריט או\r\n- פריט שני\r\n")[0]
        self.assertEqual([(f["rule"], f["line"]) for f in found],
                         [("dangling-conjunction", 1)])

    def test_filename_label(self):
        self.assertEqual(ste.lint("א; ב", filename="x.md")[0][0]["file"], "x.md")


class Cli(unittest.TestCase):
    def test_clean_stdin_exits_zero(self):
        self.assertEqual(run_cli(stdin="לפתוח את הקובץ.").returncode, 0)

    def test_hard_violation_exits_one(self):
        self.assertEqual(run_cli(stdin="א; ב").returncode, 1)

    def test_baseline_tolerates(self):
        self.assertEqual(run_cli("--baseline", "1", stdin="א; ב").returncode, 0)

    def test_disable(self):
        self.assertEqual(run_cli("--disable", "semicolon", stdin="א; ב").returncode, 0)

    def test_json_keeps_hebrew_readable(self):
        result = run_cli("--json", stdin="- לפתוח או")
        self.assertEqual(json.loads(result.stdout)["hard_count"], 1)
        self.assertIn("לפתוח", result.stdout)

    def test_missing_file_exits_two(self):
        result = run_cli("no-such-file.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)

    def test_flag_without_value_exits_two(self):
        self.assertEqual(run_cli("--baseline").returncode, 2)

    def test_bad_baseline_value_exits_two(self):
        self.assertEqual(run_cli("--baseline", "abc", stdin="").returncode, 2)

    def test_utf8_bom_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8-sig",
                                         delete=False) as fh:
            fh.write("לפתוח את הקובץ.\n")
        result = run_cli(fh.name)
        self.assertEqual(result.returncode, 0, result.stdout)
        pathlib.Path(fh.name).unlink()


class WordRules(unittest.TestCase):
    def test_maqaf_counts_as_hyphen(self):
        self.assertNotIn("prefix-hyphen", rules("לשלוח ל־API ב־2025."))

    def test_space_before_number_is_fine(self):
        self.assertNotIn("prefix-hyphen", rules("שלב 3 מסתיים."))

    def test_noun_homographs_not_nominalization(self):
        for text in ("ערך ברירת המחדל הוא 5.", "מבצע קיץ בחנות.",
                     "ביצועים טובים.", "עורך הטקסט פתוח."):
            with self.subTest(text=text):
                self.assertNotIn("nominalization", rules(text))

    def test_part_is_not_marketing(self):
        self.assertNotIn("marketing-word", rules("חלק מהקבצים חסרים."))

    def test_exceeds_is_not_slang(self):
        self.assertNotIn("idiom-slang", rules("המספר עלה על 100."))

    def test_perform_with_concrete_object_is_advisory(self):
        found = [f for f in ste.lint("לבצע את הפקודה.")[0] if f["rule"] == "nominalization"]
        self.assertEqual([f["level"] for f in found], ["advisory"])
        self.assertEqual(run_cli(stdin="הפקודה מתבצעת כל שעה.").returncode, 0)

    def test_perform_with_action_noun_is_hard(self):
        for text in ("לבצע בדיקה של המסנן.", "וביצוע עדכון למערכת.", "לבצע את הבדיקה."):
            with self.subTest(text=text):
                levels = [f["level"] for f in ste.lint(text)[0] if f["rule"] == "nominalization"]
                self.assertEqual(levels, ["hard"])

    def test_wrinkle_is_not_slang(self):
        self.assertNotIn("idiom-slang", rules("לקמט את הנייר."))


class SynonymRotation(unittest.TestCase):
    def test_first_member_is_named_as_keeper(self):
        found = [f for f in ste.lint("לבדוק את הקובץ. אחר כך לוודא את הפלט.")[0]
                 if f["rule"] == "synonym-rotation"]
        self.assertEqual(len(found), 1)
        self.assertIn("'לוודא' and 'לבדוק'", found[0]["message"])

    def test_rotation_across_lines(self):
        self.assertIn("synonym-rotation", rules("להציג את הרשימה.\n\nלהראות את התוצאה."))

    def test_user_noun_is_not_rotation(self):
        self.assertNotIn("synonym-rotation", rules("המשתמש מנצל את המכסה."))


class Advisory(unittest.TestCase):
    def test_niqqud_does_not_hide_matches(self):
        self.assertIn("passive-voice", rules("הַקֹּבֶץ נִמְחַק."))
        self.assertIn("nominalization", rules("לְבַצֵּעַ בְּדִיקָה."))

    def test_maqaf_survives_niqqud_removal(self):
        self.assertNotIn("prefix-hyphen", rules("בְּ־API"))

    def test_advisory_never_fails_the_run(self):
        result = run_cli(stdin="הקובץ נמחק. בד\"כ זה מהיר.")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("passive-voice", result.stdout)

    def test_hedge_with_passive_free_text(self):
        self.assertEqual(ste.lint("ייתכן שהשרת לא זמין כרגע.")[0], [])

    def test_cantillation_is_stripped(self):
        found = [f for f in ste.lint("ה֑קובץ נמחק.")[0] if f["rule"] == "passive-voice"]
        self.assertEqual([f["col"] for f in found], [7])
        self.assertIn("passive-voice", rules("נִמְחַ֥ק."))


def after_blocks(text):
    """Return each blockquote that follows a '**After:**' line, joined into one string."""
    blocks, current, active = [], [], False
    for line in text.splitlines():
        if line.strip() == "**After:**":
            active, current = True, []
            continue
        if not active:
            continue
        if line.startswith(">"):
            current.append(line.lstrip("> ").rstrip())
        elif current:
            blocks.append(" ".join(current))
            active = False
    if active and current:
        blocks.append(" ".join(current))
    return blocks


class Fixtures(unittest.TestCase):
    def test_edge_case_fixture_reports_exactly_two(self):
        result = run_cli("--json", str(ROOT / "examples" / "linter-edge-cases.md"))
        self.assertEqual(result.returncode, 1)
        found = [(f["rule"], f["line"]) for f in json.loads(result.stdout)["violations"]]
        self.assertEqual(found, [("dangling-conjunction", 7), ("dangling-conjunction", 8)])

    def test_after_examples_lint_clean(self):
        text = (ROOT / "examples" / "before-after.md").read_text(encoding="utf-8")
        blocks = after_blocks(text)
        self.assertEqual(len(blocks), 4)
        for block in blocks:
            with self.subTest(block=block[:40]):
                self.assertEqual(ste.lint(block)[0], [])


if __name__ == "__main__":
    unittest.main()
