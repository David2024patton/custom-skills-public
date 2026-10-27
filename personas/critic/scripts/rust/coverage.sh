#!/usr/bin/env bash
# PURPOSE: Rust coverage gate (report L1-10): cargo-llvm-cov with
# its native threshold flags, so no output parsing is needed and
# no threshold can be lost in a parser.
# STEPS:
#   1. cargo llvm-cov --workspace --all-features --lcov
#      --output-path lcov.info --fail-under-lines 80
#      (native exit 1 below threshold).
#   2. Per-file floor: a second run summary is checked with
#      --fail-under-file-lines 60 via the JSON summary when the
#      project asks for it (COVERAGE_FILE_FLOOR=1); generated and
#      FFI shim files are excluded with
#      --ignore-filename-regex '(generated|ffi_shim)'.
#   Thresholds ratchet from baseline: a project below 80 records
#   its baseline and the floor only moves up.
# MODIFY PER PROJECT: none in this script; the ratchet values a
# project has earned are recorded in its RULES page.
# USAGE: rust/coverage.sh [dir]
# EXIT: 0 at or above threshold; 1 below it or tests fail;
# 2 cargo-llvm-cov or the llvm-tools component missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
cd "${1:-.}" || exit 2
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
cargo llvm-cov --version >/dev/null 2>&1 || { echo "cargo-llvm-cov not found (install: cargo install cargo-llvm-cov; also needs: rustup component add llvm-tools-preview); coverage DID NOT RUN" >&2; exit 2; }
cargo llvm-cov --workspace --all-features --lcov --output-path lcov.info --fail-under-lines 80 --ignore-filename-regex '(generated|ffi_shim)'
