#!/usr/bin/env python3
# evidence-gate.py - P-01 mechanical evidence gate for judgment findings.
# Steps:
#   1. Read a findings JSON file: a list of records in the canonical
#      finding schema shared with finding-ledger.py and sarif-emit.py:
#      id, critic, lens, path, line (int or "start-end"), symbol, and
#      evidence_snippet (the cited text). Documented input aliases are
#      accepted and normalised: file for path, quote or snippet for
#      evidence_snippet.
#   2. For each record, resolve the citation against the artifact root:
#      the file must exist inside the root (component-wise containment,
#      so a sibling directory whose name extends the root name cannot
#      pass), the line range must be inside the file, and the
#      whitespace-normalised quote must match the artifact text at those
#      lines AND cover the cited defect site: when a symbol is cited,
#      the quote must include the symbol line's text; otherwise the
#      quote must cover at least 60 percent of the cited span (the full
#      line for a single-line citation). A true fragment that does not
#      cover the defect site does not pass.
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
    root_resolved = root.resolve()
    passed, voided, penalties, resolved = [], [], [], {}
    for rec in records:
        fid = rec.get("id", "?")
        reason = None
        # Canonical schema with documented aliases (D-15).
        rel = rec.get("path") or rec.get("file", "")
        quote = rec.get("evidence_snippet") or rec.get("quote") or rec.get("snippet", "")
        symbol = rec.get("symbol", "")
        target = (root / rel).resolve()
        # Component-wise containment (D-14): a sibling directory whose
        # name extends the root name resolves outside the root and fails.
        if not target.is_relative_to(root_resolved):
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
                    q = norm(quote)
                    if q not in snippet:
                        reason = "quote does not match artifact text at cited lines"
                    elif symbol:
                        # The quote must cover the defect site: the cited
                        # range must contain the symbol, and the quote
                        # must include that symbol line's text (D-47).
                        sym_lines = [ln for ln in lines[start - 1:end] if symbol in ln]
                        if not sym_lines:
                            reason = f"cited range does not contain the cited symbol: {symbol}"
                        elif norm(sym_lines[0]) not in q:
                            reason = "quote matches the range but does not cover the symbol line"
                        else:
                            resolved[fid] = symbol
                    elif len(q) < 0.6 * len(snippet):
                        reason = ("quote matches only a fragment of the cited span "
                                  "(under 60 percent coverage and no symbol cited)")
        if reason is None:
            passed.append(fid)
            resolved.setdefault(fid, symbol or None)
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
    print(json.dumps({"passed": passed, "voided": voided, "resolved_symbols": resolved,
                      "penalties_recorded": len(penalties)}, indent=2))
    return 1 if voided else 0

if __name__ == "__main__":
    sys.exit(main())
