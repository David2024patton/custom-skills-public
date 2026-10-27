#!/usr/bin/env bash
# PURPOSE: Rust test gate (report L1-09): cargo-nextest for the
# suite, plus a MANDATORY separate doctest lane, because nextest
# silently drops doctests (lies-green register #5).
# STEPS:
#   1. If cargo-nextest is installed: cargo nextest run
#      --workspace --all-features. Nextest exits 100 on test
#      failure and 101 on setup errors; both normalise to gate
#      exit 1 here. Retries and slow-timeouts come from the
#      project's .config/nextest.toml (template shipped beside
#      this script: retries 2, slow-timeout). A test that passes
#      only on retry is reported by nextest as flaky; treat that
#      line as a finding even when the lane is green.
#   2. If nextest is NOT installed: cargo test --workspace
#      --all-features runs instead, and the substitution is
#      stated out loud (never hidden).
#   3. Doctest lane, always: cargo test --workspace --doc.
#   Loom and Shuttle lanes are opt-in for crates with concurrency
#   primitives, bounded (LOOM_MAX_PREEMPTIONS=3), nightly or
#   weekly; they are project CI, not this gate.
# MODIFY PER PROJECT: nextest behaviour lives in
# .config/nextest.toml, not here.
# USAGE: rust/test.sh [dir]
# EXIT: 0 pass; 1 fail; 2 cargo missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
cd "${1:-.}" || exit 2
fail=0
if cargo nextest --version >/dev/null 2>&1; then
  cargo nextest run --workspace --all-features || fail=1
else
  echo "note: cargo-nextest not installed; running cargo test for the suite (stated substitution, not hidden)"
  cargo test --workspace --all-features || fail=1
fi
echo "doctest lane (mandatory beside nextest):"
cargo test --workspace --doc || fail=1
exit "$fail"
