#!/usr/bin/env bash
# go-qa.sh: run the full Go quality gate and report real exit codes.
# Usage: scripts/go-qa.sh [pkg]        (default: ./...)
# Runs build, vet, lint, race-test, and mod-tidy drift. Prints PASS/FAIL per step
# and exits non-zero if any required step fails. A missing tool is reported
# UNTESTED, never silently skipped.
set -uo pipefail

PKG="${1:-./...}"
fail=0
report=()

run() { # run <label> <required:1|0> <cmd...>
  local label="$1" required="$2"; shift 2
  local out rc
  out=$("$@" 2>&1); rc=$?
  if [ $rc -eq 0 ]; then
    report+=("PASS     $label")
  elif [ $rc -eq 127 ] || echo "$out" | grep -qiE "command not found|not recognized"; then
    report+=("UNTESTED $label (tool missing: $1)")
    [ "$required" = "1" ] && fail=1
  else
    report+=("FAIL     $label")
    printf '%s\n' "$out" | tail -n 40
    fail=1
  fi
}

echo "== go-qa on $PKG =="

run "build" 1 go build "$PKG"
run "vet" 1 go vet "$PKG"

if command -v golangci-lint >/dev/null 2>&1; then
  run "golangci-lint" 1 golangci-lint run "$PKG"
else
  report+=("UNTESTED golangci-lint (not installed; install for the full lint gate)")
fi

run "test -race" 1 go test "$PKG" -race -count=1

if git rev-parse --git-dir >/dev/null 2>&1; then
  go mod tidy >/dev/null 2>&1
  if ! git diff --quiet go.mod go.sum 2>/dev/null; then
    report+=("WARN     go mod tidy produced drift (go.mod/go.sum changed)")
  else
    report+=("PASS     go mod tidy (no drift)")
  fi
fi

echo
printf '%s\n' "${report[@]}"
echo
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS (a step marked UNTESTED is coverage debt, not a pass)"
else
  echo "RESULT: FAIL (fix and re-run the whole gate, not just the failed step)"
fi
exit "$fail"
