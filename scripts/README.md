# QA Script Packs

Ready-to-run QA instruments for the critic. A critic without its instruments does not start.
Each `qa.sh` runs build, then lint/vet, then test, with real exit codes; a missing tool is reported SKIP, never silently passed.

Usage: `bash scripts/<lang>/qa.sh [project-dir]`

## Language packs (12)

- `c/qa.sh`
- `cpp/qa.sh`
- `csharp/qa.sh`
- `flutter/qa.sh`
- `go/qa.sh`
- `java/qa.sh`
- `js/qa.sh`
- `mojo/qa.sh`
- `php/qa.sh`
- `python/qa.sh`
- `rust/qa.sh`
- `swift/qa.sh`

## Shared instruments

- `security/threat-feed.sh`: CISA KEV + OSV refresh, stamps freshness. Run at the START of every security review.
- `security/secret-scan.sh`: gitleaks over full git history, with a trufflehog cross-check. Rotate first, purge second.
- `web/browser-check.sh`: Playwright driver. Boots the app, screenshots every route at desktop, tablet, and phone, logs console errors. Feeds ui-visual-check.

## Pointer folders and duplicated assets

- Pointer folder rule: a folder whose SKILL.md frontmatter carries `pointer-to:` is a pointer, not a skill copy. It holds only SKILL.md, plus LICENSE where the license rule requires it. It holds no references, scripts, or any other file; the canonical copy named by the pointer governs.
- `check_duplicated_assets.py`: publish gate check for duplicated canonical assets and pointer folder contents. A file that shares a basename with a canonical asset passes only when it is byte-identical to the canonical file or is a pointer to it (it carries the pointer marker); anything else fails by name. Run: `python3 scripts/check_duplicated_assets.py [repo-root]`. Exit 1 on any failure, 0 clean.

## Publish and fleet tooling

- `publish-public-mirror.sh`: publishes the redacted public snapshot (see the Publishing section of the root README).
- `sanitize_snapshot.py`: builds the snapshot tree and applies the blocked list and exclusion rules.
- `gitleaks_diff.py` and `gitleaks-baseline.json`: the gitleaks gate and its documented baseline of known example findings.
- `cron/heartbeat.py`: fleet watchdog for the Hermes persona install. This file is excluded from the public snapshot and lives only in the operator's private copy; a public copy will not contain it.

## Proven

- Go pack run against a production Go codebase: build PASS, vet PASS, and it independently reproduced a real test-harness bug the critics had found.
- threat-feed.sh pulled live CISA KEV (catalog 2026.10.23, 1756 entries).
