#!/usr/bin/env bash
# PURPOSE: PHP test gate: PHPUnit with a zero-test guard. A suite
# that discovers nothing must not pass quietly: PHPUnit can exit 0
# over an empty suite with only a "No tests executed" line, so the
# runner output is captured, printed in full, and read by the
# guard before any verdict.
# STEPS:
#   1. Discovery: any *Test.php outside vendor/. None: exit 1.
#   2. Runner: vendor/bin/phpunit when present, else phpunit on
#      PATH. Neither: exit 2, stated (test gate DID-NOT-RUN).
#   3. Run: bare when phpunit.xml or phpunit.xml.dist exists (the
#      project's own suite definition), else against the tests
#      directory (tests/, test/, or the directory of the first
#      discovered test file).
#   4. Zero-test guard: output containing "No tests executed", or
#      an OK line reporting 0 tests, is a failure (exit 1) even
#      when the runner itself exits 0.
# MODIFY PER PROJECT: suite layout and config live in
# phpunit.xml, never here.
# USAGE: php/test.sh [dir]
# EXIT: 0 pass; 1 test failure, no tests found, or zero tests
# executed; 2 phpunit missing.
set -u
cd "${1:-.}" || exit 2
first_test="$(find . -path './vendor' -prune -o -name '*Test.php' -print 2>/dev/null | head -1)"
if [ -z "$first_test" ]; then
  echo "no tests found (no *Test.php outside vendor/)" >&2
  exit 1
fi
runner=""
if [ -x vendor/bin/phpunit ]; then runner="vendor/bin/phpunit"
elif command -v phpunit >/dev/null 2>&1; then runner="phpunit"; fi
[ -z "$runner" ] && { echo "phpunit not found (no vendor/bin/phpunit, none on PATH); test gate DID-NOT-RUN" >&2; exit 2; }
if [ -f phpunit.xml ] || [ -f phpunit.xml.dist ]; then
  echo "test runner: $runner (project config)"
  out="$("$runner" 2>&1)"; rc=$?
else
  tdir="tests"; [ -d tests ] || tdir="test"; [ -d "$tdir" ] || tdir="$(dirname "$first_test")"
  echo "test runner: $runner $tdir (no phpunit.xml; discovered suite directory)"
  out="$("$runner" "$tdir" 2>&1)"; rc=$?
fi
printf '%s\n' "$out"
fail=0
[ "$rc" != 0 ] && fail=1
if printf '%s' "$out" | grep -q 'No tests executed'; then
  echo "finding: phpunit executed zero tests; an empty suite does not pass quietly" >&2
  fail=1
fi
if printf '%s' "$out" | grep -qE 'OK \(0 tests'; then
  echo "finding: phpunit reports OK with 0 tests; an empty suite does not pass quietly" >&2
  fail=1
fi
[ "$fail" = 0 ] && echo "php test: suite ran and passed"
exit "$fail"
