#!/usr/bin/env bash
# PURPOSE: Go test gate: full test suite with the race detector.
# MODIFY PER PROJECT: none. Packages that cannot run under race (rare)
# are excluded per package with a comment in the test file, not here.
# USAGE: go/test.sh [module-dir]
# EXIT: 0 pass; 1 fail; 2 go toolchain missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
go test -race ./...
