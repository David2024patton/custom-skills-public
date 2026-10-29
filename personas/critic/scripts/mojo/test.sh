#!/usr/bin/env bash
# PURPOSE: Mojo test gate, rebuilt on the TestSuite pattern.
# FACTS this gate is built on (deep-research report L1-12, checked
# 2026-10-27):
#   - `mojo test` was REMOVED in Mojo 1.2.0 stable (2026-10-22).
#     This script never invokes it; an earlier version of this gate
#     did, on a deprecation note, and was broken on arrival.
#   - Current Mojo testing is the in-language TestSuite framework:
#     each test file carries its own main that discovers and runs
#     its tests, and the gate executes the file with `mojo run`.
#   - Pin the exact Mojo version in the project manifest (latest
#     stable at the check date: 1.2.0).
# STEPS:
#   1. Resolve the toolchain: `pixi run mojo` when a pixi.toml is
#      present and pixi is installed, else the mojo binary, else
#      exit 2 (stated).
#   2. Discover test files: every test_*.mojo in the tree
#      (excluding .pixi/ and node_modules/). None found: exit 1,
#      stated; a Mojo project with no tests fails this gate on
#      purpose (add tests, or record the exception in RULES).
#   3. Verify each discovered file carries the TestSuite entry
#      point (a `TestSuite.discover_tests` call, in a main shaped
#      like: def main() raises:
#      TestSuite.discover_tests[__functions_in_module()]().run()).
#      A test_*.mojo without it would run ZERO tests under
#      `mojo run` and still exit 0, which is a green lie: the gate
#      names the file and fails.
#   4. Run each verified file with `mojo run <file>`; any non-zero
#      exit fails the gate. All files run, so one failure does not
#      hide another.
# MODIFY PER PROJECT: none. Filtering a run to a subset is the
# project's own call (`mojo run <file>` with the TestSuite
# --only/--skip flags), not the gate's.
# USAGE: mojo/test.sh [dir]
# EXIT: 0 all discovered suites pass; 1 a suite failed, a file lacks the TestSuite entry point, or no test files exist; 2 mojo toolchain missing.
set -u
cd "${1:-.}" || exit 2
if [ -f pixi.toml ] && command -v pixi >/dev/null 2>&1; then MOJO="pixi run mojo"
elif command -v mojo >/dev/null 2>&1; then MOJO="mojo"
else echo "mojo not found (install Mojo, or pixi with a Mojo project)" >&2; exit 2; fi
mapfile -t files < <(find . -name 'test_*.mojo' -not -path './.pixi/*' -not -path './node_modules/*' | sort)
[ "${#files[@]}" = 0 ] && { echo "no test_*.mojo files found: add TestSuite tests (see this script's header), or record the exception in the repo RULES page" >&2; exit 1; }
fail=0
for f in "${files[@]}"; do
  if ! grep -q 'TestSuite\.discover_tests' "$f"; then
    echo "no TestSuite entry point in $f: without TestSuite.discover_tests in main, mojo run executes zero tests and exits 0 (green lie); add the entry point" >&2
    fail=1
    continue
  fi
  # shellcheck disable=SC2086
  $MOJO run "$f" || fail=1
done
exit "$fail"
