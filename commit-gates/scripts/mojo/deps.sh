#!/usr/bin/env bash
# PURPOSE: Mojo dependency lane and property harness (report
# L1-14). Pixi has no built-in vulnerability scanner and
# osv-scanner does not support pixi.lock, so the lane is a
# composition, stated honestly:
# STEPS:
#   1. Syft over the Pixi environment (.pixi/envs/default) into a
#      CycloneDX SBOM, then Grype over that SBOM. Grype's
#      database max-age discipline applies: a stale DB is stated
#      and the result is provisional. Either tool missing: that
#      half is DID-NOT-RUN (exit 2 if neither ran).
#   2. osv-scanner over exported PyPI lockfiles when the project
#      carries them (requirements*.txt, uv.lock, poetry.lock,
#      Pipfile.lock beside pixi.toml).
#   3. `pixi audit`, when pixi offers it, is printed ADVISORY
#      ONLY (it is beta): it never decides this gate.
#   4. Mode prop (arg 2): the fuzz substitute. A seeded
#      randomised TestSuite harness under AddressSanitizer:
#      test files marked PROPERTY-HARNESS run via mojo run with
#      the sanitizer build. This is labelled PROPERTY-STYLE in
#      all output; it is never called coverage-guided, because
#      no Mojo coverage-guided fuzzer exists.
# EXPLICIT GAP LINES (also in SKILL.md, report L1-14): no Mojo
# linter, no Mojo SAST tool, no Mojo coverage tool, no OSV
# support for pixi.lock, no coverage-guided Mojo fuzzer, as of
# October 2026.
# USAGE: mojo/deps.sh [dir] [deps|prop]
# EXIT: 0 clean; 1 findings or harness failure; 2 a required
# tool missing (stated per half).
set -u
cd "${1:-.}" || exit 2
MODE="${2:-deps}"
if [ "$MODE" = prop ]; then
  if [ -f pixi.toml ] && command -v pixi >/dev/null 2>&1; then MOJO="pixi run mojo"
  elif command -v mojo >/dev/null 2>&1; then MOJO="mojo"
  else echo "mojo not found" >&2; exit 2; fi
  mapfile -t files < <(grep -rl 'PROPERTY-HARNESS' --include='test_*.mojo' . 2>/dev/null | sort)
  [ "${#files[@]}" = 0 ] && { echo "no PROPERTY-HARNESS TestSuite files found (lane exit 2: harness missing, not a pass)" >&2; exit 2; }
  fail=0
  for f in "${files[@]}"; do
    echo "PROPERTY-STYLE harness (seeded randomised, AddressSanitizer; not coverage-guided): $f"
    # shellcheck disable=SC2086
    $MOJO run --sanitize address "$f" || fail=1
  done
  exit "$fail"
fi
ran=0; fail=0
if command -v syft >/dev/null 2>&1 && command -v grype >/dev/null 2>&1; then
  if [ -d .pixi/envs/default ]; then
    ran=1
    syft packages dir:.pixi/envs/default -o cyclonedx-json > /tmp/mojo-sbom.json 2>/dev/null || fail=1
    grype sbom:/tmp/mojo-sbom.json || fail=1
  else
    echo "note: no .pixi/envs/default environment present; Syft/Grype half skipped (stated)"
  fi
else
  echo "note: syft/grype not both installed; SBOM half DID NOT RUN (stated)"
fi
for lock in requirements.txt requirements-dev.txt uv.lock poetry.lock Pipfile.lock; do
  if [ -f "$lock" ] && command -v osv-scanner >/dev/null 2>&1; then
    ran=1; osv-scanner --lockfile "$lock" || fail=1
  fi
done
if command -v pixi >/dev/null 2>&1; then
  echo "pixi audit (ADVISORY ONLY, beta; never decides this gate):"
  pixi audit 2>/dev/null || echo "note: pixi audit unavailable in this pixi version (stated)"
fi
echo "GAP: no OSV support for pixi.lock; dependency truth here comes from the SBOM half and exported PyPI locks only (report L1-14)"
[ "$ran" = 0 ] && { echo "DID-NOT-RUN: neither the SBOM half nor an exported-lock scan ran" >&2; exit 2; }
exit "$fail"
