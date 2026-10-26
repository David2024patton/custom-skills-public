#!/usr/bin/env python3
"""Read-only GitHub landscape survey helper for the github-research skill.

Runs `gh search repos` once per query, dedupes results by full name, and
writes a JSON shortlist sorted by stars. Each entry keeps the list of
queries that surfaced it, so a survey can resume or be audited later.

Usage:
    gh-landscape.py QUERY [QUERY ...] [--limit N] --output PATH

Two or more query strings are required: a landscape survey is defined by
comparing several keyword angles, never one search. --limit caps results
per query (default 15). Standard library only; the only external tool is
the gh CLI, used read-only.

Exit codes: 0 on success, 2 on usage errors, a missing gh CLI, or a gh
failure (auth, rate limit, network). The failing query is named on stderr
so a stopped survey can resume from that query.
"""

import argparse
import json
import shutil
import subprocess
import sys

FIELDS = "fullName,stargazersCount,description,pushedAt,license"


def run_query(query: str, limit: int) -> list:
    proc = subprocess.run(
        ["gh", "search", "repos", query, "--limit", str(limit),
         "--json", FIELDS],
        capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "no output").strip()
        raise RuntimeError(f"query {query!r} failed: {detail}")
    try:
        rows = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"query {query!r} returned non-JSON output: {exc}")
    return rows


def normalize(row: dict, query: str) -> dict:
    license_obj = row.get("license") or {}
    return {
        "full_name": row.get("fullName", ""),
        "stars": row.get("stargazersCount", 0),
        "license": license_obj.get("key") if isinstance(license_obj, dict) else None,
        "pushed_at": row.get("pushedAt", ""),
        "description": row.get("description") or "",
        "queries": [query],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only GitHub landscape survey")
    parser.add_argument("queries", nargs="+", help="two or more search query strings")
    parser.add_argument("--limit", type=int, default=15,
                        help="max results per query (default 15)")
    parser.add_argument("--output", required=True, help="path for the JSON shortlist")
    args = parser.parse_args()

    if len(args.queries) < 2:
        print("gh-landscape: a landscape survey needs at least two queries", file=sys.stderr)
        return 2
    if args.limit < 1:
        print("gh-landscape: --limit must be at least 1", file=sys.stderr)
        return 2
    if shutil.which("gh") is None:
        print("gh-landscape: gh CLI not found on PATH; install GitHub CLI and run `gh auth login` first", file=sys.stderr)
        return 2

    by_name = {}
    for query in args.queries:
        try:
            rows = run_query(query, args.limit)
        except RuntimeError as exc:
            print(f"gh-landscape: {exc}", file=sys.stderr)
            print(f"gh-landscape: survey stopped; resume by rerunning from query {query!r}", file=sys.stderr)
            return 2
        for row in rows:
            entry = normalize(row, query)
            name = entry["full_name"]
            if not name:
                continue
            if name in by_name:
                if query not in by_name[name]["queries"]:
                    by_name[name]["queries"].append(query)
            else:
                by_name[name] = entry

    shortlist = sorted(by_name.values(), key=lambda e: (-e["stars"], e["full_name"]))
    payload = {
        "queries": args.queries,
        "limit_per_query": args.limit,
        "count": len(shortlist),
        "repos": shortlist,
    }
    try:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        print(f"gh-landscape: cannot write output: {exc}", file=sys.stderr)
        return 2
    print(f"gh-landscape: wrote {len(shortlist)} unique repos to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
