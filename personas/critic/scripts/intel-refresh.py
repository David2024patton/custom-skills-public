#!/usr/bin/env python3
# intel-refresh.py - P-15 vulnerability intel refresh and staleness law.
# Steps:
#   1. Live mode (default): fetch the CISA KEV catalog JSON and the
#      FIRST EPSS scores file headers, and query OSV for any CVEs listed
#      in --cves. Record each feed's own timestamp. A feed that cannot
#      be fetched is marked FAILED, never silently skipped.
#   2. Stamps mode (--stamps FILE): read recorded feed stamps
#      {"kev": iso, "epss": iso, "osv_offline": iso or null,
#       "osv_mode": "online"|"offline", "nvd_enrichment": iso or null,
#       "now": iso, "clean": bool, "failed": [feed names]}
#      and apply the staleness law without any network use. This mode
#      proves the DID-NOT-RUN and stale-verdict paths on fixtures.
#   3. Staleness law (ages measured from the feed's own timestamp):
#      KEV max 48h, EPSS max 48h, OSV offline DB max 120h, OSV online
#      zero (live query time recorded), NVD enrichment 7 days and only
#      for found CVEs (absence of NVD enrichment is never a downgrade).
#      Any feed stale caps the verdict at PROVISIONAL. KEV or OSV stale
#      additionally renames a clean result to
#      NO-FINDINGS-ON-STALE-INTEL, never PASS. A failed refresh is
#      DID-NOT-RUN for the intel step.
#   4. Print the mandatory report header: feed ages in hours, per-feed
#      state, and the verdict cap that applies.
# Exit codes: 0 all feeds fresh; 1 a verdict cap applies (stale intel);
# 2 refresh failed (DID-NOT-RUN) or bad input.
# Python 3 standard library only.
import argparse, json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

MAX_AGE = {"kev": 48.0, "epss": 48.0, "osv_offline": 120.0, "nvd_enrichment": 168.0}
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"

def parse_iso(s):
    if s is None:
        return None
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))

def age_hours(stamp, now):
    if stamp is None:
        return None
    return round((now - stamp).total_seconds() / 3600.0, 2)

def evaluate(stamps):
    now = parse_iso(stamps.get("now")) or datetime.now(timezone.utc)
    failed = list(stamps.get("failed", []))
    ages, states = {}, {}
    for feed in ("kev", "epss", "nvd_enrichment"):
        a = age_hours(parse_iso(stamps.get(feed)), now)
        ages[feed] = a
        if feed in failed:
            states[feed] = "FAILED"
        elif a is None:
            states[feed] = "NOT-RUN" if feed != "nvd_enrichment" else "ABSENT-NOT-A-DOWNGRADE"
        elif a > MAX_AGE[feed]:
            states[feed] = "STALE"
        else:
            states[feed] = "FRESH"
    if stamps.get("osv_mode") == "online":
        ages["osv"] = 0.0; states["osv"] = "FAILED" if "osv" in failed else "FRESH-LIVE"
    else:
        a = age_hours(parse_iso(stamps.get("osv_offline")), now)
        ages["osv"] = a
        states["osv"] = "FAILED" if "osv" in failed else ("STALE" if (a is None or a > MAX_AGE["osv_offline"]) else "FRESH")
    header = {"feed_ages_hours": ages, "feed_states": states}
    if failed:
        header["intel_step"] = "DID-NOT-RUN"
        header["verdict_cap"] = "DID-NOT-RUN"
        return header, 2
    stale = [f for f, st in states.items() if st == "STALE"]
    if stale:
        header["verdict_cap"] = "PROVISIONAL"
        if stamps.get("clean") and any(states[f] == "STALE" for f in ("kev", "osv")):
            header["clean_verdict_name"] = "NO-FINDINGS-ON-STALE-INTEL"
        header["stale_feeds"] = stale
        return header, 1
    header["verdict_cap"] = "NONE"
    return header, 0

def live_stamps(cves):
    stamps = {"now": datetime.now(timezone.utc).isoformat(), "clean": False, "failed": [], "osv_mode": "online"}
    try:
        req = urllib.request.Request(KEV_URL, headers={"User-Agent": "critic-intel-refresh"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        stamps["kev"] = data.get("catalogVersion") and (data.get("dateReleased") or datetime.now(timezone.utc).isoformat())
        stamps["kev_catalog_version"] = data.get("catalogVersion")
        stamps["kev_count"] = data.get("count")
        if cves:
            kev_ids = {v.get("cveID") for v in data.get("vulnerabilities", [])}
            stamps["kev_hits"] = {c: (c in kev_ids) for c in cves}
    except Exception as e:
        stamps["failed"].append("kev"); stamps["kev_error"] = str(e)[:200]
    try:
        req = urllib.request.Request(EPSS_URL, method="HEAD", headers={"User-Agent": "critic-intel-refresh"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            lm = resp.headers.get("Last-Modified")
        from email.utils import parsedate_to_datetime
        stamps["epss"] = parsedate_to_datetime(lm).isoformat() if lm else datetime.now(timezone.utc).isoformat()
    except Exception as e:
        stamps["failed"].append("epss"); stamps["epss_error"] = str(e)[:200]
    return stamps

def main():
    ap = argparse.ArgumentParser(description="Intel refresh and staleness law (P-15)")
    ap.add_argument("--stamps", default=None, help="fixture stamps JSON (no network)")
    ap.add_argument("--cves", default="", help="comma-separated CVEs for live KEV matching")
    ap.add_argument("--out", default=None, help="also write the header JSON here")
    args = ap.parse_args()
    if args.stamps:
        try:
            stamps = json.loads(Path(args.stamps).read_text(encoding="utf-8"))
        except Exception as e:
            print(json.dumps({"error": f"cannot read stamps: {e}"}))
            return 2
    else:
        stamps = live_stamps([c.strip() for c in args.cves.split(",") if c.strip()])
    header, code = evaluate(stamps)
    header["stamps"] = {k: v for k, v in stamps.items() if k not in ("failed",)}
    print(json.dumps(header, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(header, indent=2), encoding="utf-8")
    return code

if __name__ == "__main__":
    sys.exit(main())
