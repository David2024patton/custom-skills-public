#!/usr/bin/env bash
# PURPOSE: TypeScript lint/typecheck gate. Core step: `tsc --noEmit`.
# STEPS:
#   1. Refuse non-TypeScript projects: if there is no tsconfig.json
#      and no typescript dependency, state that and exit 2 (that
#      project belongs to another set).
#   2. Typecheck, from what the target repo declares:
#      a. the project's own typecheck script, when one is defined
#         (monorepos wire turbo/workspaces there);
#      b. else `npx tsc --noEmit` at the root, PLUS `npx tsc --noEmit`
#         in every nested apps/*, packages/*, services/* folder that
#         carries its own tsconfig.json (a root config alone misses
#         per-package configs in a monorepo).
#   3. Lint, from what the target repo declares:
#      a. the project's own lint script, when one is defined;
#      b. else `npx eslint . --max-warnings 0`, when eslint is a
#         declared dependency (--max-warnings 0 so warnings cannot
#         pass green through this gate's own invocation);
#      c. else print the library "NO LINT CONFIGURED" line (step 2
#         still ran and still gates).
# MODIFY PER PROJECT: nothing here; compiler options live in the
# project's tsconfig files, rule sets in its eslint config.
# USAGE: typescript/lint.sh [dir]
# FLAT CONFIG: eslint.config.* is required when eslint is
# declared (inserted enforcement, report L1-22; see the block
# before the exit line).
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm or not a TypeScript project.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
has_script() { node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts['$1']?0:1)" 2>/dev/null; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
if [ ! -f tsconfig.json ] && ! has_dep typescript; then
  echo "not a TypeScript project: no tsconfig.json and no typescript dependency (stated, not hidden)" >&2
  exit 2
fi
if has_script typecheck; then
  npm run typecheck || fail=1
else
  if [ -f tsconfig.json ]; then
    npx tsc --noEmit || fail=1
  else
    echo "note: typescript is a declared dependency but no root tsconfig.json; checking nested configs only"
  fi
  for tc in apps/*/tsconfig.json packages/*/tsconfig.json services/*/tsconfig.json; do
    [ -f "$tc" ] || continue
    ( cd "$(dirname "$tc")" && npx tsc --noEmit ) || fail=1
  done
fi
if has_script lint; then
  npm run lint || fail=1
elif has_dep eslint; then
  npx eslint . --max-warnings 0 || fail=1
else
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no lint script and no eslint dependency in package.json (the tsc typecheck above still ran; add eslint to enforce lint too)"
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

# Type-checked rules enforcement (report L1-22): for TypeScript
# projects, the flat config must wire typescript-eslint
# recommendedTypeChecked with projectService, or the typed rules
# are not running and a green lint proves nothing about them.
if [ -f tsconfig.json ] || has_dep typescript; then
  cfg="$(ls eslint.config.* 2>/dev/null | head -1)"
  if [ -n "$cfg" ]; then
    if ! grep -q 'recommendedTypeChecked' "$cfg" || ! grep -q 'projectService' "$cfg"; then
      echo "finding: $cfg does not wire typescript-eslint recommendedTypeChecked with projectService: true; type-checked lint rules are not in force (report L1-22)" >&2
      fail=1
    fi
  fi
fi
exit "$fail"
