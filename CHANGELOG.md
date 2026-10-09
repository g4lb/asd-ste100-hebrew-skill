# Changelog

All notable changes to this project are in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- The linter skips text between `<!-- ste-lint: off -->` and `<!-- ste-lint: on -->`, and skips YAML front matter.
- CI lints the docs, so they keep following their own rules.
- `CONTRIBUTING.md` and this changelog.

### Fixed

- A sentence that ends before closing markup (`**`, `*`, `)`, `"`) now counts as a separate sentence.
- Bare punctuation no longer counts as a word, and a code span counts as one word.
- The docs now pass the linter. "Before" examples that are bad on purpose are marked to be skipped.

## [0.1.0] - 2026-10-09

### Added

- First public release: the `asd-ste100-hebrew` skill (`SKILL.md`, writing rules, examples) and the standard-library linter `scripts/ste-lint-he.py`.

[Unreleased]: https://github.com/g4lb/asd-ste100-hebrew-skill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/g4lb/asd-ste100-hebrew-skill/releases/tag/v0.1.0
