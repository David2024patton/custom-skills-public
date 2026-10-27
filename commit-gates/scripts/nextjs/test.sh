#!/usr/bin/env bash
# PURPOSE: Next.js heavy gate: production build, then project tests.
# STEPS:
#   1. Refuse non-Next projects: if next is not a declared
#      dependency, state that and exit 2.
#   2. Run `npx next build`. This is the real proof a Next.js app
#      compiles and prerenders, and it lives in THIS script (the
#      test slot) because it is the heavy step, not in lint.
#   3. If the build passed and package.json defines a test script,
#      run `npm test`. No test script does NOT fail this gate: the
#      build is the proof here, and the absence is stated out loud.
# COST, stated plainly:
#   - A production build takes minutes on a real app, writes the
#     .next/ directory, and needs whatever build-time environment
#     the app itself requires. A build failing for missing build
#     env is a real failure of this gate.
#   - Since Next.js 16 the build no longer runs linting, so a green
#     build says nothing about lint; that is the lint gate's job.
# MODIFY PER PROJECT: nothing here. Build settings live in the
# project's next.config.* and package.json.
# USAGE: nextjs/test.sh [dir]
# EXIT: 0 build (and tests, when declared) pass; 1 build or tests fail; 2 no npm or not a Next.js project.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies.next)||(p.devDependencies&&p.devDependencies.next)?0:1)" 2>/dev/null \
  || { echo "not a Next.js project: no next dependency declared (stated, not hidden)" >&2; exit 2; }
fail=0
npx next build || fail=1
if [ "$fail" = 0 ]; then
  if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.test?0:1)" 2>/dev/null; then
    npm test || fail=1
  else
    echo "note: no test script in package.json; the build above is this gate's proof (stated, not hidden)"
  fi
fi
exit "$fail"
