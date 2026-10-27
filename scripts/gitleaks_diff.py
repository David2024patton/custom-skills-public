"""Compare a gitleaks report against the documented baseline.

Usage: python3 gitleaks_diff.py <report.json> <baseline.json> <source-root>
Findings are normalized to (rule, source-relative path with /, line, secret)
so baselines survive path differences between machines and staging dirs.
Fingerprints are normalized the same way on BOTH sides before comparing:
a fingerprint is "<file>:<rule>:<line>", and its file part is reduced to
repo-relative form (see fingerprint_file), so a baseline written on one
machine matches findings produced on any other machine, including
findings whose fingerprint carries an absolute Windows path.
Exit 1 and list any NEW finding; exit 0 when everything is documented.
Missing or extra arguments print usage to stderr and exit 2.
"""
import json, os, re, sys

USAGE = "usage: python3 gitleaks_diff.py <report.json> <baseline.json> <source-root>"

if len(sys.argv) != 4:
    sys.stderr.write(USAGE + "\n")
    sys.exit(2)

report_path, baseline_path, source = sys.argv[1], sys.argv[2], sys.argv[3]
source = os.path.abspath(source).replace("\\", "/").rstrip("/")


def repo_relative(p):
    """Reduce a file path to repo-relative form when it can be proven.

    Relative paths pass through with slashes normalized. Absolute paths
    are stripped only when they sit under the source root; anything else
    is returned normalized but unstripped, and fingerprint_file below
    gets the final say for fingerprint-carried paths.
    """
    p = str(p).replace("\\", "/").strip()
    if not p:
        return p
    is_absolute = p.startswith("/") or re.match(r"^[A-Za-z]:/", p)
    if not is_absolute:
        return p.lstrip("./")
    ap = os.path.abspath(p).replace("\\", "/") if not re.match(r"^[A-Za-z]:/", p) else p
    if ap.startswith(source + "/"):
        return ap[len(source) + 1:]
    return ap


def fingerprint_file(fp, file_field):
    """Extract and relativize the file part of a gitleaks fingerprint.

    A fingerprint is "<file>:<rule>:<line>"; the file part may itself
    contain colons (a Windows drive letter), so split from the right.
    The file part is repo-relative when it equals the finding's File
    field or ends with "/" plus that field (the machine-specific prefix
    in front of it is dropped), or when it sits under the source root.
    """
    parts = str(fp).replace("\\", "/").rsplit(":", 2)
    if len(parts) != 3:
        return None
    raw = parts[0]
    rel = repo_relative(file_field)
    if rel and (raw == rel or raw.endswith("/" + rel)):
        return rel
    stripped = repo_relative(raw)
    if stripped != raw:
        return stripped
    if rel:
        return rel
    return raw


def norm(f):
    rel = repo_relative(f.get("File", ""))
    fp = f.get("Fingerprint")
    if fp:
        fp_file = fingerprint_file(fp, f.get("File", ""))
        if fp_file:
            rel = fp_file
    return (f.get("RuleID"), rel, f.get("StartLine"), f.get("Secret"))

def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write("error: cannot load %s: %s\n" % (path, exc))
        sys.exit(2)


report = load_json(report_path)
report = [f for f in report if not str(f.get("File", "")).replace("\\\\", "/").endswith("scripts/gitleaks-baseline.json")]
baseline = load_json(baseline_path)
base_keys = {norm(f) for f in baseline}


def is_known(f):
    """True when a finding matches a baseline entry after normalization.

    Exact normalized match first. As a second chance, a finding whose
    path is still absolute (a machine-specific root the fingerprint
    could not strip) matches a baseline entry with the same rule, line,
    and secret when the baseline's repo-relative path is a whole
    component suffix of the finding's path, or the reverse.
    """
    key = norm(f)
    if key in base_keys:
        return True
    rule, path, line, secret = key
    for b_rule, b_path, b_line, b_secret in base_keys:
        if (b_rule, b_line, b_secret) != (rule, line, secret):
            continue
        if path.endswith("/" + b_path) or b_path.endswith("/" + path):
            return True
    return False


new = [f for f in report if not is_known(f)]
if new:
    print("FAIL: %d gitleaks finding(s) not in the documented baseline:" % len(new))
    for f in new:
        print("  [%s] %s:%s  %s" % (f.get("RuleID"), f.get("File"), f.get("StartLine"), str(f.get("Secret"))[:50]))
    sys.exit(1)
print("GATE 2 clean: %d finding(s), all documented in baseline" % len(report))
