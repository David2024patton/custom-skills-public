# Snapshots

## snapshot-2026-10-26

snapshot-2026-10-26 is the initial tracked snapshot. It predates generated diffs: no earlier tracked snapshot exists to diff it against, so no Added, Removed, Changed, or License-changed lists are generated for it here. It is the baseline every future snapshot diff is measured from.

## Format for future snapshots

Each future snapshot appends a new section to this file, newest first, directly under this format note's position in the file order chosen at that time. Each section is grouped under four headings: Added, Removed, Changed, and License-changed. The contents of each section are generated from the publish gate's known-files diff between the previous snapshot and the new one, not written from memory.

## snapshot-2026-10-27-critic-upgrade (2026-10-27)

Generated from the publish gate's known-files diff against snapshot-2026-10-27-github-research.
Files in tree: 1,986. Added: 33. Removed: 0. Changed: 16 (commit-gates/SKILL.md, commit-gates/scripts/js-ts/debug-add.sh, commit-gates/scripts/js-ts/debug-check.sh, commit-gates/scripts/js-ts/lint.sh, commit-gates/scripts/js-ts/test.sh, commit-gates/scripts/run-gates.sh, personas/critic/SOUL.md, personas/skeptic/SOUL.md, registry.json, skill-aliases.json, skills/software-development/critic-lens-claims/SKILL.md, skills/software-development/critic-lens-code/SKILL.md, skills/software-development/critic-lens-compliance/SKILL.md, skills/software-development/critic-lens-growth/SKILL.md, skills/software-development/critic-lens-ux/SKILL.md, skills/software-development/persona-skeptic/SKILL.md).
Source mapping: this snapshot is generated from the private repo at commit 26fc3942c6ac130a79c37415457e857441f1d753 (the critic upgrade registry commit after the owner-correction pass), which is also the registry stamp generated_from_commit. The one private commit after it touches only SNAPSHOT.md and CHANGELOG.md; it corrects the assembly record first drafted at 6adb486488eb62d8d277b9152f87fe46f7bd87d9, before the owner-correction pass landed. This section and the matching CHANGELOG.md entry are the assembly record and are not counted in the diff above.

### Added

- commit-gates/scripts/mojo/ (4 files: lint.sh, test.sh, debug-add.sh, debug-check.sh): the Mojo gate set, pattern-copied from the Go and Rust sets (format check via temp-copy diff, compile check via mojo build with debug info, no dedicated Mojo linter exists and the scripts say so).
- personas/critic/scripts/ (28 files): the commit-gates scripts library bundled inside the critic persona (common/, dart-flutter/, go/, js-ts/, mojo/, python/, rust/, shell/, run-gates.sh), byte-identical to commit-gates/scripts/ in this same tree, so the critic carries its gates with it. The bundle was re-synced against the library at private commit 5de24bc262ed7c8ca8490fd1096dca0d7031120e before this publish (five files had predated the js-ts hardening and Mojo wiring).
- skills/software-development/critic-lens-code/references/vuln-watch.md: the seeded vulnerability watchlist (seed date 2026-10-27, two items, each with named sources and a verified date; the file states it is a seed snapshot, not a live feed, and every critic refreshes it by live research before any scan).

### Removed

- None.

### Changed

- The critic protocol is now the five-critic standard with 1-to-10 scoring, replacing the three-critic, 0-to-100 form. personas/critic/SOUL.md carries the protocol with whole-repo ingestion as step zero; personas/skeptic/SOUL.md and skills/software-development/persona-skeptic/SKILL.md are synced to the same standard.
- Owner-correction pass (private commits b18a4359, 377fcba6, 61e5990f, landed during this publish): the standard run is five identical full-spectrum critics on identical briefs, not five differently-briefed critics; every lens is a checklist every critic carries. personas/critic/SOUL.md and personas/skeptic/SOUL.md state the identical-run standard, and the lens skills (critic-lens-claims, critic-lens-code, critic-lens-compliance, critic-lens-growth, critic-lens-ux) are reframed accordingly: When-to-Use written for every critic, the code lens checklists A and A1 and the vuln-watch refresh applying to every critic in a run, and the compliance lens rewritten for consensus fit.
- skills/software-development/critic-lens-code/SKILL.md: the bundled-scripts checklist, the mandatory vulnerability refresh step, and the prompt injection finding class.
- commit-gates/SKILL.md: language list now includes Mojo.
- commit-gates/scripts/js-ts/ (4 files): hardened with target-declared tool detection (project lint and typecheck scripts used when declared, TypeScript checks only when a tsconfig or the typescript dependency is declared, nested tsconfigs typechecked, debug source roots detected, diag.js or diag.ts pattern by repo language).
- commit-gates/scripts/run-gates.sh: Mojo dispatched when a .mojo file or mojoproject.toml is present.
- registry.json and skill-aliases.json regenerated from this tree (304 records, 50 aliases); the records whose checksums moved are critic, critic-lens-claims, critic-lens-code, critic-lens-compliance, critic-lens-growth, critic-lens-ux, persona-skeptic, and skeptic, checksum changes only.

### License-changed

- None. THIRD-PARTY.md is byte-identical to the previous snapshot: section A 62, section B 161, section C 58. No skill was added to or removed from the collection; the critic lenses and commit-gates were already registry units, and the bundled scripts live inside the existing personas/critic unit.

### Gate results for this snapshot

- Sanitizer gate: exit 0. Gate 1 clean (no blocked identifiers), gate 1c clean (no duplicate skill names, no dangling excluded-path references), gate 1d clean (no reference to the private credential store filename). 33 new files human-reviewed and approved: the 4 Mojo gate scripts, the 28 bundled gate scripts (verified byte-identical to commit-gates/scripts/ in this tree), and the vulnerability watchlist (read in full). Registry and license map were regenerated from the final post-scrub staging, so shipped checksums verify against shipped bytes.
- Sanitizer regression test: PASS, 5 of 5 cases. Registry generator tests: PASS, 7 of 7. Ledger regression test: PASS, 3 of 3. QA pack regression test and secret scan regression test: PASS.
- Registry gate (scripts/check_registry.py): clean. 304 records (228 canonical skills, 23 personas, 3 pointers, 50 duplicates), 50 aliases, generated_from_commit 26fc3942c6ac130a79c37415457e857441f1d753, the private source commit.
- License integrity check: clean, 281 skill folders checked.
- Duplicated assets gate: clean.
- Gitleaks: 6 findings, all in the documented baseline. Gate 2 clean.

## snapshot-2026-10-27-github-research (2026-10-27)

Generated from the publish gate's known-files diff against snapshot-2026-10-27-readme.
Files in tree: 1,953. Added: 1. Removed: 0. Changed: 4 (THIRD-PARTY.md, registry.json, skill-aliases.json, skills/github-research/SKILL.md).
Source mapping: this snapshot is generated from the private repo at commit fdff45e3f59ce58c45aa351877cb9b4c44b1da51 (the github-research licensing registry commit), which is also the registry stamp generated_from_commit. The one private commit after it touches only SNAPSHOT.md and CHANGELOG.md. This section and the matching CHANGELOG.md entry are the assembly record and are not counted in the diff above.

### Added

- skills/github-research/LICENSE (MIT, Copyright (c) David Patton, copied verbatim from the collection's sibling template).

### Removed

- None.

### Changed

- skills/github-research/SKILL.md: frontmatter now states author David Patton and license MIT.
- THIRD-PARTY.md, registry.json, and skill-aliases.json regenerated from this tree.

### License-changed

- skills/github-research moves from Section C to Section A. The licensing fix's provenance pass had left this unit undecidable (its author field was deferred: "needs owner confirmation, license not invented"); David Patton confirmed on 2026-10-27 that the skill is his own work, and it is licensed MIT with author David Patton, the same pattern as the 16 units licensed in snapshot-2026-10-27-licensing. Section counts on this tree: A 61 to 62, B 161 unchanged, C 59 to 58. The remaining Section C units (the 55 platform bundled skills, plus skills/golang, skills/golang-pro, and skills/golang-web) are unchanged in content and status: no license stated, not cleared for redistribution.

## snapshot-2026-10-27-readme (2026-10-27)

Generated from the publish gate's known-files diff against snapshot-2026-10-27-licensing.
Files in tree: 1,952. Added: 0. Removed: 0. Changed: 1 (README.md).
Source mapping: this snapshot is generated from the private repo at commit 852250b2d59069f383baec73133afe9da98b52d5 (the README front door commit), which changes no registry input; the registry stamp stays generated_from_commit 68a6aa2950fe8fd608a8ccf66479f96ddbee5891. The one private commit after it touches only SNAPSHOT.md and CHANGELOG.md. This section and the matching CHANGELOG.md entry are the assembly record and are not counted in the diff above.

### Added

- None.

### Removed

- None.

### Changed

- README.md: the top of the README is now a consumer front door (what the library is, pin-the-tag install, the three files that run the show, risk classes, the Section C warning, and the Critic family), with the publishing and maintenance sections kept below it. One stale count was corrected against this tree: 110 of the 281 skills carry a skill.yaml.

### License-changed

- None. THIRD-PARTY.md is unchanged: section A 61, section B 161, section C 59.

## snapshot-2026-10-27-licensing (2026-10-27)

Generated from the publish gate's known-files diff against snapshot-2026-10-26-step2c.
Files in tree: 1,952. Added: 16. Removed: 1. Changed: 27.
Source mapping: this snapshot is generated from the private repo at commit 68a6aa2950fe8fd608a8ccf66479f96ddbee5891 (the licensing fix registry commit), which is also the registry stamp generated_from_commit. The one private commit after it touches only SNAPSHOT.md and CHANGELOG.md and changes no registry input. This snapshot also carries the private commits landed after step 2c (through 722508e8) that had not been published before; their shipped effect is inside the counts above.

### Added

- 15 folder LICENSE files for the newly licensed units listed under License-changed.
- skills/golang-web/reference/api-ship-gate.md (from the private tree's post-step2c commits).

### Removed

- scripts/gitleaks-baseline.json (the private repo no longer ships it; the publish gates keep reading the private copy).

### Changed

27 files: the metadata file of each of the 16 licensed units (author and license now stated); THIRD-PARTY.md, registry.json, and skill-aliases.json regenerated from this tree; README.md and MANIFEST.md pruned of stale lines by the sanitizer; .gitignore; and the post-step2c private updates to scripts/build-registry.py, scripts/publish-public-mirror.sh, scripts/sanitize_snapshot.py, skills/golang-web/SKILL.md, and skills/persona-sdlc-tester/SKILL.md, in their sanitized forms.

### License-changed

David's order (2026-10-27): put the proper licensing on the Section C units that are his own work. A provenance pass over all 75 Section C units (evidence: diffs against the Muse bundled skills and against David's working set, authorship markers, commit history, and the program research record; full record kept in the private program folder) classified 55 as platform bundled skills, 16 as David's own, and 4 as unknown or third-party with no license stated. The 16 David units now state MIT with their author, and carry a folder LICENSE where the sibling pattern has one:

- Author David Patton (12): android-keyboard, audit_code, game-creation, google-business-profiles, local-android-keyboard, local-playwright, meta-leads, playwright, skills/competitor-crawl-pipeline, skills/crawl4ai-competitor-intel, social_publishing_rejected_media, youtube.
- Author Hermes Agent for David Patton (4): alphaflux-research, deep-research (the flat pointer, frontmatter only, no LICENSE file), skills/docker-ops, skills/software-development/critic-lens-compliance.

Section counts on this tree: A 45 to 61, B 161 unchanged, C 75 to 59. The 59 remaining Section C units (the 55 platform bundled skills, plus skills/golang, skills/golang-pro, skills/golang-web, and skills/github-research) are unchanged in content and status: no license stated, not cleared for redistribution. No license was invented for any unit.

### Gate results for this snapshot

- Sanitizer gate: exit 0. Gate 1 clean (no blocked identifiers), gate 1c clean (no duplicate skill names, no dangling excluded-path references), gate 1d clean (no reference to the private credential store filename). 16 new files human-reviewed and approved: the 15 LICENSE files verified byte-identical to the sibling templates they copy, and skills/golang-web/reference/api-ship-gate.md read in full. Inline scrubs applied to staging copies of files carried in from the private tree's post-step2c commits; README.md pruned 15 stale lines, MANIFEST.md pruned 3.
- Sanitizer regression test: PASS, 5 of 5 cases.
- Registry gate (scripts/check_registry.py): clean. 304 records (228 canonical skills, 23 personas, 3 pointers, 50 duplicates), 50 aliases, generated_from_commit 68a6aa2950fe8fd608a8ccf66479f96ddbee5891, the private source commit.
- Registry generator tests: PASS, 7 of 7. Ledger regression test: PASS, 3 of 3.
- License integrity check: clean, 281 skill folders checked.
- Duplicated assets gate: clean.
- Gitleaks: 6 findings, all in the documented baseline. Gate 2 clean.

## snapshot-2026-10-26-step2c (2026-10-26)

Generated from the publish gate's known-files diff against snapshot-2026-10-26-step2b.
Files in tree: 1,937. Added: 1. Removed: 0. Changed: 22.
Source mapping: this snapshot is generated from the private repo at the step 2c assembly commits. The registry stamp generated_from_commit b0ea2dd92f582ad15fca5e0db64896c981dd00a8 is the private source commit the registry was generated from (step 2c assembly 1); the one private commit after it touches only SNAPSHOT.md and CHANGELOG.md and changes no registry input.

### Added

- scripts/test_research_ledger.py (regression test for the ledger hop numbering checks)

### Removed

- None.

### Changed

22 files changed, covering the critic round 3b fix list (one Medium, eleven Low, all lone wolf findings): the research ledger lint now reads the hop key its writer writes, with a regression test; the registry generator validates an explicit source commit value and fills record descriptions from the sibling skill.yaml or the persona SOUL.md first content line (empty descriptions on this tree drop from 135 to 5); the registry checker warns, never fails, when the source stamp is not verifiable in the checkout; gitleaks_diff.py reports a missing input file as a clean exit 2 error; the audit_code runner's empty-stack skip fires again; knowledge ingest exits 1 on failure; the publish script refuses to report success when an existing mirror tag points at a different commit than the one just pushed; the two crawl skill bindings are values-free and a new sanitizer Gate 1d fails any future reference to the private credential store filename in a shipped file; the desktop projects path convention is genericized and both wording checkers now catch backslash drive paths; the deep-research and critic-lens-claims bindings state the search endpoint by role only, with no hostname; and the README skill index gains the collection-router row its completeness claim requires. THIRD-PARTY.md regenerated from this tree, byte-identical to the previous snapshot (A 45, B 161, C 75).

### License-changed

- None. Counts on this tree are unchanged from snapshot-2026-10-26-step2b (A 45, B 161, C 75).

### Gate results for this snapshot

- Sanitizer gate: exit 0. Gate 1 clean (no blocked identifiers), gate 1c clean (no duplicate skill names, no dangling excluded-path references), gate 1d clean (no reference to the private credential store filename). One new file human-reviewed and approved (scripts/test_research_ledger.py).
- Sanitizer regression test: PASS, 5 of 5 cases, including the new Gate 1d credential filename case.
- Registry gate (scripts/check_registry.py): clean. 304 records (228 canonical skills, 23 personas, 3 pointers, 50 duplicates), 50 aliases, generated_from_commit b0ea2dd92f582ad15fca5e0db64896c981dd00a8, the private source commit. Zero records for publish-excluded units; zero read-by-default risk records; 5 records carry an empty description (two canonical skills with no description source, three pointer records), down from 135.
- Registry generator tests: PASS, 7 of 7, including the bad source commit refusal case.
- Ledger regression test (scripts/test_research_ledger.py): PASS, 3 of 3 (duplicate hop numbers fail, a numbering gap fails, a CLI-built ledger lints clean).
- License integrity check: clean, 281 skill folders checked.
- Duplicated assets gate: clean.
- Gitleaks: 6 findings, all in the documented baseline. Gate 2 clean.
- QA pack regression test and secret scan regression test: PASS.

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
