#!/usr/bin/env bash
# PURPOSE: Dart/Flutter analyze gate (report L1-15, L1-16).
# STEPS:
#   1. Strict modes: analysis_options.yaml must enable all three
#      of strict-casts, strict-inference, strict-raw-types under
#      analyzer.language. Any missing mode is a finding (the
#      baseline lint floor does not enforce them). No
#      analysis_options.yaml at all: the NO LINT CONFIGURED line,
#      stated, and the strict check cannot pass, exit 1.
#   2. Migration findings in pubspec.yaml (report L1-15):
#      - a custom_lint dependency: it is no longer actively
#        developed; the official replacement is
#        analysis_server_plugin (Dart 3.10 / Flutter 3.38+).
#        Finding, stated with the replacement named.
#      - a dart_code_metrics dependency: the OSS package is
#        discontinued; its successor DCM is commercial and
#        optional only. Finding, stated.
#   3. Pub get first (tall style is language-versioned, so the
#      format gate must run after dependencies resolve), then:
#      dart format --output=none --set-exit-if-changed .
#   4. Analyze: dart analyze --fatal-infos --fatal-warnings
#      (flutter analyze equivalent flags where flutter is used).
# MODIFY PER PROJECT: lint rules live in analysis_options.yaml,
# not here.
# USAGE: dart-flutter/lint.sh [app-dir]
# EXIT: 0 clean; 1 findings; 2 flutter/dart missing.
set -u
cd "${1:-.}" || exit 2
F="${FLUTTER_BIN:-flutter}"
command -v "$F" >/dev/null 2>&1 || command -v dart >/dev/null 2>&1 || { echo "no flutter/dart" >&2; exit 2; }
fail=0
AO=""
for c in analysis_options.yaml analysis_options.yml; do [ -f "$c" ] && AO="$c"; done
if [ -z "$AO" ]; then
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "finding: no analysis_options.yaml; strict modes cannot be verified (report L1-15)" >&2
  fail=1
else
  for m in strict-casts strict-inference strict-raw-types; do
    grep -Eq "$m:[[:space:]]*true" "$AO" || { echo "finding: analysis_options.yaml does not enable $m (report L1-15)" >&2; fail=1; }
  done
fi
if [ -f pubspec.yaml ]; then
  grep -qE '^[[:space:]]*custom_lint:' pubspec.yaml && echo "finding: custom_lint dependency present; it is no longer actively developed, migrate to analysis_server_plugin (Dart 3.10 / Flutter 3.38+)" >&2 && fail=1
  grep -qE '^[[:space:]]*dart_code_metrics:' pubspec.yaml && echo "finding: dart_code_metrics dependency present; the OSS package is discontinued (successor DCM is commercial, optional only)" >&2 && fail=1
fi
if command -v dart >/dev/null 2>&1; then
  dart pub get >/dev/null 2>&1 || echo "note: dart pub get failed or no pubspec; format runs on the tree as-is (stated)"
  dart format --output=none --set-exit-if-changed . || fail=1
  dart analyze --fatal-infos --fatal-warnings || fail=1
elif command -v "$F" >/dev/null 2>&1; then
  "$F" pub get >/dev/null 2>&1 || true
  "$F" analyze --fatal-infos --fatal-warnings || fail=1
fi
exit "$fail"
