#!/usr/bin/env bash
# PURPOSE: Check a Next.js project HAS a diagnostic path, and ships
# no stray debugging.
# STEPS:
#   1. Detect source roots from what the repo actually has (app/,
#      src/, lib/, components/, else the repo root).
#      Extensions: .js/.jsx/.ts/.tsx. .next/ is always excluded.
#   2. Search those roots for a seam: a logger/diag module, an error
#      reporter (including @sentry/nextjs), or structured
#      console.info/warn/error. None yet: step 3.
#   3. Framework surfaces also count as a seam: an app/error.* or
#      app/global-error.* boundary file, or an instrumentation.*
#      file, anywhere under the roots. None anywhere: fail.
#   4. Search the roots for stray console.log calls outside
#      test/tests/__tests__/scripts folders and *.test/*.spec
#      files. Any found: fail, and list them.
# MODIFY PER PROJECT: logger names can be added via .gates-extra.
# USAGE: nextjs/debug-check.sh [dir]
# EXIT: 0 seam found, no strays; 1 findings.
set -u
cd "${1:-.}" || exit 2
pat='pino|winston|debug\(|logger|diag|console\.(info|warn|error)|@sentry/nextjs|@sentry|errorHandler|reportError'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
roots=""
for d in app src lib components; do [ -d "$d" ] && roots="$roots $d"; done
[ -z "$roots" ] && roots="."
fail=0
seam=1
# shellcheck disable=SC2086
grep -rEq "$pat" $roots --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next 2>/dev/null && seam=0
if [ "$seam" != 0 ]; then
  # shellcheck disable=SC2086
  if find $roots -name 'error.js' -o -name 'error.jsx' -o -name 'error.ts' -o -name 'error.tsx' -o -name 'global-error.*' -o -name 'instrumentation.*' 2>/dev/null | grep -q .; then
    seam=0
    echo "note: diagnostic seam is a Next.js error/instrumentation surface file"
  fi
fi
[ "$seam" != 0 ] && { echo "no logger/diagnostic seam and no Next.js error surface found" >&2; fail=1; }
strays=""
for d in $roots; do
  # shellcheck disable=SC2086
  s="$(grep -rn 'console\.log' "$d" --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next 2>/dev/null | grep -vE '/(test|tests|__tests__|scripts)/|\.test\.|\.spec\.' || true)"
  [ -n "$s" ] && strays="$strays
$s"
done
[ -n "$strays" ] && { echo "console.log calls in source (route through the logger):$strays" >&2; fail=1; }
[ "$fail" = 0 ] && echo "nextjs debug check: seam found, no console.log strays"
exit "$fail"
