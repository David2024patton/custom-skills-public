---
name: exec-scripts
description: "Use to run build/test/lint/browser/threat-feed commands."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [scripts, execution, build, test, lint, threat-feed, automation]
    related_skills: [persona-skeptic, critic-lens-code, golang, flutter, rust, mojo, alpha-infra]
---

# Exec Scripts: The Critic's Instruments

## When to Use

A critic loads this before review so execution is one command, not a guess. A critic without its instruments does not start. Every command runs for real and its exit code and output are captured; a command the critic did not run is not evidence.

## Go stack

One command runs the whole gate: `scripts/go-qa.sh [pkg]` (default `./...`). It sequences the steps below, prints PASS/FAIL/UNTESTED per step with real exit codes, and exits non-zero on any required failure. Run it rather than the individual commands when the stack is Go.

- Build: `go build ./...`
- Vet: `go vet ./...`
- Lint: `golangci-lint run` (or the repo's configured linter)
- Test with race: `go test ./... -race -count=1`
- Coverage on the file under review: `go test ./... -run <TestName> -v`
- Tidy check: `go mod tidy` then `git diff --exit-code go.mod go.sum`

## Flutter / Dart stack

- Analyze: `flutter analyze` (treat info-level as findings to triage)
- Test: `flutter test`
- Build web: `flutter build web` (and check the bundle has no runtime CDN fetch)
- Format check: `dart format --output=none --set-exit-if-changed .`

## Rust stack

- Build: `cargo build`
- Clippy: `cargo clippy -- -D warnings`
- Test: `cargo test`

## Mojo / GPU stack

- Build/run the kernel or example in `mojo` skill's `examples/`.
- Verify against `resources/max_cheatsheet.md` for the SDK version in use.

## Web app visual check

- Boot the server, then drive a browser: navigate every route, click every
  control, screenshot every state to the report folder, capture console and
  network logs. See `ui-visual-check` for the full checklist.

## Threat feed refresh (security reviews)

- CISA KEV: `curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
- NVD recency: query NVD for the run date; note last-modified.
- OSV per dependency: `osv-scanner` against the committed lockfile, or the
  OSV batch API.
- Stamp feed freshness (catalog version, last-modified) into the report
  header. A clean scan on stale feeds is provisional and says so.

## Secret scan (history, not just working tree)

- `gitleaks detect --source . --log-opts="--all"` (full history), plus a
  second engine (trufflehog) as cross-check.

## Rules

- Capture real exit codes and raw trailing output, never a paraphrase.
- Re-run any delegated agent's command yourself before trusting its summary.
- If a tool is missing for the stack, say so and mark that checklist item
  UNTESTED rather than skipping it silently.
- Scripts are per-stack and live with the language skills; this skill is the
  index the critic reads to know what to run.
