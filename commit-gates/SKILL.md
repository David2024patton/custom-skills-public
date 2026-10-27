---
name: commit-gates
description: "Commit Gates: nothing lands on red (David Patton). Debugging, linting, testing, and security gates for every commit."
version: 1.0.0
author: David Patton
license: MIT
platforms: [linux, macos, windows]
---

# Commit Gates: nothing lands on red (David Patton)

Linked from the github-repo-standard skill. This skill owns everything
about proving code before it commits: debugging built in, linting clean,
tests passing, security checked. The github-repo-standard skill defers
to this one for all gate questions.

## The law

- No commit, push, or merge happens while any applicable gate is red.
  A failing gate is fixed or the work is honestly reverted; it is never
  committed broken and never skipped silently.
- Every module in every project, any language, ships with BOTH debugging
  and linting built in from birth. They are not the same thing:
  - Linting reads the code for mistakes without running it.
  - Debugging is finding out why the program misbehaved when it ran,
    backed by diagnostics built into the module: structured logs, a
    diagnostic channel every refusal and verdict flows through, and a
    way to pull the bug information out.
- A module that cannot say what it did and why it refused, or that has
  no lint gate, is not done.
- Tests assert values, not mere survival. A test that cannot fail is not
  a test.
- Emulation-proven is not bench-proven; gate output states which.

## The gate set

These are the gates this skill names. The per-layer map below says,
for each one, which layers actually execute it. No layer runs a gate
that the map does not list for that layer.

1. Format check for the languages present. Status: manual, not
   scripted as a standalone gate. There is no standalone format gate
   in run-gates.sh or in any template. Some per-language lint scripts
   include a format check inside the lint gate: Go (gofmt list), Rust
   (cargo fmt --check), Dart/Flutter (dart format check), and Python
   (ruff format --check, only when ruff is the linter that runs). The
   JS/TS and shell lint scripts include no format check.
2. Lint clean (warnings are failures), via the per-language lint
   scripts. A lint script that finds no lint configured for the
   project says so out loud: it prints "NO LINT CONFIGURED: lint gate
   not enforced for this project" and still exits 0 for that part.
   That is the case for JS/TS with no lint script in package.json,
   for Go with no golangci-lint config file, and for Dart/Flutter
   with no analysis_options.yaml.
3. Unit tests pass; race detector where the language supports it
   (the Go test script runs go test -race).
4. Debug check: the module has its diagnostic seam (see scripts).
5. Secret scan: betterleaks (preferred) or gitleaks over the tree; any
   hit stops the commit. No passwords, keys, or tokens in the repo,
   ever; credentials live in secure storage only. The scan script
   exits 2 when no scanner is installed, and run-gates.sh turns that
   into a red gate, so a machine or runner with no scanner fails
   instead of passing silently.
6. Vulnerability scan: the common script runs osv-scanner where
   installed, plus the native tool for an ecosystem present
   (govulncheck for Go, cargo audit for Rust, npm audit for JS/TS;
   there is no pip-audit step in the Python scripts). Known
   vulnerability data comes from osv.dev; check it before adding any
   dependency. The scan script exits 2 when no scanner ran at all.
7. Fuzz targets exist for untrusted-input parsers. Status: manual,
   not scripted. No script in this library checks for fuzz targets
   and no template runs one; a repo that parses external data adds
   its own fuzz targets and its own CI for them (the ClusterFuzzLite
   pattern is the suggested shape, named here as guidance only).
8. Commit message gate: commit messages follow the shipped config in
   templates/commitlint.config.js (Conventional Commits based
   config-conventional, extended with the repo standard's needs),
   enforced by commitlint (or an equivalent parser) in the commit-msg
   hook and re-checked in CI over the PR commit range. run-gates.sh
   does not check commit messages.

## Enforcement layers: the per-layer map

The layers do not all run the same gate set. The shared piece is the
entry point: the hook templates and the CI template both call
scripts/run-gates.sh (or the repo-local gate script where one
exists), but at different stages and with different flags, and each
layer adds steps of its own.

### scripts/run-gates.sh, no flags (the full form)

- Detects languages from marker files: go.mod (Go), Cargo.toml
  (Rust), pubspec.yaml (Dart/Flutter), package.json (JS/TS), either
  pyproject.toml or requirements.txt (Python), and any .sh file
  (shell).
- For each detected language except shell: that language's lint
  script, debug check script, and test script. For shell: the lint
  script only (there is no shell debug check or test script).
- Common scans: the secret scan, then the vulnerability scan.
- Does not run: a standalone format gate (format checks ride inside
  some lint scripts, per gate 1), fuzz targets, commit message form,
  or actionlint.

### scripts/run-gates.sh --quick (the commit-stage form)

- Same language detection and the same lint and debug check scripts
  as the full form.
- Skips the test scripts and skips the vulnerability scan.
- The secret scan still runs. A commit-stage result therefore says
  nothing about tests or known vulnerabilities.

### templates/.pre-commit-config.yaml (pre-commit framework)

- Commit stage: one local hook running run-gates.sh --quick (lint,
  debug check, secret scan; no tests, no vulnerability scan), plus
  the external gitleaks hook at the commit stage.
- Commit-msg stage: commitlint with the shipped config.
- Push stage: one local hook running run-gates.sh with no flags
  (lint, debug check, tests, secret scan, vulnerability scan).
- Its one external hook repo is gitleaks, pinned to rev v8.30.1.
  The local hooks carry no revision; they call the vendored scripts
  library in the repo.

### templates/lefthook.yml (Lefthook)

- Pre-commit: run-gates.sh --quick (lint, debug check, secret scan;
  no tests, no vulnerability scan), plus the common secret scan
  script again on its own.
- Commit-msg: commitlint with the shipped config.
- Pre-push: run-gates.sh with no flags (lint, debug check, tests,
  secret scan, vulnerability scan).
- Lefthook itself is installed per repo; this template pins no tool
  versions.

### templates/.github/workflows/gates.yml (CI)

- Job actionlint: checks out the repo, installs actionlint 1.7.12
  from its pinned release download, verified against the sha256
  checksums file published with that release, and lints the workflow
  files. It runs no code gates.
- Job gates: checks out the repo, installs the two common-scan tools
  run-gates.sh needs at pinned versions with release checksum
  verification (gitleaks 8.30.1 and osv-scanner 2.7.0), then runs
  run-gates.sh with no flags, whole-tree. That is lint, debug check,
  and tests per detected language, plus the secret scan and the
  vulnerability scan. Per-language tools (the Go, Rust, Flutter,
  Node, and Python toolchains and their linters) are not installed
  by this template; a repo adds the setup steps for the languages it
  uses, and a language whose toolchain is missing fails its scripts
  instead of passing.
- Job commit messages, pull requests only: checks out the PR with
  full history, sets up Node, installs commitlint from npm (not
  version pinned in this template), and checks commit message form
  over the PR commit range with the shipped config.
- CI does not run: fuzz targets, or a standalone format gate.
- On every pull request and every push to the default branch, this
  workflow is the proof layer: its results are checked on a machine
  the author does not control, unlike a local hook result.

### Branch protection

Branch protection runs no gates. It is the enforcement: requiring
the CI checks on the default branch is what makes a red gate block
a merge. Without branch protection, CI is only a report and nothing
is enforced. Local hooks are bypassable by design (a skip flag or a
missing install defeats them), so a hook result is fast feedback,
never proof; a result from the local layer alone is reported as
local only.

The trigger layer that makes the gates run uninvited ships in
templates/: templates/.pre-commit-config.yaml (the pre-commit
framework config, wiring the scripts library by stage; its one
external hook, gitleaks, is pinned to rev v8.30.1),
templates/lefthook.yml (the sanctioned alternative config, for repos
that run Lefthook instead), templates/commitlint.config.js (the
commit message gate config), and templates/.github/workflows/
gates.yml (the CI workflow). The scripts library is what runs; the
templates are what makes it run uninvited. Copy the templates into
the repo; do not rewrite them per repo beyond the paths and pins
their headers name.

Two gates are hook-first as their first check, because CI is too
late for both:

- Commit message form: the message is fixed at commit time, so the
  commit-msg hook is the only place it can be corrected before it
  lands. CI re-checks the PR range as proof, after the fact.
- Secret scanning: a secret that reaches history is already leaked
  when CI catches it, so the first scan runs in the commit stage
  hook, before the commit exists.

## Security standing rules

- Bounded parsers for untrusted input; no unbounded waits, spins, or
  stores anywhere (config caps with defaults, never compiled constants).
- Dependencies: check the shelf first (google-org-harvest USE-IT.md),
  prefer maintained and license-clean, pin versions, scan before merge.
- Multi-tenant code gets a tenancy sweep: every query scoped, every
  cross-tenant path refused and logged through the diag channel.
- Auth and approval paths fail closed.

## The scripts library

scripts/ is organized by coding language. Each folder holds that
language's ready-to-fire scripts: lint, tests, debug check, and debug
scaffold. Every script carries its instructions in its own header: what
it does, what to modify per project, usage, exit codes. An agent loads
only the folder for the language it is working in, which keeps standing
instructions small. scripts/run-gates.sh detects the languages present
in a repo and runs the matching folders plus the common scans.

Languages covered: go, rust, dart-flutter, js-ts, python, mojo, shell, plus
common (secret scan, vulnerability scan) used by all.

## Workflow

1. Before writing code in a language, open that language's folder and
   read the script headers; they carry the per-language standard.
2. Build the module with its debug seam from the first commit (the
   debug-add script scaffolds or prints the pattern).
3. Before committing: run scripts/run-gates.sh (or the repo's own gate
   script where one exists, like AlphaVision's tools/check.sh, which
   this skill treats as the repo-local form of the same law).
4. Report gate results honestly: what ran, what passed, what was
   skipped and why. Skipped is stated, never hidden.
