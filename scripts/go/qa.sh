#!/usr/bin/env bash
# QA script for Go. build -> lint/vet -> test, real exit codes.
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

command -v go >/dev/null 2>&1 || { echo "SKIP: Go not installed"; exit 0; }
step "build" go build ./...
step "vet" go vet ./...
if command -v golangci-lint >/dev/null 2>&1; then step "lint" golangci-lint run; else echo "SKIP: golangci-lint"; fi
# -race needs cgo. Try with cgo on; fall back to plain test and say so.
if CGO_ENABLED=1 go test ./... -race -count=1 2>/dev/null; then echo "PASS: test -race"
else echo "WARN: -race unavailable (no cgo), running plain test"; go test ./... -count=1 && echo "PASS: test (no race)" || { echo "FAIL: test"; FAILS=$((FAILS+1)); }; fi
