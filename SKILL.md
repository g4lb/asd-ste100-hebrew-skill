---
name: asd-ste100-hebrew
description: "Use when Hebrew text must be parsed without a human to resolve ambiguity — tool descriptions, error messages, inter-agent instructions, system prompts, procedures, UI text — and misreading has a real cost, or when Hebrew text reads as dense, bureaucratic, hedged, or easy to misparse. Triggers: פשט את הטקסט, עברית טכנית פשוטה, STE בעברית, נסח מחדש כך שסוכן לא יטעה, simplify this Hebrew, Simplified Technical Hebrew. Not for creative or marketing copy, and not for English text."
license: MIT
metadata:
  version: 0.1.0
---

# Simplified Technical Hebrew (based on ASD-STE100)

ASD-STE100 is a controlled-language standard for English. The aerospace and defense industry built it so maintenance technicians cannot misread instructions. It removes the two biggest sources of misreading. These are words with more than one meaning, and sentences with more than one possible structure.

This skill applies the same discipline to **Hebrew**. Hebrew adds its own sources of misreading. Words can be unvocalized homographs, and prefix letters are glued to words. Construct chains (סמיכות) and chains of ש- clauses grow long. An instruction can take four competing forms. One reader is an AI agent that parses Hebrew with no human to ask. The other is a human reader of technical Hebrew, including readers with weaker Hebrew.

ASD-STE100 defines English only. Every Hebrew rule below is this skill's adaptation, not an official standard.

## When to Use This Skill

- Hebrew text reads as dense, bureaucratic, or ambiguous. Examples: a tool description, an error message, an instruction between agents, a system prompt, a procedure, UI text.
- Hebrew text goes to an agent, a translation pipeline, or a reader with weaker Hebrew, and misreading has a cost.
- The user asks for a before/after table that names each broken rule. The default output is the rewritten text alone (see Output Format).

Do not use it for creative, marketing, or persuasive copy. Do not use it for English text: the English skill `asd-ste100` covers English.

## Two Modes

Pick a mode before you rewrite. If the user does not say which, infer it from the type of text. Keep the choice internal unless the user asks for the rule table.

**Strict**: procedures, error messages, tool and function descriptions, instructions between agents, safety text. Apply every rule, including the length caps, one word for one meaning, and the infinitive for every instruction.

**Flavored**: READMEs, PR descriptions, changelogs, explanatory prose. Apply the structural rules in full. Treat the lexical rules (one word for one meaning, one part of speech per word) as advisory. Prose needs some range of vocabulary.

## Source and Scope

The rule categories come from ASD-STE100 Issue 9 (January 2025). Issue 9 has 53 writing rules in 9 sections, and a dictionary of about 900 approved English words. This skill does not reproduce that dictionary. It is free to obtain but not free to redistribute, and it is English anyway. The skill applies the principle instead: use the plainest common Hebrew word, and use it the same way every time. Full mapping and sources: `references/writing-rules.md`.

## Core Rewrite Rules

### Structural rules — apply these

<!-- ste-lint: off -->

| Rule | Do | Don't |
|---|---|---|
| Active voice | "הסוכן מוחק את הקובץ." | "הקובץ נמחק." / "מוחקים את הקובץ." — unless the actor is unknown or irrelevant |
| One instruction form | Infinitive every time: "לפתוח את הקובץ. לקרוא את שורה 3." | Mixing "פתח", "פתחי", "תפתח", "יש לפתוח" |
| One instruction per sentence | "לפתוח את הקובץ. לקרוא את שורה 3." | "לפתוח את הקובץ ולקרוא את שורה 3, ואז לבדוק אם היא תואמת." |
| Sentence length | ≤16 words for instructions, ≤20 words for descriptions | Long sentences with stacked clauses |
| No semicolons (Rule 8.1) | Separate sentences | Any `;` |
| Construct chains | ≤3 nouns: "שסתום משאבת דלק" | "מכלול שסתום כניסת משאבת דלק לחץ גבוה" |
| One ש- clause | "הקובץ שהסוכן יצר נמצא בתיקייה." | "הקובץ שהוא יצר שלא נמצא בתיקייה שבה…" |
| No dropped words | "למחוק את הקובץ הזמני." | "יש למחוק קובץ זמני." (which file?) |
| Keep modality | "ייתכן שהבקשה נכשלה." stays as it is | "הבקשה נכשלה." — a hedge became a fact |
| One hedge per uncertain claim | "ייתכן שהחיבור נכשל. ייתכן שהסיבה היא בעיה בהגדרות הפרוקסי." | "ייתכן שהחיבור נכשל בגלל בעיה בהגדרות הפרוקסי." — the source doubted both the failure and its cause |
| Hyphen before Latin text or digits | "ב-API", "ה-JSON", "ב-2025" | "בAPI", "הJSON", "ב2025" |
| No abbreviations | "בדרך כלל", "על פי" | "בד\"כ", "עפ\"י", "וכו'" |
| Mixed-direction text | Code in backticks. The sentence starts with a Hebrew word | A sentence that starts with a Latin term |
| Paragraphs and lists | One topic per paragraph, ≤6 sentences. A list for 3+ steps | A sequence hidden in one sentence |
| Conditions next to their step | "לבדוק את הלוגים. אם יש שגיאות קריטיות: לעצור את כל הפעולות. לדווח מיד. אחרת: לדווח מה הלוגים מראים." | A stop condition placed after the step it should prevent |

<!-- ste-lint: on -->

### Lexical rules — direction of travel only

<!-- ste-lint: off -->

| Rule | Do | Don't |
|---|---|---|
| One word, one meaning | Always "לבדוק" for one action | Rotating "לבדוק" / "לוודא" / "לאמת" |
| One part of speech per word | "המשתמש מפעיל את הכלי." (`משתמש` stays a noun) | "המשתמש משתמש בכלי." |
| Verb, not noun (Rule 3.7) | "לבדוק את הלוג." | "לבצע בדיקה של הלוג." / "לערוך השוואה" / "לקבל החלטה" |
| No idioms, slang, or loanword verbs | "לפרוס", "להגדיר", "לנפות שגיאות", "למצוא" | "לדפלי", "לקנפג", "לדבג", "לעלות על" |
| Homographs | Full spelling (כתיב מלא). Rephrase or add niqqud to one word if it is still ambiguous | "ספר", "מנהל" where both readings fit |
| Domain terms | Keep a necessary technical term. Define it once if it is not common Hebrew | Jargon that is never defined |

<!-- ste-lint: on -->

## Scan Checklist

Scan for all eight before you rewrite anything:

1. **Synonym rotation**: one thing with several names (`המשתמש`, `הלקוח`, `המנוי`). Pick one name.
2. **Hedge stacking and filler**: `חשוב לציין ש…`, `יש לציין כי…`, `ייתכן שאולי`. State the claim or delete it. Keep a single honest hedge.
3. **Nominalization**: `לבצע`, `ביצוע`, `לערוך`, `מתן`, `קבלת` + an action noun. Use the verb.
4. **Marketing words**: `חדשני`, `עוצמתי`, `בצורה חלקה`, `פורץ דרך`. Delete them, or give the measurement.
5. **Run-on sentences**: semicolons, or chains of `ו`, `ש-`, `אשר`. One idea per sentence.
6. **Slang and loanword verbs**: `לדפלי`, `לקנפג`, `לפוש`. Use the standard Hebrew verb.
7. **Passive voice and the impersonal plural**: `נמחק`, `עודכן`, `מוחקים`. Name the actor.
8. **Mixed instruction forms**: imperative, `יש ל…`, and future tense next to the infinitive. Use the infinitive.

## Process

1. Pick the mode. Say which only when the user asked for the rule table.
2. Read the input once for meaning. Do not rewrite before you know what it must still say afterward.
3. Walk it sentence by sentence. Flag every rule violation and every checklist item. In Flavored mode, flag the lexical rules but do not enforce them. For a mechanical first pass, run `python3 <this skill's directory>/scripts/ste-lint-he.py` (files or stdin, `--json` for structured output). It checks semicolons, sentence length, nominalization, marketing words, prefix hyphens, slang, synonym rotation, and dangling conjunctions in lists. Its advisory findings are passive voice, abbreviations, and ש- chains. `לבצע` before a word that is not a listed action noun is also advisory. It never flags hedges. It cannot check construct chains, homographs, the impersonal plural, dropped `את`, or the infinitive rule. Check those by hand.
4. Rewrite each flagged sentence and preserve the meaning exactly. If a rewrite would drop necessary precision, keep the longer phrasing and flag it. Necessary precision includes a safety condition, a scope qualifier, and a number.
   - **Check modality before you commit to a rewrite.** `ייתכן`, `עשוי`, `אולי`, `כנראה`, `לעיתים`, `אפשרי`, and attempt verbs such as `ינסה` and `מנסה` carry the author's confidence. Count the uncertain claims in the source. Keep one hedge for each claim, even when you split or merge sentences. A shorter sentence that turns a hedge into a fact makes a different claim.
   - Never add a fact the source did not state.
   - Keep the gender and number agreement correct after every change. Hebrew verbs and adjectives agree with their subject.
5. Output the rewritten text (see Output Format).
6. If the input already complies, say so. Do not force changes onto compliant text.

## Output Format

**Default: the rewritten Hebrew text, and nothing else.** No preamble, no mode announcement, no violation count, no summary of changes, no rule table, no closing offer.

There is one permitted addition. If step 4 kept a longer phrasing on purpose, add one sentence after the text that starts with `Kept as-is:`. It names the phrase and the precision that a shorter version would lose. Do not use this line to explain a hedge you kept, a rule you applied, or an ambiguity you noticed. Leave the line out when there is nothing to report.

**On request: the rule table.** Example requests: "show the diff", "which rules did it break", "הסבר את השינויים", "לפני/אחרי". For such a request, output this instead:

```markdown
<!-- ste-lint: off -->

| Rule violated | Original | Simplified |
|---|---|---|
| Nominalization | "לבצע בדיקה של הלוג" | "לבדוק את הלוג" |
| Passive voice | "הקובץ נמחק" | "הסוכן מוחק את הקובץ" |

<!-- ste-lint: on -->

Mode: Strict. 2 violations found.
```

Follow the table with one line about anything you did **not** simplify, and why.

## Boundaries

**Will:**
- Rewrite ambiguous or dense Hebrew into short, active sentences where each word has one meaning.
- Return the rewritten text alone by default, and name the rules when the user asks.
- Preserve every fact, condition, scope qualifier, and hedge strength.
- Suggest a one-line glossary entry for a technical term that must stay.

**Will not:**
- Claim official STE compliance. No official Hebrew STE exists.
- Rewrite English text. Use `asd-ste100` for English.
- Simplify creative, marketing, or persuasive copy.
- Drop a safety condition, exception, or scope qualifier to shorten a sentence.
- Turn `ייתכן שהבקשה נכשלה` into `הבקשה נכשלה`.
- Make weak content useful. A hollow paragraph becomes a short, clean, hollow paragraph. Say so instead of polishing it.
- Shorten past the point of clarity. Stop when the sentence is unambiguous, not when it is shortest.

## Additional Resources

- **`references/writing-rules.md`**: the full mapping from STE to Hebrew, with sources.
- **`examples/before-after.md`**: STE rules shown in Hebrew, and four examples of agent output.
- **`scripts/ste-lint-he.py`**: a deterministic linter that uses only the Python standard library. Exit 1 when hard violations exceed `--baseline` (default 0). Advisory findings never fail the run. `--disable` silences named rules. `--selftest` asserts that `ייתכן שהבקשה נכשלה` passes clean. For Flavored text (READMEs, prose), add `--disable synonym-rotation`. In that mode synonym rotation is advisory, but the linter treats it as hard. The linter skips code, YAML front matter, and text between `<!-- ste-lint: off -->` and `<!-- ste-lint: on -->`.
