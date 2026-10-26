"""Sanitize a staged snapshot and fail-closed gate it.

Usage: python3 sanitize_snapshot.py <snapshot-dir> [known-files.txt]
Applies scripts/redact-map.json (safety net), then scans for any remaining
blocked value (every key, plus any subdomain listed under blocked_subdomains),
then runs generic identifier scans (emails, phone numbers, private host IPs)
that do not depend on the private list, so an identifier nobody listed yet
still aborts the publish.

Private config requirement: scripts/redact-map.json and
scripts/public-exclude.json live only in the private repo and are never
published. If either is missing (for example when this script is run from
the published public tree), the script prints one clear line and exits 3
with no traceback.

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
  snapshot: that is where an unlisted private identifier would enter. The
  known-files list is hash pinned: each line is path<TAB>sha256, the
  SHA-256 hex of the file bytes in the previous public tree (produced by
  list_mirror_files.py). A file whose current bytes hash to its pin is
  BASELINE for gate 1b: generic hits in it are printed, not fatal, because
  this repo ships third party documentation full of public upstream contact
  addresses and example values (the awesome-list maintainer emails in
  knowledge/, git@github.com, an example gateway address in a security
  reference), classified by human review on 2026-10-26. A file whose hash
  differs from its pin, whose entry has no hash (legacy path-only line),
  or that is absent from the list is treated as NEW: generic hits are
  fatal. Pinning acceptance to content, not to path membership, is what
  closes the round 2 U1 bypass, where planting a private IP in an edited
  known file passed the gate. The blocked-list gate (1a) stays fatal
  everywhere regardless of pins, so a known private value is caught even
  inside a hash-matched file. Without a known-files list, every generic
  hit is fatal (fail safe default).
- Gate 1c (after exclusions): duplicate skill names and dangling
  references to excluded paths are fatal. Pointer files no longer carry
  name fields, so a clean tree has no duplicate name values.
"""
import hashlib, json, os, re, sys

if len(sys.argv) < 2:
    sys.stderr.write("usage: python3 sanitize_snapshot.py <snapshot-dir> [known-files.txt]\n")
    sys.exit(2)

root = sys.argv[1]
known_files = None
known_pins = None
if len(sys.argv) > 2:
    known_files = set()
    known_pins = {}
    with open(sys.argv[2], encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            path = parts[0].strip().replace(os.sep, "/")
            if not path:
                continue
            known_files.add(path)
            pin = None
            if len(parts) > 1:
                cand = parts[1].strip().lower()
                if len(cand) == 64 and all(c in "0123456789abcdef" for c in cand):
                    pin = cand
            known_pins[path] = pin

SKIP_FILES = {"redact-map.json", "gitleaks-baseline.json", "public-exclude.json"}
TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh",
             ".js", ".ts", ".go", ".rs", ".html", ".css", ".xml", ".csv",
             ".lock", ".mdc", ".yaml", ".cfg", ".ini", ".env"}
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# ---- private config: required, graceful exit when absent ----
_redact_path = os.path.join(_cfg_dir, "redact-map.json")
_exc_path = os.path.join(_cfg_dir, "public-exclude.json")
if not os.path.isfile(_redact_path):
    sys.stderr.write("ERROR: private config scripts/redact-map.json is required; run sanitize_snapshot.py from the private repo (the public tree does not ship it).\n")
    sys.exit(3)
if not os.path.isfile(_exc_path):
    sys.stderr.write("ERROR: private config scripts/public-exclude.json is required; run sanitize_snapshot.py from the private repo (the public tree does not ship it).\n")
    sys.exit(3)

# ---- public-scope exclusions (universal content only) ----
_exc = json.load(open(_exc_path, encoding="utf-8"))["exclude"]
excluded_paths = list(_exc)
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

cfg = json.load(open(_redact_path, encoding="utf-8"))
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


def _record(lst, entry):
    if entry not in lst:
        lst.append(entry)


def read_text(p):
    """Return file text, or None after recording why it was not scanned."""
    if os.path.getsize(p) > 5_000_000:
        _record(unscanned_text if os.path.splitext(p)[1].lower() in TEXT_EXTS
                else unscanned_binary,
                os.path.relpath(p, root) + " (too large)")
        return None
    try:
        return open(p, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        _record(unscanned_text if os.path.splitext(p)[1].lower() in TEXT_EXTS
                else unscanned_binary,
                os.path.relpath(p, root) + " (undecodable)")
        return None


def file_sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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
# Baseline treatment requires a hash pin match (see module docstring).
# CIDR ranges (match immediately followed by /) are network documentation,
# not host identifiers, and are exempt. Values listed under "allowed" in the
# redact map are exempt literals. ----
GENERIC = [
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone number", re.compile(r"\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b")),
    # Generic secret shapes (round 3 finding M1): the patterns above only
    # cover identifiers, so a leaked credential in a file nobody listed
    # passed clean. These shapes are tight on purpose: an AWS access key
    # id is exactly AKIA plus 16 uppercase alphanumerics, GitHub tokens
    # carry a fixed prefix plus a long token body, and a PEM header is a
    # literal banner line. Teaching prose that merely names these formats
    # does not match any of them.
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(
        r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"
        r"|\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("PEM private key header", re.compile(
        r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY-----")),
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
    is_baseline = False
    if known_pins is not None:
        pin = known_pins.get(rel)
        if pin:
            try:
                is_baseline = (file_sha256(p) == pin)
            except OSError:
                is_baseline = False
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
            if is_baseline:
                baseline_hits.setdefault(rel, []).append(entry)
            else:
                hits.setdefault(rel, []).append(entry)
if baseline_hits:
    print("baseline generic hits in hash-matched previously published files (human classified, not fatal):")
    for f in sorted(baseline_hits):
        print("  %s: %s" % (f, ", ".join(baseline_hits[f][:6])))

# ---- gate 1c: duplicate skill names and dangling excluded-path references.
# Runs after exclusions, so only shipped files are scanned. ----
# Legitimate mentions of excluded paths, as (file, excluded entry) pairs;
# the value "*" means every excluded entry is allowed in that file.
DANGLING_ALLOWLIST = {
    # The registry generator: its private-only and risk tables must name
    # the excluded skills to classify them. Naming them is the mechanism.
    "scripts/build-registry.py": "*",
    # bootstrap.sh names the heartbeat script only inside an existence
    # test that prints a SKIP line when the file is absent (it is excluded
    # from the public snapshot). Naming the path is the guard itself.
    "bootstrap.sh": {"scripts/cron/heartbeat.py"},
    # SNAPSHOT.md is the snapshot record: its Removed sections name the
    # items each snapshot removed or started excluding. Naming them is
    # the record itself. registry.json and skill-aliases.json carried a
    # blanket allowance until step 2b; since the registry is now
    # generated from the post-exclusion tree, neither file may name an
    # excluded path, and gate 1c now proves it.
    "SNAPSHOT.md": {"tiny-go-web-tool", "skills/.curator_ledger.jsonl",
                    "skills/.hub"},
}
# The gate tooling itself is not scanned for dangling references: these
# files implement or test the check and may embed excluded strings as
# fixtures or documentation.
DANGLING_SCAN_SKIP = {
    "scripts/sanitize_snapshot.py",
    "scripts/list_mirror_files.py",
    "scripts/check_license_integrity.py",
    "scripts/test_sanitize_snapshot.py",
}
_NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")


def _is_path_reference(text, entry):
    """True when entry appears in text as a path reference.

    An entry containing a slash is an unambiguous path and matches
    literally anywhere. A single-component entry (a folder or file name)
    matches only in a path context: followed by a slash (used as a path
    component), or quoted or backticked as a standalone token. Bare prose
    mentions do not count: several excluded names are also ordinary words
    or tool names (pulse, dokploy, hostinger) and a plain substring match
    would fail clean files on English text and CSS keyframes.
    """
    if "/" in entry:
        return entry in text
    i = 0
    while True:
        j = text.find(entry, i)
        if j < 0:
            return False
        before = text[j - 1] if j > 0 else ""
        after = text[j + len(entry)] if j + len(entry) < len(text) else ""
        if before not in _NAME_CHARS and after not in _NAME_CHARS:
            if after == "/" or before in "`\"'" or after in "`\"'":
                return True
        i = j + 1


def _frontmatter_name(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for ln in lines[1:80]:
        if ln.strip() == "---":
            break
        m = re.match(r"^name:\s*(.+?)\s*$", ln)
        if m:
            return m.group(1).strip("\"'").strip()
    return None


gate_extra = {}
_by_name = {}
for p in iter_files():
    if os.path.basename(p) != "SKILL.md":
        continue
    t = read_text(p)
    if t is None:
        continue
    nm = _frontmatter_name(t)
    if nm:
        _by_name.setdefault(nm, []).append(os.path.relpath(p, root).replace(os.sep, "/"))
for nm, files_ in sorted(_by_name.items()):
    if len(files_) > 1:
        for f in files_:
            others = ", ".join(x for x in files_ if x != f)
            gate_extra.setdefault(f, []).append(
                "duplicate skill name: %s (also in %s)" % (nm, others))
for p in iter_files():
    rel = os.path.relpath(p, root).replace(os.sep, "/")
    if os.path.basename(p) in SKIP_FILES:
        continue
    if rel in DANGLING_SCAN_SKIP:
        continue
    if os.path.splitext(p)[1].lower() not in TEXT_EXTS:
        continue
    allow = DANGLING_ALLOWLIST.get(rel)
    if allow == "*":
        continue
    t = read_text(p)
    if t is None:
        continue
    for entry in excluded_paths:
        if allow and entry in allow:
            continue
        if _is_path_reference(t, entry):
            gate_extra.setdefault(rel, []).append(
                "dangling reference to excluded path: %s" % entry)
if not gate_extra:
    print("GATE 1c clean: no duplicate skill names, no dangling excluded-path references")

if unscanned_binary:
    _ub = sorted(set(unscanned_binary))
    print("note: %d binary file(s) not content-scanned: %s"
          % (len(_ub), ", ".join(_ub[:10])))
if unscanned_text:
    _ut = sorted(set(unscanned_text))
    print("FAIL: %d text file(s) could not be scanned, publish aborted:" % len(_ut))
    for f in _ut:
        print("  %s" % f)
    sys.exit(1)

if hits or gate_extra:
    print("FAIL: blocked or unlisted identifiers present, publish aborted:")
    for f, bs in hits.items():
        print("  %s: %s" % (f, ", ".join(bs)))
    for f in sorted(gate_extra):
        print("  %s: %s" % (f, ", ".join(gate_extra[f])))
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
