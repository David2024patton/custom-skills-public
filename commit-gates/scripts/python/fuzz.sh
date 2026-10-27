#!/usr/bin/env bash
# PURPOSE: Python fuzz lane, Tier 2 (report L1-21): Atheris,
# nightly. Tier 1 everywhere is Hypothesis (see test.sh); this
# lane is the coverage-guided fuzzer where its wheels exist.
# FACTS: Atheris 3.1.0 ships wheels for CPython 3.12 to 3.14 on
# x86_64 Linux. Outside that matrix there is no wheel and the
# lane is exit 2, stated, never a fake run.
# STEPS:
#   1. Platform check: Linux x86_64 and CPython 3.12-3.14, else
#      exit 2 with the matrix named.
#   2. Discover targets: files matching fuzz_*.py or
#      tests/fuzz_*.py that call atheris.Setup / instrument.
#      A target without atheris.instrument_imports() is a
#      finding: coverage guidance needs instrumentation.
#   3. Run each target briefly: python <target> -max_total_time
#      =60 with the libFuzzer flags Atheris passes through.
# MODIFY PER PROJECT: targets are the project's own files.
# USAGE: python/fuzz.sh [dir]
# EXIT: 0 targets clean; 1 crash or missing instrumentation;
# 2 platform outside the wheel matrix, atheris missing, or no
# targets (stated).
set -u
cd "${1:-.}" || exit 2
python3 - <<'PY' || exit 2
import platform, sys
ok = (platform.system() == "Linux" and platform.machine() in ("x86_64", "AMD64")
      and (3, 12) <= sys.version_info[:2] <= (3, 14))
print(f"platform: {platform.system()} {platform.machine()} CPython {platform.python_version()}")
if not ok:
    print("atheris wheels exist only for CPython 3.12-3.14 x86_64 Linux; lane DID-NOT-RUN", file=sys.stderr)
sys.exit(0 if ok else 1)
PY
python3 -c "import atheris" 2>/dev/null || { echo "atheris not installed; lane DID-NOT-RUN" >&2; exit 2; }
targets="$(find . -name 'fuzz_*.py' -not -path './node_modules/*' 2>/dev/null | sort)"
[ -n "$targets" ] || { echo "no fuzz targets (fuzz_*.py) found; lane exit 2, stated" >&2; exit 2; }
fail=0
for t in $targets; do
  grep -q 'instrument_imports' "$t" || { echo "finding: $t lacks atheris.instrument_imports(); coverage guidance requires instrumentation" >&2; fail=1; continue; }
  echo "fuzzing $t (60s)"
  python3 "$t" -max_total_time=60 || fail=1
done
exit "$fail"
