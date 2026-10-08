# Simplified Technical Hebrew — Rules and Sources

This file maps the public rule categories of ASD-STE100 to Hebrew. It paraphrases rule *categories*. It does not reproduce the standard's text or its dictionary. ASD-STE100 defines English only. No official Hebrew version exists, so every Hebrew adaptation below belongs to this project, not to ASD.

## What ASD-STE100 Is

ASD-STE100 is a controlled language for English. It was first released in 1986 by what is now ASD (the AeroSpace and Defense Industries Association of Europe). Airlines asked for it because their maintenance staff were mostly not native English speakers, and a misread instruction on an aircraft can kill people. The current edition is Issue 9 (January 2025): 53 writing rules in 9 sections, and a dictionary of about 900 approved words.

## Rules That Carry Over Unchanged

- No semicolons (Rule 8.1). Write separate sentences.
- One instruction per sentence.
- One topic per paragraph, with at most 6 sentences.
- Use a numbered or bulleted list for 3 or more steps or conditions.
- A safety instruction starts with the command or the condition.
- Keep modality. `ייתכן ש…`, `עשוי`, `אולי`, and `כנראה` keep their strength.
- Add no facts: no new cause, frequency, or mechanism.
- No marketing words: `חדשני`, `מהפכני`, `עוצמתי`, `אינטואיטיבי`, `מושלם`, `בצורה חלקה`, `פורץ דרך`, `ללא מאמץ`, `חסר תקדים`.

## Rules Adapted for Hebrew

| STE rule | Hebrew rule | Why it changes |
|---|---|---|
| ≤20 words (instructions), ≤25 words (descriptions) | ≤16 words (instructions), ≤20 words (descriptions) | Hebrew attaches ו, ה, ב, כ, ל, מ, ש to the next word, so the same content uses about 20% fewer words. |
| Noun clusters ≤3 words | סמיכות chain ≤3 nouns (`שסתום משאבת דלק` is the limit) | A construct chain is the Hebrew noun cluster. Split a longer chain with `של` or a clause. |
| Active voice | Avoid נפעל/פועל/הופעל/התפעל when the actor is known. Avoid the impersonal plural (`מוחקים את הקובץ`) | Both forms hide who acts. |
| Verb, not noun (Rule 3.7) | `לבדוק`, not `לבצע בדיקה של`. `להשוות`, not `לערוך השוואה`. `להחליט`, not `לקבל החלטה` | The helper verb carries no meaning. |
| No phrasal verbs (Rule 9.3) | No idioms, slang, or loanword verbs (`לעלות על`, `לסגור פינה`, `לדפלי`, `לקנפג`, `לדבג`) | Hebrew has no phrasal verbs. Idioms and slang cause the same problem: the meaning does not come from the words. |
| Simple tenses only | One verb form for instructions: the infinitive (`לפתוח את הקובץ`) | Hebrew has no present perfect. Its problem is mixed instruction forms (`פתח`, `פתחי`, `יש לפתוח`, `תפתח`). The infinitive is gender-neutral and standard in Israeli procedures. |
| No dropped words | Keep `את` before a definite direct object. No headline style. Keep the subject in the third person | `יש למחוק קובץ` does not say which file. |

## Rules for Hebrew Only

- **Homographs.** Use full spelling (כתיב מלא) as the Academy of the Hebrew Language defines it. If a word can still be read two ways (`ספר`, `מנהל`), rephrase it, or add a vowel mark (ניקוד) to that word only.
- **Hyphen before Latin text or digits.** `ב-API`, `ה-JSON`, `ב-2025`. A maqaf (`־`) is also correct.
- **No abbreviations.** Write the full words: `בדרך כלל`, not `בד"כ`. `על פי`, not `עפ"י`. List the items instead of `וכו'`.
- **Mixed-direction text.** Put code, paths, and identifiers in backticks. Do not start a sentence with a Latin term: right-to-left display moves it to the wrong end of the line.
- **ש- clauses.** At most one per sentence. A chain of ש- clauses is the Hebrew run-on sentence.

## What the Linter Checks

`scripts/ste-lint-he.py` checks only patterns that a regex can find:

| Rule ID | Level |
|---|---|
| `semicolon`, `sentence-length` (>20 words), `nominalization` (verb + listed action noun), `marketing-word`, `prefix-hyphen`, `idiom-slang`, `synonym-rotation`, `dangling-conjunction` | hard |
| `nominalization` (verb + any other word, e.g. `לבצע את הפקודה`), `passive-voice`, `abbreviation`, `she-chain` | advisory |

It does not check סמיכות chain length, homographs, the impersonal plural, dropped `את`, or the infinitive-only rule. Those need a morphological analyzer. Check them by hand.

## Sources

- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [ASD-STE100 — About STE](https://www.asd-ste100.org/about_STE.html)
- [ASD Europe — Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [Simplified Technical English — Wikipedia](https://en.wikipedia.org/wiki/Simplified_Technical_English)
- [The Academy of the Hebrew Language — spelling rules (כללי הכתיב חסר הניקוד)](https://hebrew-academy.org.il/wp-content/uploads/כללי-הכתיב-חסר-הניקוד.pdf)
- [The Academy of the Hebrew Language — punctuation rules (כללי הפיסוק)](https://hebrew-academy.org.il/topic/hahlatot/punctuation/)
- [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), the English skill this project adapts
