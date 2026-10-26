#!/usr/bin/env python3
"""Research run ledger for the deep-research skill.

Standard library only. Tracks the hops and evidence of one research run in a
JSON ledger with a version field, and renders a Markdown evidence table.

Commands:
  init          Create a run folder with ledger.json, notes.md, report.md
  add-hop       Record one deliberate information action
  add-evidence  Record one source and the claim it supports
  add-claim     Record one material claim in the formal claim ledger
  status        Print hop, evidence, and claim counts against the effort target
  lint          Check the run for the failure patterns the skill forbids

If this script is unavailable in the current environment, create an equivalent
Markdown or JSON ledger in the run folder with the same fields and continue.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

LEDGER_VERSION = 2

CLAIM_STATUSES = ("verified", "probable", "contested", "unsupported")
ACCESS_STATUSES = ("full", "partial", "snippet-only")

EFFORT_HOPS = {
    "quick": (2, 4),
    "standard": (5, 8),
    "deep": (9, 14),
    "exhaustive": (15, None),
}

VERIFY_MODES = {"verify", "contradict", "counterevidence", "counter"}


def slugify(text, limit=40):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (slug[:limit].rstrip("-") or "research")


def load_ledger(run_dir):
    path = Path(run_dir) / "ledger.json"
    if not path.exists():
        sys.exit(f"No ledger.json in {run_dir}. Run init first.")
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"corrupt ledger.json in {run_dir}: {exc}. Restore it before continuing.")
    return ledger, path


def save_ledger(ledger, path):
    with path.open("w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_evidence_md(ledger):
    lines = [
        f"# Evidence table: {ledger['question']}",
        "",
        "| ID | Claim supported | Source | Publisher | Date | Tier | Access | Stance | Interest | Locator |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for ev in ledger["evidence"]:
        lines.append(
            "| {id} | {claim} | [{title}]({url}) | {publisher} | {date} | {tier} "
            "| {access} | {stance} | {interest} | {locator} |".format(
                id=ev["id"],
                claim=_cell(ev.get("claim")),
                title=_cell(ev.get("title")),
                url=ev.get("url", ""),
                publisher=_cell(ev.get("publisher")),
                date=_cell(ev.get("date")),
                tier=_cell(ev.get("tier")),
                access=_cell(ev.get("access", "full")),
                stance=_cell(ev.get("stance")),
                interest=_cell(ev.get("interest")),
                locator=_cell(ev.get("locator")),
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_claims_md(ledger):
    lines = [
        f"# Claim ledger: {ledger['question']}",
        "",
        "| ID | Claim | Importance | Status | Evidence | Tier | Locator | Freshness | Counterevidence checked | Access | Final wording |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for cl in ledger.get("claims", []):
        lines.append(
            "| {id} | {claim} | {importance} | {status} | {evidence} | {tier} "
            "| {locator} | {freshness} | {counter} | {access} | {wording} |".format(
                id=cl["id"],
                claim=_cell(cl.get("claim")),
                importance=_cell(cl.get("importance")),
                status=_cell(cl.get("status")),
                evidence=_cell(", ".join(cl.get("evidence", []))),
                tier=_cell(cl.get("source_tier")),
                locator=_cell(cl.get("locator")),
                freshness=_cell(cl.get("freshness")),
                counter=_cell(cl.get("counterevidence_checked")),
                access=_cell(cl.get("access")),
                wording=_cell(cl.get("final_wording")),
            )
        )
        if cl.get("counterevidence"):
            lines.append(f"\nCounterevidence for {cl['id']}: {cl['counterevidence']}\n")
    lines.append("")
    return "\n".join(lines)


def cmd_init(args):
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    run_dir = out_dir / f"{slugify(args.question)}-{stamp}"
    suffix = 2
    while run_dir.exists():
        run_dir = out_dir / f"{slugify(args.question)}-{stamp}-{suffix}"
        suffix += 1
    run_dir.mkdir(parents=True)
    ledger = {
        "version": LEDGER_VERSION,
        "question": args.question,
        "effort": args.effort,
        "deliverable": args.deliverable or "",
        "created": datetime.now().isoformat(timespec="seconds"),
        "hops": [],
        "evidence": [],
        "claims": [],
    }
    save_ledger(ledger, run_dir / "ledger.json")
    (run_dir / "notes.md").write_text(
        f"# Run notes: {args.question}\n\n"
        "## Contract\n\n"
        f"Question: {args.question}\n\n"
        f"Effort: {args.effort}\n\n"
        f"Deliverable: {args.deliverable or ''}\n\n"
        "Audience: \n\nScope and exclusions: \n\nTime range: \n\n"
        "Geography: \n\nFreshness requirement: \n\n"
        "User-provided facts (authoritative context, not independently verified unless a source verifies them): \n\n"
        "## Outline (items and fields)\n\n"
        "## Dimensions and disagreements\n\n"
        "## Findings as they emerge\n\n",
        encoding="utf-8",
    )
    (run_dir / "report.md").write_text(
        f"# {args.question}\n\nTODO: draft not written\n", encoding="utf-8"
    )
    (run_dir / "evidence.md").write_text(render_evidence_md(ledger), encoding="utf-8")
    (run_dir / "claims.md").write_text(render_claims_md(ledger), encoding="utf-8")
    print(str(run_dir))
    return 0


def cmd_add_hop(args):
    ledger, path = load_ledger(args.run_dir)
    number = args.hop if args.hop else len(ledger["hops"]) + 1
    if args.hop is None:
        args.hop = len(ledger["hops"]) + 1
    ledger["hops"].append(
        {
            "hop": number,
            "mode": args.mode,
            "action": args.action,
            "result": args.result,
            "next": args.next or "",
            "at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_ledger(ledger, path)
    print(f"hop {number} recorded ({len(ledger['hops'])} total)")
    return 0


def cmd_add_evidence(args):
    ledger, path = load_ledger(args.run_dir)
    if args.source_id:
        ev_id = args.source_id
    else:
        used_ids = []
        for _ev in ledger["evidence"]:
            _m = re.match(r"E(\d+)$", _ev.get("id", ""))
            if _m:
                used_ids.append(int(_m.group(1)))
        ev_id = args.source_id if args.source_id else f"E{(max(used_ids) + 1) if used_ids else 1:04d}"
        if ev_id in {e.get("id") for e in ledger["evidence"]}:
            sys.exit(f"evidence id {ev_id} already exists; pass a unique --source-id")
    ledger["evidence"].append(
        {
            "id": ev_id,
            "title": args.title,
            "url": args.url,
            "publisher": args.publisher or "",
            "date": args.date or "",
            "tier": args.tier,
            "stance": args.stance,
            "claim": args.claim,
            "locator": args.locator or "",
            "interest": args.interest or "none",
            "access": args.access,
        }
    )
    save_ledger(ledger, path)
    run_dir = Path(args.run_dir)
    (run_dir / "evidence.md").write_text(render_evidence_md(ledger), encoding="utf-8")
    print(f"evidence {ev_id} recorded ({len(ledger['evidence'])} total)")
    return 0


def cmd_add_claim(args):
    ledger, path = load_ledger(args.run_dir)
    cl_id = args.claim_id or f"C{len(ledger['claims']) + 1:04d}"
    evidence = [e.strip() for e in (args.evidence or "").split(",") if e.strip()]
    ledger["claims"].append(
        {
            "id": cl_id,
            "claim": args.claim,
            "importance": args.importance,
            "status": args.status,
            "evidence": evidence,
            "source_tier": args.tier or "",
            "locator": args.locator or "",
            "freshness": args.freshness or "",
            "counterevidence_checked": args.counterevidence_checked,
            "counterevidence": args.counterevidence or "",
            "access": args.access,
            "final_wording": args.final_wording or "",
        }
    )
    save_ledger(ledger, path)
    run_dir = Path(args.run_dir)
    (run_dir / "claims.md").write_text(render_claims_md(ledger), encoding="utf-8")
    print(f"claim {cl_id} recorded ({len(ledger['claims'])} total)")
    return 0


def cmd_status(args):
    ledger, _ = load_ledger(args.run_dir)
    lo, hi = EFFORT_HOPS.get(ledger["effort"], (0, None))
    tiers = {}
    for ev in ledger["evidence"]:
        tiers[ev.get("tier", "?")] = tiers.get(ev.get("tier", "?"), 0) + 1
    target = f"{lo}+" if hi is None else f"{lo} to {hi}"
    print(f"question: {ledger['question']}")
    print(f"effort: {ledger['effort']} (hop planning estimate {target}, not a quota)")
    print(f"hops: {len(ledger['hops'])}")
    print(f"evidence: {len(ledger['evidence'])} by tier {tiers}")
    statuses = {}
    for cl in ledger.get("claims", []):
        statuses[cl.get("status", "?")] = statuses.get(cl.get("status", "?"), 0) + 1
    print(f"claims: {len(ledger.get('claims', []))} by status {statuses}")
    return 0


def cmd_lint(args):
    ledger, _ = load_ledger(args.run_dir)
    run_dir = Path(args.run_dir)
    errors, warnings = [], []
    lo, _hi = EFFORT_HOPS.get(ledger["effort"], (0, None))

    if not ledger["hops"]:
        errors.append("no hops recorded, the run has no auditable trail")
    elif len(ledger["hops"]) < lo:
        warnings.append(
            f"only {len(ledger['hops'])} hops recorded, below the "
            f"{ledger['effort']} planning estimate of {lo} "
            f"(estimates are not quotas; check claim sufficiency before adding hops)"
        )

    if not ledger["evidence"]:
        errors.append("no evidence recorded, no claim in a report can be traced")

    ids = [ev["id"] for ev in ledger["evidence"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate evidence IDs present")

    for ev in ledger["evidence"]:
        missing = [k for k in ("title", "url", "date", "tier") if not ev.get(k)]
        if missing:
            warnings.append(f"{ev['id']} is missing fields: {', '.join(missing)}")

    for ev in ledger["evidence"]:
        if ev.get("access") in ("partial", "snippet-only"):
            warnings.append(
                f"{ev['id']} access is {ev['access']}; it must not solely "
                f"support a material claim"
            )

    # Claim ledger checks
    claims = ledger.get("claims", [])
    if not ledger.get("claims"):  # any effort level: the claims ledger is mandatory everywhere
        warnings.append("no claim ledger records")
    claim_ids = [cl["id"] for cl in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("duplicate claim IDs present")
    hop_nums = [h.get("n") for h in ledger["hops"]]
    if any(n is None for n in hop_nums):
        warnings.append("some hops carry no sequence number")
    hop_nums = [n for n in hop_nums if n is not None]
    if len(hop_nums) != len(set(hop_nums)):
        errors.append("duplicate hop numbers present")
    if hop_nums and sorted(hop_nums) != list(range(1, len(hop_nums) + 1)):
        errors.append(f"hop numbering is not sequential 1..{len(hop_nums)}")
    known_evidence = set(ids)
    for cl in claims:
        missing_refs = [e for e in cl.get("evidence", []) if e not in known_evidence]
        if missing_refs:
            errors.append(f"{cl['id']} references unknown evidence: {', '.join(missing_refs)}")
        if cl.get("status") == "verified" and not cl.get("evidence"):
            errors.append(f"{cl['id']} is verified but cites no evidence")
        if cl.get("importance") == "high" and cl.get("counterevidence_checked") != "yes":
            warnings.append(f"{cl['id']} is high importance but counterevidence was not checked")
        if cl.get("status") == "unsupported" and cl.get("final_wording"):
            warnings.append(
                f"{cl['id']} is unsupported but has final wording; "
                f"cut it or move it to What could not be verified"
            )
        if cl.get("access") in ("partial", "snippet-only") and cl.get("status") == "verified":
            warnings.append(
                f"{cl['id']} is verified on {cl['access']} access alone; "
                f"find the source in full or downgrade it"
            )

    tiers = {ev.get("tier") for ev in ledger["evidence"]}
    if ledger["evidence"] and tiers <= {"C"}:
        warnings.append("all evidence is Tier C, no primary or independent source")

    modes = {h.get("mode", "").lower() for h in ledger["hops"]}
    if ledger["effort"] in ("deep", "exhaustive") and not (modes & VERIFY_MODES):
        warnings.append(
            "no verify or counterevidence hop recorded on a deep run, "
            "the skeptic pass has nothing to stand on"
        )

    if ledger["effort"] in ("deep", "exhaustive"):
        has_github = any(
            "github.com" in (ev.get("url") or "")
            or "github" in (ev.get("title") or "").lower()
            for ev in ledger["evidence"]
        )
        if not has_github:
            warnings.append(
                f"Gate G: no GitHub evidence for topic {ledger['question']}; "
                "the GitHub step is part of the gate, run it or record the gap"
            )

    report = run_dir / "report.md"
    if not report.exists():
        warnings.append("report.md missing")
    else:
        report_text = report.read_text(encoding="utf-8")
        if "TODO: draft not written" in report_text:
            warnings.append("report.md is still the unwritten placeholder")
        if re.search(r"^\[\d+\]\s*:", report_text, flags=re.MULTILINE):
            warnings.append(
                "report.md uses numbered references; the citation system is "
                "evidence IDs only ([E0007]), keyed in the evidence table, "
                "claim ledger, and References section"
            )

        known_ids = {ev.get("id") for ev in ledger["evidence"]}
        cited = set(re.findall(r"\[(E\d{4})\]", report_text))
        unknown = sorted(cited - known_ids)
        if unknown:
            errors.append(f"report.md cites evidence IDs absent from the ledger: {', '.join(unknown)}")
        inline_nums = re.findall(r"(?<!\[)\[(\d{1,2})\](?!\s*:)", report_text)
        if inline_nums:
            warnings.append(
                f"report.md contains inline numbered citations {sorted(set(inline_nums))}; "
                "the citation system is evidence IDs only"
            )
    for msg in warnings:
        print(f"WARNING: {msg}")
    for msg in errors:
        print(f"ERROR: {msg}")
    if not warnings and not errors:
        print("lint clean")
    print(
        f"hops: {len(ledger['hops'])}, evidence: {len(ledger['evidence'])}, "
        f"claims: {len(ledger.get('claims', []))}"
    )
    return (1 if errors else 0) if getattr(args, "allow_warnings", False) else (1 if (errors or warnings) else 0)


def main():
    parser = argparse.ArgumentParser(description="Deep research run ledger")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--question", required=True)
    p.add_argument("--out-dir", default="~/workspace/research_notes")
    p.add_argument("--effort", choices=sorted(EFFORT_HOPS), default="standard")
    p.add_argument("--deliverable", default="")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-hop")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--hop", type=int, default=None)
    p.add_argument("--mode", required=True,
                   help="seed, deepen, verify, contradict, follow, or inspect")
    p.add_argument("--action", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--next", default="")
    p.set_defaults(func=cmd_add_hop)

    p = sub.add_parser("add-evidence")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--source-id", default=None)
    p.add_argument("--title", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--publisher", default="")
    p.add_argument("--date", default="")
    p.add_argument("--tier", choices=["A", "B", "C"], required=True)
    p.add_argument("--stance", choices=["supports", "contradicts", "context"],
                   default="supports")
    p.add_argument("--claim", required=True)
    p.add_argument("--locator", default="")
    p.add_argument("--interest", default="none")
    p.add_argument("--access", choices=list(ACCESS_STATUSES), default="full")
    p.set_defaults(func=cmd_add_evidence)

    p = sub.add_parser("add-claim")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--claim-id", default=None)
    p.add_argument("--claim", required=True)
    p.add_argument("--importance", choices=["high", "medium", "low"], required=True)
    p.add_argument("--status", choices=list(CLAIM_STATUSES), required=True)
    p.add_argument("--evidence", default="",
                   help="comma separated evidence IDs, e.g. E0001,E0002")
    p.add_argument("--tier", default="", help="highest supporting tier or tier mix")
    p.add_argument("--locator", default="")
    p.add_argument("--freshness", default="")
    p.add_argument("--counterevidence-checked", choices=["yes", "no"], default="no")
    p.add_argument("--counterevidence", default="")
    p.add_argument("--access", choices=list(ACCESS_STATUSES), default="full")
    p.add_argument("--final-wording", default="")
    p.set_defaults(func=cmd_add_claim)

    p = sub.add_parser("status")
    p.add_argument("--run-dir", required=True)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("lint")
    p.add_argument("--allow-warnings", action="store_true", help="exit 0 despite warnings (David accepted them)")
    p.add_argument("--run-dir", required=True)
    p.set_defaults(func=cmd_lint)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
