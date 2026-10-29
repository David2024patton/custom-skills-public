#!/usr/bin/env python3
# consensus-stats.py - P-03 measured consensus; P-17 ordinal confidence.
# Steps:
#   1. Read an adjudication history JSON covering the last 10 passes:
#      {"findings": [{"lens": "code", "severity": "High", "votes": 3,
#       "adjudicated_true": true, "stated_confidence": 8}, ...],
#       "ratings": {"code|High": [[critic ratings per item], ...]}}
#      Ratings rows are per-item lists of 0 or 1 (reported or not) with
#      one entry per critic, used for Fleiss kappa.
#   2. Vote-band precision per lens: for each band 5, 4, 3, 2, 1, the
#      adjudicated-true fraction. If 3-of-5 precision is not above the
#      pass base rate for a lens, print MAJORITY LABEL SUSPENDED for it.
#   3. Effective sample size from the mean pairwise co-report rate:
#      n_eff = n / (1 + (n-1) * rho), where rho is the mean over critic
#      pairs of the share of rated items both critics reported, computed
#      from the per-item per-critic ratings when the history carries
#      them. When ratings are absent the tool falls back to a vote-band
#      concentration proxy, prints it under that name with its limits
#      (it counts joint non-reporting as agreement, so it overstates
#      agreement), and marks the output as a proxy. Printed always; the
#      protocol prints it in the report when under 2.0.
#   4. Fleiss kappa per lens and severity with item N and a bootstrap
#      interval (seeded, deterministic). Kappa under 0.40 prints
#      RUBRIC DEFECT for that lens/severity: revise the rubric, re-run.
#   5. P-17 reliability table: stated confidence 1..10 mapped to the
#      adjudicated-true fraction per lens. Confidences are ordinal and
#      are never averaged into a panel probability by this tool.
# Exit codes: 0 computed, no rubric defect; 1 a rubric defect flag or a
# suspended majority label was raised; 2 bad input.
# Python 3 standard library only.
import argparse, json, random, sys
from collections import defaultdict
from pathlib import Path

def fleiss_kappa(rows):
    # rows: list of items, each a list of rater category counts summing to n raters.
    if not rows:
        return None
    n = sum(rows[0])
    if n < 2:
        return None
    cats = len(rows[0])
    N = len(rows)
    p_j = [sum(r[j] for r in rows) / (N * n) for j in range(cats)]
    pe = sum(p * p for p in p_j)
    p_i = []
    for r in rows:
        s = sum(x * (x - 1) for x in r)
        p_i.append(s / (n * (n - 1)))
    pbar = sum(p_i) / N
    if pe >= 1.0:
        return 1.0
    return (pbar - pe) / (1.0 - pe)

def kappa_for(ratings_lists):
    # ratings_lists: per-item lists of 0/1 per critic.
    rows = []
    for item in ratings_lists:
        ones = sum(item); zeros = len(item) - ones
        rows.append([zeros, ones])
    return fleiss_kappa(rows), len(rows)

def bootstrap_ci(ratings_lists, seed=20261027, reps=200):
    if len(ratings_lists) < 3:
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        sample = [ratings_lists[rng.randrange(len(ratings_lists))] for _ in ratings_lists]
        k, _ = kappa_for(sample)
        if k is not None:
            vals.append(k)
    if not vals:
        return None
    vals.sort()
    return [round(vals[int(0.025 * len(vals))], 3), round(vals[min(len(vals) - 1, int(0.975 * len(vals)))], 3)]

def main():
    ap = argparse.ArgumentParser(description="Measured consensus statistics (P-03, P-17)")
    ap.add_argument("--history", required=True)
    ap.add_argument("--critics", type=int, default=5)
    args = ap.parse_args()
    try:
        data = json.loads(Path(args.history).read_text(encoding="utf-8"))
        findings = data.get("findings", [])
    except Exception as e:
        print(json.dumps({"error": f"cannot read history: {e}"}))
        return 2
    exit_code = 0
    n = args.critics
    # Effective sample size. Preferred input: the per-item per-critic
    # ratings rows, which give the true pairwise co-report rate. Fallback:
    # the vote-band concentration proxy, printed under its true name.
    import itertools
    from math import comb
    rating_rows = [row for rows in data.get("ratings", {}).values() for row in rows]
    rho = None; ess_method = None
    if rating_rows:
        pair_rates = []
        for a, b in itertools.combinations(range(n), 2):
            both = sum(1 for row in rating_rows if len(row) > b and row[a] and row[b])
            pair_rates.append(both / len(rating_rows))
        rho = sum(pair_rates) / len(pair_rates) if pair_rates else 0.0
        ess_method = "pairwise co-report rate from per-critic ratings"
    elif findings:
        total_pairs = 0.0; agree = 0.0
        for fd in findings:
            v = fd.get("votes", 0)
            total_pairs += comb(n, 2)
            agree += comb(v, 2) + comb(n - v, 2)
        rho = max(0.0, min(1.0, ((agree / total_pairs) - 0.5) * 2.0)) if total_pairs else 0.0
        ess_method = ("band concentration proxy (no per-critic ratings in history): "
                      "counts joint non-reporting as agreement; treat n_eff as an upper bound")
    n_eff = n / (1.0 + (n - 1) * rho) if rho else float(n)
    out = {"effective_sample_size": round(n_eff, 2),
           "effective_sample_size_method": ess_method or "no findings and no ratings; n_eff = panel size",
           "effective_sample_size_note": "print in report when under 2.0" if n_eff < 2.0 else "at or above 2.0",
           "vote_band_precision": {}, "reliability_table": {}, "kappa": {}}
    by_lens = defaultdict(list)
    for fd in findings:
        by_lens[fd.get("lens", "?")].append(fd)
    for lens, items in sorted(by_lens.items()):
        base = sum(1 for i in items if i.get("adjudicated_true")) / len(items) if items else 0.0
        bands = {}
        for band in (5, 4, 3, 2, 1):
            sel = [i for i in items if i.get("votes") == band]
            bands[str(band)] = (round(sum(1 for i in sel if i.get("adjudicated_true")) / len(sel), 3) if sel else None)
        out["vote_band_precision"][lens] = {"bands": bands, "base_rate": round(base, 3)}
        p3 = bands["3"]
        if p3 is not None and p3 <= base:
            out["vote_band_precision"][lens]["majority_label"] = "SUSPENDED: 3-of-5 precision not above base rate"
            exit_code = 1
        rel = {}
        for conf in range(1, 11):
            sel = [i for i in items if i.get("stated_confidence") == conf]
            rel[str(conf)] = (round(sum(1 for i in sel if i.get("adjudicated_true")) / len(sel), 3) if sel else None)
        out["reliability_table"][lens] = rel
    for key, rows in sorted(data.get("ratings", {}).items()):
        k, count = kappa_for(rows)
        ci = bootstrap_ci(rows)
        entry = {"kappa": round(k, 3) if k is not None else None, "n_items": count, "bootstrap_95_interval": ci}
        if k is not None and k < 0.40:
            entry["flag"] = "RUBRIC DEFECT: kappa under 0.40; revise rubric and re-run"
            exit_code = 1
        out["kappa"][key] = entry
    out["panel_confidence_rule"] = "calibrated vote-band precision plus capture-recapture residual; never an average of stated confidences"
    print(json.dumps(out, indent=2))
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
