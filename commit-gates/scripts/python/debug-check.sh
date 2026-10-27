#!/usr/bin/env bash
# PURPOSE: Check the project HAS its debugging built in: the logging
# module (or structlog) configured somewhere, and no bare print()
# debugging left outside CLI entry points.
# MODIFY PER PROJECT: CLI tools whose output IS print may list their
# entry files in .gates-extra (one path per line) to exempt them.
# USAGE: python/debug-check.sh [dir]
# EXIT: 0 seam found; 1 findings.
set -u
cd "${1:-.}" || exit 2
fail=0
grep -rEq 'import logging|structlog|getLogger' --include='*.py' . \
  || { echo "no logging configured" >&2; fail=1; }
strays="$(grep -rn '^\s*print(' --include='*.py' . | grep -v '/test' || true)"
[ -n "$strays" ] && { echo "print() calls outside tests:"; echo "$strays"; fail=1; }
[ "$fail" = 0 ] && echo "python debug check: logging configured, no stray prints"
exit "$fail"
