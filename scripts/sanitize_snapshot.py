"""Sanitize a staged snapshot and fail-closed gate it.

Usage: python sanitize_snapshot.py <snapshot-dir> [known-files.txt]
Applies scripts/redact-map.json (safety net), then scans for any remaining
blocked value (every key, plus any subdomain listed under blocked_subdomains),
then runs generic identifier scans (emails, phone numbers, private host IPs)
that do not depend on the private list, so an identifier nobody listed yet
still aborts the publish.

Fail-closed rules (fixed 2026-10-26 after the Critic run):
- Blocked PATTERNS are regular expressions and are tested with re.search.
  The old gate tested them with str.count, a literal string count, so a
  pattern could never match and pattern survivors always passed.
- A text file that cannot be scanned (too large, undecodable) ABORTS the
  publish instead of being silently skipped. Binary files are listed as
  unscanned and reported, never silently ignored.
- If a known-files list is passed (the previous public tree), any file not
  on it is reported as NEW and the gate exits 2 until a human has read the
  new files and reruns with SANITIZE_APPROVE_NEW=1.
- Generic identifier scans (gate 1b) are FATAL in files that are new to the
  snapshot: that is where an unlisted private identifier would enter. In
  files the previous public tree already carried, generic hits are printed
  as BASELINE and are not fatal: this repo ships third party documentation
  full of public upstream contact addresses and example values (the
  awesome-list maintainer emails in knowledge/, git@github.com, the example
  gateway 10.0.0.1 in a security reference). Those were classified by human
  review on 2026-10-26. The blocked-list gate (1a) stays fatal everywhere,
  so a known private value is caught even inside an old file, and changed
  files are covered by the private repo diff review. Without a known-files
  list, every generic hit is fatal (fail safe default).
"""
import json, os, re, sys

root = sys.argv[1]
known_files = None
if len(sys.argv) > 2:
    known_files = set()
    with open(sys.argv[2], encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                known_files.add(line.replace(os.sep, "/"))

SKIP_FILES = {"redact-map.json", "gitleaks-baseline.json", "public-exclude.json"}
TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh",
             ".js", ".ts", ".go", ".rs", ".html", ".css", ".xml", ".csv",
             ".lock", ".mdc", ".yaml", ".cfg", ".ini", ".env"}
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# ---- public-scope exclusions (universal content only) ----
_exc_path = os.path.join(_cfg_dir, "public-exclude.json")
if os.path.exists(_exc_path):
    _exc = json.load(open(_exc_path, encoding="utf-8"))["exclude"]
    _names = set()
    for rel in _exc:
        target = os.path.join(root, rel.replace("/", os.sep))
        if os.path.isdir(target):
            import shutil as _sh
            _sh.rmtree(target, ignore_errors=True)
            print("excluded (dir): %s" % rel)
        elif os.path.isfile(target):
            os.remove(target)
            print("excluded (file): %s" % rel)
        _names.add(os.path.basename(rel.rstrip("/")))
    # prune index docs: drop any line naming an excluded path (stale enumerations)
    for idx in ("README.md", "MANIFEST.md"):
        ipath = os.path.join(root, idx)
        if not os.path.isfile(ipath):
            continue
        lines = open(ipath, encoding="utf-8").read().splitlines()
        kept = [ln for ln in lines if not any(n in ln for n in _names)]
        if len(kept) != len(lines):
            open(ipath, "w", encoding="utf-8", newline="\n").write("\n".join(kept) + "\n")
            print("%s: pruned %d stale line(s)" % (idx, len(lines) - len(kept)))

cfg = json.load(open(os.path.join(_cfg_dir, "redact-map.json"), encoding="utf-8"))
redact = cfg["redact"]
domains = cfg.get("blocked_subdomains", [])
allowed = cfg.get("allowed", [])

unscanned_text = []   # text files we could not scan: publish must abort
unscanned_binary = []  # binary files: reported, not scanned


def iter_files():
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            yield os.path.join(dirpath, fn)


def read_text(p):
    """Return file text, or None after recording why it was not scanned."""
    if os.path.getsize(p) > 5_000_000:
        (unscanned_text if os.path.splitext(p)[1].lower() in TEXT_EXTS
         else unscanned_binary).append(os.path.relpath(p, root) + " (too large)")
        return None
    try:
        return open(p, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        (unscanned_text if os.path.splitext(p)[1].lower() in TEXT_EXTS
         else unscanned_binary).append(os.path.relpath(p, root) + " (undecodable)")
        return None


# safety net: re-apply the map (future commits may reintroduce values)
changed = 0
for p in iter_files():
    if os.path.basename(p) in SKIP_FILES:
        continue
    t = read_text(p)
    if t is None:
        continue
    o = t
    for k, v in redact.items():
        t = t.replace(k, v)
    for dom in domains:
        t = re.sub(r"\b[a-z0-9-]+\." + re.escape(dom) + r"\b", "<ALPHAFLUX_HOST>", t, flags=re.I)
    if t != o:
        open(p, "w", encoding="utf-8", newline="").write(t)
        changed += 1
print("safety-net replacements applied to %d file(s)" % changed)

# ---- snapshot-only inline scrub (ordered rules; private repo keeps originals) ----
_rules = cfg.get("inline_replace", [])
if _rules:
    _touched = 0
    for _p in iter_files():
        if os.path.basename(_p) in SKIP_FILES:
            continue
        _t = read_text(_p)
        if _t is None:
            continue
        _o = _t
        for _frm, _to in _rules:
            _t = _t.replace(_frm, _to)
        if _t != _o:
            _t = re.sub(r"  +", " ", _t)
            open(_p, "w", encoding="utf-8", newline="").write(_t)
            _touched += 1
    print("inline scrub applied to %d file(s)" % _touched)

# ---- gate 1a: blocked values. Literal keys counted literally; pattern
# entries (blocked_patterns and blocked_subdomains) compiled as regex. ----
literal_blocked = list(redact.keys())
pattern_blocked = []
for d in domains:
    pattern_blocked.append(r"[a-z0-9-]+\." + re.escape(d))
pattern_blocked += cfg.get("blocked_patterns", [])
compiled_patterns = []
for pat in pattern_blocked:
    try:
        compiled_patterns.append((pat, re.compile(pat, re.I)))
    except re.error:
        compiled_patterns.append((pat, None))  # falls back to literal count

hits = {}
for p in iter_files():
    rel = os.path.relpath(p, root)
    if os.path.basename(p) in SKIP_FILES:
        continue
    t = read_text(p)
    if t is None:
        continue
    for b in literal_blocked:
        n = t.count(b)
        if n:
            hits.setdefault(rel, []).append("%s x%d" % (b, n))
    for pat, rx in compiled_patterns:
        if rx is not None:
            m = rx.search(t)
            if m:
                hits.setdefault(rel, []).append("pattern %s matched %r" % (pat, m.group(0)))
        elif t.count(pat):
            hits.setdefault(rel, []).append("%s x%d" % (pat, t.count(pat)))
for _bw in cfg.get("banned_words", []):
    _pat = re.compile(re.escape(_bw), re.I)
    for _p in iter_files():
        if os.path.basename(_p) in SKIP_FILES:
            continue
        _t = read_text(_p)
        if _t is None:
            continue
        for _m in _pat.finditer(_t):
            rel = os.path.relpath(_p, root)
            hits.setdefault(rel, []).append("%s (banned word)" % _m.group(0))

# ---- gate 1b: generic identifier scans. These do not depend on the private
# list, so a NEW identifier in a NEW file aborts the publish on its own.
# CIDR ranges (match immediately followed by /) are network documentation,
# not host identifiers, and are exempt. Values listed under "allowed" in the
# redact map are exempt literals. ----
GENERIC = [
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone number", re.compile(r"\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b")),
    ("private host IP", re.compile(
        r"\b(192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        r"|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
        r"|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3})\b")),
]
SAFE_EMAIL_DOMAINS = ("example.com", "example.org", "example.net")
baseline_hits = {}
for p in iter_files():
    rel = os.path.relpath(p, root).replace(os.sep, "/")
    if os.path.basename(p) in SKIP_FILES:
        continue
    t = read_text(p)
    if t is None:
        continue
    is_new = known_files is not None and rel not in known_files
    for label, rx in GENERIC:
        seen = set()
        for m in rx.finditer(t):
            val = m.group(0)
            if val in seen:
                continue
            seen.add(val)
            if label == "email address" and val.rsplit("@", 1)[-1].lower() in SAFE_EMAIL_DOMAINS:
                continue
            if label == "phone number" and ("555-01" in val or "55501" in val.replace(" ", "")):
                continue
            if label == "private host IP" and t[m.end():m.end() + 1] == "/":
                continue  # CIDR notation, not a host
            if any(a in val or val in a for a in allowed):
                continue
            entry = "%s: %s" % (label, val)
            if is_new or known_files is None:
                hits.setdefault(rel, []).append(entry)
            else:
                baseline_hits.setdefault(rel, []).append(entry)
if baseline_hits:
    print("baseline generic hits in previously published files (human classified, not fatal):")
    for f in sorted(baseline_hits):
        print("  %s: %s" % (f, ", ".join(baseline_hits[f][:6])))

if unscanned_binary:
    _ub = sorted(set(unscanned_binary))
    print("note: %d binary file(s) not content-scanned: %s"
          % (len(_ub), ", ".join(_ub[:10])))
if unscanned_text:
    print("FAIL: %d text file(s) could not be scanned, publish aborted:" % len(unscanned_text))
    for f in sorted(set(unscanned_text)):
        print("  %s" % f)
    sys.exit(1)

if hits:
    print("FAIL: blocked or unlisted identifiers present, publish aborted:")
    for f, bs in hits.items():
        print("  %s: %s" % (f, ", ".join(bs)))
    sys.exit(1)
print("GATE 1 clean: no blocked identifiers in snapshot")

# ---- new file review: anything not in the previous public tree needs a
# human read before it ships. ----
if known_files is not None:
    current = set()
    for p in iter_files():
        current.add(os.path.relpath(p, root).replace(os.sep, "/"))
    new_files = sorted(current - known_files)
    if new_files and os.environ.get("SANITIZE_APPROVE_NEW") != "1":
        print("NEW FILES REQUIRING HUMAN REVIEW (%d):" % len(new_files))
        for f in new_files:
            print("  %s" % f)
        print("Read each new file, then rerun with SANITIZE_APPROVE_NEW=1.")
        sys.exit(2)
    if new_files:
        print("new files approved for this publish: %d" % len(new_files))
