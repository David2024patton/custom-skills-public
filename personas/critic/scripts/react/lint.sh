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
# FLAT CONFIG: eslint.config.* is required when eslint is
# declared (inserted enforcement, report L1-22; see the block
# before the exit line).
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
# Flat-config enforcement (report L1-22): ESLint 10 is flat-config
# only. A repo whose eslint setup is legacy-only (.eslintrc*) or
# has eslint declared with NO flat config cannot be running the
# blocking typed rule set; that is a finding, not a pass.
if has_dep eslint; then
  if ! ls eslint.config.js eslint.config.mjs eslint.config.cjs eslint.config.ts eslint.config.mts >/dev/null 2>&1; then
    echo "finding: eslint is declared but no flat config (eslint.config.*) exists; ESLint 10 is flat-config only (report L1-22)" >&2
    fail=1
  fi
fi
# React Compiler-era rules (report L1-24): eslint-plugin-react-hooks
# v7 absorbs the React Compiler rules (immutability, purity, refs,
# set-state-in-effect/render, unsupported-syntax). Those detect
# silent compiler bailouts, so they gate as ERRORS, not warnings.
if has_dep eslint-plugin-react-hooks; then
  hv="$(node -e "const p=require('./package.json');const v=(p.devDependencies&&p.devDependencies['eslint-plugin-react-hooks'])||(p.dependencies&&p.dependencies['eslint-plugin-react-hooks'])||'';const m=String(v).match(/(\d+)/);console.log(m?m[1]:'')" 2>/dev/null)"
  if [ -n "$hv" ] && [ "$hv" -lt 7 ]; then
    echo "finding: eslint-plugin-react-hooks $hv declared; v7 is required for the React Compiler rule set (report L1-24)" >&2
    fail=1
  fi
  cfg="$(ls eslint.config.* 2>/dev/null | head -1)"
  if [ -n "$cfg" ] && ! grep -q 'react-hooks' "$cfg"; then
    echo "finding: eslint-plugin-react-hooks declared but not wired in $cfg; compiler rules are not running" >&2
    fail=1
  fi
  if [ -n "$cfg" ] && grep -E 'react-hooks/' "$cfg" | grep -q "'warn'\|\"warn\""; then
    echo "finding: a react-hooks rule is set to warn in $cfg; compiler rules gate as errors (report L1-24)" >&2
    fail=1
  fi
else
  echo "finding: eslint-plugin-react-hooks is not declared; React Compiler-era rules cannot run (report L1-24)" >&2
  fail=1
fi
exit "$fail"
