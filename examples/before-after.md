# Before / After Examples

## Part 1 — STE rules, shown in Hebrew

ASD-STE100 defines English only. These rows show how each rule carries over to Hebrew. They are illustrations, not quotes from the standard.

| Rule | Before | After | Why |
|---|---|---|---|
| One word, one meaning | "לבדוק את המערכת." / "לבחון את החיבורים." / "לאמת את הקבלה." | "לבדוק את המערכת. לבדוק את החיבורים. לבדוק את הקבלה." | Three near-synonyms make the reader guess whether they are one action or three. |
| One part of speech per word | "המשתמש משתמש בכלי." | "המשתמש מפעיל את הכלי." | `משתמש` is both a noun ("user") and a verb ("uses"). Keep it a noun, and use another verb for the action. |
| Verb, not noun (Rule 3.7) | "לבצע בדיקה של המסנן." | "לבדוק את המסנן." | `לבצע` carries little meaning. The action hides in the noun. |
| No idioms or slang (replaces Rule 9.3) | "לעלות על התקלה." / "לדפלי את השירות." | "למצוא את התקלה." / "לפרוס את השירות." | An idiom's meaning does not come from its words. A slang loanword has no fixed spelling. |
| Active voice | "הקובץ נמחק." | "הסוכן מוחק את הקובץ." | The passive form hides the actor. |
| One instruction form | "פתח את הקובץ. יש לקרוא את שורה 3. תבדוק את הפלט." | "לפתוח את הקובץ. לקרוא את שורה 3. לבדוק את הפלט." | One form, the infinitive, which is gender-neutral. |
| Keep `את` | "למחוק קובץ ההגדרות." | "למחוק את קובץ ההגדרות." | Headline style drops `את` before a definite object. Keep it so the direct object is explicit. |
| Hyphen before Latin text or digits | "להתקין את הגרסה בשרת הAPI." | "להתקין את הגרסה בשרת ה-API." | Without the hyphen, the prefix merges with the term. |
| No abbreviations | "בד\"כ התהליך מסתיים תוך 5 דק'." | "בדרך כלל התהליך מסתיים תוך 5 דקות." | An abbreviation can stand for more than one phrase. |

## Part 2 — Applied to agent output

These are original examples for this skill's use case. Word counts are whitespace-separated tokens.

### Example A — Tool description (Strict)

**Before:**

> כלי זה ינסה לבצע סנכרון של המצב בין מערכות הגיבוי השונות שהוגדרו, ובמידה שיזוהה קונפליקט, ייתכן שהוא יפתור אותו באופן אוטומטי בהתאם לאסטרטגיה שנקבעה; אחרת, הקונפליקט יוצג לבדיקה ידנית.

**Violations flagged:**
- Nominalization: "לבצע סנכרון".
- Passive verbs: "יזוהה", "יוצג". Relative clauses with a passive verb: "שהוגדרו", "שנקבעה".
- A semicolon, and 29 words in one sentence.
- Loanword: "קונפליקט".

Not flagged: "ינסה" and "ייתכן שהוא יפתור". They are hedges. The rewrite must not promise success.

**After:**

> הכלי מנסה לסנכרן את המצב בין מערכות הגיבוי המוגדרות. אם הכלי מזהה התנגשות, ייתכן שהוא יפתור אותה באופן אוטומטי לפי האסטרטגיה המוגדרת. אם הכלי לא פותר את ההתנגשות, הוא מציג אותה לבדיקה ידנית.

"שהוגדרו" became the adjective "המוגדרות". STE permits a past participle used as an adjective. The source does not say who configured the systems, so the rewrite does not name an actor. "אחרת" became an explicit condition: the tool shows the conflict when it does not resolve it.

### Example B — Error message (Strict)

**Before:**

> ייתכן שאירעה שגיאה במהלך עיבוד הבקשה שלך עקב אי-התאמה אפשרית בפורמט הנתונים הצפוי, אשר עשויה להיגרם כתוצאה מגרסת לקוח שאינה מעודכנת.

**Violations flagged:**
- One sentence with three claims (an error, a format mismatch, a client version).
- A ש- chain ("אשר", "שאינה") and bureaucratic phrasing ("במהלך", "כתוצאה מ").

Not flagged: "ייתכן" and "עשויה". The system does not know the cause. Both hedges report that accurately.

**After:**

> ייתכן שאירעה שגיאה בעיבוד הבקשה. ייתכן שהסיבה היא אי-התאמה בפורמט הנתונים הצפוי. ייתכן שגרסת לקוח לא מעודכנת גרמה לאי-ההתאמה הזו.

**This example is why the modality rule exists.** "אירעה שגיאה" reads better than "ייתכן שאירעה שגיאה", but it asserts an error that the system only suspects. Each of the three hedges in the source stays a hedge. The rewrite also adds no instruction: the source does not tell the reader what to do.

### Example C — Instruction between agents (Strict)

**Before:**

> לאחר שהעבודה במעלה הזרם תסתיים ובהנחה שלא הועלו שגיאות, על הסוכן במורד הזרם להמשיך ולצרוך את תוצר הפלט, אם כי חשוב לציין שלעיתים נוצרים תוצרים חלקיים במצבי timeout.

**Violations flagged:**
- Passive forms: "הועלו", "נוצרים".
- Filler: "חשוב לציין ש".
- One sentence with three facts (a condition, an action, a warning). 28 words.

**After:**

> לחכות שהעבודה במעלה הזרם תסתיים. אם העבודה לא העלתה שגיאות, לקרוא את תוצר הפלט. אזהרה: במצבי חריגת זמן (timeout), לפעמים יש תוצר חלקי.

Two deliberate choices:
- "על הסוכן במורד הזרם להמשיך ולצרוך" became the infinitive "לקרוא". That is correct for an instruction to the agent that does the work. Do not make the same change in descriptive text.
- "ובהנחה שלא הועלו שגיאות" became an explicit condition ("אם העבודה לא העלתה שגיאות"), not a wait for success. "לעיתים" stays as "לפעמים": the frequency hedge keeps its strength. The warning keeps the source's link between timeouts and partial outputs, without claiming that the timeout causes them.

### Example D — README prose (Flavored)

**Before:**

> שכבת המטמון שלנו תוכננה להשתלב בצורה חלקה בסטאק הקיים שלכם עם מינימום חיכוך וללא נעילת ספק; היא ממנפת דמיון סמנטי כדי להפחית באופן דרמטי את החטאות המטמון שפוגעות באופן מסורתי בעומסי עבודה של LLM.

**Violations flagged:**
- Marketing words with no measurement: "בצורה חלקה", "מינימום חיכוך", "באופן דרמטי".
- A semicolon, and 34 words.
- Loanwords and slang: "סטאק", "ממנפת".

**After:**

> בנינו את שכבת המטמון שלנו כדי שתשתלב במערכת הקיימת שלכם בלי לקשור אתכם לספק אחד. היא משווה בקשות לפי דמיון במשמעות, כדי להפחית החטאות מטמון. החטאות כאלה הן בעיה נפוצה בעומסי עבודה של LLM.

Flavored mode deleted "בצורה חלקה", "מינימום חיכוך", and "באופן דרמטי", because the source gives no measurement for them. If the source has a measured number, put the number in their place. Every other claim stays: the fit with the existing system, no vendor lock-in, comparison by meaning, and fewer cache misses. The purpose wording stays: "כדי" keeps the design intent and does not promise a result.

## How to Read These Examples

Part 1 shows the STE rules carried over to Hebrew. Part 2 shows the same discipline applied to agent output. One meaning per word, active voice, one instruction per sentence, and explicit conditions make Hebrew text safer for an agent and for a human reader.
