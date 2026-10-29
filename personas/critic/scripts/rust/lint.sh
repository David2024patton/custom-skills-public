#!/usr/bin/env bash
# PURPOSE: Rust lint gate (report L1-07): format check against the
# committed rustfmt.toml, plus clippy over ALL targets and ALL
# features with warnings denied.
# STEPS:
#   1. Format: cargo fmt --all -- --check. The project must carry
#      a committed rustfmt.toml pinning edition = "2024" and
#      style_edition = "2024" (template shipped beside this
#      script); a missing file, or one without style_edition
#      2024, is a finding, because an unpinned style edition
#      drifts with the toolchain.
#   2. Lint: cargo clippy --workspace --all-targets --all-features
#      -- -D warnings. The narrower --workspace-only invocation
#      misses tests, examples, and benches. Cherry-picked
#      restriction lints ride along as warnings-denied too:
#      unwrap_used, expect_used, dbg_macro,
#      undocumented_unsafe_blocks. Restriction and nursery groups
#      are never enabled as groups; pedantic enters only as a
#      counted warning ratchet after triage (project clippy.toml
#      and crate attributes own that, not this script).
#   3. A nightly lane (not this gate) adds a --no-default-features
#      clippy run for feature-heavy crates.
#   Clippy component missing: exit 2 with the rustup hint.
# MODIFY PER PROJECT: style lives in rustfmt.toml, clippy config
# in clippy.toml / crate attributes, never in this script.
# USAGE: rust/lint.sh [dir ...]
# EXIT: 0 clean; 1 findings; 2 cargo or clippy missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
cargo clippy --version >/dev/null 2>&1 || { echo "clippy component missing: rustup component add clippy" >&2; exit 2; }
fail=0
for d in "${@:-.}"; do
  ( cd "$d" || exit 2
    if [ ! -f rustfmt.toml ]; then
      echo "finding: no committed rustfmt.toml (copy the template shipped beside this script; style_edition must be pinned)" >&2; exit 1
    fi
    grep -q 'style_edition[[:space:]]*=[[:space:]]*"2024"' rustfmt.toml || { echo "finding: rustfmt.toml does not pin style_edition = \"2024\"" >&2; exit 1; }
    cargo fmt --all -- --check || exit 1
    cargo clippy --workspace --all-targets --all-features -- -D warnings -D clippy::unwrap_used -D clippy::expect_used -D clippy::dbg_macro -D clippy::undocumented_unsafe_blocks || exit 1
  ) || fail=1
done
exit "$fail"
