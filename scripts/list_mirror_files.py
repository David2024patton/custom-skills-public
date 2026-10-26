"""Print the tracked files of the public mirror's main branch, hash pinned.

Usage: python3 list_mirror_files.py <mirror-git-url>
Clones the mirror shallow into a temp directory and prints one line per
tracked file in the form path<TAB>sha256, where sha256 is the SHA-256 hex
of the file bytes in the clone. Used by publish-public-mirror.sh to build
the known-files list for the sanitizer: a snapshot file gets baseline
treatment for generic identifier scans only when its bytes still hash to
the pin, so an edited known file is scanned as new (round 2 finding U1).
Exits nonzero if the mirror cannot be cloned, so the caller can fall back
to an empty list (fail safe: every file is then reported as new).
"""
import hashlib, os, shutil, subprocess, sys, tempfile

url = sys.argv[1]
tmp = tempfile.mkdtemp(prefix="mirror-list-")
try:
    dest = os.path.join(tmp, "m")
    r = subprocess.run(["git", "clone", "--quiet", "--depth", "1", url, dest],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    r = subprocess.run(["git", "-C", dest, "ls-files"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    out = []
    for line in r.stdout.splitlines():
        rel = line.strip()
        if not rel:
            continue
        fpath = os.path.join(dest, rel.replace("/", os.sep))
        try:
            h = hashlib.sha256()
            with open(fpath, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
        except OSError as exc:
            sys.stderr.write("cannot hash tracked file %s: %s\n" % (rel, exc))
            sys.exit(1)
        out.append("%s\t%s" % (rel.replace(os.sep, "/"), h.hexdigest()))
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
