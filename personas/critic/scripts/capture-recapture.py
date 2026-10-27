#!/usr/bin/env python3
# capture-recapture.py - P-02 exit instrument: residual defect estimation.
# Steps:
#   1. Read a capture history JSON: {"captures": {"C1": [fingerprint, ...],
#      "C2": [...], ...}} over JUDGMENT findings only (deterministic
#      findings have capture probability near 1 and poison the overlap
#      statistics; the caller filters them out, see P-06).
#   2. Refuse to compute with fewer than four critics (exit 2): with
#      fewer inspectors no model is sufficiently accurate.
#   3. Build the capture distribution f1..fk (defects seen by exactly i
#      critics), check strict order sanity (f counts non-negative, sum of
#      i times fi equals total captures).
#   4. Estimate total defects with two heterogeneous-detectability (Mh)
#      estimators: Chao1 and the first-order jackknife. Report the larger
#      residual. Every estimate is a LOWER BOUND over panel-reachable
#      defects only: defect classes invisible to the whole panel family
#      contribute zero captures and are not estimated.
#   5. With --threshold N, exit 1 when the residual exceeds N.
# Exit codes: 0 estimate computed (and within threshold when given);
# 1 residual above threshold; 2 cannot compute (bad input, under 4 critics).
# Python 3 standard library only.
import argparse, json, sys
from collections import Counter
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Capture-recapture residual estimate (P-02)")
    ap.add_argument("--history", required=True)
    ap.add_argument("--threshold", type=float, default=None)
    args = ap.parse_args()
    try:
        data = json.loads(Path(args.history).read_text(encoding="utf-8"))
        captures = data["captures"]
    except Exception as e:
        print(json.dumps({"error": f"cannot read capture history: {e}"}))
        return 2
    critics = sorted(captures.keys())
    t = len(critics)
    if t < 4:
        print(json.dumps({"error": f"capture-recapture must not be computed with fewer than 4 critics (got {t})"}))
        return 2
    seen = Counter()
    for c in critics:
        for fp in set(captures[c]):
            seen[fp] += 1
    observed = len(seen)
    dist = Counter(seen.values())
    f = {i: dist.get(i, 0) for i in range(1, t + 1)}
    total_captures = sum(len(set(captures[c])) for c in critics)
    if sum(i * f[i] for i in f) != total_captures:
        print(json.dumps({"error": "capture distribution fails strict-order sanity check"}))
        return 2
    f1, f2 = f[1], f[2]
    if f2 > 0:
        chao = observed + (f1 * f1) / (2.0 * f2)
    else:
        chao = observed + f1 * (f1 - 1) / 2.0
    jack = observed + f1 * (t - 1) / float(t)
    estimate = max(chao, jack)
    residual = max(0.0, estimate - observed)
    out = {"critics": t, "observed_unique": observed,
           "capture_distribution": {f"f{i}": f[i] for i in f},
           "chao1_estimate": round(chao, 2), "jackknife_mh_estimate": round(jack, 2),
           "residual_estimate": round(residual, 2),
           "caveat": "lower bound over panel-reachable defects only"}
    print(json.dumps(out, indent=2))
    if args.threshold is not None and residual > args.threshold:
        print(f"RESIDUAL ABOVE THRESHOLD: {residual:.2f} > {args.threshold}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
