#!/usr/bin/env bash
# PURPOSE: Go benchmark and mutation lanes, nightly shape (report
# L1-06). These are deliberately NOT per-commit gates: wall-time on
# shared runners is noisy and mutation is slow.
# MODES:
#   smoke (default): go test -run='^$' -bench=. -benchmem
#     -benchtime=1x ./...  (proves benchmarks run and reports
#     allocations; it does not gate on wall time)
#   compare <baseline-file>: rerun benchmarks at -count=10 and
#     benchstat against the baseline. FAILS only on an allocation
#     regression significant at p<0.05. A time regression over 10%
#     at p<0.05 is a printed WARNING, not a failure.
#   mutation: Gremlins, diff-scoped only: gremlins unleash
#     --diff=<base> --threshold-efficacy=80. Never a full-repo
#     per-PR gate. Base ref from GREMLINS_BASE or arg 3.
# MODIFY PER PROJECT: none.
# USAGE: go/bench.sh [module-dir] [smoke|compare <base.txt>|mutation [base-ref]]
# EXIT: 0 pass; 1 regression (allocations) or mutation below
# threshold or benchmarks fail; 2 tool missing for the mode asked.
set -u
cd "${1:-.}" || exit 2
MODE="${2:-smoke}"
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
export PATH="$HOME/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
case "$MODE" in
  smoke)
    go test -run='^$' -bench=. -benchmem -benchtime=1x ./... ;;
  compare)
    BASE="${3:-}"
    [ -n "$BASE" ] && [ -f "$BASE" ] || { echo "compare mode needs an existing baseline file" >&2; exit 2; }
    command -v benchstat >/dev/null 2>&1 || { echo "benchstat not found" >&2; exit 2; }
    NEW="$(mktemp)"
    go test -run='^$' -bench=. -benchmem -count=10 ./... > "$NEW" || exit 1
    out="$(benchstat "$BASE" "$NEW")"
    echo "$out"
    if echo "$out" | grep -E 'allocs/op|B/op' | grep -qE '\+[0-9]+(\.[0-9]+)?%.*\(p=0\.0[0-4]'; then
      echo "FAIL: allocation regression significant at p<0.05" >&2; rm -f "$NEW"; exit 1
    fi
    if echo "$out" | grep -E 'sec/op' | grep -qE '\+1[0-9]+(\.[0-9]+)?%|\+[2-9][0-9]+(\.[0-9]+)?%'; then
      echo "WARNING: time regression over 10% (report-only on shared runners)"
    fi
    rm -f "$NEW" ;;
  mutation)
    command -v gremlins >/dev/null 2>&1 || { echo "gremlins not found (nightly lane tool)" >&2; exit 2; }
    BASE="${3:-${GREMLINS_BASE:-main}}"
    gremlins unleash --diff="$BASE" --threshold-efficacy=80 ;;
  *) echo "unknown mode: $MODE" >&2; exit 2 ;;
esac
