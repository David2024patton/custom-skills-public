#!/usr/bin/env python3
"""Fixture tests for scripts/build-registry.py and scripts/check_registry.py.

Builds small fixture trees in a temporary directory and asserts:

  - the generator stamps the commit passed via --from-commit into both
    output files and never writes the old placeholder stamp;
  - the generator refuses (exit 2, nothing written) when no commit is
    available, run in a non-git temporary root without --from-commit;
  - the generator refuses (exit 2, nothing written) when --from-commit
    carries a value that is not a 40 character hex string, such as the
    literal placeholder "working-tree";
  - the generator --help exits 0 and writes nothing;
  - trigger tags survive a flattened frontmatter layout (tags placed as
    siblings of hermes under metadata, with hermes not a mapping);
  - check_registry.py exits 0 on a clean generated fixture;
  - check_registry.py exits 1 on a fixture whose registry names an
    absent path.

Prints one PASS or FAIL line per test and exits nonzero on any failure.
Run: python3 scripts/test_registry.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GENERATOR = os.path.join(HERE, "build-registry.py")
CHECKER = os.path.join(HERE, "check_registry.py")
TEST_COMMIT = "0123456789abcdef0123456789abcdef01234567"

RESULTS = []


def report(name, ok, detail=""):
    RESULTS.append((name, ok))
    print("%s: %s%s" % ("PASS" if ok else "FAIL", name,
                         (" (%s)" % detail) if detail else ""))


def run(args, cwd=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run([sys.executable] + args, cwd=cwd, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True, timeout=120)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def make_fixture(root):
    write(os.path.join(root, "demo-skill", "SKILL.md"),
          "---\n"
          "name: demo-skill\n"
          "description: \"Demo skill for registry tests.\"\n"
          "license: MIT\n"
          "metadata:\n"
          "  hermes:\n"
          "    tags: [demo, fixture]\n"
          "    category: meta\n"
          "---\n\n# Demo\n")
    # Flattened layout: tags sit as siblings of hermes under metadata
    # and hermes itself is not a mapping. The tags must still land in
    # the generated record's trigger keywords.
    write(os.path.join(root, "flat-skill", "SKILL.md"),
          "---\n"
          "name: flat-skill\n"
          "description: \"Flattened frontmatter fixture.\"\n"
          "license: MIT\n"
          "metadata:\n"
          "  hermes: flattened\n"
          "  tags: [alpha, beta]\n"
          "---\n\n# Flat\n")
    write(os.path.join(root, "personas", "demo", "SOUL.md"),
          "# Demo persona\n")


def test_stamps_commit(base):
    root = os.path.join(base, "stamped")
    os.makedirs(root)
    make_fixture(root)
    proc = run([GENERATOR, "--root", root, "--from-commit", TEST_COMMIT])
    if proc.returncode != 0:
        report("generator stamps --from-commit", False,
               "generator exited %d: %s" % (proc.returncode,
                                           proc.stderr.strip()[:200]))
        return None
    ok = True
    detail = ""
    for name in ("registry.json", "skill-aliases.json"):
        path = os.path.join(root, name)
        text = open(path, encoding="utf-8").read()
        doc = json.loads(text)
        if doc.get("generated_from_commit") != TEST_COMMIT:
            ok = False
            detail = "%s stamped %r" % (name,
                                        doc.get("generated_from_commit"))
        if "working-tree" in text:
            ok = False
            detail = "%s contains the placeholder stamp" % name
    report("generator stamps --from-commit and never the placeholder",
           ok, detail)
    return root


def test_flattened_tags(root):
    if root is None:
        report("flattened frontmatter tags survive", False,
               "no generated fixture")
        return
    doc = json.load(open(os.path.join(root, "registry.json"),
                         encoding="utf-8"))
    rec = next((u for u in doc["units"] if u["id"] == "flat-skill"), None)
    keywords = (rec or {}).get("triggers", {}).get("keywords", [])
    ok = rec is not None and "alpha" in keywords and "beta" in keywords
    report("flattened frontmatter tags survive", ok,
           "keywords=%s" % (keywords,))


def test_refuses_without_commit(base):
    root = os.path.join(base, "no-commit")
    os.makedirs(root)
    make_fixture(root)
    proc = run([GENERATOR, "--root", root], cwd=root)
    wrote = os.path.exists(os.path.join(root, "registry.json")) or \
        os.path.exists(os.path.join(root, "skill-aliases.json"))
    ok = proc.returncode == 2 and not wrote
    report("generator refuses with exit 2 and writes nothing when no "
           "commit is available", ok,
           "exit=%d wrote=%s" % (proc.returncode, wrote))


def test_bad_from_commit(base):
    root = os.path.join(base, "bad-commit")
    os.makedirs(root)
    make_fixture(root)
    proc = run([GENERATOR, "--root", root, "--from-commit", "working-tree"])
    wrote = os.path.exists(os.path.join(root, "registry.json")) or \
        os.path.exists(os.path.join(root, "skill-aliases.json"))
    ok = proc.returncode == 2 and not wrote
    report("generator refuses a bad --from-commit with exit 2 and "
           "writes nothing", ok,
           "exit=%d wrote=%s" % (proc.returncode, wrote))


def test_help_writes_nothing(base):
    root = os.path.join(base, "help")
    os.makedirs(root)
    proc = run([GENERATOR, "--help"])
    ok = proc.returncode == 0 and "usage" in proc.stdout.lower() and \
        not os.listdir(root)
    report("generator --help exits 0 and writes nothing", ok,
           "exit=%d" % proc.returncode)


def test_check_clean(root):
    if root is None:
        report("check_registry exits 0 on a clean fixture", False,
               "no generated fixture")
        return
    proc = run([CHECKER, root])
    report("check_registry exits 0 on a clean fixture",
           proc.returncode == 0,
           "exit=%d out=%s" % (proc.returncode, proc.stdout.strip()[:200]))


def test_check_absent_path(base, root):
    if root is None:
        report("check_registry exits 1 on an absent path", False,
               "no generated fixture")
        return
    broken = os.path.join(base, "broken")
    shutil.copytree(root, broken)
    reg_path = os.path.join(broken, "registry.json")
    doc = json.load(open(reg_path, encoding="utf-8"))
    doc["units"][0]["path"] = "no-such-unit-anywhere"
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    proc = run([CHECKER, broken])
    ok = proc.returncode == 1 and "absent" in proc.stdout
    report("check_registry exits 1 on an absent path", ok,
           "exit=%d out=%s" % (proc.returncode, proc.stdout.strip()[:200]))


def main():
    with tempfile.TemporaryDirectory() as base:
        stamped = test_stamps_commit(base)
        test_flattened_tags(stamped)
        test_refuses_without_commit(base)
        test_bad_from_commit(base)
        test_help_writes_nothing(base)
        test_check_clean(stamped)
        test_check_absent_path(base, stamped)
    failed = [n for n, ok in RESULTS if not ok]
    print("test_registry: %d passed, %d failed"
          % (len(RESULTS) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
