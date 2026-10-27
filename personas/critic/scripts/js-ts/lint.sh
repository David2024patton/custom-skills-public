#!/usr/bin/env bash
# PURPOSE: JS/TS lint gate, driven by what the TARGET repo declares
# in package.json, never by assumption: run the project's own lint
# script when it defines one (eslint/prettier config lives in the
# project); fall back to `npx eslint . --max-warnings 0` (so
# warnings cannot pass green through this gate's own invocation;
# report L1-22/L1-28) when eslint is a declared
# dependency but no lint script exists; and run a TypeScript type
# check ONLY when the repo is a TypeScript repo (a tsconfig.json
# exists or typescript is a declared dependency). A plain-JavaScript
# repo with no tsconfig and no typescript dependency is NEVER failed
# for lacking TypeScript tooling. A TypeScript repo MUST actually be
# typechecked: prefer its own typecheck script when package.json
# defines one (monorepos wire turbo/workspaces there), else run
# `npx tsc --noEmit` at the root and in every nested package that
# carries its own tsconfig.json (turborepo-style apps/*, packages/*).
# MODIFY PER PROJECT: nothing here; rule sets are the project's own
# eslint/prettier configs. If the project has no lint script and no
# eslint dependency, add one to package.json rather than editing
# this file.
# USAGE: js-ts/lint.sh [dir]
# FLAT CONFIG: eslint.config.* is required when eslint is
# declared (inserted enforcement, report L1-22; see the block
# before the exit line).
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
has_script() { node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts['$1']?0:1)" 2>/dev/null; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
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
    for tc in apps/*/tsconfig.json packages/*/tsconfig.json services/*/tsconfig.json; do
      [ -f "$tc" ] || continue
      ( cd "$(dirname "$tc")" && npx tsc --noEmit ) || fail=1
    done
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
