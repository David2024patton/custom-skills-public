#!/usr/bin/env python3
"""Turn a GitHub repo into a prompt-ready text digest for the knowledge base.

Usage:
  python ingest.py <github-url> <label>
  python ingest.py --batch            # ingest the curated priority set

Writes knowledge/<label>.md (summary + directory tree + file contents).
Labels map to the language/domain the digest serves, so a persona working in
that language loads only its own digest (fits the 1M window per-language,
not all-at-once).
"""
import os, re, subprocess, sys, json

KB = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# Curated priority set: David's stack + the cross-language masters.
# label -> github url
BATCH = {
    "go":          "https://github.com/avelino/awesome-go",
    "dart":        "https://github.com/yissachar/awesome-dart",
    "python":      "https://github.com/vinta/awesome-python",
    "cpp":         "https://github.com/fffaraz/awesome-cpp",
    "java":        "https://github.com/akullpp/awesome-java",
    "javascript":  "https://github.com/Chalarangelo/30-seconds-of-code",
    "awesome":     "https://github.com/sindresorhus/awesome",
    "c":           "https://github.com/aleksandar-todorovic/awesome-c",
}

USAGE = ("usage: python3 ingest.py <github-url> <label>\n"
         "       python3 ingest.py --batch\n"
         "label must be a plain token: ^[A-Za-z0-9][A-Za-z0-9._-]*$ "
         "with no '..' sequence and no path separator")

_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

def valid_label(label: str) -> bool:
    """A label becomes a file name inside KB, so it must stay a plain
    token: no path separator, no '..' sequence, nothing that could make
    os.path.join(KB, label + '.md') land outside the knowledge base."""
    return (bool(_LABEL_RE.match(label)) and ".." not in label
            and "/" not in label and "\\" not in label)

def require_valid_label(label: str) -> None:
    if not valid_label(label):
        sys.stderr.write("error: invalid label %r\n%s\n" % (label, USAGE))
        sys.exit(2)

def ingest(url: str, label: str) -> str:
    require_valid_label(label)
    out = os.path.join(KB, label + ".md")
    # gitingest streams structured text to stdout with -o -
    proc = subprocess.run(
        [PY, "-m", "gitingest", url, "-o", "-", "-s", "2097152"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    # gitingest logs go to stderr; stdout is the digest (but it may interleave) -> use -o file instead
    if proc.returncode != 0 or len(proc.stdout) < 200:
        tmp = out + ".tmp"
        proc2 = subprocess.run(
            [PY, "-m", "gitingest", url, "-o", tmp, "-s", "2097152"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if os.path.exists(tmp):
            content = open(tmp, encoding="utf-8", errors="replace").read()
            os.remove(tmp)
        else:
            return "FAIL %s (%s)" % (label, proc2.stderr[-200:])
    else:
        content = proc.stdout
    # strip any leaked log lines that slipped into stdout
    lines = [l for l in content.splitlines() if not l.startswith("20") or "| INFO" not in l]
    content = "\n".join(lines)
    header = ("# Knowledge digest: %s\nSource: %s\nGenerated: %s\n"
              "Load ONLY when working in this language/domain.\n\n---\n\n"
              % (label, url, __import__("datetime").datetime.utcnow().isoformat()[:19] + "Z"))
    open(out, "w", encoding="utf-8").write(header + content)
    tokens = len(content) // 4
    return "OK   %-12s %8d bytes  ~%d tokens" % (label, len(content), tokens)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        require_valid_label(sys.argv[2])
        result = ingest(sys.argv[1], sys.argv[2])
        print(result)
        if result.startswith("FAIL"):
            sys.exit(1)
    elif len(sys.argv) >= 2 and sys.argv[1] == "--batch":
        results = []
        for label, url in BATCH.items():
            print("ingesting", label, "from", url, flush=True)
            results.append(ingest(url, label))
        print("\n".join(results))
        failures = sum(1 for r in results if r.startswith("FAIL"))
        print("SUMMARY: %d succeeded, %d failed, %d total" % (len(results) - failures, failures, len(results)))
        if failures:
            sys.exit(1)
    else:
        print(__doc__)
