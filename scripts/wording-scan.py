#!/usr/bin/env python3
"""Wording inventory scanner: the step-by-step sweep backlog.

Scans a tree and reports wording hits by class, per WORDING-STANDARD.md.
This is an inventory tool: it reports and never gates (exit 0 unless the
input is unusable). The fix sweep works cluster by cluster from its
report.

Classes:
  HARNESS-TERM        harness-specific tool vocabulary in method text
  ABS-PATH            absolute local path patterns (generic, no values)
  PRIVATE-ENDPOINT    a URL whose host ends with a blocked subdomain from
                      scripts/redact-map.json (when that private config is
                      present beside this script; otherwise the class is
                      skipped and the skip is reported)
  UNLABELED-BINDING   a file with ABS-PATH or HARNESS-TERM hits but no
                      labeled local binding section (WORDING-STANDARD.md)
  KEY-REF             mentions of credential stores or stored logins
                      (informational: a binding should name where a
                      credential lives, never the credential)

Usage:
  python3 wording-scan.py [root] [--out report.md] [--self-test]
Diagnostics go to stderr; the report goes to stdout or --out.

Self-exemption: the checker sources and the wording standard's own
documents are exempt from their own scans. The exempt paths are
scripts/check-neutral.py, scripts/wording-scan.py, and
WORDING-STANDARD.md. The exemptions are printed in the report.
"""
import json, os, re, sys

TEXT_EXTS = {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".locks", ".hub"}
SKIP_FILES = {"redact-map.json", "gitleaks-baseline.json", "public-exclude.json"}
SELF_EXEMPT_RELS = (
    "scripts/check-neutral.py",
    "scripts/wording-scan.py",
    "WORDING-STANDARD.md",
)


def is_self_exempt(rel):
    norm = rel.replace(os.sep, "/")
    for exempt in SELF_EXEMPT_RELS:
        if norm == exempt or norm.endswith("/" + exempt):
            return exempt
    return None

HARNESS_TERMS = [
    "delegate_task", "web_search", "web_extract", "spawn_agent",
    "run_agent", "hermes-agent", "claude-code", "codex-cli",
    "C:/Users/", "AppData/Local/hermes",
]
ABS_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\[^\s\\]+"),
    re.compile(r"[A-Za-z]:/[Uu]sers/[^\s/]+"),
    re.compile(r"/Users/[^\s/]+/"),
    re.compile(r"/home/[a-z_][a-z0-9_-]*/"),
    re.compile(r"G:/[^\s]+"),
    re.compile(r"\b[A-Za-z]:\\[^\s\\][^\s]+"),
]
KEY_REF_PATTERNS = [
    re.compile(r"CREDENTIALS\.md"),
    re.compile(r"stored (login|credential|password)", re.I),
    re.compile(r"password is stored", re.I),
    re.compile(r"~/\.ssh/"),
]
URL_RX = re.compile(r"https?://([A-Za-z0-9.-]+)")


def diag(msg):
    print("wording-scan: %s" % msg, file=sys.stderr)


def blocked_suffixes():
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = os.path.join(here, "redact-map.json")
    if not os.path.exists(cfg):
        diag("redact-map.json not found beside the script: PRIVATE-ENDPOINT class skipped")
        return []
    try:
        data = json.load(open(cfg, encoding="utf-8"))
        return [d.lower() for d in data.get("blocked_subdomains", [])]
    except (ValueError, OSError) as e:
        diag("redact-map.json unreadable (%s): PRIVATE-ENDPOINT class skipped" % e)
        return []


def scan(root):
    suffixes = blocked_suffixes()
    counts = {}
    per_file = {}
    unlabeled = []
    exempted = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            exempt = is_self_exempt(rel)
            if exempt:
                if exempt not in exempted:
                    exempted.append(exempt)
                continue
            if fn in SKIP_FILES or os.path.splitext(fn)[1].lower() not in TEXT_EXTS:
                continue
            try:
                text = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            file_hits = {}
            for term in HARNESS_TERMS:
                n = text.count(term)
                if n:
                    file_hits["HARNESS-TERM"] = file_hits.get("HARNESS-TERM", 0) + n
            for rx in ABS_PATH_PATTERNS:
                n = len(rx.findall(text))
                if n:
                    file_hits["ABS-PATH"] = file_hits.get("ABS-PATH", 0) + n
            if suffixes:
                n = 0
                for m in URL_RX.finditer(text):
                    host = m.group(1).lower()
                    if any(host == s or host.endswith("." + s) for s in suffixes):
                        n += 1
                if n:
                    file_hits["PRIVATE-ENDPOINT"] = n
            for rx in KEY_REF_PATTERNS:
                n = len(rx.findall(text))
                if n:
                    file_hits["KEY-REF"] = file_hits.get("KEY-REF", 0) + n
            if file_hits:
                per_file[rel] = file_hits
                for cls, n in file_hits.items():
                    counts[cls] = counts.get(cls, 0) + n
                if ("ABS-PATH" in file_hits or "HARNESS-TERM" in file_hits) \
                        and "local binding" not in text.lower():
                    unlabeled.append(rel)
    counts["UNLABELED-BINDING (files)"] = len(unlabeled)
    return counts, per_file, unlabeled, exempted


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "a.md"), "w", encoding="utf-8") as f:
            f.write("Call delegate_task, then read C:/Users/X/y.md\n")
        counts, per_file, unlabeled, exempted = scan(d)
    ok = counts.get("HARNESS-TERM", 0) >= 1 and counts.get("ABS-PATH", 0) >= 1 \
        and unlabeled == ["a.md"]
    print("self-test %s: %s" % ("ok" if ok else "FAIL", counts))
    return 0 if ok else 1


def parse_args(argv):
    args, opts = [], {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and "=" in a:
            k, v = a.split("=", 1)
            opts[k] = v
        elif a == "--out" and i + 1 < len(argv):
            opts[a] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            opts[a] = True
        else:
            args.append(a)
        i += 1
    return args, opts


def main(argv):
    args, opts = parse_args(argv)
    if "--self-test" in opts:
        return self_test()
    root = args[0] if args else "."
    if not os.path.isdir(root):
        diag("root is not a directory: %s" % root)
        return 2
    counts, per_file, unlabeled, exempted = scan(root)
    lines = ["# Wording scan report", "", "Root: `%s`" % root, "",
             "## Self-exempt (not scanned)", ""]
    for rel in SELF_EXEMPT_RELS:
        lines.append("- Self-exempt (not scanned): %s" % rel)
    lines += ["", "## Totals by class", ""]
    for cls in sorted(counts):
        lines.append("- %s: %d" % (cls, counts[cls]))
    lines += ["", "## Files with hits (%d)" % len(per_file), ""]
    for rel in sorted(per_file):
        parts = ", ".join("%s %d" % (c, n) for c, n in sorted(per_file[rel].items()))
        lines.append("- `%s`: %s" % (rel, parts))
    lines += ["", "## Unlabeled binding candidate files (%d)" % len(unlabeled), ""]
    for rel in unlabeled:
        lines.append("- `%s`" % rel)
    report = "\n".join(lines) + "\n"
    if "--out" in opts:
        with open(opts["--out"], "w", encoding="utf-8") as f:
            f.write(report)
        diag("report written to %s" % opts["--out"])
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
