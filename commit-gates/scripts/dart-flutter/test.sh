#!/usr/bin/env bash
# PURPOSE: Dart/Flutter test gate.
# MODIFY PER PROJECT: golden tests and device tests belong to the
# project's own test setup; this runs the unit/widget suite.
# USAGE: dart-flutter/test.sh [app-dir]
# EXIT: 0 pass; 1 fail; 2 flutter missing.
set -u
cd "${1:-.}" || exit 2
command -v flutter >/dev/null 2>&1 || { echo "flutter not found" >&2; exit 2; }
flutter test
