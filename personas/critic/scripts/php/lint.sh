#!/usr/bin/env bash
# PURPOSE: PHP lint and static analysis gate. Two halves, and the
# second half is UNCONDITIONAL, the same law the Python set carries:
# a syntax-only pass does not wear this gate's name.
# STEPS:
#   1. Syntax: php -l over every *.php source in the tree,
#      excluding vendor/ and node_modules/. Any parse failure is
#      a finding. The php binary missing is exit 2, stated.
#   2. Static analysis: PHPStan when the project provides it
#      (vendor/bin/phpstan, or phpstan on PATH), Psalm otherwise
#      (vendor/bin/psalm or PATH, and only when the project carries
#      a psalm.xml or psalm.xml.dist; this gate never writes project
#      config). PHPStan runs with the project's own config when a
#      phpstan.neon or phpstan.neon.dist exists, else with a
#      stated default of --level=5 over the source dirs. When the
#      project declares phpstan or psalm in composer.json
#      require-dev but the binary is absent (vendor not installed),
#      that is named in the DID-NOT-RUN line.
#      Neither analyzer available: STATIC ANALYSIS DID NOT RUN,
#      exit 2. The syntax results still print, labelled partial;
#      they never promote to a pass on their own.
# MODIFY PER PROJECT: analyzer choice, level, and config live in
# the project's composer.json, phpstan.neon, or psalm.xml, never
# here.
# USAGE: php/lint.sh [dir]
# EXIT: 0 clean; 1 findings (syntax or analyzer); 2 php missing, or
# static analysis could not run at all.
set -u
cd "${1:-.}" || exit 2
command -v php >/dev/null 2>&1 || { echo "php not found; lint gate DID-NOT-RUN" >&2; exit 2; }
fail=0
count=0
while IFS= read -r f; do
  count=$((count + 1))
  php -l "$f" >/dev/null 2>&1 || { echo "syntax: php -l failed: $f" >&2; php -l "$f" 2>&1 | head -3 >&2; fail=1; }
done <<EOF
$(find . -name '*.php' -not -path './vendor/*' -not -path './node_modules/*')
EOF
[ "$count" = 0 ] && { echo "no PHP sources found; lint gate DID-NOT-RUN" >&2; exit 2; }
echo "php -l: $count file(s) checked"
stan=""
if [ -x vendor/bin/phpstan ]; then stan="vendor/bin/phpstan"
elif command -v phpstan >/dev/null 2>&1; then stan="phpstan"; fi
psalm=""
if [ -x vendor/bin/psalm ]; then psalm="vendor/bin/psalm"
elif command -v psalm >/dev/null 2>&1; then psalm="psalm"; fi
if [ -n "$stan" ]; then
  if [ -f phpstan.neon ] || [ -f phpstan.neon.dist ]; then
    echo "static analysis: $stan (project config)"
    "$stan" analyse --no-progress || fail=1
  else
    SRC=""
    for d in src app lib; do [ -d "$d" ] && SRC="$SRC $d"; done
    [ -z "$SRC" ] && SRC=" ."
    echo "static analysis: $stan (no project config; default --level=5 over:$SRC)"
    # shellcheck disable=SC2086
    "$stan" analyse --no-progress --level=5 $SRC || fail=1
  fi
elif [ -n "$psalm" ] && { [ -f psalm.xml ] || [ -f psalm.xml.dist ]; }; then
  echo "static analysis: $psalm (project config)"
  "$psalm" --no-progress || fail=1
else
  hint=""
  if [ -f composer.json ]; then
    grep -q 'phpstan' composer.json && hint=" composer.json declares phpstan but no phpstan binary is available (vendor not installed?)."
    grep -q 'vimeo/psalm' composer.json && hint=" composer.json declares psalm but no usable psalm binary or config is available."
  fi
  echo "STATIC ANALYSIS DID NOT RUN: neither PHPStan nor Psalm is available; php -l alone does not wear this gate's name, so the syntax results above are partial only.$hint" >&2
  exit 2
fi
[ "$fail" = 0 ] && echo "php lint: syntax clean, static analysis ran"
exit "$fail"
