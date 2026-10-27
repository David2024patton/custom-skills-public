#!/usr/bin/env bash
# PURPOSE: Go test gate, unified invocation (report L1-02). Both gate
# runners in this library now run the exact same command so a green
# local run and a green audit run mean the same thing.
# STEPS:
#   1. Run: go test -race -count=1 -shuffle=on -timeout=10m ./...
#      -race: the race detector only sees races that execute.
#      -count=1: kills the cached-green trap (a cached pass is not
#      a run). -shuffle=on: exposes order-dependent tests.
#   2. When COVERAGE=1 is set in the environment, add
#      -covermode=atomic -coverprofile=coverage.out (atomic is the
#      only covermode that is safe under -race and parallel tests).
# CHECKLIST (critic, even when this gate passes): t.Parallel without
# isolation, shared mutable globals across tests, and time.Sleep used
# as synchronisation are findings; a passing race run does not clear
# them.
# MODIFY PER PROJECT: none.
# USAGE: go/test.sh [module-dir]
# EXIT: 0 pass; 1 fail; 2 go toolchain missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
if [ "${COVERAGE:-0}" = 1 ]; then
  go test -race -count=1 -shuffle=on -timeout=10m -covermode=atomic -coverprofile=coverage.out ./...
else
  go test -race -count=1 -shuffle=on -timeout=10m ./...
fi
