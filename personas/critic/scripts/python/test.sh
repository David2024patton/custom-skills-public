#!/usr/bin/env bash
# PURPOSE: Python test gate: pytest when a suite exists.
# MODIFY PER PROJECT: none. A project with no tests fails on purpose;
# add a tests/ suite or record the exception in the repo RULES page.
# USAGE: python/test.sh [dir]
# EXIT: 0 pass; 1 fail or no suite; 2 pytest missing.
set -u
cd "${1:-.}" || exit 2
command -v pytest >/dev/null 2>&1 || { echo "pytest not found" >&2; exit 2; }
if [ -d tests ] || ls test_*.py >/dev/null 2>&1; then
  pytest -q
else
  echo "no tests found" >&2; exit 1
fi
