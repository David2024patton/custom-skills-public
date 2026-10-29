#!/usr/bin/env bash
# PURPOSE: Python test gate (report L1-20): pytest with BRANCH
# coverage and a fail_under ratchet, plus the property-test
# requirement.
# STEPS:
#   1. Suite discovery: tests/ or test_*.py. No suite: exit 1.
#   2. New-module law: a source module (src/**/*.py or ./*.py
#      package modules) with no test file naming it and no test
#      importing it fails the gate, named. A new module with no
#      tests must not pass quietly.
#   3. Run: pytest -q --cov --cov-branch --cov-report=term
#      --cov-fail-under=<floor>. The floor comes from the
#      project config ([tool.coverage.report] fail_under, or
#      .coveragerc), default 85 proposed by the report. The
#      coverage config must set branch = true; a config that
#      disables branch coverage is a finding.
#   4. Hypothesis requirement: parser, codec, and numeric
#      surfaces (source files matching pars|codec|serial|numeric
#      in name or content markers) must have at least one
#      Hypothesis property test (a test file importing
#      hypothesis). Missing: finding, exit 1. Hypothesis runs
#      derandomised on PR (the project sets the derandomize
#      profile), randomised nightly.
# MODIFY PER PROJECT: coverage floor lives in coverage config,
# Hypothesis profiles in conftest.py, never here.
# USAGE: python/test.sh [dir]
# EXIT: 0 pass; 1 fail, no suite, new untested module, or missing
# property tests; 2 pytest or pytest-cov missing.
set -u
cd "${1:-.}" || exit 2
command -v pytest >/dev/null 2>&1 || { echo "pytest not found" >&2; exit 2; }
if [ -d tests ] || ls test_*.py >/dev/null 2>&1 || ls tests/test_*.py >/dev/null 2>&1; then :; else
  echo "no tests found" >&2; exit 1
fi
fail=0
# New-module law (heuristic, stated): module basename must appear in a test filename or an import line.
for m in $(find src -name '*.py' ! -name '__init__.py' ! -name '__main__.py' 2>/dev/null) $(find . -maxdepth 1 -name '*.py' ! -name 'setup.py' ! -name 'conftest.py' 2>/dev/null); do
  base="$(basename "$m" .py)"
  if ! ls tests/test_"$base".py test_"$base".py >/dev/null 2>&1 && ! grep -rqE "(import|from)[[:space:]][^[:space:]]*$base([^[:alnum:]_]|$)|from [^[:space:]]+ import [^#]*$base([^[:alnum:]_]|$)" tests test_*.py 2>/dev/null; then
    echo "finding: module $m has no tests naming or importing it (new modules do not pass quietly)" >&2; fail=1
  fi
done
if [ -f .coveragerc ] && grep -q 'branch[[:space:]]*=[[:space:]]*False' .coveragerc; then
  echo "finding: branch coverage disabled in .coveragerc (report L1-20 requires branch = true)" >&2; fail=1
fi
if grep -q 'fail_under' pyproject.toml .coveragerc setup.cfg 2>/dev/null; then
  FLOOR="$(grep -h 'fail_under' pyproject.toml .coveragerc setup.cfg 2>/dev/null | grep -oE '[0-9]+' | head -1)"
else
  FLOOR=85
  echo "note: no fail_under in coverage config; using the report default of 85 (set one in [tool.coverage.report])"
fi
python3 -c "import pytest_cov" 2>/dev/null || { echo "pytest-cov not found; coverage gate DID-NOT-RUN" >&2; exit 2; }
pytest -q --cov --cov-branch --cov-report=term --cov-fail-under="$FLOOR" || fail=1
# Hypothesis requirement on parser/codec/numeric surfaces.
if find . -path ./node_modules -prune -o -name '*.py' -print 2>/dev/null | grep -v test | grep -qiE 'pars|codec|serial|numeric'; then
  if grep -rlq 'import hypothesis\|from hypothesis' tests test_*.py 2>/dev/null; then
    echo "hypothesis: property tests present for parser/codec/numeric surfaces"
  else
    echo "finding: parser/codec/numeric surface present but no Hypothesis property tests (report L1-20)" >&2; fail=1
  fi
fi
exit "$fail"
