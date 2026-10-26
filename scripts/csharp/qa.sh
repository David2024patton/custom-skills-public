#!/usr/bin/env bash
# QA script for C#. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

command -v dotnet >/dev/null 2>&1 || { echo "SKIP: dotnet not installed"; exit 0; }
step "restore" dotnet restore
step "build" dotnet build --no-restore -warnaserror
step "format" dotnet format --verify-no-changes
step "test" dotnet test --no-build
step "audit" dotnet list package --vulnerable --include-transitive

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
