#!/usr/bin/env bash
# PURPOSE: React component-stack lint gate, detection-driven.
# STEPS:
#   1. Refuse non-React projects: if react is not a declared
#      dependency, state that and exit 2.
#   2. Note which react eslint plugins the project declares
#      (eslint-plugin-react, eslint-plugin-react-hooks). Their rules
#      are enforced by the PROJECT's own eslint config (flat config
#      eslint.config.*); this gate never installs or imposes react
#      rules a project did not declare.
#   3. Lint, from what the target repo declares:
#      a. the project's own lint script, when one is defined;
#      b. else `npx eslint . --max-warnings 0`, when eslint is a
#         declared dependency (--max-warnings 0 so warnings cannot
#         pass green through this gate's own invocation);
#      c. else print the library "NO LINT CONFIGURED" line.
#   4. Typecheck ONLY when the project is TypeScript (tsconfig.json
#      exists or typescript is a declared dependency): the project's
#      typecheck script, else `npx tsc --noEmit`. A plain-JavaScript
#      React project is never failed for lacking TypeScript tooling;
#      the skip is stated out loud.
# MODIFY PER PROJECT: nothing here; rule sets are the project's own
# eslint config. Add the react plugins to the project's eslint
# config rather than editing this file.
# USAGE: react/lint.sh [dir]
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm or not a React project.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
has_script() { node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts['$1']?0:1)" 2>/dev/null; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
has_dep react || { echo "not a React project: no react dependency declared (stated, not hidden)" >&2; exit 2; }
if has_dep eslint-plugin-react || has_dep eslint-plugin-react-hooks; then
  echo "note: project declares react eslint plugin(s); its own eslint config enforces the react/react-hooks rules"
else
  echo "note: no eslint-plugin-react or eslint-plugin-react-hooks declared; react-specific rules not enforced (stated, not hidden)"
fi
if has_script lint; then
  npm run lint || fail=1
elif has_dep eslint; then
  npx eslint . --max-warnings 0 || fail=1
else
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no lint script and no eslint dependency in package.json (add eslint; stated, not hidden)"
fi
if [ -f tsconfig.json ] || has_dep typescript; then
  if has_script typecheck; then
    npm run typecheck || fail=1
  else
    npx tsc --noEmit || fail=1
  fi
else
  echo "note: no TypeScript declared (no tsconfig.json, no typescript dependency); type check skipped (stated, not hidden)"
fi
exit "$fail"
