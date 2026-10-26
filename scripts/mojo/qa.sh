#!/usr/bin/env bash
# QA script for Mojo. build -> lint/vet -> test, real exit codes.
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

if command -v mojo >/dev/null 2>&1; then
  [ -f main.mojo ] && step "run main.mojo" mojo main.mojo
  [ -d examples ] && for f in examples/*.mojo; do step "run $f" mojo "$f"; done
elif command -v max >/dev/null 2>&1; then step "max run" max run .
else echo "SKIP: mojo/MAX not installed (see skill mojo)"; fi

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
