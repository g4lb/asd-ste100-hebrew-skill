# Contributing

Issues and pull requests are welcome. For a new rule or a change to a rule, open an issue first. Then we can agree on it before you write code.

## Run the checks

The project uses only the Python standard library. Python 3.9 or later works.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ste-lint-he.py --selftest
python3 scripts/ste-lint-he.py --disable synonym-rotation README.md README.he.md SKILL.md CONTRIBUTING.md CHANGELOG.md examples/before-after.md references/writing-rules.md
```

CI runs all three on every push and pull request. All three must pass.

## Add or change a linter rule

1. Add the rule to `RULES` in `scripts/ste-lint-he.py`. Each entry has an ID, a level (`hard` or `advisory`), a compiled pattern, and a message.
2. Add a case to `SELFTEST_CASES`: a bad text that triggers the rule, and a good text that does not.
3. Add a test in `tests/test_ste_lint_he.py` for each false positive you know about. Real Hebrew words that look like a match are the usual source.
4. Update the rule list in `README.md`, `README.he.md`, and `SKILL.md`.

Make a rule `hard` only when a regex can find the problem with very few false positives. Otherwise make it `advisory`.

## Rules that do not change

- The linter never flags hedges (`ייתכן`, `עשוי`, `אולי`, `כנראה`). Confidence is content.
- A rewrite never drops a fact, a condition, or a hedge.
- ASD-STE100 defines English only. Every Hebrew rule here is this project's adaptation. Say so when you add one, and give your source.
- Do not add text from the official ASD-STE100 dictionary. It is not free to redistribute.

## Write docs that pass the linter

The docs follow their own rules. To show a "before" example that is bad on purpose, put it between `<!-- ste-lint: off -->` and `<!-- ste-lint: on -->`. To quote a bad word inside an explanation, put it in backticks.
