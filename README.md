**English** | [עברית](README.he.md)

# ASD-STE100 for Hebrew — Simplified Technical Hebrew for Agent Output

A Claude Code skill that rewrites dense or ambiguous **Hebrew** into simplified technical Hebrew. It is based on [ASD-STE100](https://www.asd-ste100.org/), the controlled-language standard that the aerospace industry built so that maintenance instructions cannot be misread.

The reader here is different. It can be an **AI agent** that parses Hebrew text with no human to ask what the author meant. It can also be a person who reads technical Hebrew, including readers whose first language is not Hebrew.

> ASD-STE100 defines English only. No official Hebrew version exists. Every Hebrew rule in this skill is this project's adaptation, not an official standard.

This is a Hebrew port of [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), which does the same for English.

## Before / After

<!-- ste-lint: off -->

| Before | After |
|---|---|
| "כלי זה ינסה לבצע סנכרון של המצב בין מערכות הגיבוי השונות שהוגדרו, ובמידה שיזוהה קונפליקט, ייתכן שהוא יפתור אותו באופן אוטומטי בהתאם לאסטרטגיה שנקבעה; אחרת, הקונפליקט יוצג לבדיקה ידנית." | "הכלי מנסה לסנכרן את המצב בין מערכות הגיבוי המוגדרות. אם הכלי מזהה התנגשות, ייתכן שהוא יפתור אותה באופן אוטומטי לפי האסטרטגיה המוגדרת. אם הכלי לא פותר את ההתנגשות, הוא מציג אותה לבדיקה ידנית." |
| "ייתכן שאירעה שגיאה במהלך עיבוד הבקשה שלך עקב אי-התאמה אפשרית בפורמט הנתונים הצפוי, אשר עשויה להיגרם כתוצאה מגרסת לקוח שאינה מעודכנת." | "ייתכן שאירעה שגיאה בעיבוד הבקשה. ייתכן שהסיבה היא אי-התאמה בפורמט הנתונים הצפוי. ייתכן שגרסת לקוח לא מעודכנת גרמה לאי-ההתאמה הזו." |

<!-- ste-lint: on -->

The first row is a tool description. The rewrite removes `לבצע סנכרון` ("perform synchronization"), the passive forms, and the semicolon. The second row is an error message. Each of its three hedges (`ייתכן`, "it may be") stays a hedge. The system does not know the cause, so the rewrite must not pretend that it does.

More examples, with explanations in English: [`examples/before-after.md`](examples/before-after.md).

## What the Skill Does

1. Picks a mode. **Strict** covers instructions, error messages, and tool descriptions. **Flavored** covers READMEs and explanatory prose.
2. Flags every rule violation:
   - synonyms rotated for the same action (`לבדוק` / `לוודא` / `לאמת`)
   - passive forms
   - actions frozen into nouns (`לבצע בדיקה`, "perform a check")
   - long construct chains (סמיכות) and chains of ש- clauses
   - long sentences and semicolons
   - slang, loanword verbs, and abbreviations
   - a Hebrew prefix glued to Latin text (`בAPI` instead of `ב-API`)
   - mixed instruction forms
3. Rewrites without dropping any fact, condition, or hedge. `ייתכן ש…` stays `ייתכן ש…`.
4. Returns only the rewritten text. To see the rules it applied, ask "show the diff" or "הסבר את השינויים".

### Rules specific to Hebrew

- **One instruction form: the infinitive** (`לפתוח את הקובץ`, "to open the file"). It is gender-neutral. Do not mix it with the imperative (`פתח`), the future (`תפתח`), or `יש לפתוח`.
- **A hyphen after a prefix before Latin text or a digit**: `ב-API`, `ה-JSON`, `ב-2025`.
- **No abbreviations**: `בדרך כלל`, not `בד"כ`.
- **Full spelling (כתיב מלא).** If a word is still ambiguous, rephrase it, or add vowel marks (ניקוד) to that one word.
- **At most one ש- clause per sentence.**
- **Up to 16 words** in an instruction sentence, and **up to 20 words** in a descriptive sentence. Hebrew attaches prefixes to words, so the same content uses about 20% fewer words than English.

Full rule mapping, with sources: [`references/writing-rules.md`](references/writing-rules.md).

## The Linter

`scripts/ste-lint-he.py` uses only the Python standard library.

```bash
python3 scripts/ste-lint-he.py FILE.md
echo "לבצע בדיקה של הקובץ; ב2025" | python3 scripts/ste-lint-he.py --json
python3 scripts/ste-lint-he.py --selftest
```

- **Hard** (fails the run): `semicolon`, `sentence-length`, `nominalization`, `marketing-word`, `prefix-hyphen`, `idiom-slang`, `synonym-rotation`, and `dangling-conjunction`. Here `nominalization` means `לבצע` before a listed action noun. `dangling-conjunction` means `או`, `וגם`, or `וכן` at the end of a list item.
- **Advisory** (never fails the run): `passive-voice`, `abbreviation`, `she-chain`, and `nominalization` when `לבצע` is followed by any other word (`לבצע את הפקודה`).
- `--baseline N` tolerates N hard findings. `--disable rule1,rule2` silences rules. For READMEs and prose, add `--disable synonym-rotation`: in Flavored mode, synonym rotation is only advisory.
- Exit codes: 0 pass, 1 hard findings above the baseline, 2 unreadable file or bad flag.
- The linter skips code, YAML front matter, and any text between `<!-- ste-lint: off -->` and `<!-- ste-lint: on -->`. Put these markers around a "before" example that is bad on purpose.
- The linter **never** flags hedges (`ייתכן`, `עשוי`, `אולי`, `כנראה`). Confidence is content.
- The linter does **not** check construct-chain length, homographs, or the impersonal plural (`מוחקים`, "one deletes"). It also does not check a dropped `את` or the infinitive rule. These need morphological analysis, so check them by hand.
- A clean result only means the structural checks found nothing. It does not prove that the rewrite kept the meaning.

## Installation

### Claude Code

```bash
npx skills add g4lb/asd-ste100-hebrew-skill
```

Or clone it into your Claude Code skills folder:

```bash
git clone https://github.com/g4lb/asd-ste100-hebrew-skill ~/.claude/skills/asd-ste100-hebrew
```

### Claude.ai and the Claude desktop app

1. Download [`asd-ste100-hebrew.zip`](https://github.com/g4lb/asd-ste100-hebrew-skill/releases/latest/download/asd-ste100-hebrew.zip) from the latest release.
2. Open [Customize > Skills](https://claude.ai/customize/skills) and upload the zip.
3. Turn the skill on.

The zip holds only the skill files: `SKILL.md`, the rules, the examples, and the linter.

## Usage

Ask in Hebrew or in English:

```
פשט את תיאור הכלי הזה
נסח מחדש את הודעת השגיאה כך שסוכן לא יטעה
Apply Simplified Technical Hebrew to this instruction
```

You get the rewritten text back and nothing else.

## Scope

Built for: messages between agents, tool descriptions, error messages, system prompts, procedures, and UI text, in Hebrew.

Not built for: creative writing, marketing copy, or English text. For English, use [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill).

The skill fixes the form of a text, not its substance. A paragraph with nothing to say comes out short, clean, and still empty.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to run the checks and add a linter rule. Changes are listed in [`CHANGELOG.md`](CHANGELOG.md).

## Credit and Licence

Based on [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) (MIT). This skill does not include ASD's official dictionary: it is free to obtain but not free to redistribute. You can request it from the [official site](https://www.asd-ste100.org/STE_downloads.html).

MIT — see [LICENSE](LICENSE).
