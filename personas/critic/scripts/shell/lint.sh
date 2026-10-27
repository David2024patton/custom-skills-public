#!/usr/bin/env bash
# PURPOSE: Shell lint gate: shellcheck over every .sh file, plus a
# syntax pass (bash -n) as the floor when shellcheck is absent.
# MODIFY PER PROJECT: shellcheck directives belong in the scripts
# themselves (# shellcheck disable=... with a reason), not here.
# USAGE: shell/lint.sh [dir]
# EXIT: 0 clean; 1 findings; 2 no checker available.
set -u
cd "${1:-.}" || exit 2
mapfile -t files < <(find . -name '*.sh' -not -path './node_modules/*')
[ "${#files[@]}" = 0 ] && { echo "no shell scripts"; exit 0; }
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "${files[@]}"
else
  fail=0
  for f in "${files[@]}"; do bash -n "$f" || fail=1; done
  echo "note: shellcheck not installed; syntax pass only (stated)"
  exit "$fail"
fi
