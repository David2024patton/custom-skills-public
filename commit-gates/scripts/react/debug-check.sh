#!/usr/bin/env bash
# PURPOSE: Check a React project HAS a diagnostic path components
# can report through, and ships no stray debugging.
# STEPS:
#   1. Detect source roots from what the repo actually has (src/,
#      lib/, app/, components/, pages/, else the repo root).
#      Extensions: .js/.jsx/.ts/.tsx.
#   2. Search those roots for a seam: a logger/diag module, an error
#      reporter, structured console.info/warn/error, OR a React
#      error boundary (getDerivedStateFromError/componentDidCatch).
#      None: fail.
#   3. Search the same roots for stray console.log calls outside
#      test/tests/__tests__/scripts folders and *.test/*.spec
#      files. Any found: fail, and list them.
# MODIFY PER PROJECT: logger names can be added via .gates-extra.
# USAGE: react/debug-check.sh [dir]
# EXIT: 0 seam found, no strays; 1 findings.
set -u
cd "${1:-.}" || exit 2
pat='pino|winston|debug\(|logger|diag|console\.(info|warn|error)|@sentry|errorHandler|reportError|getDerivedStateFromError|componentDidCatch'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
roots=""
for d in src lib app components pages; do [ -d "$d" ] && roots="$roots $d"; done
[ -z "$roots" ] && roots="."
fail=0
# shellcheck disable=SC2086
grep -rEq "$pat" $roots --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next 2>/dev/null \
  || { echo "no logger/diagnostic seam or error boundary found" >&2; fail=1; }
strays=""
for d in $roots; do
  # shellcheck disable=SC2086
  s="$(grep -rn 'console\.log' "$d" --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next 2>/dev/null | grep -vE '/(test|tests|__tests__|scripts)/|\.test\.|\.spec\.' || true)"
  [ -n "$s" ] && strays="$strays
$s"
done
[ -n "$strays" ] && { echo "console.log calls in source (route through the logger):$strays" >&2; fail=1; }
[ "$fail" = 0 ] && echo "react debug check: seam found, no console.log strays"
exit "$fail"
