#!/usr/bin/env bash
# QA script for Python. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || { echo "SKIP: python"; exit 0; }
PY=$(command -v python3 || command -v python)
step "compileall" "$PY" -m compileall -q .
"$PY" -m ruff --version >/dev/null 2>&1 && step "ruff" "$PY" -m ruff check . || echo "SKIP: ruff"
"$PY" -m mypy --version >/dev/null 2>&1 && step "mypy" "$PY" -m mypy . || echo "SKIP: mypy"
"$PY" -m pytest --version >/dev/null 2>&1 && step "pytest" "$PY" -m pytest -q || echo "SKIP: pytest"

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
