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

## The gate set (every commit)

1. Format check for the languages present.
2. Lint clean (warnings are failures).
3. Unit tests pass; race detector where the language supports it.
4. Debug check: the module has its diagnostic seam (see scripts).
5. Secret scan: betterleaks (preferred) or gitleaks over the tree; any
   hit stops the commit. No passwords, keys, or tokens in the repo,
   ever; credentials live in secure storage only.
6. Vulnerability scan: osv-scanner where available, plus the language
   native tool (govulncheck for Go, cargo audit for Rust, pip-audit for
   Python, npm audit for JS/TS). Known-vulnerability data comes from
   osv.dev; check it before adding any dependency.
7. Fuzz targets exist for untrusted-input parsers (ClusterFuzzLite
   pattern in CI for the repos that parse external data).
8. Commit message gate: commit messages follow the shipped config in
   templates/commitlint.config.js (Conventional Commits based
   config-conventional, extended with the repo standard's needs),
   enforced by commitlint (or an equivalent parser) in the commit-msg
   hook and re-checked in CI over the PR commit range.

## Enforcement layers

The gates have three layers, and all three run the same entry point
(scripts/run-gates.sh, or the repo-local gate script where one exists):

- Local hooks are the fast feedback layer. They run the commit stage
  and the push stage on the developer's own machine, so problems
  surface in seconds. Hooks are bypassable by design (a skip flag or
  a missing install defeats them), so a hook result is fast feedback,
  never proof. A result from the local layer alone is reported as
  local only.
- CI is the proof layer. On every pull request and every push to the
  default branch, CI runs the whole gate set whole-tree, lints the
  workflow files themselves with actionlint, and re-checks commit
  message form over the pull request commit range.
- Branch protection is the enforcement. Requiring the CI checks on
  the default branch is what makes a red gate block a merge. Without
  branch protection, CI is only a report and nothing is enforced.

The trigger layer that makes the gates run uninvited ships in
templates/: templates/.pre-commit-config.yaml (the pre-commit
framework config, wiring the scripts library by stage, with pinned
hook revisions), templates/lefthook.yml (the sanctioned alternative
config, for repos that run Lefthook instead), templates/
commitlint.config.js (the commit message gate config), and
templates/.github/workflows/gates.yml (the CI workflow). The scripts
library is what runs; the templates are what makes it run uninvited.
Copy the templates into the repo; do not rewrite them per repo beyond
the paths and pins their headers name.

Two gates are hook-only as their first check, because CI is too late
for both:

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

Languages covered: go, rust, dart-flutter, js-ts, python, shell, plus
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
