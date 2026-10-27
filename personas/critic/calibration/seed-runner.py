#!/usr/bin/env python3
# seed-runner.py - P-07 seed bank calibration runner.
# Steps:
#   1. Validate the calibration record header: model ID, prompt hash,
#      and checklist hash are all required. A record without any one of
#      them is VOID and the run stops (exit 2). Calibration runs blind
#      at least every 10th production pass and after any model, prompt,
#      or checklist change.
#   2. Copy the fixture artifact to an isolated review copy. Seeds are
#      injected ONLY into the copy, never the shipping tree.
#   3. Run the critic command once per critic (the command receives the
#      review-copy path and the critic id as its last two arguments and
#      prints finding lines). The runner ships with a built-in fixture
#      critic (--use-fixture-critic) that greps for planted markers, so
#      the harness itself can be proven without a live panel.
#   4. Score against the ground-truth file (kept separate from the
#      bank): catch per lens, per severity, per critic, and panel
#      union. Report-first: this runner reports; it does not gate.
#      Calibration earns gate status only with measured history.
# Exit codes: 0 run completed and report printed; 1 run completed with
# zero panel-union catch (harness sanity failure); 2 void record or
# runner could not run.
# Python 3 standard library only.
import argparse, json, shutil, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

def fixture_critic(copy_root, critic_id):
    found = []
    for p in sorted(Path(copy_root).rglob("*")):
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                if "PLANTED-DEFECT" in line:
                    found.append(line.strip())
    return found

def main():
    ap = argparse.ArgumentParser(description="Seed bank calibration runner (P-07)")
    ap.add_argument("--bank", required=True)
    ap.add_argument("--ground-truth", required=True)
    ap.add_argument("--artifact", required=True, help="clean fixture artifact directory")
    ap.add_argument("--critic-cmd", default=None)
    ap.add_argument("--use-fixture-critic", action="store_true")
    ap.add_argument("--record", required=True, help="JSON with model_id, prompt_hash, checklist_hash")
    ap.add_argument("--critics", type=int, default=5)
    args = ap.parse_args()
    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        bank = json.loads(Path(args.bank).read_text(encoding="utf-8"))
        truth = json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error": f"cannot read inputs: {e}"}))
        return 2
    missing = [k for k in ("model_id", "prompt_hash", "checklist_hash") if not record.get(k)]
    if missing:
        print(json.dumps({"error": f"calibration record VOID: missing {missing}; records without model ID, prompt hash, and checklist hash are void"}))
        return 2
    truth_by_id = {e["seed_id"]: e for e in truth["entries"]}
    workdir = Path(tempfile.mkdtemp(prefix="seed-cal-"))
    copy = workdir / "review-copy"
    try:
        shutil.copytree(args.artifact, copy)
        for seed in bank["seeds"]:
            target = copy / seed["target_file"]
            target.parent.mkdir(parents=True, exist_ok=True)
            prior = target.read_text(encoding="utf-8") if target.is_file() else ""
            target.write_text(prior + seed["insertion"] + "\n", encoding="utf-8")
        per_critic = {}
        for i in range(1, args.critics + 1):
            cid = f"C{i}"
            if args.use_fixture_critic:
                lines = fixture_critic(copy, cid)
            elif args.critic_cmd:
                r = subprocess.run(args.critic_cmd.split() + [str(copy), cid], capture_output=True, text=True, timeout=300)
                lines = (r.stdout or "").splitlines()
            else:
                print(json.dumps({"error": "give --critic-cmd or --use-fixture-critic"}))
                return 2
            caught = set()
            for seed in bank["seeds"]:
                if any(seed["seed_id"] in l for l in lines):
                    caught.add(seed["seed_id"])
            per_critic[cid] = caught
        union = set().union(*per_critic.values()) if per_critic else set()
        def rate(ids):
            return round(len(ids) / len(bank["seeds"]), 3) if bank["seeds"] else 0.0
        by_lens, by_sev = {}, {}
        for lens in sorted({s["lens"] for s in bank["seeds"]}):
            ids = {s["seed_id"] for s in bank["seeds"] if s["lens"] == lens}
            by_lens[lens] = {"caught": len(ids & union), "total": len(ids), "rate": round(len(ids & union) / len(ids), 3)}
        for sev in sorted({s["severity"] for s in bank["seeds"]}):
            ids = {s["seed_id"] for s in bank["seeds"] if s["severity"] == sev}
            by_sev[sev] = {"caught": len(ids & union), "total": len(ids), "rate": round(len(ids & union) / len(ids), 3)}
        report = {"calibration_record": record, "bank_version": bank.get("bank_version"),
                  "panel_union": {"caught": len(union), "total": len(bank["seeds"]), "rate": rate(union)},
                  "per_critic": {c: {"caught": len(v), "rate": rate(v)} for c, v in per_critic.items()},
                  "per_lens": by_lens, "per_severity": by_sev,
                  "missed": sorted(set(truth_by_id) - union),
                  "status": "report-first: calibration earns gate status only with measured history"}
        print(json.dumps(report, indent=2))
        return 0 if union else 1
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
