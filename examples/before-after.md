# Before / After Examples

## Part 1 — STE rules, shown in Hebrew

ASD-STE100 defines English only. These rows show how each rule carries over to Hebrew. They are illustrations, not quotes from the standard.

| Rule | Before | After | Why |
|---|---|---|---|
| One word, one meaning | "לוודא את המערכת." / "לבדוק את החיבורים." / "לאמת קבלה." | "לבדוק את המערכת. לבדוק את החיבורים. לבדוק שההודעה הגיעה." | Three near-synonyms make the reader guess whether they are one action or three. |
| One part of speech per word | "לשמן את השסתום." | "למרוח שמן על השסתום." | Keep "שמן" a noun. Do not turn it into a verb. |
| Verb, not noun (Rule 3.7) | "לבצע בדיקה של המסנן." | "לבדוק את המסנן." | `לבצע` carries no meaning. The action hides in the noun. |
| No idioms or slang (replaces Rule 9.3) | "לעלות על התקלה." / "לדפלי את השירות." | "למצוא את התקלה." / "לפרוס את השירות." | An idiom's meaning does not come from its words. A slang loanword has no fixed spelling. |
| Active voice | "הקובץ נמחק." | "הסוכן מוחק את הקובץ." | The passive form hides the actor. |
| One instruction form | "פתח את הקובץ. יש לקרוא את שורה 3. תבדוק את הפלט." | "לפתוח את הקובץ. לקרוא את שורה 3. לבדוק את הפלט." | One form, the infinitive, which is gender-neutral. |
| Keep `את` | "יש למחוק קובץ זמני." | "למחוק את הקובץ הזמני." | Without `את` and the article, the reader cannot tell which file. |
| Hyphen before Latin text or digits | "להתקין את הגרסה בשרת הAPI." | "להתקין את הגרסה בשרת ה-API." | Without the hyphen, the prefix merges with the term. |
| No abbreviations | "בד\"כ התהליך מסתיים תוך 5 דק'." | "בדרך כלל התהליך מסתיים תוך 5 דקות." | An abbreviation can stand for more than one phrase. |

## Part 2 — Applied to agent output

These are original examples for this skill's use case. Word counts are whitespace-separated tokens.

### Example A — Tool description (Strict)

**Before:**

> כלי זה ינסה לבצע סנכרון של המצב בין מערכות הגיבוי השונות שהוגדרו, ובמידה שיזוהה קונפליקט, ייתכן שהוא יפתור אותו באופן אוטומטי בהתאם לאסטרטגיה שנקבעה; אחרת, הקונפליקט יוצג לבדיקה ידנית.

**Violations flagged:**
- Nominalization: "לבצע סנכרון".
- Passive forms with no actor: "שהוגדרו", "יזוהה", "שנקבעה", "יוצג".
- A semicolon, and 29 words in one sentence.
- Loanword: "קונפליקט".

Not flagged: "ינסה" and "ייתכן שהוא יפתור". They are hedges. The rewrite must not promise success.

**After:**

> הכלי מנסה לסנכרן את המצב בין מערכות הגיבוי המוגדרות. אם הכלי מוצא התנגשות, הוא קורא את האסטרטגיה המוגדרת. אם האסטרטגיה מתירה פתרון אוטומטי, ייתכן שהכלי יפתור את ההתנגשות בלי משתמש. אם הכלי לא פותר את ההתנגשות, הוא מדווח עליה לבדיקה ידנית.

### Example B — Error message (Strict)

**Before:**

> ייתכן שאירעה שגיאה במהלך עיבוד הבקשה שלך עקב אי-התאמה אפשרית בפורמט הנתונים הצפוי, אשר עשויה להיגרם כתוצאה מגרסת לקוח שאינה מעודכנת.

**Violations flagged:**
- One sentence with three claims (an error, a format mismatch, a client version).
- A ש- chain ("אשר", "שאינה") and bureaucratic phrasing ("במהלך", "כתוצאה מ").

Not flagged: "ייתכן" and "עשויה". The system does not know the cause. Both hedges report that accurately.

**After:**

> ייתכן שהבקשה נכשלה. ייתכן שהסיבה היא פורמט נתונים שלא מתאים למה שהשרת מצפה לו. לקוח בגרסה ישנה יכול לגרום לאי-התאמה הזו. לבדוק את גרסת הלקוח.

**This example is why the modality rule exists.** "הבקשה נכשלה" reads better than "ייתכן שהבקשה נכשלה", but it asserts a failure the system only suspects.

### Example C — Instruction between agents (Strict)

**Before:**

> לאחר שהעבודה במעלה הזרם תסתיים ובהנחה שלא הועלו שגיאות, על הסוכן במורד הזרם להמשיך ולצרוך את תוצר הפלט, אם כי חשוב לציין שלעיתים נוצרים תוצרים חלקיים במצבי timeout.

**Violations flagged:**
- Passive forms: "הועלו", "נוצרים".
- Filler: "חשוב לציין ש".
- One sentence with three facts (a condition, an action, a warning). 28 words.

**After:**

> לחכות שהעבודה הקודמת בתהליך תסתיים בלי שגיאות. אחר כך לקרוא את קובץ הפלט. אזהרה: חריגת זמן (timeout) יכולה ליצור קובץ פלט חלקי. לבדוק שהקובץ שלם לפני שהסוכן משתמש בו.

Two deliberate choices:
- "על הסוכן להמשיך ולצרוך" became the infinitive "לקרוא". That is correct for an instruction to the agent that does the work. Do not make the same change in descriptive text.
- The last sentence is **new**. The source warned about partial files but did not say what to do. The check makes the warning actionable. It is added content, so this note says so. If the source left it out on purpose, delete the sentence.

### Example D — README prose (Flavored)

**Before:**

> שכבת המטמון שלנו תוכננה להשתלב בצורה חלקה בסטאק הקיים שלכם עם מינימום חיכוך וללא נעילת ספק; היא ממנפת דמיון סמנטי כדי להפחית באופן דרמטי את החטאות המטמון שפוגעות באופן מסורתי בעומסי עבודה של LLM.

**Violations flagged:**
- Marketing words with no measurement: "בצורה חלקה", "מינימום חיכוך", "באופן דרמטי".
- A semicolon, and 34 words.
- Loanwords and slang: "סטאק", "ממנפת".

**After:**

> מטמון רגיל משווה בקשות לפי טקסט זהה, ולכן שינוי קטן בניסוח גורם להחטאה. המטמון הזה משווה את המשמעות של הנחיה חדשה להנחיות שהוא כבר שומר. הוא רץ לצד המערכת הקיימת שלכם ולא שומר נתונים מחוץ לה.

Flavored mode kept the explanatory rhythm. It removed the marketing words, the semicolon, and the length.

## How to Read These Examples

Part 1 shows the STE rules carried over to Hebrew. Part 2 shows the same discipline applied to agent output. One meaning per word, active voice, one instruction per sentence, and explicit conditions make Hebrew text safer for an agent and for a human reader.
