#!/usr/bin/env python3
# exit-check.py - P-02 exit stack checker.
# Steps: read a run-state JSON and test all four exit elements:
#   1. two consecutive clean full passes (full checklist, fresh critics,
#      no lens sampling): clean_full_passes_consecutive >= 2.
#   2. capture-recapture residual at or below the threshold that was
#      recorded BEFORE the exit passes began: threshold_recorded_before
#      must be true, and residual <= threshold.
#   3. planted-seed catch at or above its floor in BOTH exit passes:
#      seed_passes is a list of exactly the last two passes, each with
#      catch_rate and floor.
#   4. coverage denominator printed: coverage object with checks, files,
#      gates_green, suppressions present in the run state (the report
#      prints it; this tool verifies the numbers exist).
# Output: exit-eligible, or "not exit-eligible: [element]" naming every
# missing element. Zero findings alone never passes this check.
# Exit codes: 0 exit-eligible; 1 not exit-eligible; 2 bad input.
# Python 3 standard library only.
import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Exit stack checker (P-02)")
    ap.add_argument("--state", required=True)
    args = ap.parse_args()
    try:
        s = json.loads(Path(args.state).read_text(encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error": f"cannot read run state: {e}"}))
        return 2
    missing = []
    if int(s.get("clean_full_passes_consecutive", 0)) < 2:
        missing.append("two consecutive clean full passes")
    if not s.get("threshold_recorded_before"):
        missing.append("capture-recapture threshold recorded before the exit passes")
    elif s.get("residual") is None or s.get("threshold") is None or float(s["residual"]) > float(s["threshold"]):
        missing.append(f"capture-recapture residual at or below threshold (residual={s.get('residual')}, threshold={s.get('threshold')})")
    passes = s.get("seed_passes", [])
    if len(passes) < 2:
        missing.append("planted-seed catch recorded in both exit passes")
    else:
        for i, p in enumerate(passes[-2:], start=1):
            if float(p.get("catch_rate", 0)) < float(p.get("floor", 1)):
                missing.append(f"planted-seed catch at floor in exit pass {i} (catch={p.get('catch_rate')}, floor={p.get('floor')})")
    cov = s.get("coverage", {})
    if not all(k in cov for k in ("checks", "files", "gates_green", "suppressions")):
        missing.append("coverage denominator printed (checks, files, gates green, suppressions)")
    if missing:
        print("not exit-eligible: " + "; ".join(missing))
        print(json.dumps({"exit_eligible": False, "missing": missing}, indent=2))
        return 1
    cov = s["coverage"]
    print(f"exit-eligible: 0 findings across {cov['checks']} checks times {cov['files']} files, {cov['gates_green']} gates green, {cov['suppressions']} suppressions listed")
    print(json.dumps({"exit_eligible": True, "missing": []}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
