#!/usr/bin/env bash
# PURPOSE: Go lint gate: format, vet, and (when installed) golangci-lint
# and staticcheck. Warnings are failures.
# MODIFY PER PROJECT: linter selection lives in the repo's .golangci.yml,
# not here. Toolchain: this VM keeps Go at ~/goroot/go/bin; the script
# adds it to PATH when present.
# USAGE: go/lint.sh [module-dir]   (default: current directory)
# EXIT: 0 clean; 1 lint findings; 2 go toolchain missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
fail=0
out="$(gofmt -l .)" && [ -z "$out" ] || { echo "gofmt: $out"; fail=1; }
go vet ./... || fail=1
golangci_configured=0
for cfg in .golangci.yml .golangci.yaml .golangci.toml .golangci.json; do
  [ -f "$cfg" ] && golangci_configured=1
done
if [ "$golangci_configured" = 0 ]; then
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no golangci-lint config (.golangci.yml or sibling) in this project; gofmt and go vet above still ran, golangci-lint did not (stated, not hidden)"
elif command -v golangci-lint >/dev/null 2>&1; then golangci-lint run || fail=1
else echo "note: golangci-lint not installed, skipped (stated, not hidden)"; fi
if command -v staticcheck >/dev/null 2>&1; then staticcheck ./... || fail=1; fi
exit "$fail"
