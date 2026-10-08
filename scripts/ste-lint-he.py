#!/usr/bin/env python3
"""Deterministic linter for the structural rules of Simplified Technical Hebrew.

Ported from danyuchn/asd-ste100-skill (MIT). Checks only rules that a regex
can verify without a morphological analyzer. Never flags hedges or modality
(ייתכן, עשוי, אולי, כנראה): confidence is content.

Usage:
    ste-lint-he.py FILE [FILE ...]
    echo "טקסט" | ste-lint-he.py [--json]
    ste-lint-he.py --baseline 5 FILE      # pass unless hard violations exceed 5
    ste-lint-he.py --disable passive-voice,abbreviation FILE
    ste-lint-he.py --selftest

Exit 1 when hard violations exceed the baseline (default 0). Exit 2 when a
file cannot be read or a flag has no valid value. Advisory findings never
fail the run.
"""
import json
import re
import sys

HEB = "א-ת"
START = rf"(?<![{HEB}A-Za-z0-9_])"
END = rf"(?![{HEB}A-Za-z0-9_])"
PFX = "[ובכלמשה]{0,3}"          # prefix letters on nouns and adjectives
VPFX = "(?:ו?(?:כש|ש|ה)?)"      # prefix letters on verbs and participles


def alt(*forms):
    return "(?:" + "|".join(forms) + ")"


def term(*forms, prefix=PFX):
    return re.compile(START + prefix + alt(*forms) + END)


NOMINAL_VERBS = alt("לבצע", "ביצוע", "ביצע", "ביצעה", "ביצעו", "יבצע", "תבצע",
                    "נבצע", "מבצעת", "התבצע", "התבצעה", "מתבצע", "מתבצעת")
EDIT_VERBS = alt("לערוך", "עריכת", "ערכנו", "נערוך", "יערוך", "תערוך")
ACTION_NOUNS = alt("בדיקה", "בדיקת", "בדיקות", "השוואה", "השוואת", "ניתוח",
                   "סקירה", "סקירת", "ניסוי", "ניסויים", "הערכה", "הערכת",
                   "מעקב", "תיקון", "תיקונים", "עדכון", "עדכונים", "סנכרון",
                   "התקנה", "התקנת", "הגדרה", "הגדרת", "הרצה", "הרצת",
                   "מחיקה", "מחיקת", "שמירה", "שמירת", "גיבוי", "חיפוש",
                   "הרחבה", "הרחבת", "אימות", "ניקוי", "שחזור", "סריקה",
                   "סריקת", "טעינה", "טעינת", "העברה", "העברת", "הפעלה",
                   "הפעלת", "חישוב", "ניתוב")
NOMINAL_MSG = "Action frozen into a noun. Use the verb (לבדוק, not לבצע בדיקה)."

RULES = [
    ("semicolon", "hard", re.compile(r";"),
     "STE bans the semicolon (Rule 8.1). Split into separate sentences."),
    ("nominalization", "hard",
     re.compile(START + PFX + NOMINAL_VERBS + r"\s+(?:את\s+)?" + PFX + ACTION_NOUNS + END),
     NOMINAL_MSG),
    ("nominalization", "advisory",
     re.compile(START + PFX + NOMINAL_VERBS + rf"\s+(?:את\s+)?(?!(?:את\s+)?{PFX}{ACTION_NOUNS}{END})[{HEB}]{{2,}}"),
     "Possible nominalization. If the noun names an action, use its verb (לבדוק, not לבצע בדיקה). If it names a thing (לבצע את הפקודה), consider a precise verb such as להריץ."),
    ("nominalization", "hard",
     re.compile(START + PFX + EDIT_VERBS + r"\s+" + PFX + ACTION_NOUNS + END),
     NOMINAL_MSG),
    ("nominalization", "hard",
     re.compile(START + PFX + alt("מתן") + r"\s+" + PFX
                + alt("מענה", "תמיכה", "גישה", "הרשאה", "הרשאות", "שירות") + END),
     NOMINAL_MSG),
    ("nominalization", "hard",
     re.compile(START + PFX + alt("לקבל", "קבלת", "קיבל", "קיבלה", "קיבלו",
                                  "יקבל", "נקבל") + r"\s+" + PFX
                + alt("החלטה", "החלטות") + END),
     NOMINAL_MSG),
    ("marketing-word", "hard",
     term("חדשני(?:ת|ים|ות)?", "מהפכני(?:ת|ים|ות)?", "עוצמתי(?:ת|ים|ות)?",
          "אינטואיטיבי(?:ת|ים|ות)?", "מושלמ(?:ת|ים|ות)", "מושלם",
          r"פורצ(?:ת|י|ות)\s+דרך", r"פורץ\s+דרך", r"בצורה\s+חלקה", r"באופן\s+חלק",
          r"ללא\s+מאמץ", r"בלי\s+מאמץ", r"חסר(?:ת|י)?\s+תקדים",
          r"ברמה\s+עולמית", r"מהשורה\s+הראשונה"),
     "Marketing word. Delete it, or replace it with the measurement that earns the claim."),
    ("prefix-hyphen", "hard",
     re.compile(rf"(?<![{HEB}A-Za-z0-9_\-־])[ובכלמשה]{{1,3}}(?=[A-Za-z0-9])"),
     "Hebrew prefix glued to Latin text or a digit. Add a hyphen: ב-API, ה-JSON, ב-2025."),
    ("idiom-slang", "hard",
     term(r"לסגור\s+פינ(?:ה|ות)", r"סוגרים\s+פינה", "לדפלי", "דיפלוי", "לקנפג",
          "קינפוג", "מקנפג", "לדבג", "דיבוג", "מדבג", "לפשש", "לפוש",
          "לטסט", "לטסטט", "סבבה", "יאללה", "בקטנה", "אחלה", r"על\s+הפנים",
          r"חבל\s+על\s+הזמן", "תכלס", "תכל['׳]ס"),
     "Idiom, slang, or loanword verb. Use the standard Hebrew verb (לפרוס, להגדיר, לנפות שגיאות)."),
]

MAX_WORDS = 20  # descriptions cap. The instructions cap (16) needs context.

CODE_FENCE = re.compile(r"^(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LIST_ITEM_START = re.compile(
    r"^(?P<indent> {0,3})(?P<marker>[-*+]|[0-9]+[.)])(?P<gap> +)(?P<body>.*)$"
)
CONJUNCTION_END = re.compile(rf"(?<![{HEB}])(?:או|וגם|וכן|ו-|ו־)\s*$")
TABLE_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _finding(filename, line, col, rule, level, match, message):
    return {"file": filename, "line": line, "col": col, "rule": rule,
            "level": level, "match": match, "message": message}


def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _is_list_continuation(line, content_indent):
    if not line.strip():
        return True
    if LIST_ITEM_START.match(line):
        return False
    return _leading_spaces(line) >= content_indent


def _split_table_row(line):
    """Return trimmed table cells and their zero-based source columns."""
    left = len(line) - len(line.lstrip())
    right = len(line.rstrip())
    content = line[left:right]
    if "|" not in content:
        return None
    if content.startswith("|"):
        content = content[1:]
        left += 1
    if content.endswith("|"):
        content = content[:-1]
    raw_cells = re.split(r"(?<!\\)\|", content)
    if len(raw_cells) < 2:
        return None
    cells = []
    column = left
    for raw_cell in raw_cells:
        leading = len(raw_cell) - len(raw_cell.lstrip())
        cells.append((raw_cell.strip(), column + leading))
        column += len(raw_cell) + 1
    return cells


def _markdown_table_cells(lines):
    """Map Markdown table rows (anchored on the separator row) to their cells."""
    table_cells = {}
    index = 1
    while index < len(lines):
        separator = _split_table_row(lines[index])
        header = _split_table_row(lines[index - 1])
        if (not separator or not header or len(separator) != len(header)
                or not all(TABLE_SEPARATOR_CELL.fullmatch(cell)
                           for cell, _ in separator)):
            index += 1
            continue
        table_cells[index - 1] = header
        table_cells[index] = []
        index += 1
        while index < len(lines):
            row = _split_table_row(lines[index])
            if not row or len(row) != len(separator):
                break
            table_cells[index] = row
            index += 1
    return table_cells


def _dangling_conjunction_findings(lines, filename):
    findings = []
    in_fence = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if CODE_FENCE.match(line.strip()):
            in_fence = not in_fence
            index += 1
            continue
        start = None if in_fence else LIST_ITEM_START.match(line)
        if not start:
            index += 1
            continue
        content_indent = (len(start.group("indent")) + len(start.group("marker"))
                          + len(start.group("gap")))
        item_lines = [(index, start.group("body"))]
        next_index = index + 1
        item_fence = False
        while next_index < len(lines):
            candidate = lines[next_index]
            if CODE_FENCE.match(candidate.strip()):
                item_fence = not item_fence
                next_index += 1
                continue
            if item_fence:
                next_index += 1
                continue
            if not _is_list_continuation(candidate, content_indent):
                break
            item_lines.append((next_index, candidate))
            next_index += 1
        meaningful = [(i, INLINE_CODE.sub(" CODE ", text).strip())
                      for i, text in item_lines]
        meaningful = [(i, text) for i, text in meaningful if text]
        if meaningful:
            end_index, end_text = meaningful[-1]
            if CONJUNCTION_END.search(end_text):
                col = (start.start("marker") + 1 if end_index == index
                       else _leading_spaces(lines[end_index]) + 1)
                findings.append(_finding(
                    filename, end_index + 1, col, "dangling-conjunction", "hard",
                    end_text,
                    "List item ends with a conjunction (או, וגם, וכן). Complete the item or join it with the next item."))
        index = next_index
    return findings


def lint(text, filename="<stdin>"):
    """Return (findings, words_total)."""
    findings = []
    words_total = 0
    in_fence = False
    lines = text.splitlines()
    table_cells = _markdown_table_cells(lines)
    for lineno, raw_line in enumerate(lines, 1):
        if CODE_FENCE.match(raw_line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for segment, source_column in table_cells.get(lineno - 1, [(raw_line, 0)]):
            line = INLINE_CODE.sub("", segment)
            words_total += len(line.split())
            for rule_id, level, pattern, msg in RULES:
                for m in pattern.finditer(line):
                    findings.append(_finding(filename, lineno,
                                             source_column + m.start() + 1,
                                             rule_id, level, m.group(0), msg))
            for sentence in SENTENCE_SPLIT.split(line):
                n = len(sentence.split())
                if n > MAX_WORDS:
                    findings.append(_finding(
                        filename, lineno, source_column + 1, "sentence-length",
                        "hard", f"{n} words",
                        f"Sentence has {n} words (cap {MAX_WORDS}). Split it."))
    findings.extend(_dangling_conjunction_findings(lines, filename))
    findings.sort(key=lambda f: (f["line"], f["col"]))
    return findings, words_total


def report(findings, words_total, as_json, hard_count, baseline):
    rate = round(len(findings) * 100 / words_total, 1) if words_total else 0.0
    if as_json:
        print(json.dumps({"violations": findings, "count": len(findings),
                          "hard_count": hard_count, "baseline": baseline,
                          "words": words_total, "per_100_words": rate},
                         indent=2, ensure_ascii=False))
        return
    for f in findings:
        print(f"{f['file']}:{f['line']}:{f['col']} {f['rule']}: {f['message']} [{f['match']}]")
    print(f"\n{len(findings)} violations ({hard_count} hard, baseline {baseline}), "
          f"{words_total} words, {rate} per 100 words")
    print("Hedges (ייתכן, עשוי, אולי, כנראה) are never flagged: confidence is content.")


# (rule, text that must trigger it, text that must not trigger it)
SELFTEST_CASES = [
    ("semicolon", "לפתוח את הקובץ; לקרוא את השורה.", "לפתוח את הקובץ. לקרוא את השורה."),
    ("sentence-length", " ".join(["מילה"] * 21) + ".", " ".join(["מילה"] * 20) + "."),
    ("dangling-conjunction", "- להגדיר את היעד וגם\n- לרשום את התוצאה",
     "- להגדיר את היעד\n- לרשום את התוצאה"),
    ("dangling-conjunction", "1. לפתוח את הקובץ או\n2. לסגור אותו",
     "1. לפתוח את הקובץ\n2. לסגור אותו"),
    ("nominalization", "לבצע בדיקה של המסנן.", "לבדוק את המסנן."),
    ("nominalization", "וביצוע עדכון למערכת.", "ביצועים טובים של המערכת."),
    ("nominalization", "לערוך השוואה בין הגרסאות.", "לערוך את הקובץ."),
    ("nominalization", "מתן גישה למשתמש.", "לתת גישה למשתמש."),
    ("nominalization", "לקבל החלטה מהירה.", "לקבל גישה לשרת."),
    ("marketing-word", "פתרון חדשני ועוצמתי.", "פתרון שמגיב תוך 20 מילישניות."),
    ("marketing-word", "משתלב בצורה חלקה במערכת.", "חלק מהמערכת."),
    ("prefix-hyphen", "לשלוח בקשה לAPI.", "לשלוח בקשה ל-API."),
    ("prefix-hyphen", "השינוי נכנס ב2025.", "השינוי נכנס ב־2025."),
    ("idiom-slang", "צריך לדפלי את השירות.", "לפרוס את השירות."),
    ("idiom-slang", "המצב על הפנים.", "המצב גרוע."),
]

HEDGES = "ייתכן שהבקשה נכשלה. הסיבה עשויה להיות חריגת זמן. כנראה שהדיסק מלא. אולי השרת לא זמין."


def _rules(text):
    return {f["rule"] for f in lint(text)[0]}


def selftest():
    for rule, bad, good in SELFTEST_CASES:
        assert rule in _rules(bad), (rule, bad, lint(bad)[0])
        assert rule not in _rules(good), (rule, good, lint(good)[0])
    assert lint(HEDGES)[0] == [], lint(HEDGES)[0]
    print("selftest OK")


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    as_json = "--json" in argv
    baseline = 0
    disabled = set()
    paths = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--baseline", "--disable"):
            if i + 1 >= len(argv):
                print(f"error: {a} needs a value", file=sys.stderr)
                return 2
            i += 1
            if a == "--disable":
                disabled = set(argv[i].split(","))
            elif argv[i].isdigit():
                baseline = int(argv[i])
            else:
                print(f"error: --baseline needs a whole number, got {argv[i]!r}",
                      file=sys.stderr)
                return 2
        elif not a.startswith("--"):
            paths.append(a)
        i += 1

    findings, words_total = [], 0
    if paths:
        for p in paths:
            try:
                with open(p, encoding="utf-8-sig") as fh:
                    text = fh.read()
            except (OSError, UnicodeDecodeError) as exc:
                print(f"error: cannot read {p}: {exc}", file=sys.stderr)
                return 2
            f, w = lint(text, filename=p)
            findings.extend(f)
            words_total += w
    else:
        findings, words_total = lint(sys.stdin.read())

    findings = [f for f in findings if f["rule"] not in disabled]
    hard_count = sum(1 for f in findings if f["level"] == "hard")
    report(findings, words_total, as_json, hard_count, baseline)
    return 1 if hard_count > baseline else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
