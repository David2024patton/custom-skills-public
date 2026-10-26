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

## Publish and fleet tooling

- `publish-public-mirror.sh`: publishes the redacted public snapshot (see the Publishing section of the root README).
- `sanitize_snapshot.py`: builds the snapshot tree and applies the blocked list and exclusion rules.
- `gitleaks_diff.py` and `gitleaks-baseline.json`: the gitleaks gate and its documented baseline of known example findings.
- `cron/heartbeat.py`: fleet watchdog for the Hermes persona install.

## Proven

- Go pack run against a production Go codebase: build PASS, vet PASS, and it independently reproduced a real test-harness bug the critics had found.
- threat-feed.sh pulled live CISA KEV (catalog 2026.10.23, 1756 entries).
