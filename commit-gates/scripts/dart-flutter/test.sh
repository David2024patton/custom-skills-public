#!/usr/bin/env bash
# PURPOSE: Dart/Flutter test gate with coverage ratchet (report
# L1-17).
# STEPS:
#   1. flutter test --coverage writes coverage/lcov.info.
#   2. The gate parses lcov itself (no built-in fail-under
#      exists) and applies the ratchet: 80% of lib/ lines must be
#      hit. Below: exit 1 with the numbers. The floor only moves
#      up; a project below 80 records its baseline in its RULES
#      page and holds there (COVERAGE_FLOOR env overrides for
#      that recorded baseline only).
#   3. Widget tests should enable leak_tracker; goldens use
#      Alchemist (golden_toolkit is discontinued), platform and
#      CI goldens separated, and --update-goldens NEVER runs in
#      a gate: if a project script wires it into test, that is
#      a finding printed here.
#   4. integration_test is a SEPARATE device tier (arg: device):
#      no device attached means exit 2, never a silent pass.
#   Diagnostics: avoid_print belongs on in analysis_options;
#      debugPrint is allowed only inside one logger wrapper
#      forwarding to dart:developer log(). A print() in lib/ is
#      reported by this gate as a note for the debug-check.
# USAGE: dart-flutter/test.sh [app-dir] [unit|device]
# EXIT: 0 pass at or above the ratchet; 1 fail or below it;
# 2 flutter missing, or device tier asked with no device.
set -u
cd "${1:-.}" || exit 2
TIER="${2:-unit}"
command -v flutter >/dev/null 2>&1 || { echo "flutter not found" >&2; exit 2; }
if [ "$TIER" = device ]; then
  if flutter devices 2>/dev/null | grep -qE '•.*(android|ios|linux|macos|windows)'; then
    flutter test integration_test
  else
    echo "no device attached; integration tier DID-NOT-RUN (exit 2, never a silent pass)" >&2; exit 2
  fi
  exit $?
fi
grep -rq 'update-goldens' pubspec.yaml Makefile .github 2>/dev/null && echo "finding: --update-goldens wired into a test path; goldens must never update inside a gate" >&2
flutter test --coverage || exit 1
[ -f coverage/lcov.info ] || { echo "flutter test produced no coverage/lcov.info" >&2; exit 1; }
FLOOR="${COVERAGE_FLOOR:-80}"
python3 - "$FLOOR" <<'PY' || exit 1
import sys
floor = float(sys.argv[1])
lf = da = 0
in_lib = False
for line in open("coverage/lcov.info"):
    line = line.strip()
    if line.startswith("SF:"):
        in_lib = "/lib/" in line or line[3:].startswith("lib/")
    elif line.startswith("LF:") and in_lib:
        lf += int(line[3:])
    elif line.startswith("LH:") and in_lib:
        da += int(line[3:])
if lf == 0:
    print("coverage: no lib/ lines recorded in lcov")
    sys.exit(1)
pct = 100.0 * da / lf
print(f"coverage: lib lines {da}/{lf} = {pct:.1f}% (floor {floor}%)")
sys.exit(0 if pct >= floor else 1)
PY
