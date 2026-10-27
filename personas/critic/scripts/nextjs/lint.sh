#!/usr/bin/env bash
# PURPOSE: Next.js lint + typecheck gate. Lint is ESLint DIRECTLY,
# on every Next.js version.
# FACTS this gate is built on (Next.js docs and deep-research
# report L1-25, checked 2026-10-27):
#   - `next lint` was deprecated in Next.js 15.5 and REMOVED in
#     16.0 (the CLI then treats `lint` as a project directory).
#     This gate NEVER invokes it, on any version: a fallback to a
#     removed command is a lies-green mode (report L1-28), and
#     pre-16 projects have the same direct-ESLint path available
#     through their declared eslint-config-next setup.
#   - ESLint 10 is flat-config only; on ESLint 9/10 the project's
#     eslint.config.* spreads eslint-config-next. On older ESLint
#     the project's own declared CLI reads its legacy config. The
#     gate runs the project's declared ESLint either way.
#   - `next typegen` (generated route types) was added in 15.5.
# STEPS:
#   1. Refuse non-Next projects: if next is not a declared
#      dependency, state that and exit 2.
#   2. Read the declared Next.js major/minor version from
#      package.json (used for the typegen step and notes only;
#      lint does not branch on it).
#   3. Config honesty (report L1-25): if a next.config.* file sets
#      typescript.ignoreBuildErrors or eslint.ignoreDuringBuilds
#      to true, that is a finding and fails the gate: a build that
#      ignores its own errors is a green lie.
#   4. Lint, ESLint directly:
#      a. the project's own lint script, when one is defined;
#      b. else `npx eslint . --max-warnings 0` when eslint is a
#         declared dependency (--max-warnings 0 so warnings cannot
#         pass green through this gate's own invocation);
#      c. else print the library "NO LINT CONFIGURED" line.
#   5. Typecheck, ONLY for TypeScript projects (tsconfig.json or
#      typescript dependency):
#      a. the project's own typecheck script, when one is defined;
#      b. else `npx next typegen` first when the declared version
#         provides it (15.5+), then `npx tsc --noEmit`.
#      Plain-JavaScript Next projects skip this step, stated.
# MODIFY PER PROJECT: nothing here; rule sets are the project's own
# eslint config, compiler options its tsconfig.
# USAGE: nextjs/lint.sh [dir]
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm or not a Next.js project.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
has_script() { node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts['$1']?0:1)" 2>/dev/null; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
has_dep next || { echo "not a Next.js project: no next dependency declared (stated, not hidden)" >&2; exit 2; }
ver="$(node -e "const p=require('./package.json');const v=(p.dependencies&&p.dependencies.next)||(p.devDependencies&&p.devDependencies.next)||'';const m=String(v).match(/(\d+)\.(\d+)/);console.log(m?m[1]+' '+m[2]:'')" 2>/dev/null)"
major=""; minor=""
if [ -n "$ver" ]; then major="${ver%% *}"; minor="${ver##* }"; fi
for cfg in next.config.js next.config.mjs next.config.ts next.config.cjs; do
  [ -f "$cfg" ] || continue
  if grep -qE 'ignoreBuildErrors[[:space:]]*:[[:space:]]*true|ignoreDuringBuilds[[:space:]]*:[[:space:]]*true' "$cfg"; then
    echo "finding: $cfg sets ignoreBuildErrors/ignoreDuringBuilds to true; builds that ignore their own errors are a green lie (report L1-25)" >&2
    fail=1
  fi
done
if [ -n "$major" ]; then
  echo "note: declared Next.js $major.$minor; lint runs ESLint directly (next lint is never invoked: deprecated 15.5, removed 16.0)"
else
  echo "note: could not parse a numeric Next.js version from package.json; lint runs ESLint directly (next lint is never invoked on any version)"
fi
if has_script lint; then
  npm run lint || fail=1
elif has_dep eslint; then
  npx eslint . --max-warnings 0 || fail=1
else
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no lint script and no eslint dependency in package.json (add eslint with eslint-config-next; stated, not hidden)"
fi
if [ -f tsconfig.json ] || has_dep typescript; then
  if has_script typecheck; then
    npm run typecheck || fail=1
  else
    if [ -n "$major" ] && { [ "$major" -gt 15 ] || { [ "$major" -eq 15 ] && [ "$minor" -ge 5 ]; }; }; then
      npx next typegen || fail=1
    else
      echo "note: declared Next.js version does not provide next typegen (added in 15.5); typechecking without generated route types"
    fi
    npx tsc --noEmit || fail=1
  fi
else
  echo "note: no TypeScript declared (no tsconfig.json, no typescript dependency); typegen/type check skipped (stated, not hidden)"
fi
exit "$fail"
