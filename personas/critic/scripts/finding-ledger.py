#!/usr/bin/env python3
# finding-ledger.py - P-05 fingerprints, dedup, REOPENED tracking; P-06 two currencies.
# Steps:
#   fingerprint: print the fingerprint of one finding JSON object read from stdin.
#     Fingerprint = sha256 of: normalised path | symbol or AST anchor |
#     normalised evidence snippet | lens | defect class, truncated to 16 hex.
#     Rewording a finding does not change its fingerprint.
#   dedup: read a findings JSON list, group by fingerprint, print groups.
#     Dedup always runs before any statistic (P-05).
#   check-reopened: compare a prior ledger JSON (fingerprints with status)
#     against a current findings JSON list. A fingerprint whose prior status
#     was FIXED and which appears again is REOPENED, a headline metric.
#     A reopened Critical prints HALT and exits 1: the loop stops for
#     human review.
#   summary: read a findings JSON list and print counts per currency class
#     (DETERMINISTIC and JUDGMENT) separately. The two counts are never
#     summed. Deterministic records must carry tool, version, rule, and
#     config hash; judgment records must carry critic, lens, rubric cell,
#     and anchor comparison. A record missing its class fields is an error.
#   suppress: append a suppression event (fingerprint, reason, actor) to a
#     ledger events file. Suppression is append-only; suppressed items
#     still count in the coverage denominator (the caller reads the events
#     file; this tool never deletes or edits prior events).
# Exit codes: 0 ok; 1 reopened Critical, class-field error, or dedup
# duplicates found under --strict; 2 tool could not run.
# Python 3 standard library only.
import argparse, hashlib, json, re, sys
from pathlib import Path

DET_FIELDS = ["tool", "version", "rule", "config_hash"]
JUD_FIELDS = ["critic", "lens", "rubric_cell", "anchor_comparison"]

def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()

def fingerprint(f):
    parts = [norm(f.get("path", "")), norm(f.get("symbol", "")),
             norm(f.get("evidence_snippet", "")), norm(f.get("lens", "")),
             norm(f.get("defect_class", ""))]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]

def load_list(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("expected a JSON list")
    return data

def main():
    ap = argparse.ArgumentParser(description="Finding ledger tooling (P-05, P-06)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fingerprint")
    d = sub.add_parser("dedup"); d.add_argument("--findings", required=True); d.add_argument("--strict", action="store_true")
    r = sub.add_parser("check-reopened"); r.add_argument("--prior", required=True); r.add_argument("--current", required=True)
    s = sub.add_parser("summary"); s.add_argument("--findings", required=True)
    sp = sub.add_parser("suppress"); sp.add_argument("--events", required=True); sp.add_argument("--fingerprint", required=True); sp.add_argument("--reason", required=True); sp.add_argument("--actor", required=True)
    args = ap.parse_args()
    try:
        if args.cmd == "fingerprint":
            f = json.loads(sys.stdin.read())
            print(fingerprint(f)); return 0
        if args.cmd == "dedup":
            groups = {}
            for f in load_list(args.findings):
                groups.setdefault(fingerprint(f), []).append(f.get("id", "?"))
            dups = {k: v for k, v in groups.items() if len(v) > 1}
            print(json.dumps({"unique": len(groups), "duplicate_groups": dups}, indent=2))
            return 1 if (dups and args.strict) else 0
        if args.cmd == "check-reopened":
            prior = {e["fingerprint"]: e for e in load_list(args.prior)}
            reopened = []
            for f in load_list(args.current):
                fp = f.get("fingerprint") or fingerprint(f)
                old = prior.get(fp)
                if old and old.get("status") == "FIXED":
                    reopened.append({"fingerprint": fp, "id": f.get("id", "?"),
                                     "severity": f.get("severity", "?")})
            crit = [x for x in reopened if x["severity"] == "Critical"]
            print(json.dumps({"reopened": reopened, "reopened_count": len(reopened)}, indent=2))
            if crit:
                print("HALT: reopened Critical finding; loop stops for human review")
                return 1
            return 0
        if args.cmd == "summary":
            counts = {"DETERMINISTIC": 0, "JUDGMENT": 0}
            errors = []
            for f in load_list(args.findings):
                cls = f.get("class")
                if cls not in counts:
                    errors.append({"id": f.get("id", "?"), "error": f"unknown class: {cls}"}); continue
                need = DET_FIELDS if cls == "DETERMINISTIC" else JUD_FIELDS
                missing = [k for k in need if not f.get(k)]
                if missing:
                    errors.append({"id": f.get("id", "?"), "error": f"missing class fields: {missing}"}); continue
                counts[cls] += 1
            print(json.dumps({"counts_by_class_never_summed": counts, "errors": errors}, indent=2))
            return 1 if errors else 0
        if args.cmd == "suppress":
            p = Path(args.events)
            events = []
            if p.is_file():
                events = json.loads(p.read_text(encoding="utf-8"))
            events.append({"event": "suppress", "fingerprint": args.fingerprint,
                           "reason": args.reason, "actor": args.actor})
            p.write_text(json.dumps(events, indent=2), encoding="utf-8")
            print(json.dumps({"appended": True, "total_events": len(events),
                              "note": "suppressed items still count in the coverage denominator"}))
            return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return 2
    return 2

if __name__ == "__main__":
    sys.exit(main())
