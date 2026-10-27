#!/usr/bin/env bash
# PURPOSE: Go lint gate (report L1-03): go vet as a fast lane, plus
# golangci-lint and staticcheck as MANDATORY lanes. A mandatory tool
# that is missing is exit 2, never a silent skip: a sometimes-gate
# is a green lie (report L1-28).
# STEPS:
#   1. go vet ./... (fast lane, always runs).
#   2. golangci-lint run ./... against the project .golangci.yml.
#      The shipped template (go/golangci.yml in this library) is
#      version "2", linters.default: none, with an explicit enable
#      list. No config in the project: exit 2 with the template
#      named, because without the config the explicit list is not
#      in force. golangci-lint binary missing: exit 2.
#   3. staticcheck -checks="all,-ST1000" ./... (stylecheck ST1000
#      package-comment rule excluded, library-wide convention).
#   4. A separate dead-code pass: staticcheck -checks="U1000" ./...
#      Its findings are reported; unused code in a library module
#      may be public API, so this pass reports but does not fail
#      the gate on its own. It is labelled REPORT-ONLY in output.
#      NilAway is report-only and only runs when the project opts
#      in with a .nilaway-opt-in flag file; absent the flag, that
#      is stated.
# MODIFY PER PROJECT: linter selection lives in the repo's
# .golangci.yml (start from the shipped template), not here.
# USAGE: go/lint.sh [module-dir]
# EXIT: 0 clean; 1 lint findings; 2 go toolchain or a mandatory
# lint tool or the golangci config missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
export PATH="$HOME/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
fail=0
go vet ./... || fail=1
cfg=""
for c in .golangci.yml .golangci.yaml .golangci.toml .golangci.json; do
  [ -f "$c" ] && cfg="$c"
done
if [ -z "$cfg" ]; then
  echo "NO LINT CONFIGURED: no .golangci.yml in this project; the mandatory golangci-lint lane DID NOT RUN (copy the template shipped at go/golangci.yml in this library)" >&2
  exit 2
fi
command -v golangci-lint >/dev/null 2>&1 || { echo "golangci-lint not found: mandatory lint lane DID NOT RUN (install golangci-lint v2)" >&2; exit 2; }
golangci-lint run ./... || fail=1
command -v staticcheck >/dev/null 2>&1 || { echo "staticcheck not found: mandatory lint lane DID NOT RUN" >&2; exit 2; }
staticcheck -checks="all,-ST1000" ./... || fail=1
echo "REPORT-ONLY dead-code pass (staticcheck U1000):"
staticcheck -checks="U1000" ./... || echo "note: U1000 findings above are report-only (public API may be intentionally unused)"
if [ -f .nilaway-opt-in ]; then
  if command -v nilaway >/dev/null 2>&1; then nilaway ./... || echo "note: NilAway is report-only"
  else echo "note: .nilaway-opt-in present but nilaway not installed; NilAway DID NOT RUN (stated)" >&2; fi
else
  echo "note: NilAway report-only lane not opted in (no .nilaway-opt-in file); stated, not hidden"
fi
exit "$fail"
