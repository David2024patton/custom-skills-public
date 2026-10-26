"""Print the tracked file paths of the public mirror's main branch.

Usage: python list_mirror_files.py <mirror-git-url>
Clones the mirror shallow into a temp directory and prints one path per
line. Used by publish-public-mirror.sh to build the known-files list for
the sanitizer's new-file review gate. Exits nonzero if the mirror cannot
be cloned, so the caller can fall back to an empty list (fail safe: every
file is then reported as new).
"""
import os, subprocess, sys, tempfile

url = sys.argv[1]
tmp = tempfile.mkdtemp(prefix="mirror-list-")
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
sys.stdout.write(r.stdout)
