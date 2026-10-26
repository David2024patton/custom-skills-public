#!/usr/bin/env bash
# PURPOSE: JS/TS test gate: run the project's test script.
# MODIFY PER PROJECT: the test runner is the project's choice in
# package.json. A project with no test script fails this gate on
# purpose: add tests, or record the exception in the repo RULES page.
# USAGE: js-ts/test.sh [dir]
# EXIT: 0 pass; 1 fail or no test script; 2 no npm.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.test?0:1)" 2>/dev/null; then
  npm test
else
  echo "no test script in package.json" >&2; exit 1
fi
