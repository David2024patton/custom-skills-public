#!/usr/bin/env bash
# PURPOSE: Rust lint gate: rustfmt check plus clippy with warnings
# denied, for the workspace and any separately pinned trees the repo
# defines (pass them as extra args).
# MODIFY PER PROJECT: clippy configuration lives in the repo
# (clippy.toml / crate attributes), not here. The repo toolchain pin
# (rust-toolchain.toml) is respected automatically by rustup.
# USAGE: rust/lint.sh [dir ...]   (default: current directory)
# EXIT: 0 clean; 1 findings; 2 cargo missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
fail=0
for d in "${@:-.}"; do
  ( cd "$d" && cargo fmt --check && cargo clippy --workspace -- -D warnings ) || fail=1
done
exit "$fail"
