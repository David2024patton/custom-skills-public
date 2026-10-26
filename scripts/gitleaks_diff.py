"""Compare a gitleaks report against the documented baseline.

Usage: python gitleaks_diff.py <report.json> <baseline.json> <source-root>
Findings are normalized to (rule, source-relative path with /, line, secret)
so baselines survive path differences between machines and staging dirs.
Exit 1 and list any NEW finding; exit 0 when everything is documented.
"""
import json, os, sys

report_path, baseline_path, source = sys.argv[1], sys.argv[2], sys.argv[3]
source = os.path.abspath(source).replace("\\", "/").rstrip("/")

def norm(f):
    p = str(f.get("File", "")).replace("\\", "/")
    ap = os.path.abspath(p).replace("\\", "/")
    if ap.startswith(source + "/"):
        p = ap[len(source) + 1:]
    return (f.get("RuleID"), p, f.get("StartLine"), f.get("Secret"))

report = json.load(open(report_path, encoding="utf-8"))
report = [f for f in report if not str(f.get("File", "")).replace("\\\\", "/").endswith("scripts/gitleaks-baseline.json")]
baseline = json.load(open(baseline_path, encoding="utf-8"))
base_keys = {norm(f) for f in baseline}
new = [f for f in report if norm(f) not in base_keys]
if new:
    print("FAIL: %d gitleaks finding(s) not in the documented baseline:" % len(new))
    for f in new:
        print("  [%s] %s:%s  %s" % (f.get("RuleID"), f.get("File"), f.get("StartLine"), str(f.get("Secret"))[:50]))
    sys.exit(1)
print("GATE 2 clean: %d finding(s), all documented in baseline" % len(report))
