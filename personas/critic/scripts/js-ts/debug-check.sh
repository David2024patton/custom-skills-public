#!/usr/bin/env bash
# PURPOSE: Check the project HAS a logging/diagnostic path (a logger
# module, pino/winston/debug, or an error reporter) and no stray
# console.log debugging ships in source. Source roots are detected
# from what the target repo actually has (src/, lib/, app/, api/,
# server/, or the repo root for flat Node projects), never assumed
# to be src/ alone.
# MODIFY PER PROJECT: logger names can be added via .gates-extra.
# USAGE: js-ts/debug-check.sh [dir]
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
grep -rEq "$pat" $roots --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.ts' --include='*.tsx' --include='*.jsx' --exclude-dir=node_modules 2>/dev/null \
  || { echo "no logger/diagnostic seam found" >&2; fail=1; }
strays=""
for d in $roots; do
  # shellcheck disable=SC2086
  s="$(grep -rn 'console\.log' "$d" --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --include='*.jsx' --exclude-dir=node_modules 2>/dev/null | grep -vE '/(test|tests|__tests__|scripts)/|\.test\.|\.spec\.' || true)"
  [ -n "$s" ] && strays="$strays
$s"
done
[ -n "$strays" ] && { echo "console.log calls in source (route through the logger):$strays" >&2; fail=1; }
[ "$fail" = 0 ] && echo "js debug check: seam found, no console.log strays"
exit "$fail"
