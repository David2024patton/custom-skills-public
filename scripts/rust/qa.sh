#!/usr/bin/env bash
# QA script for Rust. build -> lint/vet -> test, real exit codes.
# Usage: qa.sh [project-dir]. A missing tool is reported SKIP, never silently passed.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

command -v cargo >/dev/null 2>&1 || { echo "SKIP: cargo not installed"; exit 0; }
step "build" cargo build
step "clippy" cargo clippy -- -D warnings
step "test" cargo test
step "fmt" cargo fmt -- --check

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
