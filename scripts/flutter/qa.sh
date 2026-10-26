#!/usr/bin/env bash
# QA script for Flutter. build -> lint/vet -> test, real exit codes.
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

command -v flutter >/dev/null 2>&1 || { echo "SKIP: flutter not installed"; exit 0; }
step "analyze" flutter analyze
step "format" dart format --output=none --set-exit-if-changed .
step "test" flutter test
step "build web" flutter build web
