# Snapshots

## snapshot-2026-10-26

snapshot-2026-10-26 is the initial tracked snapshot. It predates generated diffs: no earlier tracked snapshot exists to diff it against, so no Added, Removed, Changed, or License-changed lists are generated for it here. It is the baseline every future snapshot diff is measured from.

## Format for future snapshots

Each future snapshot appends a new section to this file, newest first, directly under this format note's position in the file order chosen at that time. Each section is grouped under four headings: Added, Removed, Changed, and License-changed. The contents of each section are generated from the publish gate's known-files diff between the previous snapshot and the new one, not written from memory.

## snapshot-2026-10-26-step2b (2026-10-26)

Generated from the publish gate's known-files diff against snapshot-2026-10-26-step2.
Files in tree: 1,936. Added: 5. Removed: 10. Changed: 57.

### Added

- scripts/check_registry.py and scripts/test_registry.py (the registry gate and its regression tests)
- scripts/check_duplicated_assets.py (the canonical asset gate)
- scripts/test_qa_packs.sh and scripts/test_secret_scan.sh (QA pack and secret scan regression tests)

### Removed

- skills/.hub (9 machine cache files: audit.log, lock files, index caches; the folder is publish-excluded from this snapshot on)
- deep-research/references/evaluation.md (pointer folders now hold only SKILL.md, plus LICENSE where required)

### Changed

57 files changed, covering the critic round 3 fix list: the registry generator (real commit stamps, parsed-structure tag reading, alias hygiene) and the router risk rules; all 12 language QA packs and the secret scan, which now exit nonzero on failures; the research ledger (Gate G enforced as a lint error for deep and exhaustive software runs) and the AlphaFlux ledger pointer shim; commit-gates templates (SHA-pinned actions, checksum-verified installs, real pre-commit revs) and its per-layer gate map; the wording checker scoping and self exemption; README and MANIFEST counts for this tree (110 of 281 skills carry a skill.yaml; 115 SKILL.md under skills/); and the small correctness batch (CLI exit codes, argv validation, baseline fingerprint paths, publish tag reporting, download-inspect-run installers, the audit_code eval removed, and the two MCP manifest surfaces that still described the operator-session credential model, rewritten per principal). THIRD-PARTY.md regenerated from this tree: A 45, B 161, C 75, with the header now disclosing that section A membership is inherited and spot-verified.

### License-changed

- None. Counts on this tree are unchanged from snapshot-2026-10-26-step2 (A 45, B 161, C 75).

### Gate results for this snapshot

- Sanitizer gate: exit 0. Gate 1 clean (no blocked identifiers), gate 1c clean (no duplicate skill names, no dangling excluded-path references). Generic secret shapes (AWS key id, GitHub token prefixes, PEM private key headers) are now scanned; baseline hits only in hash-matched, previously published files.
- Sanitizer regression test: PASS, 4 of 4 cases, including the new AWS-shaped key case.
- Registry gate (scripts/check_registry.py): clean. 304 records (228 canonical skills, 23 personas, 3 pointers, 50 duplicates), 50 aliases, generated_from_commit 21d669ef42526461803011e81fbffba938546cc1, the private source commit. Zero records for publish-excluded units; zero read-by-default risk records.
- License integrity check: clean, 281 skill folders checked.
- Duplicated assets gate: clean.
- Gitleaks: 6 findings, all in the documented baseline. Gate 2 clean.
- QA pack regression test and secret scan regression test: PASS.

## snapshot-2026-10-26-step2 (2026-10-26)

Generated from the publish gate's known-files diff against snapshot-2026-10-26.
Files in tree: 1,941. Added: 115. Removed: 5. Changed: 246.

### Added

The step 0e and step 2 additions: registry.json and skill-aliases.json, the
collection-router skill, CHANGELOG.md and SNAPSHOT.md, LICENSES/MIT.txt,
48 restored per-folder LICENSE files (46 local-golang, 2 local-appllama),
the imported subagent-driven-development skill (16 files), the GitHub skill's
new references and scripts from step 0e, and the step 2 gate scripts
(generate_license_map.py, check_license_integrity.py, test_sanitize_snapshot.py,
check-linter-count.py, gh-landscape.py, fetch-or-transcribe.sh).

### Removed

- deep-research/references/skeptic-probe.md and deep-research/scripts/research_ledger.py (diverged duplicates under the pointer folder; canonical copies live in skills/deep-research/)
- skills/.curator_ledger.jsonl (machine ledger, excluded)
- tiny-go-web-tool/SKILL.md and tiny-go-web-tool/skill.yaml (folder excluded from publish starting this snapshot; its machine-specific lines moved to a labeled local binding in the private repo)

### Changed

246 files changed, including all six step 2 workstreams: licensing provenance
in 48 skill.yaml files, the sanitizer and publish tooling, the dangling
reference sweep, the content repairs (Swiss tables, lint counts, frontmatter
repairs), the wording sweep across 52 files, and the persona seam fixes
across 41 files. One credential-shaped example value in a Hermes MCP config
example was replaced with an obvious placeholder during this publish.

### License-changed

- 46 local-golang folders: no license on file to MIT (upstream LICENSE restored verbatim, provenance recorded in skill.yaml). Section C to section B in THIRD-PARTY.md.
- local-appllama-app-design-skill and local-appllama-usage: no license on file to MIT (LICENSE restored from the canonical copies). Section C to section B.
- THIRD-PARTY.md is now generated from the post-exclusion tree at publish: this snapshot reads A 45, B 161, C 75.

### Gate results for this snapshot

- Sanitizer gate: exit 0. Gate 1 clean (no blocked identifiers), gate 1c clean (no duplicate skill names, no dangling excluded-path references). Baseline generic hits only in hash-matched, previously published files.
- Regression test for the hash pinning (the round 2 U1 bypass case): PASS, 3 of 3 cases.
- Gitleaks: 6 findings, all in the documented baseline. Gate 2 clean.
- License integrity check: clean, 281 skill folders checked.
- Registry: regenerated, 320 records (242 canonical skills, 23 personas, 3 pointers, 52 duplicates), 55 aliases.
