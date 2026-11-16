#!/usr/bin/env python3
"""Build plugin/, the copy of the skill for Anthropic's plugin directory.

The directory accepts code files only from Verified organizations, so plugin/
holds the skill without the linter: Markdown, JSON, the license, and the icon.
The root of the repository stays the source. Edit the root files, then run:

    python3 scripts/build-plugin.py          # write plugin/
    python3 scripts/build-plugin.py --check  # exit 1 if plugin/ is out of date
"""

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "plugin"
SKILL = "skills/asd-ste100-hebrew"
REPO = "`g4lb/asd-ste100-hebrew-skill`"

# (source, destination in plugin/, [(old, new), ...]). Each old string must
# occur exactly once, so a change in the source fails the build loudly.
FILES = [
    (".claude-plugin/plugin.json", ".claude-plugin/plugin.json", []),
    (".claude-plugin/icon.png", ".claude-plugin/icon.png", []),
    ("LICENSE", "LICENSE", []),
    (
        "SKILL.md",
        f"{SKILL}/SKILL.md",
        [
            (
                "For a mechanical first pass, run `python3 <this skill's directory>/scripts/ste-lint-he.py` (files or stdin, `--json` for structured output). It checks semicolons, sentence length, nominalization, marketing words, prefix hyphens, slang, synonym rotation, and dangling conjunctions in lists. Its advisory findings are passive voice, abbreviations, and ש- chains. `לבצע` before a word that is not a listed action noun is also advisory. It never flags hedges. It cannot check construct chains, homographs, the impersonal plural, dropped `את`, or the infinitive rule. Check those by hand.",
                "Check every rule by hand.",
            ),
            (
                "- **`scripts/ste-lint-he.py`**: a deterministic linter that uses only the Python standard library. Exit 1 when hard violations exceed `--baseline` (default 0). Advisory findings never fail the run. `--disable` silences named rules. `--selftest` asserts that `ייתכן שהבקשה נכשלה` passes clean. For Flavored text (READMEs, prose), add `--disable synonym-rotation`. In that mode synonym rotation is advisory, but the linter treats it as hard. The linter skips code, YAML front matter, and text between `<!-- ste-lint: off -->` and `<!-- ste-lint: on -->`.",
                f"- **Linter**: the GitHub repository {REPO} has `scripts/ste-lint-he.py`. It checks the rules that a regex can find. This plugin does not include it.",
            ),
        ],
    ),
    (
        "references/writing-rules.md",
        f"{SKILL}/references/writing-rules.md",
        [
            (
                "`scripts/ste-lint-he.py` checks only patterns that a regex can find:",
                f"The linter is `scripts/ste-lint-he.py` in the GitHub repository {REPO}. This plugin does not include it. It checks only patterns that a regex can find:",
            ),
        ],
    ),
    ("examples/before-after.md", f"{SKILL}/examples/before-after.md", []),
]

README = f"""# Simplified Technical Hebrew (ASD-STE100) plugin

This folder is the plugin for Anthropic's plugin directory. The script `scripts/build-plugin.py` makes it from the files at the root of the repository. Do not edit this folder by hand.

This plugin does not include the linter `scripts/ste-lint-he.py`. The plugin directory accepts code files only from Verified organizations. To get the skill with the linter, install it from the root of the repository {REPO}.
"""


def build(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    for src, dst, edits in FILES:
        target = out / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        if not edits:
            shutil.copyfile(ROOT / src, target)
            continue
        text = (ROOT / src).read_text(encoding="utf-8")
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                sys.exit(f"{src}: expected 1 match, found {count}: {old[:60]}...")
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
    (out / "README.md").write_text(README, encoding="utf-8")


def snapshot(folder: Path) -> dict:
    return {
        p.relative_to(folder).as_posix(): p.read_bytes()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


def main() -> None:
    if "--check" in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "plugin"
            build(fresh)
            if not OUT.exists() or snapshot(fresh) != snapshot(OUT):
                sys.exit("plugin/ is out of date. Run: python3 scripts/build-plugin.py")
        print("plugin/ is up to date.")
        return
    build(OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
