#!/usr/bin/env bash
# PURPOSE: Go fuzz lanes (report L1-05).
# STEPS:
#   1. Detect fuzz targets: grep for ^func Fuzz[A-Z] in *_test.go.
#   2. No targets at all: if the module has parser or decoder
#      surfaces (files matching parse/decode/unmarshal/codec in
#      non-test sources), that absence is a checklist finding and
#      this lane exits 2 (target-missing is not a pass). With no
#      targets and no such surface, exit 0 with the absence stated.
#   3. PR smoke (default): per target, go test -run='^$'
#      -fuzz='^<Target>$' -fuzztime=30s <pkg>.
#   4. Nightly mode (arg: nightly): -fuzztime=10m per target.
#   Committed seed corpora under testdata/fuzz already run as
#   regression tests under the normal test gate; this lane is the
#   active fuzzing on top of that.
# MODIFY PER PROJECT: none.
# USAGE: go/fuzz.sh [module-dir] [smoke|nightly]
# EXIT: 0 all targets clean (or no surface, stated); 1 a fuzz run
# found a failure; 2 go missing, or fuzz targets missing on a
# parser/decoder surface.
set -u
cd "${1:-.}" || exit 2
MODE="${2:-smoke}"
[ -x "$HOME/goroot/go/bin/go" ] && PATH="$HOME/goroot/go/bin:$PATH"
command -v go >/dev/null 2>&1 || { echo "go not found" >&2; exit 2; }
case "$MODE" in nightly) DUR=10m ;; *) DUR=30s ;; esac
targets="$(grep -rhoE '^func (Fuzz[A-Z][A-Za-z0-9_]*)' --include='*_test.go' . 2>/dev/null | awk '{print $2}' | sort -u)"
if [ -z "$targets" ]; then
  if grep -rliE 'pars|decod|unmarshal|codec' --include='*.go' . 2>/dev/null | grep -v '_test\.go' | grep -q .; then
    echo "FINDING: no fuzz targets, but this module has parser/decoder surfaces; add a fuzz target (lane exit 2: target missing, not a pass)" >&2
    exit 2
  fi
  echo "no fuzz targets and no parser/decoder surface detected (stated, not hidden)"
  exit 0
fi
fail=0
for t in $targets; do
  pkg="$(grep -rl "^func $t" --include='*_test.go' . | head -1 | xargs -r dirname)"
  echo "fuzz $t in ./$pkg ($MODE, $DUR)"
  go test -run='^$' -fuzz="^${t}$" -fuzztime="$DUR" "./$pkg" || fail=1
done
exit "$fail"
