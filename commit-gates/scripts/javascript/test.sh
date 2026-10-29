#!/usr/bin/env bash
# PURPOSE: JavaScript (plain ESM Node) test gate.
# STEPS:
#   1. If package.json defines a test script, run `npm test`. The
#      runner is whatever the project declares (node --test, vitest,
#      jest); this gate picks no runner and installs nothing.
#   2. No test script: fail on purpose (exit 1). Add tests, or
#      record the exception in the repo RULES page.
# MODIFY PER PROJECT: the test runner is the project's choice in
# package.json.
# USAGE: javascript/test.sh [dir]
# EXIT: 0 pass; 1 fail or no test script; 2 no npm.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.test?0:1)" 2>/dev/null; then
  npm test
else
  echo "no test script in package.json" >&2; exit 1
fi
