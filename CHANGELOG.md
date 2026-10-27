# Changelog

All notable changes to this skill collection are documented in this file.

The format is based on Keep a Changelog (https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [snapshot-2026-10-27-critic-upgrade] - 2026-10-27

Generated from the publish gate diff against snapshot-2026-10-27-github-research:
33 files added, 0 removed, 16 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- commit-gates Mojo gate set (scripts/mojo/: lint, test, debug-add, debug-check).
- The commit-gates scripts library bundled inside personas/critic/scripts/ (28 files, byte-identical to commit-gates/scripts/), re-synced against the library before this publish.
- skills/software-development/critic-lens-code/references/vuln-watch.md, the seeded vulnerability watchlist (2026-10-27).

### Changed

- The critic family moves to the five-critic standard with 1-to-10 scoring, and an owner-correction pass landed during this publish: the standard run is five identical full-spectrum critics on identical briefs, and every lens is a checklist every critic carries (critic and skeptic SOUL.md, persona-skeptic, and the claims, code, compliance, growth, and ux lens skills reframed accordingly). critic-lens-code gains the bundled-scripts checklist, the mandatory vulnerability refresh step, and the prompt injection finding class.
- commit-gates js-ts gates hardened with target-declared tool detection; run-gates.sh dispatches Mojo; SKILL.md language list includes Mojo.
- registry.json and skill-aliases.json regenerated from this tree (304 records, 50 aliases). THIRD-PARTY.md unchanged: A 62, B 161, C 58.

## [snapshot-2026-10-27-github-research] - 2026-10-27

Generated from the publish gate diff against snapshot-2026-10-27-readme:
1 file added, 0 removed, 4 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- skills/github-research/LICENSE (MIT).

### Changed

- skills/github-research now states its MIT license and author (David Patton) in its SKILL.md frontmatter, on the owner's confirmation that the skill is his own work; it was the one unit the licensing fix left undecidable. THIRD-PARTY.md regenerated from this tree: section A grows 61 to 62, section C shrinks 59 to 58. registry.json and skill-aliases.json regenerated from this tree.

## [snapshot-2026-10-27-readme] - 2026-10-27

Generated from the publish gate diff against snapshot-2026-10-27-licensing:
0 files added, 0 removed, 1 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Changed

- README.md rewritten at the top as a consumer front door: what the library is, pin-the-tag install, the three files that run the show (registry.json, collection-router, THIRD-PARTY.md), risk classes, the Section C warning, and the Critic family. The publishing and maintenance sections are kept below. One stale count corrected against the tree: 110 of the 281 skills carry a skill.yaml.

## [snapshot-2026-10-27-licensing] - 2026-10-27

Generated from the publish gate diff against snapshot-2026-10-26-step2c:
16 files added, 1 removed, 27 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- Folder LICENSE files (MIT) for 15 of David Patton's own skills that previously shipped with no license stated.
- skills/golang-web/reference/api-ship-gate.md, carried in from the private tree.

### Changed

- 16 of David's own skills now state their MIT license and author in their frontmatter or skill.yaml: alphaflux-research, android-keyboard, audit_code, deep-research (flat pointer), game-creation, google-business-profiles, local-android-keyboard, local-playwright, meta-leads, playwright, skills/competitor-crawl-pipeline, skills/crawl4ai-competitor-intel, skills/docker-ops, skills/software-development/critic-lens-compliance, social_publishing_rejected_media, youtube.
- THIRD-PARTY.md regenerated from this tree: section A grows 45 to 61, section C shrinks 75 to 59. The remaining Section C units are unchanged and still state no license.
- registry.json and skill-aliases.json regenerated from this tree.

### Removed

- scripts/gitleaks-baseline.json no longer ships; the publish tooling reads the private copy.

## [snapshot-2026-10-26-step2c] - 2026-10-26

Generated from the publish gate diff against snapshot-2026-10-26-step2b:
1 file added, 0 removed, 22 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- scripts/test_research_ledger.py, the regression test proving the research ledger's hop numbering checks fire.
- Sanitizer Gate 1d: a publish now fails when a shipped file references the private credential store filename.

### Fixed

- The research ledger's hop numbering checks were dead code (the writer stores the sequence under one key, the lint read another); lint now reads the written key with the legacy key as fallback.
- The registry generator accepts an explicit source commit only when it is a real 40 hex stamp, and registry record descriptions fall back to the sibling skill.yaml, then to the persona SOUL.md first content line; empty descriptions drop from 135 to 5 on this tree.
- The registry checker warns when the source stamp is not verifiable in the checkout, instead of silently accepting any 40 hex value.
- gitleaks_diff.py exits 2 with a named error on a missing input file, the audit_code runner's no-stack skip fires again, knowledge ingest exits 1 on a failed ingest, and the publish script fails loudly when an existing mirror tag points at a commit other than the one just pushed.
- The two crawl skill bindings no longer name a private credential store file; the desktop projects path convention carries no drive letters, and both wording checkers catch the backslash drive form; the deep-research and critic-lens-claims bindings state the search endpoint by role only, with no hostname.
- The README skill index now lists collection-router, matching its every-flat-skill claim (165 folders, 165 rows on this tree).

## [snapshot-2026-10-26-step2b] - 2026-10-26

Generated from the publish gate diff against snapshot-2026-10-26-step2:
5 files added, 10 removed, 57 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- scripts/check_registry.py, the publish gate that verifies every registry record against the tree it ships in, with scripts/test_registry.py.
- scripts/check_duplicated_assets.py, the gate that canonical assets are byte-identical or pointers.
- Regression tests for the language QA packs and the secret scan (scripts/test_qa_packs.sh, scripts/test_secret_scan.sh), and a fourth sanitizer regression case for generic secret shapes.

### Changed

- Registry and aliases are regenerated from the post-exclusion tree at publish, stamped with the real source commit; risk classification now covers the collection (known map, derivation from each skill's declared description, write default), and the router treats unclassified records as confirmation-required.
- Gate G in the research ledger is a lint error for deep and exhaustive software runs (10 GitHub repo studies with the five per-repo fields), a warning or recorded waiver at standard effort.
- Commit-gates templates: actions pinned to commit SHAs, tool installs pinned and checksum verified, pre-commit revs pinned; run-gates.sh accepts either Python manifest and skips the vulnerability scan in quick mode; the gate list is documented as an accurate per-layer map.
- The license map header discloses that section A membership is inherited and spot-verified; the map was regenerated and gained the subagent-driven-development row it had missed.

### Removed

- deep-research/references/evaluation.md (pointer folders now hold only SKILL.md, plus LICENSE where required).
- The copied research_ledger.py under alphaflux-research, replaced by a pointer shim to the canonical script.

### Fixed

- All 12 language QA packs and scripts/security/secret-scan.sh can now fail: they exit nonzero when their checks find failures.
- README and MANIFEST counts, the SNAPSHOT imported-skill count, sanitizer generic secret shapes, CLI exit codes on missing helpers, gate tooling argv handling, gitleaks baseline fingerprint paths, publish tag reporting, the five curl-piped-to-shell installers, the audit_code eval, and the two MCP manifest surfaces that still described the operator-session credential model.

## [snapshot-2026-10-26-step2] - 2026-10-26

Generated from the publish gate diff against snapshot-2026-10-26:
115 files added, 5 removed, 246 changed. See SNAPSHOT.md for the
full generated record of this snapshot.

### Added

- registry.json and skill-aliases.json, the collection-router skill, and the imported subagent-driven-development skill.
- Router and MCP manifest v2.
- The step 2 gate scripts, including the license map generator and the license integrity check.

### Changed

- Licensing restoration: 48 per-folder LICENSE files restored (46 local-golang, 2 local-appllama), with provenance recorded in skill.yaml.
- Sanitizer hash pinning: the snapshot sanitizer now pins file hashes, with a regression test for the bypass case.
- Registry generation: the registry is now generated rather than hand maintained.
- Wording sweep across the collection, applying the wording standard.

### Removed

- 5 files, including the diverged deep-research duplicates under the pointer folder and the excluded tiny-go-web-tool folder. See SNAPSHOT.md for the full list.

## [snapshot-2026-10-26] - 2026-10-26

### Added

- Initial tracked release: snapshot-2026-10-26 is the first snapshot of the collection recorded in this changelog, with the full skill tree as published at that date.
