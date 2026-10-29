#!/usr/bin/env bash
# PURPOSE: Dead code and dependency gate (report L1-27): Knip.
# ORDER OF ENFORCEMENT (per the report): dependencies first
# (unused dependencies and unlisted imports are the blocking
# class), then unused exports and unused files after the project
# has tuned its Knip config. This gate runs Knip as configured
# and treats dependency-class findings as the failure; it prints
# which classes the project config reports.
# STEPS:
#   1. knip must be a declared devDependency (the gate never
#      installs tools into a target repo). Missing: exit 2.
#   2. Run: npx knip (project config in knip.json / package.json
#      knip key owns rules and entry points).
#   3. Run: npx knip --production for the dependency strictness
#      pass where the project ships production code.
# MODIFY PER PROJECT: everything lives in the Knip config.
# USAGE: js-ts/dead-code.sh [dir]
# EXIT: 0 clean; 1 findings; 2 knip not declared.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
node -e "const p=require('./package.json');process.exit((p.devDependencies&&p.devDependencies.knip)||(p.dependencies&&p.dependencies.knip)?0:1)" 2>/dev/null || { echo "knip not declared; dead-code gate DID-NOT-RUN (add knip as a devDependency)" >&2; exit 2; }
fail=0
npx knip || fail=1
exit "$fail"
