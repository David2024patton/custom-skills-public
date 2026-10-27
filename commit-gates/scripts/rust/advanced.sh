#!/usr/bin/env bash
# PURPOSE: Rust mutation, fuzz, unsafe, and semver lanes (report
# L1-11). Nightly and release lanes, not per-commit gates.
# MODES (arg 2):
#   mutants-diff <base.diff>: cargo mutants --in-diff <file>
#     --test-tool=nextest --jobs=4. cargo-mutants exits 0 caught,
#     2 missed, 4 baseline failing, 8 other errors; every non-zero
#     normalises to gate exit 1 here (the raw codes are printed).
#   mutants-full: sharded full run; reports the missed count as a
#     trend line. Hard-fails only on NEW misses in changed crates
#     is a CI comparison; this script prints the count.
#   fuzz: where fuzz/fuzz_targets exists, per target:
#     cargo +nightly fuzz run <target> -- -max_total_time=60.
#     No target on a parser or unsafe crate (grep for parse/unsafe
#     surfaces) is a finding: lane exit 2. No fuzz dir and no such
#     surface: stated, exit 0.
#   miri: cargo +nightly miri test on crates containing unsafe;
#     no nightly or no miri component: exit 2, stated.
#   semver: libraries only: cargo semver-checks check-release.
#     No lib target: exit 2 with the skip-with-note stated (a
#     binary crate has no release API to check).
# MODIFY PER PROJECT: none.
# USAGE: rust/advanced.sh [dir] <mode> [mode-arg]
# EXIT: 0 pass; 1 findings; 2 tool missing or lane not applicable
# (stated, never a silent pass).
set -u
export PATH="$HOME/.cargo/bin:$PATH"
cd "${1:-.}" || exit 2
MODE="${2:-}"
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
case "$MODE" in
  mutants-diff)
    cargo mutants --version >/dev/null 2>&1 || { echo "cargo-mutants not found" >&2; exit 2; }
    DIFF="${3:-}"
    [ -n "$DIFF" ] && [ -f "$DIFF" ] || { echo "mutants-diff needs a diff file" >&2; exit 2; }
    cargo mutants --in-diff "$DIFF" --test-tool=nextest --jobs=4
    rc=$?
    [ "$rc" != 0 ] && { echo "cargo-mutants raw exit $rc normalised to gate exit 1" >&2; exit 1; }
    ;;
  mutants-full)
    cargo mutants --version >/dev/null 2>&1 || { echo "cargo-mutants not found" >&2; exit 2; }
    cargo mutants --jobs=4 || { echo "cargo-mutants raw exit $? normalised to gate exit 1" >&2; exit 1; }
    ;;
  fuzz)
    if [ -d fuzz/fuzz_targets ]; then
      ls fuzz/fuzz_targets/*.rs >/dev/null 2>&1 || { echo "fuzz dir exists but no targets" >&2; exit 2; }
      for t in fuzz/fuzz_targets/*.rs; do
        name="$(basename "$t" .rs)"
        cargo +nightly fuzz run "$name" -- -max_total_time=60 || exit 1
      done
    elif grep -rqE 'unsafe|fn parse|Parser' --include='*.rs' src 2>/dev/null; then
      echo "FINDING: parser or unsafe surface present but no fuzz targets (lane exit 2)" >&2; exit 2
    else
      echo "no fuzz targets and no parser/unsafe surface detected (stated)"
    fi
    ;;
  miri)
    if grep -rq 'unsafe' --include='*.rs' src 2>/dev/null; then
      cargo +nightly miri --version >/dev/null 2>&1 || { echo "miri not available (nightly + miri component required); lane DID NOT RUN" >&2; exit 2; }
      cargo +nightly miri test || exit 1
    else
      echo "no unsafe code detected; miri lane not applicable (stated)"; exit 2
    fi
    ;;
  semver)
    cargo semver-checks --version >/dev/null 2>&1 || { echo "cargo-semver-checks not found" >&2; exit 2; }
    if [ -f src/lib.rs ] || grep -q '^\[lib\]' Cargo.toml 2>/dev/null; then
      cargo semver-checks check-release || exit 1
    else
      echo "no lib target in this crate; semver lane not applicable (stated skip, not a pass)"; exit 2
    fi
    ;;
  *) echo "mode required: mutants-diff|mutants-full|fuzz|miri|semver" >&2; exit 2 ;;
esac
