#!/usr/bin/env bash
# PURPOSE: Check the app HAS its debugging built in: a logging or
# diagnostics path exists (the logging package, a diag/log service, or
# FlutterError reporting wired), and no stray print() calls ship.
# MODIFY PER PROJECT: if the app names its logger differently, add the
# name to .gates-extra (one regex per line).
# USAGE: dart-flutter/debug-check.sh [app-dir]
# EXIT: 0 seam found and no print(); 1 findings.
set -u
cd "${1:-.}" || exit 2
pat='package:logging|FlutterError\.onError|class .*Log|diag'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
fail=0
grep -rEq "$pat" lib/ 2>/dev/null || { echo "no logging/diagnostic seam in lib/" >&2; fail=1; }
if grep -rn '^\s*print(' lib/ 2>/dev/null | grep -q .; then
  echo "stray print() calls in lib/ (use the logger)" >&2; fail=1
fi
[ "$fail" = 0 ] && echo "dart debug check: seam found, no stray prints"
exit "$fail"
