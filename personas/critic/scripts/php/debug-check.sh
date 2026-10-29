#!/usr/bin/env bash
# PURPOSE: Check the project HAS its debugging built in: a
# diagnostic seam (error logging or a PSR-3 style logger) somewhere
# in the PHP sources, and no display_errors switched on in
# production-facing config or code. Pure grep; no PHP binary
# needed, so this gate produces signal on a bare review host.
# WHAT COUNTS AS THE SEAM (any one): error_log(), Monolog, a
# PSR-3 LoggerInterface or Psr\Log use, a framework logger call
# (Log::, logger()), set_error_handler or set_exception_handler,
# or a logger ->error() or ->log() call.
# WHAT FAILS THE CONFIG HALF: display_errors set to On, 1, or true
# in a *.ini file, in .htaccess (php_flag or php_value), or via
# ini_set('display_errors', ...) in code. The safe spellings (Off,
# 0, stderr) never match these patterns.
# MODIFY PER PROJECT: none normally. A project that logs only
# through its web server may record that decision in its own docs;
# this gate still reports the absent seam, stated, and the human
# verdict decides.
# USAGE: php/debug-check.sh [dir]
# EXIT: 0 seam found and no display_errors findings; 1 findings;
# 2 bad dir.
set -u
cd "${1:-.}" || exit 2
fail=0
PHPFILES="$(find . -name '*.php' -not -path './vendor/*' -not -path './node_modules/*')"
[ -z "$PHPFILES" ] && { echo "no PHP sources found" >&2; exit 2; }
if echo "$PHPFILES" | xargs grep -lE 'error_log[[:space:]]*\(|Monolog|Psr\\Log|LoggerInterface|Log::|logger[[:space:]]*\(|set_error_handler|set_exception_handler|->error[[:space:]]*\(|->log[[:space:]]*\(' >/dev/null 2>&1; then
  echo "php debug check: diagnostic seam present (error logging or logger usage found)"
else
  echo "finding: no diagnostic seam: no error_log(), logger, or error handler usage in any PHP source" >&2
  fail=1
fi
hits=""
hits="$hits$(grep -rnE '^[[:space:]]*display_errors[[:space:]]*=[[:space:]]*(On|on|1|true|True)' --include='*.ini' . 2>/dev/null | grep -v '/vendor/' || true)"
hits="$hits$(grep -rnE "ini_set[[:space:]]*\([[:space:]]*['\"]display_errors['\"][[:space:]]*,[[:space:]]*['\"]?(1|On|on|true)" --include='*.php' . 2>/dev/null | grep -v '/vendor/' || true)"
for h in $(find . -name '.htaccess' -not -path './vendor/*'); do
  hits="$hits$(grep -nE 'php_(flag|value)[[:space:]]+display_errors[[:space:]]+(on|On|1|true)' "$h" 2>/dev/null | sed "s|^|$h:|" || true)"
done
if [ -n "$(printf '%s' "$hits" | tr -d '[:space:]')" ]; then
  echo "finding: display_errors switched on (production config must keep it off; log instead):" >&2
  printf '%s\n' "$hits" | grep -v '^$' >&2
  fail=1
fi
[ "$fail" = 0 ] && echo "php debug check: seam present, no display_errors findings"
exit "$fail"
