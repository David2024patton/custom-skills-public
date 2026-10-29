#!/usr/bin/env bash
# PURPOSE: Go standalone format gate (report L1-03). Format is its
# own gate, separate from lint, so a formatting failure is never
# buried inside a lint report.
# STEPS:
#   1. Run: gofumpt -extra -l .   (-extra is the stricter rule set:
#      it catches what plain gofmt allows.)
#   2. Any file listed is unformatted: exit 1, files named.
#   3. gofumpt missing is exit 2, stated. It is never silently
#      replaced by gofmt: gofmt passing is not this gate passing.
# MODIFY PER PROJECT: none. Fix with: gofumpt -extra -w .
# USAGE: go/format.sh [module-dir]
# EXIT: 0 formatted; 1 unformatted files listed; 2 gofumpt missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
export PATH="$HOME/go/bin:$PATH"
command -v gofumpt >/dev/null 2>&1 || { echo "gofumpt not found (install: go install mvdan.cc/gofumpt@latest)" >&2; exit 2; }
out="$(gofumpt -extra -l .)"
if [ -n "$out" ]; then
  echo "unformatted (gofumpt -extra):" >&2
  echo "$out" >&2
  exit 1
fi
echo "go format: clean (gofumpt -extra)"
