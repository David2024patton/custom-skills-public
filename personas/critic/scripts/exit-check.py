#!/usr/bin/env python3
# exit-check.py - P-02 exit stack checker.
# Two modes. In --run-dir mode the checker DERIVES all four exit elements
# from the run's own tool artifacts and treats the state JSON as an index
# naming where those artifacts live; a number that no artifact supports
# is UNVERIFIED and blocks eligibility. In legacy mode (no --run-dir) the
# caller-supplied state values are trusted as written, and the output
# prints that trust ceiling plainly.
# The four exit elements:
#   1. two consecutive clean full passes (full checklist, fresh critics,
#      no lens sampling). Run-dir derivation: the last two pass verdict
#      artifacts listed in the index, each a JSON with clean and full
#      both true.
#   2. capture-recapture residual at or below the threshold that was
#      recorded BEFORE the exit passes began. Run-dir derivation: the
#      capture artifact (capture-recapture output saved by the run)
#      carries residual, threshold, and threshold_recorded_before as the
#      capture step recorded them.
#   3. planted-seed catch at or above its floor in BOTH exit passes.
#      Run-dir derivation: the last two calibration artifacts (seed-runner
#      reports) listed in the index; the catch rate is read from each
#      report's panel_union. The floor is a policy input read from the
#      index (seed_floor, default 1.0); it is a threshold, not a
#      measurement, so it may be caller-supplied.
#   4. coverage denominator printed: checks, files, gates_green,
#      suppressions. Run-dir derivation: checks counted from the coverage
#      artifact's items; the remaining numbers read from the coverage
#      artifact's top level when the run's tooling recorded them there.
# Output: exit-eligible, or "not exit-eligible: [element]" naming every
# missing and every unverified element. Zero findings alone never passes
# this check.
# Exit codes: 0 exit-eligible; 1 not exit-eligible; 2 bad input.
# Python 3 standard library only.
import argparse, json, sys
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def catch_rate_of(report):
    pu = report.get("panel_union")
    if isinstance(pu, dict):
        if pu.get("rate") is not None:
            return float(pu["rate"])
        if pu.get("total"):
            return float(pu.get("caught", 0)) / float(pu["total"])
    if report.get("catch_rate") is not None:
        return float(report["catch_rate"])
    return None

def derive_from_run_dir(s, run_dir):
    """Return (missing, unverified, derived) reading artifacts, not claims."""
    idx = s.get("artifacts", {})
    missing, unverified, derived = [], [], {}
    def artifact(rel):
        if not rel:
            return None
        p = Path(run_dir) / rel
        if not p.is_file():
            return None
        try:
            return load_json(p)
        except Exception:
            return None
    # 1. clean full passes from pass verdict artifacts
    pass_files = idx.get("passes", [])
    verdicts = [artifact(rel) for rel in pass_files]
    if len(pass_files) < 2 or any(v is None for v in verdicts[-2:]):
        unverified.append("two consecutive clean full passes (pass verdict artifacts absent or unreadable)")
    else:
        last_two = verdicts[-2:]
        derived["clean_full_passes_consecutive"] = 2 if all(
            v.get("clean") is True and v.get("full") is True for v in last_two) else 0
        if derived["clean_full_passes_consecutive"] < 2:
            missing.append("two consecutive clean full passes")
    # 2. capture-recapture from the capture artifact
    cap = artifact(idx.get("capture", "capture-history.json"))
    if cap is None or cap.get("residual") is None:
        unverified.append("capture-recapture residual (capture artifact absent or carries no residual)")
    else:
        derived["residual"] = cap.get("residual")
        derived["threshold"] = cap.get("threshold")
        if cap.get("threshold_recorded_before") is not True:
            missing.append("capture-recapture threshold recorded before the exit passes")
        elif cap.get("threshold") is None or float(cap["residual"]) > float(cap["threshold"]):
            missing.append(f"capture-recapture residual at or below threshold "
                           f"(residual={cap.get('residual')}, threshold={cap.get('threshold')})")
    # 3. seed catch from calibration artifacts
    cal_files = idx.get("calibration", [])
    reports = [artifact(rel) for rel in cal_files]
    floor = float(s.get("seed_floor", 1.0))
    if len(cal_files) < 2 or any(r is None for r in reports[-2:]):
        unverified.append("planted-seed catch recorded in both exit passes (calibration artifacts absent or unreadable)")
    else:
        rates = [catch_rate_of(r) for r in reports[-2:]]
        if any(r is None for r in rates):
            unverified.append("planted-seed catch recorded in both exit passes (a calibration artifact carries no panel catch rate)")
        else:
            derived["seed_catch_rates"] = rates
            for i, r in enumerate(rates, start=1):
                if r < floor:
                    missing.append(f"planted-seed catch at floor in exit pass {i} (catch={r}, floor={floor})")
    # 4. coverage from the coverage artifact
    cov_art = artifact(idx.get("coverage", "coverage.json"))
    if cov_art is None:
        unverified.append("coverage denominator printed (coverage artifact absent)")
    else:
        cov = {}
        items = cov_art.get("items")
        if isinstance(items, dict):
            cov["checks"] = len(items)
        for k in ("checks", "files", "gates_green", "suppressions"):
            if cov_art.get(k) is not None:
                cov[k] = cov_art[k]
        derived["coverage"] = cov
        if not all(k in cov for k in ("checks", "files", "gates_green", "suppressions")):
            unverified.append("coverage denominator printed (coverage artifact lacks "
                              + ", ".join(k for k in ("checks", "files", "gates_green", "suppressions") if k not in cov) + ")")
    return missing, unverified, derived

def main():
    ap = argparse.ArgumentParser(description="Exit stack checker (P-02)")
    ap.add_argument("--state", required=True)
    ap.add_argument("--run-dir", default=None,
                    help="derive every element from this run folder's artifacts; the state file is only an index")
    args = ap.parse_args()
    try:
        s = json.loads(Path(args.state).read_text(encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error": f"cannot read run state: {e}"}))
        return 2
    if args.run_dir:
        missing, unverified, derived = derive_from_run_dir(s, args.run_dir)
        if missing or unverified:
            named = missing + [f"UNVERIFIED: {u}" for u in unverified]
            print("not exit-eligible: " + "; ".join(named))
            print(json.dumps({"exit_eligible": False, "missing": missing,
                              "unverified": unverified, "derived": derived}, indent=2))
            return 1
        cov = derived["coverage"]
        print(f"exit-eligible: derived from run artifacts in {args.run_dir}: "
              f"{cov['checks']} checks, {cov['files']} files, {cov['gates_green']} gates green, "
              f"{cov['suppressions']} suppressions listed")
        print(json.dumps({"exit_eligible": True, "missing": [], "unverified": [],
                          "derived": derived}, indent=2))
        return 0
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
        print(json.dumps({"exit_eligible": False, "missing": missing,
                          "trust_ceiling": "caller-supplied state trusted as written; "
                                           "no run artifacts were opened (use --run-dir to derive)"}, indent=2))
        return 1
    cov = s["coverage"]
    print(f"exit-eligible: 0 findings across {cov['checks']} checks times {cov['files']} files, {cov['gates_green']} gates green, {cov['suppressions']} suppressions listed")
    print(json.dumps({"exit_eligible": True, "missing": [],
                      "trust_ceiling": "caller-supplied state trusted as written; "
                                       "no run artifacts were opened (use --run-dir to derive)"}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
