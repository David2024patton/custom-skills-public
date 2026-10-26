"""Regression tests for sanitize_snapshot.py (round 2 finding U1).

Usage: python3 test_sanitize_snapshot.py
Builds a temp snapshot with fixture files and a fixture redact map, runs
the sanitizer as a subprocess, and asserts:

(a) U1 bypass case: a known file edited to append a private-range IP
    FAILS the gate, and the output names the file. Under the old
    path-only baseline this passed silently. The IP value itself is
    assembled at runtime from parts (see PRIVATE_IP below): written
    literally, it would trip the private redact map's blocked patterns
    (gate 1a) whenever this test file itself ships in a snapshot.
(b) The same file unedited, with a matching hash pin, gets baseline
    treatment in gate 1b: its benign pre-existing generic hit (an
    upstream maintainer email) is reported as baseline, not fatal, and
    the run passes.
(c) Running without scripts/redact-map.json exits with code 3 and no
    traceback text (graceful private-config exit for the public tree).
(d) Round 3 finding M1: a known file edited to append an AWS-shaped
    access key id, with an EMPTY redact map, FAILS the gate with code 1.
    The generic scan must catch generic secret shapes on its own, with
    no private list entry pointing at the value. The key value is
    assembled at runtime from parts, like PRIVATE_IP below, so this
    test file never carries the literal shape itself.

Prints PASS or FAIL per case and exits nonzero on any failure.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SANITIZER = os.path.join(HERE, "sanitize_snapshot.py")

# The fixture maintainer email, assembled from parts for the same reason
# as PRIVATE_IP below: written literally in this source file, it would be
# a generic-scan hit in a file that is new to the snapshot on its first
# publish, and new-file generic hits are fatal with no override.
FIXTURE_EMAIL = "maintainer@" + "some-upstream.org"
FIXTURE_BODY = (
    "# Fixture Skill\n"
    "\n"
    "Contact %s for help with this skill.\n"
    "Documentation example only: user@example.com\n"
) % FIXTURE_EMAIL
# The planted private-range host address, assembled from parts on purpose
# (see the module docstring). At runtime this is exactly the U1 case value.
PRIVATE_IP = "192.168." + "10.55"
PRIVATE_IP_LINE = "Mirror host: %s\n" % PRIVATE_IP
# An AWS-shaped access key id, assembled from parts for the same reason
# as PRIVATE_IP above: AKIA plus exactly 16 uppercase alphanumerics.
AWS_KEY = "AKIA" + "IOSFODNN7" + "EXAMPLE"
AWS_KEY_LINE = "Leaked key: %s\n" % AWS_KEY


def build_case(tmp, with_redact=True, edit_known=False, append_aws=False):
    """Create (scripts_dir, snapshot_dir, known_files_path) under tmp."""
    scripts_dir = os.path.join(tmp, "scripts")
    os.makedirs(scripts_dir)
    shutil.copyfile(SANITIZER, os.path.join(scripts_dir, "sanitize_snapshot.py"))
    if with_redact:
        with open(os.path.join(scripts_dir, "redact-map.json"), "w", encoding="utf-8") as fh:
            json.dump({"redact": {}, "blocked_subdomains": [], "allowed": [],
                       "blocked_patterns": [], "banned_words": [],
                       "inline_replace": []}, fh)
    with open(os.path.join(scripts_dir, "public-exclude.json"), "w", encoding="utf-8") as fh:
        json.dump({"exclude": []}, fh)
    snap = os.path.join(tmp, "snap")
    os.makedirs(snap)
    with open(os.path.join(snap, "doc.md"), "w", encoding="utf-8", newline="") as fh:
        fh.write(FIXTURE_BODY)
    pin = hashlib.sha256(FIXTURE_BODY.encode("utf-8")).hexdigest()
    if edit_known:
        with open(os.path.join(snap, "doc.md"), "a", encoding="utf-8", newline="") as fh:
            fh.write(PRIVATE_IP_LINE)
    if append_aws:
        with open(os.path.join(snap, "doc.md"), "a", encoding="utf-8", newline="") as fh:
            fh.write(AWS_KEY_LINE)
    known = os.path.join(tmp, "known-files.txt")
    with open(known, "w", encoding="utf-8", newline="") as fh:
        fh.write("doc.md\t%s\n" % pin)
    return scripts_dir, snap, known


def run_sanitizer(scripts_dir, snap, known=None):
    cmd = [sys.executable, os.path.join(scripts_dir, "sanitize_snapshot.py"), snap]
    if known:
        cmd.append(known)
    env = dict(os.environ)
    env.pop("SANITIZE_APPROVE_NEW", None)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    failures = 0

    # (b) unedited known file with matching pin: baseline treatment, passes.
    with tempfile.TemporaryDirectory(prefix="san-test-b-") as tmp:
        scripts_dir, snap, known = build_case(tmp)
        rc, out = run_sanitizer(scripts_dir, snap, known)
        ok = (rc == 0 and "baseline" in out.lower() and "doc.md" in out
              and "FAIL" not in out)
        print("%s case (b): unedited hash-pinned known file passes gate 1b "
              "as baseline (rc=%d)" % ("PASS" if ok else "FAIL", rc))
        if not ok:
            failures += 1
            print(out)

    # (a) U1 bypass: same known file edited with a private-range IP fails.
    with tempfile.TemporaryDirectory(prefix="san-test-a-") as tmp:
        scripts_dir, snap, known = build_case(tmp, edit_known=True)
        rc, out = run_sanitizer(scripts_dir, snap, known)
        ok = (rc == 1 and "doc.md" in out and PRIVATE_IP in out)
        print("%s case (a): edited known file with planted private IP "
              "%s fails the gate and names the file (rc=%d)"
              % ("PASS" if ok else "FAIL", PRIVATE_IP, rc))
        if not ok:
            failures += 1
            print(out)

    # (c) missing private redact map: graceful exit 3, no traceback.
    with tempfile.TemporaryDirectory(prefix="san-test-c-") as tmp:
        scripts_dir, snap, known = build_case(tmp, with_redact=False)
        rc, out = run_sanitizer(scripts_dir, snap)
        nonempty = [ln for ln in out.splitlines() if ln.strip()]
        ok = (rc == 3 and "Traceback" not in out and len(nonempty) == 1
              and "private" in out.lower())
        print("%s case (c): missing redact-map.json exits 3 with one clear "
              "line and no traceback (rc=%d)" % ("PASS" if ok else "FAIL", rc))
        if not ok:
            failures += 1
            print(out)

    # (d) M1: edited known file with an appended AWS-shaped key and an
    # empty redact map fails on the generic secret-shape scan alone.
    with tempfile.TemporaryDirectory(prefix="san-test-d-") as tmp:
        scripts_dir, snap, known = build_case(tmp, append_aws=True)
        rc, out = run_sanitizer(scripts_dir, snap, known)
        ok = (rc == 1 and "doc.md" in out and AWS_KEY in out)
        print("%s case (d): edited known file with appended AWS-shaped "
              "key and empty redact map fails the gate (rc=%d)"
              % ("PASS" if ok else "FAIL", rc))
        if not ok:
            failures += 1
            print(out)

    if failures:
        print("RESULT: FAIL (%d case(s) failed)" % failures)
        return 1
    print("RESULT: PASS (all 4 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
