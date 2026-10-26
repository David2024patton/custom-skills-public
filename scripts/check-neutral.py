#!/usr/bin/env python3
"""Neutrality lint for skill and persona text (the wording gate).

Implements the check proposed for the publish gate: published skill text
must be executable by any agent, so neutral core text carries no person
names, no machine names, no absolute local paths, no harness-specific
runtime vocabulary, and no hand-written collection counts.

Rule classes:
  PERSON-NAME   literal match against a config-supplied name list
  MACHINE-NAME  literal match against a config-supplied machine list
  ABS-PATH      generic absolute local path patterns (no private values)
  RUNTIME-LEAK  harness-specific tool vocabulary in method text
  HARD-COUNT    count claims in index docs that disagree with counts
                recomputed from files on disk in the tree the document
                belongs to (never from registry.json). The README
                skill.yaml sentence is checked against the whole tree:
                the skill.yaml count and the total SKILL.md count. The
                MANIFEST skills/ row is checked against the SKILL.md
                count in the skills/ subtree only.

Binding sections (a heading containing "Local binding", per
WORDING-STANDARD.md, or <!-- local-binding:start/end --> comments) are
exempt from ABS-PATH and RUNTIME-LEAK only. Nothing is exempt from
PERSON-NAME or MACHINE-NAME when a config supplies those lists.

Self-exemption: the checker sources and the wording standard's own
documents are exempt from their own scans. The exempt paths are
scripts/check-neutral.py, scripts/wording-scan.py, and
WORDING-STANDARD.md. The exemptions are printed in the run output.

Usage:
  python3 check-neutral.py <path> [<path> ...]
      [--config neutral-config.json] [--registry registry.json]
      [--format text|json] [--self-test]

The --registry option is accepted for compatibility and is not used
for HARD-COUNT, which is always recomputed from files on disk.

Config JSON shape: {"person_names": [...], "machine_names": [...]}.
Without a config, PERSON-NAME and MACHINE-NAME are skipped. Each skip
is printed as an explicit SKIP line in the summary, never silently.

Exit codes: 0 clean, 1 violations found, 2 usage or input error.
Diagnostics go to stderr; the report goes to stdout.
"""
import json, os, re, sys

TEXT_EXTS = {".md", ".txt", ".yaml", ".yml", ".json", ".toml"}
SKIP_DIRS = {".git", "__pycache__", ".locks", ".hub"}

ABS_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\[^\s\\]+"),
    re.compile(r"[A-Za-z]:/[Uu]sers/[^\s/]+"),
    re.compile(r"/Users/[^\s/]+/"),
    re.compile(r"/home/[a-z_][a-z0-9_-]*/"),
    re.compile(r"G:/[^\s]+"),
    re.compile(r"~/\.hermes/"),
]
RUNTIME_TERMS = [
    "delegate_task", "web_search", "web_extract", "spawn_agent",
    "run_agent", "hermes-agent", "claude-code", "codex-cli",
]
COUNT_CLAIM = re.compile(r"\b(\d{2,4})\s+(skills|personas|SKILL\.md)\b")
README_YAML_CLAIM = re.compile(
    r"\b(\d+)\s+of\s+the\s+(\d+)\s+skills\b")

SELF_EXEMPT_RELS = (
    "scripts/check-neutral.py",
    "scripts/wording-scan.py",
    "WORDING-STANDARD.md",
)
EXEMPTED_SEEN = []
_DISK_COUNT_CACHE = {}


def is_self_exempt(path):
    norm = path.replace(os.sep, "/")
    for rel in SELF_EXEMPT_RELS:
        if norm == rel or norm.endswith("/" + rel):
            return rel
    return None


def note_exempt(rel):
    if rel not in EXEMPTED_SEEN:
        EXEMPTED_SEEN.append(rel)


def diag(msg):
    print("check-neutral: %s" % msg, file=sys.stderr)


def disk_counts(root):
    """Recompute collection counts from files on disk under root."""
    root = os.path.abspath(root)
    if root in _DISK_COUNT_CACHE:
        return _DISK_COUNT_CACHE[root]
    total_skill_md = 0
    skill_yaml = 0
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "SKILL.md" in files:
            total_skill_md += 1
        if "skill.yaml" in files:
            skill_yaml += 1
    skills_subtree = 0
    skills_root = os.path.join(root, "skills")
    if os.path.isdir(skills_root):
        for dirpath, dirs, files in os.walk(skills_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if "SKILL.md" in files:
                skills_subtree += 1
    personas = 0
    personas_root = os.path.join(root, "personas")
    if os.path.isdir(personas_root):
        for dirpath, dirs, files in os.walk(personas_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if "SOUL.md" in files:
                personas += 1
    counts = {
        "skills": total_skill_md,
        "skill_md_total": total_skill_md,
        "skill_yaml": skill_yaml,
        "skills_subtree": skills_subtree,
        "personas": personas,
    }
    _DISK_COUNT_CACHE[root] = counts
    return counts


def iter_files(paths):
    for base in paths:
        if os.path.isfile(base):
            rel = is_self_exempt(base)
            if rel:
                note_exempt(rel)
                continue
            yield base
        elif os.path.isdir(base):
            for dirpath, dirs, files in os.walk(base):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in sorted(files):
                    p = os.path.join(dirpath, fn)
                    rel = is_self_exempt(p)
                    if rel:
                        note_exempt(rel)
                        continue
                    if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                        yield p
        else:
            diag("input not found: %s" % base)
            raise SystemExit(2)


def binding_spans(lines):
    """Return a set of 0-based line indexes inside a binding section."""
    inside = set()
    level = None
    comment_mode = False
    for i, ln in enumerate(lines):
        if "<!-- local-binding:start -->" in ln:
            comment_mode = True
            inside.add(i)
            continue
        if "<!-- local-binding:end -->" in ln:
            comment_mode = False
            inside.add(i)
            continue
        m = re.match(r"^(#{1,6})\s", ln)
        if m:
            lvl = len(m.group(1))
            if "local binding" in ln.lower():
                level = lvl
                inside.add(i)
                continue
            if level is not None and lvl <= level:
                level = None
        if comment_mode or level is not None:
            inside.add(i)
    return inside


def check_file(path, config, registry_counts=None):
    # registry_counts is accepted for compatibility and is never used:
    # HARD-COUNT is recomputed from files on disk, scoped per document.
    hits = []
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError) as e:
        diag("cannot read %s (%s); counted as a violation" % (path, e))
        return [{"file": path, "line": 0, "class": "UNREADABLE", "text": str(e)}]
    lines = text.splitlines()
    bound = binding_spans(lines)
    persons = config.get("person_names", [])
    machines = config.get("machine_names", [])
    base = os.path.basename(path)
    for i, ln in enumerate(lines):
        lno = i + 1
        for name in persons:
            if name and name in ln:
                hits.append({"file": path, "line": lno, "class": "PERSON-NAME", "text": name})
        for name in machines:
            if name and name in ln:
                hits.append({"file": path, "line": lno, "class": "MACHINE-NAME", "text": name})
        if i not in bound:
            for rx in ABS_PATH_PATTERNS:
                m = rx.search(ln)
                if m:
                    hits.append({"file": path, "line": lno, "class": "ABS-PATH", "text": m.group(0)})
            for term in RUNTIME_TERMS:
                if term in ln:
                    hits.append({"file": path, "line": lno, "class": "RUNTIME-LEAK", "text": term})
        if base in ("README.md", "MANIFEST.md"):
            counts = disk_counts(os.path.dirname(os.path.abspath(path)))
            handled = False
            if base == "README.md":
                m_yaml = README_YAML_CLAIM.search(ln)
                if m_yaml:
                    handled = True
                    n_yaml, n_total = int(m_yaml.group(1)), int(m_yaml.group(2))
                    if n_yaml != counts["skill_yaml"]:
                        hits.append({"file": path, "line": lno, "class": "HARD-COUNT",
                                     "text": "claims %d skill.yaml, tree has %d" % (n_yaml, counts["skill_yaml"])})
                    if n_total != counts["skill_md_total"]:
                        hits.append({"file": path, "line": lno, "class": "HARD-COUNT",
                                     "text": "claims %d skills, tree has %d" % (n_total, counts["skill_md_total"])})
            if not handled:
                for m in COUNT_CLAIM.finditer(ln):
                    n, unit = int(m.group(1)), m.group(2)
                    if base == "MANIFEST.md" and "`skills/`" in ln and unit in ("skills", "SKILL.md"):
                        actual = counts["skills_subtree"]
                        scope = "skills/ subtree has"
                    elif unit == "personas":
                        actual = counts["personas"]
                        scope = "tree has"
                    else:
                        actual = counts["skill_md_total"]
                        scope = "tree has"
                    if actual is not None and n != actual:
                        hits.append({"file": path, "line": lno, "class": "HARD-COUNT",
                                     "text": "claims %d %s, %s %d" % (n, unit, scope, actual)})
    return hits


def self_test():
    cases = [
        ("Use C:\\Users\\David\\file.md here", "ABS-PATH"),
        ("run delegate_task with this brief", "RUNTIME-LEAK"),
        ("search the web for the topic", None),
    ]
    cfg = {"person_names": [], "machine_names": []}
    ok = True
    import tempfile
    for body, expect in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(body + "\n")
            p = f.name
        hits = check_file(p, cfg, None)
        got = hits[0]["class"] if hits else None
        status = "ok" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print("self-test %s: %r -> %s (expected %s)" % (status, body[:32], got, expect))
        os.unlink(p)
    return 0 if ok else 1


VALUE_OPTS = {"--config", "--registry", "--format"}


def parse_args(argv):
    args, opts = [], {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and "=" in a:
            k, v = a.split("=", 1)
            opts[k] = v
        elif a in VALUE_OPTS and i + 1 < len(argv):
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
    if not args:
        diag("usage: check-neutral.py <path> [...] [--config f] [--registry f] [--format text|json]")
        return 2
    config = {}
    if "--config" in opts:
        config = json.load(open(opts["--config"], encoding="utf-8"))
    else:
        diag("no --config given: PERSON-NAME and MACHINE-NAME checks skipped")
    if "--registry" in opts:
        diag("--registry given: accepted for compatibility, not used for HARD-COUNT (counts are recomputed from files on disk)")
    skipped = []
    if not config.get("person_names"):
        skipped.append("PERSON-NAME")
    if not config.get("machine_names"):
        skipped.append("MACHINE-NAME")
    all_hits = []
    for p in iter_files(args):
        all_hits.extend(check_file(p, config, None))
    exempt_lines = ["Self-exempt (not scanned): %s" % rel
                    for rel in SELF_EXEMPT_RELS]
    skip_lines = ["SKIP %s: no private config supplied, class not checked" % cls
                  for cls in skipped]
    if opts.get("--format") == "json":
        print(json.dumps(all_hits, indent=1))
        for ln in exempt_lines + skip_lines:
            diag(ln)
    else:
        for h in all_hits:
            print("%s:%s %s %s" % (h["file"], h["line"], h["class"], h["text"]))
        for ln in exempt_lines:
            print(ln)
        for ln in skip_lines:
            print(ln)
        print("check-neutral summary: %d violation(s) in %d file(s)"
              % (len(all_hits), len(set(h["file"] for h in all_hits))))
        print("check-neutral: %d violation(s) in %d file(s)"
              % (len(all_hits), len(set(h["file"] for h in all_hits))), file=sys.stderr)
        for ln in exempt_lines + skip_lines:
            diag(ln)
    return 1 if all_hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
