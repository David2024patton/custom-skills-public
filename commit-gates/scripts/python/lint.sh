#!/usr/bin/env bash
# PURPOSE: Python lint gate: ruff when installed (format check + lint),
# pyflakes as the floor. Type check with mypy when the project has a
# mypy config.
# MODIFY PER PROJECT: rule selection lives in the project's
# pyproject.toml [tool.ruff] section, not here.
# USAGE: python/lint.sh [dir]
# EXIT: 0 clean; 1 findings; 2 no linter available.
set -u
cd "${1:-.}" || exit 2
fail=0; ran=0
if command -v ruff >/dev/null 2>&1; then
  ran=1; ruff check . || fail=1; ruff format --check . || fail=1
elif command -v pyflakes >/dev/null 2>&1; then
  ran=1; pyflakes . || fail=1
fi
if [ -f mypy.ini ] || grep -q '\[tool.mypy\]' pyproject.toml 2>/dev/null; then
  command -v mypy >/dev/null 2>&1 && { ran=1; mypy . || fail=1; }
fi
[ "$ran" = 0 ] && { echo "no python linter installed (ruff or pyflakes)" >&2; exit 2; }
exit "$fail"
