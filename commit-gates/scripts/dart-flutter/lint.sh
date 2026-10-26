#!/usr/bin/env bash
# PURPOSE: Dart/Flutter lint gate: format check plus analyzer with
# warnings as failures.
# MODIFY PER PROJECT: lint rules live in the project's analysis_options
# .yaml, not here. Flutter SDK location differs per machine; set
# FLUTTER_BIN if flutter is not on PATH.
# USAGE: dart-flutter/lint.sh [app-dir]
# EXIT: 0 clean; 1 findings; 2 flutter/dart missing.
set -u
cd "${1:-.}" || exit 2
F="${FLUTTER_BIN:-flutter}"
command -v "$F" >/dev/null 2>&1 || command -v dart >/dev/null 2>&1 || { echo "no flutter/dart" >&2; exit 2; }
fail=0
if command -v dart >/dev/null 2>&1; then
  dart format --set-exit-if-changed . || fail=1
fi
if command -v "$F" >/dev/null 2>&1; then
  "$F" analyze --no-fatal-infos=false || fail=1
fi
exit "$fail"
