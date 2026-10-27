#!/usr/bin/env bash
# PURPOSE: Check the project HAS a logging/diagnostic path (a logger
# module, pino/winston/debug, or an error reporter) and no stray
# console.log debugging ships in src.
# MODIFY PER PROJECT: logger names can be added via .gates-extra.
# USAGE: js-ts/debug-check.sh [dir]
# EXIT: 0 seam found, no strays; 1 findings.
set -u
cd "${1:-.}" || exit 2
pat='pino|winston|debug\(|logger|diag'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
fail=0
grep -rEq "$pat" src/ 2>/dev/null || grep -rEq "$pat" lib/ 2>/dev/null \
  || { echo "no logger/diagnostic seam found" >&2; fail=1; }
if grep -rn 'console\.log' src/ 2>/dev/null | grep -q .; then
  echo "console.log calls in src/ (route through the logger)" >&2; fail=1
fi
[ "$fail" = 0 ] && echo "js debug check: seam found, no console.log strays"
exit "$fail"
