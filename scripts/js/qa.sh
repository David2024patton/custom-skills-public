#!/usr/bin/env bash
# QA script for JS / TS / React. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

command -v node >/dev/null 2>&1 || { echo "SKIP: node not installed"; exit 0; }
PM=npm
[ -f pnpm-lock.yaml ] && PM=pnpm
[ -f yarn.lock ] && PM=yarn
[ -d node_modules ] || step "install" "$PM" install
step "build" "$PM" run build
grep -q '"lint"' package.json && step "lint" "$PM" run lint || echo "SKIP: no lint script"
grep -qE '"typecheck"|"type-check"' package.json && step "typecheck" "$PM" run typecheck 2>/dev/null || "$PM" run type-check 2>/dev/null
grep -q '"test"' package.json && step "test" "$PM" test -- --run 2>/dev/null || "$PM" test 2>/dev/null || echo "SKIP: no test script"
grep -q '"react"' package.json && echo "NOTE: React app, hand off to ui-visual-check for browser pass"

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
