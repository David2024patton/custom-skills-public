#!/usr/bin/env bash
# PURPOSE: React test gate.
# STEPS:
#   1. If package.json defines a test script, run `npm test`. The
#      runner and environment are whatever the project declares
#      (vitest or jest, with jsdom and @testing-library/react when
#      the project declares them in its own config/devDependencies).
#   2. No test script: fail on purpose (exit 1). Add tests, or
#      record the exception in the repo RULES page.
#   3. This gate never installs or imposes a test environment the
#      project did not declare.
# MODIFY PER PROJECT: runner, jsdom/testing-library setup, and
# setup files are the project's choice.
# USAGE: react/test.sh [dir]
# EXIT: 0 pass; 1 fail or no test script; 2 no npm.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.test?0:1)" 2>/dev/null; then
  npm test
else
  echo "no test script in package.json" >&2; exit 1
fi
