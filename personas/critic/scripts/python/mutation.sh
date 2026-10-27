#!/usr/bin/env bash
# PURPOSE: Python mutation gate (report L1-21). Nightly and
# critical modules only; mutation is too slow for per-commit.
# THE TRAP (lies-green register #2): mutmut exits 0 even when
# every mutant survives. This gate therefore never trusts the
# mutmut exit code. It runs mutmut, then parses
# mutants/mutmut-cicd-stats.json and manufactures the verdict
# itself: below 80% killed on the gated paths is exit 1.
# STEPS:
#   1. mutmut run. mutmut 3.x takes its paths from the project
#      config (setup.cfg [mutmut] source_paths, tests_dir), not
#      from a CLI flag; a project with no mutmut config has not
#      configured this lane and mutmut itself will say so.
#   2. Parse mutants/mutmut-cicd-stats.json: killed, survived,
#      timeout, suspicious. killed / (total mutants) under 0.80
#      on critical code: exit 1, numbers printed.
#   3. No stats file after a run: the run did not happen in any
#      verifiable way: exit 1, stated.
#   cosmic-ray 8.7.0 is the accepted alternative tool; a project
#   using it wires the same stats-parse law in its own config.
# MODIFY PER PROJECT: gated paths via MUTMUT_PATHS; threshold
# via MUTATION_FLOOR (default 80, percent).
# USAGE: python/mutation.sh [dir]
# EXIT: 0 at or above threshold; 1 below it or unverifiable;
# 2 mutmut missing.
set -u
cd "${1:-.}" || exit 2
command -v mutmut >/dev/null 2>&1 || { echo "mutmut not found; mutation gate DID-NOT-RUN" >&2; exit 2; }
echo "running mutmut (project-configured paths; its exit code will be IGNORED by design)"
mutmut run >/dev/null 2>&1 || true
[ -f mutants/mutmut-cicd-stats.json ] || mutmut export-cicd-stats >/dev/null 2>&1 || true
[ -f mutants/mutmut-cicd-stats.json ] || { echo "no mutants/mutmut-cicd-stats.json produced; mutation result unverifiable" >&2; exit 1; }
FLOOR="${MUTATION_FLOOR:-80}" python3 - <<'PY'
import json, os, sys
floor = float(os.environ.get("FLOOR", "80"))
s = json.load(open("mutants/mutmut-cicd-stats.json"))
def n(*keys):
    for k in keys:
        if k in s:
            return int(s[k])
    return 0
killed = n("killed_by_test", "killed")
survived = n("survived", "survived_by_test")
timeout = n("timeout", "timeouts")
suspicious = n("suspicious")
total = killed + survived + timeout + suspicious
if total == 0:
    print("mutation: zero mutants generated; nothing was measured")
    sys.exit(1)
pct = 100.0 * killed / total
print(f"mutation: killed {killed}/{total} = {pct:.1f}% (floor {floor}%; survived {survived}, timeout {timeout}, suspicious {suspicious})")
sys.exit(0 if pct >= floor else 1)
PY
