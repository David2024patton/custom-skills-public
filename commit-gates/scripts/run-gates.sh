#!/usr/bin/env bash
# PURPOSE: Run every applicable commit gate for the repo in the current
# directory: per-language lint + tests + debug check for each language
# detected, then the common secret scan and vulnerability scan.
# MODIFY PER PROJECT: none normally. If the repo has its own gate script
# (for example tools/check.sh), prefer that and use this as the fallback.
# A project may list extra language folders in .gates-extra, one per line.
# USAGE: run-gates.sh [--quick]   (--quick skips tests and the vulnerability scan)
# EXIT: 0 all gates green; 1 a gate failed; 2 a required tool is missing.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
QUICK=0; [ "${1:-}" = "--quick" ] && QUICK=1
fail=0
run() { echo "== $*"; "$@" || fail=1; }

# Language detection
if ls go.mod >/dev/null 2>&1; then
  run "$HERE/go/lint.sh"; run "$HERE/go/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/go/test.sh"
fi
if ls Cargo.toml >/dev/null 2>&1; then
  run "$HERE/rust/lint.sh"; run "$HERE/rust/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/rust/test.sh"
fi
if ls pubspec.yaml >/dev/null 2>&1; then
  run "$HERE/dart-flutter/lint.sh"; run "$HERE/dart-flutter/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/dart-flutter/test.sh"
fi
if ls package.json >/dev/null 2>&1; then
  run "$HERE/js-ts/lint.sh"; run "$HERE/js-ts/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/js-ts/test.sh"
fi
if ls pyproject.toml >/dev/null 2>&1 || ls requirements.txt >/dev/null 2>&1; then
  run "$HERE/python/lint.sh"; run "$HERE/python/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/python/test.sh"
fi
if find . -name '*.sh' -not -path './node_modules/*' | grep -q .; then
  run "$HERE/shell/lint.sh"
fi
run "$HERE/common/secrets-scan.sh"
[ "$QUICK" = 0 ] && run "$HERE/common/vuln-scan.sh"
[ "$fail" = 0 ] && echo "GATES: ALL GREEN" || echo "GATES: RED"
exit "$fail"
