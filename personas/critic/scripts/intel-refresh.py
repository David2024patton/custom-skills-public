#!/usr/bin/env python3
# intel-refresh.py - P-15 vulnerability intel refresh and staleness law.
# Steps:
#   1. Live mode (default): fetch the CISA KEV catalog JSON, the FIRST
#      EPSS scores file headers, and query the OSV API for any CVEs
#      listed in --cves (with no CVEs listed, a single OSV API probe
#      query establishes the feed's live timestamp). Record each feed's
#      own timestamp from its response. A feed that cannot be fetched
#      is marked FAILED, never silently skipped, and never stamped
#      fresh: OSV carries a stamp only when an OSV response was
#      actually received in this run.
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
import argparse, json, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

MAX_AGE = {"kev": 48.0, "epss": 48.0, "osv_offline": 120.0, "nvd_enrichment": 168.0}
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"
OSV_VULNS_URL = "https://api.osv.dev/v1/vulns/"

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
        # FRESH-LIVE requires a recorded OSV response stamp from this
        # run. No stamp and no failure recorded means the query never
        # happened: that is a failed refresh for this feed, never fresh.
        if "osv" in failed:
            ages["osv"] = None; states["osv"] = "FAILED"
        elif stamps.get("osv"):
            ages["osv"] = age_hours(parse_iso(stamps.get("osv")), now)
            states["osv"] = "FRESH-LIVE"
        else:
            ages["osv"] = None; states["osv"] = "FAILED"
            if "osv" not in failed:
                failed.append("osv")
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

def bod_tier(entry, now):
    """BOD 26-04 tier for one KEV match, with its four variables shown.

    The catalog supplies KEV status and the due date; exposure and
    technical impact are asset-side facts this tool does not hold, and
    they are printed as not assessed rather than invented. dueDate is
    carried verbatim from the catalog, as SOUL 8.15 requires.
    """
    due_raw = entry.get("dueDate")
    ransomware = entry.get("knownRansomwareCampaignUse")
    days = None
    if due_raw:
        try:
            days = (datetime.fromisoformat(str(due_raw).replace("Z", "+00:00")).date()
                    - now.date()).days
        except Exception:
            days = None
    if ransomware == "Known":
        tier, note = 3, "3 days with mandatory forensic triage (known ransomware campaign use)"
    elif days is not None and days <= 14:
        tier, note = 14, "14 days (KEV due date inside 14 days or past)"
    elif days is not None and days <= 60:
        tier, note = 60, "60 days (KEV due date inside 60 days)"
    else:
        tier, note = None, "on-upgrade (no nearer KEV due pressure recorded)"
    return {"cveID": entry.get("cveID"), "dateAdded": entry.get("dateAdded"),
            "dueDate": due_raw, "knownRansomwareCampaignUse": ransomware,
            "bod_26_04": {"tier_days": tier, "tier_basis": note,
                          "variables": {"exposure": "not assessed by this tool (asset context required)",
                                        "kev_status": "listed in the CISA KEV catalog",
                                        "automatability": "raised: known ransomware campaign use"
                                        if ransomware == "Known" else "not scored by this tool",
                                        "technical_impact": "not assessed by this tool (asset context required)"}}}

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
            by_id = {v.get("cveID"): v for v in data.get("vulnerabilities", [])}
            stamps["kev_hits"] = {c: (c in by_id) for c in cves}
            # Retain the matched catalog entries whole: SOUL 8.15
            # requires the dueDate printed verbatim per KEV finding,
            # plus the computed BOD tier. A boolean hit discards both.
            now = datetime.now(timezone.utc)
            stamps["kev_findings"] = [bod_tier(by_id[c], now) for c in cves if c in by_id]
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
    try:
        # The live OSV query the header has always promised: fetch the
        # OSV record for each listed CVE (a 404 is a valid response
        # meaning no OSV record, not a feed failure), or one probe
        # record when no CVEs are listed. The stamp is the response
        # receipt time of THIS run; a transport error marks the feed
        # FAILED so evaluate() cannot call it fresh.
        targets = cves or ["CVE-2024-4577"]
        hits = {}
        for cve in targets:
            req = urllib.request.Request(OSV_VULNS_URL + cve,
                                         headers={"User-Agent": "critic-intel-refresh"})
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                hits[cve] = data.get("id")
            except urllib.error.HTTPError as he:
                if he.code != 404:
                    raise
                hits[cve] = None
        stamps["osv"] = datetime.now(timezone.utc).isoformat()
        stamps["osv_query"] = "api.osv.dev/v1/vulns/<CVE> per CVE"
        if cves:
            stamps["osv_records"] = hits
    except Exception as e:
        stamps["failed"].append("osv"); stamps["osv_error"] = str(e)[:200]
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
