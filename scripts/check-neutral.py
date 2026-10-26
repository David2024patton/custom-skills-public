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
  HARD-COUNT    "N skills/personas" claims in index docs that disagree
                with registry.json counts (only with --registry)

Binding sections (a heading containing "Local binding", per
WORDING-STANDARD.md, or <!-- local-binding:start/end --> comments) are
exempt from ABS-PATH and RUNTIME-LEAK only. Nothing is exempt from
PERSON-NAME or MACHINE-NAME when a config supplies those lists.

Usage:
  python3 check-neutral.py <path> [<path> ...]
      [--config neutral-config.json] [--registry registry.json]
      [--format text|json] [--self-test]

Config JSON shape: {"person_names": [...], "machine_names": [...]}.
Without a config, PERSON-NAME and MACHINE-NAME are skipped and the skip is
reported on stderr (never silently).

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


def diag(msg):
    print("check-neutral: %s" % msg, file=sys.stderr)


def iter_files(paths):
    for base in paths:
        if os.path.isfile(base):
            yield base
        elif os.path.isdir(base):
            for dirpath, dirs, files in os.walk(base):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in sorted(files):
                    if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                        yield os.path.join(dirpath, fn)
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


def check_file(path, config, registry_counts):
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
        if registry_counts and base in ("README.md", "MANIFEST.md"):
            for m in COUNT_CLAIM.finditer(ln):
                n, unit = int(m.group(1)), m.group(2)
                key = "personas" if unit == "personas" else "skills"
                actual = registry_counts.get(key)
                if actual is not None and n != actual:
                    hits.append({"file": path, "line": lno, "class": "HARD-COUNT",
                                 "text": "claims %d %s, registry says %d" % (n, unit, actual)})
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
    registry_counts = None
    if "--registry" in opts:
        reg = json.load(open(opts["--registry"], encoding="utf-8"))
        units = reg.get("units", [])
        registry_counts = {
            "skills": sum(1 for u in units if u.get("kind") == "skill"),
            "personas": sum(1 for u in units if u.get("kind") == "persona"),
        }
    all_hits = []
    for p in iter_files(args):
        all_hits.extend(check_file(p, config, registry_counts))
    if opts.get("--format") == "json":
        print(json.dumps(all_hits, indent=1))
    else:
        for h in all_hits:
            print("%s:%s %s %s" % (h["file"], h["line"], h["class"], h["text"]))
        print("check-neutral: %d violation(s) in %d file(s)"
              % (len(all_hits), len(set(h["file"] for h in all_hits))), file=sys.stderr)
    return 1 if all_hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
