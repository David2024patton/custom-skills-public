#!/usr/bin/env bash
# PURPOSE: Python lint gate: ruff when installed (format check + lint),
# pyflakes as the floor. Type check with mypy whenever the mypy
# binary is present (config or not); see the type-check block below.
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
# Type check (report L1-19 / L1-28 lies-green mode: a checker that
# is silently skipped when its config is absent, or when its binary
# is missing, lets a green gate claim a check that never ran):
# - mypy binary present: run it BLOCKING, with or without a config
#   file. "No config" no longer means "no check"; mypy defaults
#   apply where the project has not configured it.
# - a mypy config exists (mypy.ini or [tool.mypy]) but the binary
#   is missing: the check the project configured DID NOT RUN, so
#   this is exit 2, stated, never a silent skip.
# - neither binary nor config: the type check did not run; that is
#   printed out loud below, not hidden.
if command -v mypy >/dev/null 2>&1; then
  ran=1; mypy . || fail=1
elif [ -f mypy.ini ] || grep -q '\[tool.mypy\]' pyproject.toml 2>/dev/null; then
  echo "TYPE CHECK DID NOT RUN: project configures mypy but the mypy binary is not installed" >&2
  exit 2
else
  echo "note: TYPE CHECK DID NOT RUN: no mypy config and mypy not installed (stated, not hidden)"
fi
[ "$ran" = 0 ] && { echo "no python linter installed (ruff or pyflakes)" >&2; exit 2; }
exit "$fail"
