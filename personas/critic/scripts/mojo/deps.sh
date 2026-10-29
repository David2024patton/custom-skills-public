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
#      DECISION 2026-10-29 (lane 6, DECISION.md): advisory-only
#      is KEPT, and the reason is now stronger than beta status.
#      pixi 0.83.0 stable, the current release, does not contain
#      the audit subcommand at all (exact error: "error:
#      unrecognized subcommand 'audit'"); there is nothing to
#      promote. Promotion trigger, both halves required: (a)
#      `pixi audit` ships in a stable pixi release, and (b) a
#      fixture run on the same environment shows its findings
#      match or beat the Syft plus Grype composition in step 1.
#   4. Mode prop (arg 2): the fuzz substitute. A seeded
#      randomised TestSuite harness under AddressSanitizer:
#      test files marked PROPERTY-HARNESS are compiled with
#      mojo build --sanitize address and the resulting binary
#      is executed. This is labelled PROPERTY-STYLE in all
#      output; it is never called coverage-guided, because no
#      Mojo coverage-guided fuzzer exists.
#      FIX 2026-10-29 (lane 6): the previous form ran
#      `mojo run --sanitize address <file>` directly. On the
#      real Mojo 1.2.0 toolchain that fails before any test
#      executes: the JIT session cannot resolve the ASan
#      runtime symbols (exact error in lane 6 RUN-EVIDENCE/
#      mojo-run-sanitize-probe.txt: "JIT session error:
#      Symbols not found: [ __asan_report_load8, ... ]").
#      `mojo build --sanitize address` produces a binary that
#      runs clean on the same fixture, so prop mode builds
#      first, then executes the artifact.
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
  propbin="$(mktemp -d)/prop-harness"
  for f in "${files[@]}"; do
    echo "PROPERTY-STYLE harness (seeded randomised, AddressSanitizer; not coverage-guided): $f"
    # Build with the sanitizer, then execute the artifact. mojo run
    # --sanitize address cannot work: its JIT session lacks the ASan
    # runtime symbols (see header, FIX 2026-10-29).
    # shellcheck disable=SC2086
    if $MOJO build --sanitize address "$f" -o "$propbin"; then
      "$propbin" || fail=1
    else
      fail=1
    fi
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
  echo "pixi audit (ADVISORY ONLY; never decides this gate; decision 2026-10-29, see DECISION.md in lane 6):"
  pixi audit 2>/dev/null || echo "note: pixi audit unavailable in this pixi version (stated)"
fi
echo "GAP: no OSV support for pixi.lock; dependency truth here comes from the SBOM half and exported PyPI locks only (report L1-14)"
[ "$ran" = 0 ] && { echo "DID-NOT-RUN: neither the SBOM half nor an exported-lock scan ran" >&2; exit 2; }
exit "$fail"
