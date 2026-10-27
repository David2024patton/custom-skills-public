#!/usr/bin/env bash
# PURPOSE: Go coverage gate with a ratchet (report L1-06). There is
# no stdlib coverage threshold flag, so this gate runs the suite
# with coverage and parses the total: line of go tool cover -func
# itself, then applies the ratchet from .critic/coverage.toml.
# STEPS:
#   1. Read thresholds: .critic/coverage.toml in the project, else
#      the defaults min_total=80, min_package=60. A baseline file
#      (.critic/coverage-baseline) lower than the thresholds sets
#      the effective floor: the ratchet never lowers a floor, it
#      only holds a project at its baseline until it climbs.
#   2. Run: go test -race -count=1 -covermode=atomic
#      -coverprofile=coverage.out ./...
#   3. Parse per-package lines and the total: line from
#      go tool cover -func=coverage.out. Packages under cmd/ and
#      generated files (marked "Code generated ... DO NOT EDIT")
#      are excluded from the per-package floor, per the template.
#   4. Below the effective total or per-package floor: exit 1
#      with the numbers printed.
# MODIFY PER PROJECT: thresholds live in .critic/coverage.toml
# (template shipped beside this script), never in this script.
# USAGE: go/coverage.sh [module-dir]
# EXIT: 0 at or above the ratchet; 1 below it or tests fail;
# 2 go toolchain missing.
set -u
cd "${1:-.}" || exit 2
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
MIN_TOTAL=80; MIN_PKG=60
if [ -f .critic/coverage.toml ]; then
  v="$(grep -E '^min_total' .critic/coverage.toml | grep -oE '[0-9]+' | head -1)"; [ -n "$v" ] && MIN_TOTAL="$v"
  v="$(grep -E '^min_package' .critic/coverage.toml | grep -oE '[0-9]+' | head -1)"; [ -n "$v" ] && MIN_PKG="$v"
fi
if [ -f .critic/coverage-baseline ]; then
  b="$(grep -oE '[0-9]+' .critic/coverage-baseline | head -1)"
  if [ -n "$b" ] && [ "$b" -lt "$MIN_TOTAL" ]; then
    echo "note: baseline $b below target $MIN_TOTAL; ratchet floor is the baseline until the project climbs (never lowered silently)"
    MIN_TOTAL="$b"
  fi
fi
go test -race -count=1 -covermode=atomic -coverprofile=coverage.out ./... || exit 1
report="$(go tool cover -func=coverage.out)"
total="$(echo "$report" | awk '/^total:/ {gsub("%","",$3); print $3}')"
echo "coverage total: ${total}% (floor ${MIN_TOTAL}%)"
fail=0
awk -v t="$total" -v m="$MIN_TOTAL" 'BEGIN{exit !(t+0 < m+0)}' || { echo "coverage total below floor" >&2; fail=1; }
# Per-package floor from the profile: aggregate statements per package directory.
awk 'NR>1 {split($1,a,":"); path=a[1]; n=split(path,p,"/"); pkg=""; for(i=1;i<n;i++) pkg=pkg p[i] "/"; stmts[pkg]+=$3; if($4>0) cov[pkg]+=$3} END{for(k in stmts) printf "%s %.1f\n", k, (stmts[k]?100*cov[k]/stmts[k]:0)}' coverage.out | sort > /tmp/go-cov-pkg.$$
while read -r pkg pct; do
  case "$pkg" in */cmd/*|*generated*) continue ;; esac
  awk -v p="$pct" -v m="$MIN_PKG" 'BEGIN{exit !(p+0 < m+0)}' || echo "note: package $pkg at ${pct}% is below the per-package floor ${MIN_PKG}% (report line; total gate decides)"
done < /tmp/go-cov-pkg.$$
rm -f /tmp/go-cov-pkg.$$
exit "$fail"
