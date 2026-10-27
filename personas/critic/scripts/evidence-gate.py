#!/usr/bin/env python3
# evidence-gate.py - P-01 mechanical evidence gate for judgment findings.
# Steps:
#   1. Read a findings JSON file: a list of records, each with id, critic,
#      lens, file, line (int or "start-end"), and quote (the cited text).
#   2. For each record, resolve the citation against the artifact root:
#      the file must exist, the line range must be inside the file, and
#      the whitespace-normalised quote must match the artifact text at
#      those lines (normalised substring match).
#   3. A finding whose citation does not resolve or does not match is
#      VOIDED: it never enters the ledger. A precision penalty event is
#      appended to the penalties JSON for the authoring critic.
#   4. Print a JSON summary: passed ids, voided ids with reasons.
# Exit codes: 0 every citation verified; 1 at least one finding voided;
# 2 gate could not run (bad input, missing files argument).
# Python 3 standard library only. No network. Read-only on the artifact.
import argparse, json, re, sys
from pathlib import Path

def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()

def main():
    ap = argparse.ArgumentParser(description="Mechanical evidence gate (P-01)")
    ap.add_argument("--findings", required=True, help="findings JSON file")
    ap.add_argument("--root", required=True, help="artifact root directory")
    ap.add_argument("--penalties", default=None, help="append penalty events to this JSON file")
    args = ap.parse_args()
    try:
        records = json.loads(Path(args.findings).read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("findings file must contain a JSON list")
    except Exception as e:
        print(json.dumps({"error": f"cannot read findings: {e}"}))
        return 2
    root = Path(args.root)
    if not root.is_dir():
        print(json.dumps({"error": f"artifact root not a directory: {root}"}))
        return 2
    passed, voided, penalties = [], [], []
    for rec in records:
        fid = rec.get("id", "?")
        reason = None
        rel = rec.get("file", "")
        target = (root / rel).resolve()
        if not str(target).startswith(str(root.resolve())):
            reason = "citation path escapes artifact root"
        elif not target.is_file():
            reason = f"file does not exist: {rel}"
        else:
            lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
            raw = str(rec.get("line", ""))
            m = re.fullmatch(r"(\d+)(?:-(\d+))?", raw.strip())
            if not m:
                reason = f"unparseable line spec: {raw}"
            else:
                start = int(m.group(1)); end = int(m.group(2) or m.group(1))
                if start < 1 or end > len(lines) or end < start:
                    reason = f"line range {start}-{end} outside file ({len(lines)} lines)"
                else:
                    snippet = norm("\n".join(lines[start - 1:end]))
                    if norm(rec.get("quote", "")) not in snippet:
                        reason = "quote does not match artifact text at cited lines"
        if reason is None:
            passed.append(fid)
        else:
            voided.append({"id": fid, "critic": rec.get("critic", "?"), "reason": reason})
            penalties.append({"event": "precision-penalty", "finding": fid,
                              "critic": rec.get("critic", "?"), "reason": reason})
    if args.penalties and penalties:
        p = Path(args.penalties)
        prior = []
        if p.is_file():
            try: prior = json.loads(p.read_text(encoding="utf-8"))
            except Exception: prior = []
        p.write_text(json.dumps(prior + penalties, indent=2), encoding="utf-8")
    print(json.dumps({"passed": passed, "voided": voided,
                      "penalties_recorded": len(penalties)}, indent=2))
    return 1 if voided else 0

if __name__ == "__main__":
    sys.exit(main())
