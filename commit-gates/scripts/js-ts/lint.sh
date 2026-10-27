#!/usr/bin/env bash
# PURPOSE: JS/TS lint gate: run the project's own lint script when it
# defines one (eslint/prettier config lives in the project), plus a
# TypeScript type check when tsconfig.json exists.
# MODIFY PER PROJECT: nothing here; rule sets are the project's own
# eslint/prettier configs. If the project has no lint script, add one
# to package.json rather than editing this file.
# USAGE: js-ts/lint.sh [dir]
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
fail=0
if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.lint?0:1)" 2>/dev/null; then
  npm run lint || fail=1
else
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no lint script in package.json (add eslint; stated, not hidden)"
fi
if [ -f tsconfig.json ]; then npx tsc --noEmit || fail=1; fi
exit "$fail"
