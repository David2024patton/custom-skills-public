#!/usr/bin/env bash
# PURPOSE: Dart/Flutter vulnerability gate (report L1-16). There
# is no `dart pub audit`. The hard gate is osv-scanner over
# pubspec.lock (package_config.json accepted as the resolved
# lock equivalent).
# STEPS:
#   1. Require a lock: pubspec.lock (or .dart_tool/
#      package_config.json). No lock: exit 2, stated; an
#      unresolved dependency set cannot be scanned honestly.
#   2. osv-scanner over the lock; any vulnerability fails.
#   3. Print the ecosystem gap line every run:
#      ECOSYSTEM-GAP: Dart SAST. Semgrep Dart support is
#      experimental and advisory only, CodeQL has no Dart; this
#      gate claims dependency scanning, not SAST coverage.
# MODIFY PER PROJECT: suppressions live in the osv-scanner
# config in the repo, with reason and date, never here.
# USAGE: dart-flutter/vuln.sh [app-dir]
# EXIT: 0 no known vulns; 1 vulns found; 2 osv-scanner or lock
# missing (DID-NOT-RUN, stated).
set -u
cd "${1:-.}" || exit 2
command -v osv-scanner >/dev/null 2>&1 || { echo "osv-scanner not found; Dart vuln gate DID-NOT-RUN" >&2; exit 2; }
echo "ECOSYSTEM-GAP: Dart SAST (Semgrep Dart is experimental-advisory; CodeQL has no Dart). This gate is dependency scanning only."
if [ -f pubspec.lock ]; then
  osv-scanner --lockfile pubspec.lock
elif [ -f .dart_tool/package_config.json ]; then
  osv-scanner --lockfile .dart_tool/package_config.json
else
  echo "no pubspec.lock or package_config.json; run pub get first (DID-NOT-RUN)" >&2; exit 2
fi
