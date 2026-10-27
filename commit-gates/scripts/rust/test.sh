#!/usr/bin/env bash
# PURPOSE: Rust test gate: workspace tests on the host target.
# MODIFY PER PROJECT: cross-target checks (for example aarch64 or
# riscv kernel checks) belong to the repo's own gate script; this runs
# the host suite only.
# USAGE: rust/test.sh [dir]
# EXIT: 0 pass; 1 fail; 2 cargo missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
cd "${1:-.}" && cargo test --workspace
