#!/usr/bin/env python3
# decorrelate.py - P-04 replica decorrelation support tooling.
# Steps:
#   plan: given --run-id and the artifact file list, print for each of
#     the five critics a deterministic permutation of lens order and of
#     file traversal order (seeded by sha256 of run-id plus critic id,
#     so the plan is reproducible and loggable), plus a framing drawn
#     from the same seeded stream (a balanced framing list shuffled by
#     the run seed, so framing rotates across runs and is never
#     confounded with critic identity), plus a rubric order permutation
#     over the shipped rubric refs when a rubric file is available
#     (SOUL 8.16, with P-04). Lens orders are re-drawn until no two
#     critics share one. The plan is logged in the run folder; identical
#     briefs stay identical except for these orders and framings.
#   matrices: given a capture history JSON (same shape as
#     capture-recapture.py) plus an adjudication JSON mapping
#     fingerprint to adjudicated_true, print the 5x5 co-failure matrix
#     (pairs that both missed an adjudicated-true defect that at least
#     one critic caught) and the 5x5 co-fabrication matrix (pairs that
#     both reported the same adjudicated-false finding). Rising
#     co-failure is a correlation alarm and is flagged in the output.
# Exit codes: 0 ok; 1 correlation alarm raised; 2 bad input.
# Python 3 standard library only.
import argparse, hashlib, itertools, json, random, sys
from pathlib import Path

LENSES = ["code", "claims", "ux", "growth", "compliance"]
FRAMINGS = ["evidence-first", "adversary-first"]

def seeded_perm(items, seed_text):
    seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed)
    out = list(items)
    rng.shuffle(out)
    return out

def main():
    ap = argparse.ArgumentParser(description="Replica decorrelation (P-04)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--run-id", required=True); p.add_argument("--files", required=True, help="text file, one artifact path per line"); p.add_argument("--critics", type=int, default=5)
    p.add_argument("--rubric-file", default=None, help="rubric JSON whose refs get a per-critic order permutation (default: references/rubric.json in the bundle when present)")
    m = sub.add_parser("matrices"); m.add_argument("--history", required=True); m.add_argument("--adjudication", required=True)
    args = ap.parse_args()
    try:
        if args.cmd == "plan":
            files = [l.strip() for l in Path(args.files).read_text(encoding="utf-8").splitlines() if l.strip()]
            # Framing comes from the seeded stream, not from the critic
            # index: a balanced list (both framings represented) shuffled
            # by the run seed, so framing rotates across runs and cannot
            # be confounded with critic identity in the matrices.
            balanced = [FRAMINGS[i % len(FRAMINGS)] for i in range(args.critics)]
            framing_draw = seeded_perm(balanced, f"{args.run_id}|panel|framing")
            # Rubric refs for the 8.16 order permutation, when available.
            rubric_refs = []
            rubric_source = None
            candidates = [args.rubric_file] if args.rubric_file else [
                str(Path(__file__).resolve().parent.parent / "references" / "rubric.json"),
                "references/rubric.json", "personas/critic/references/rubric.json"]
            for cand in candidates:
                if cand and Path(cand).is_file():
                    try:
                        rubric_refs = sorted(json.loads(Path(cand).read_text(encoding="utf-8")).get("rubrics", {}))
                        rubric_source = cand
                    except Exception:
                        rubric_refs = []
                    if rubric_refs:
                        break
            plan = []
            used_lens_orders = set()
            for i in range(1, args.critics + 1):
                cid = f"C{i}"
                lens_order = seeded_perm(LENSES, f"{args.run_id}|{cid}|lens")
                salt = 0
                while tuple(lens_order) in used_lens_orders and salt < 50:
                    salt += 1
                    lens_order = seeded_perm(LENSES, f"{args.run_id}|{cid}|lens|{salt}")
                used_lens_orders.add(tuple(lens_order))
                entry = {"critic": cid,
                         "lens_order": lens_order,
                         "traversal_order": seeded_perm(files, f"{args.run_id}|{cid}|files"),
                         "framing": framing_draw[i - 1]}
                if rubric_refs:
                    entry["rubric_order"] = seeded_perm(rubric_refs, f"{args.run_id}|{cid}|rubric")
                plan.append(entry)
            framings_used = sorted({c["framing"] for c in plan})
            print(json.dumps({"run_id": args.run_id, "framings_used": framings_used,
                              "rubric_source": rubric_source, "plan": plan}, indent=2))
            return 0 if len(framings_used) >= 2 else 1
        if args.cmd == "matrices":
            hist = json.loads(Path(args.history).read_text(encoding="utf-8"))["captures"]
            adj = json.loads(Path(args.adjudication).read_text(encoding="utf-8"))
            critics = sorted(hist.keys())
            caught = {c: set(hist[c]) for c in critics}
            all_fps = set()
            for c in critics: all_fps |= caught[c]
            true_fps = {fp for fp in all_fps if adj.get(fp) is True}
            false_fps = {fp for fp in all_fps if adj.get(fp) is False}
            cofail = {a: {b: 0 for b in critics} for a in critics}
            cofab = {a: {b: 0 for b in critics} for a in critics}
            for fp in true_fps:
                missers = [c for c in critics if fp not in caught[c]]
                if len(missers) < len(critics):
                    for a, b in itertools.combinations(missers, 2):
                        cofail[a][b] += 1; cofail[b][a] += 1
            for fp in false_fps:
                reporters = [c for c in critics if fp in caught[c]]
                for a, b in itertools.combinations(reporters, 2):
                    cofab[a][b] += 1; cofab[b][a] += 1
            alarm = any(cofail[a][b] >= 3 for a, b in itertools.combinations(critics, 2))
            print(json.dumps({"co_failure_matrix": cofail, "co_fabrication_matrix": cofab,
                              "correlation_alarm": alarm}, indent=2))
            return 1 if alarm else 0
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return 2
    return 2

if __name__ == "__main__":
    sys.exit(main())
