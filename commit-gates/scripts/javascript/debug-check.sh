#!/usr/bin/env bash
# PURPOSE: Check a plain JavaScript (ESM) project HAS a diagnostic
# seam and ships no stray debugging.
# STEPS:
#   1. Detect source roots from what the repo actually has (src/,
#      lib/, app/, api/, server/, else the repo root); never assume
#      src/ alone. Extensions: .js/.mjs/.cjs/.jsx.
#   2. Search those roots for a seam: a logger module, pino/winston,
#      a debug/diag call, structured console.info/warn/error, an
#      uncaughtException handler, or an error reporter. None: fail.
#   3. Search the same roots for stray console.log calls outside
#      test/tests/__tests__/scripts folders and *.test/*.spec
#      files. Any found: fail, and list them.
# MODIFY PER PROJECT: logger names can be added via .gates-extra.
# USAGE: javascript/debug-check.sh [dir]
# EXIT: 0 seam found, no strays; 1 findings.
set -u
cd "${1:-.}" || exit 2
pat='pino|winston|debug\(|logger|diag|console\.(info|warn|error)|process\.on\(.uncaughtException|@sentry|errorHandler|reportError'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
roots=""
for d in src lib app api server; do [ -d "$d" ] && roots="$roots $d"; done
[ -z "$roots" ] && roots="."
fail=0
# shellcheck disable=SC2086
grep -rEq "$pat" $roots --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.jsx' --exclude-dir=node_modules 2>/dev/null \
  || { echo "no logger/diagnostic seam found" >&2; fail=1; }
strays=""
for d in $roots; do
  # shellcheck disable=SC2086
  s="$(grep -rn 'console\.log' "$d" --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.jsx' --exclude-dir=node_modules 2>/dev/null | grep -vE '/(test|tests|__tests__|scripts)/|\.test\.|\.spec\.' || true)"
  [ -n "$s" ] && strays="$strays
$s"
done
[ -n "$strays" ] && { echo "console.log calls in source (route through the logger):$strays" >&2; fail=1; }
[ "$fail" = 0 ] && echo "javascript debug check: seam found, no console.log strays"
exit "$fail"
