#!/usr/bin/env python3
# finding-ledger.py - P-05 fingerprints, dedup, REOPENED tracking; P-06 two currencies.
# Steps:
#   fingerprint: print the fingerprint of one finding JSON object read from stdin.
#     Fingerprint = sha256 of: normalised path | symbol or AST anchor |
#     lens | defect class, truncated to 16 hex. The evidence snippet is
#     evidence payload and is NOT part of the hash: two critics who find
#     the same defect but quote it differently produce one fingerprint,
#     so rewording or requoting a finding cannot split it in dedup and
#     cannot remove it from the ledger.
#     Records use the canonical finding schema shared with
#     evidence-gate.py and sarif-emit.py (path, line, symbol,
#     evidence_snippet); the aliases file and quote or snippet are
#     normalised on load.
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
RUBRIC_PATH = Path(__file__).resolve().parent.parent / "references" / "rubric.json"
RUBRIC_REF_RX = re.compile(r"rubric:[a-z]+:[a-z0-9-]+")

def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()

def canon(f):
    """Normalise a record to the canonical finding schema (aliases in)."""
    f = dict(f)
    if not f.get("path") and f.get("file"):
        f["path"] = f["file"]
    if not f.get("evidence_snippet"):
        f["evidence_snippet"] = f.get("quote") or f.get("snippet") or ""
    return f

def fingerprint(f):
    f = canon(f)
    parts = [norm(f.get("path", "")), norm(f.get("symbol", "")),
             norm(f.get("lens", "")), norm(f.get("defect_class", ""))]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]

def load_list(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("expected a JSON list")
    return [canon(x) for x in data]

def load_rubric(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")).get("rubrics", {})
    except Exception:
        return {}

def main():
    ap = argparse.ArgumentParser(description="Finding ledger tooling (P-05, P-06)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fingerprint")
    d = sub.add_parser("dedup"); d.add_argument("--findings", required=True); d.add_argument("--strict", action="store_true")
    r = sub.add_parser("check-reopened"); r.add_argument("--prior", required=True); r.add_argument("--current", required=True)
    s = sub.add_parser("summary"); s.add_argument("--findings", required=True)
    s.add_argument("--rubric", default=None,
                   help="rubric JSON to validate against (default: the bundle rubric at references/rubric.json when present)")
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
            rubric_path = args.rubric or (str(RUBRIC_PATH) if RUBRIC_PATH.is_file() else None)
            rubrics = load_rubric(rubric_path) if rubric_path else {}
            for f in load_list(args.findings):
                cls = f.get("class")
                if cls not in counts:
                    errors.append({"id": f.get("id", "?"), "error": f"unknown class: {cls}"}); continue
                need = DET_FIELDS if cls == "DETERMINISTIC" else JUD_FIELDS
                missing = [k for k in need if not f.get(k)]
                if missing:
                    errors.append({"id": f.get("id", "?"), "error": f"missing class fields: {missing}"}); continue
                if cls == "JUDGMENT" and rubrics:
                    # P-16: a rubric ref that is present must resolve to a
                    # shipped anchor, and a Critical or High record must
                    # name that anchor in its forced comparison.
                    m = RUBRIC_REF_RX.search(str(f.get("rubric_cell", "")))
                    if m and m.group(0) not in rubrics:
                        errors.append({"id": f.get("id", "?"),
                                       "error": f"rubric_cell names an unshipped rubric: {m.group(0)}"}); continue
                    if str(f.get("severity", "")) in ("Critical", "High"):
                        anchor_id = rubrics.get(m.group(0), {}).get("anchor_id") if m else None
                        if not anchor_id or anchor_id not in str(f.get("anchor_comparison", "")):
                            errors.append({"id": f.get("id", "?"),
                                           "error": "Critical/High record does not name a shipped "
                                                    "anchor in anchor_comparison (P-16)"}); continue
                counts[cls] += 1
            print(json.dumps({"counts_by_class_never_summed": counts, "errors": errors,
                              "rubric_validated": bool(rubrics)}, indent=2))
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
