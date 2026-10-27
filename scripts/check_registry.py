#!/usr/bin/env python3
"""Check registry.json and skill-aliases.json against a collection tree.

Usage:
  python3 scripts/check_registry.py <tree-root>

Loads registry.json and skill-aliases.json at the given root and verifies
them against the files actually present in that tree:

  - every record's path exists in the tree;
  - every record's checksum matches the SHA-256 of the file it names,
    using the generator's checksum definition exactly (the SHA-256 of
    the unit's main file: SKILL.md when present, else skill.yaml, else
    SOUL.md for a persona folder);
  - generated_from_commit in each file is a 40 character hex string;
  - every alias target names a canonical record present in the registry
    and every alias path exists in the tree;
  - no self-alias exists (an alias equal to its canonical id).

The generated_from_commit stamp is also checked for verifiability, as a
warning only. Warnings never change the exit code: the public snapshot
history is parentless, so ancestry can never hold there and the gate must
not start failing on the public tree. When the tree is inside a git
checkout, the stamp is tested with git cat-file and
git merge-base --is-ancestor against HEAD; a stamp that exists but is not
an ancestor of HEAD prints a WARNING line. When git is unavailable, the
tree is not a git checkout, or the stamped commit object is absent, a
WARNING line notes that the stamp names the private source commit and is
not verifiable in this checkout.

Exit codes: 0 when the registry is clean (a summary is printed), 1 when
any check fails (one line is printed per failure), 2 on usage error.
"""
import argparse, hashlib, json, os, re, subprocess, sys

COMMIT_RX = re.compile(r"^[0-9a-fA-F]{40}$")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main_file_for(root, rel):
    """Return the unit main file path for a record path, or None."""
    folder = os.path.join(root, rel)
    for name in ("SKILL.md", "skill.yaml", "SOUL.md"):
        candidate = os.path.join(folder, name)
        if os.path.isfile(candidate):
            return candidate
    return None


def stamp_warnings(root, commit):
    """Return WARNING lines about the stamp commit, never failures."""
    if not (isinstance(commit, str) and COMMIT_RX.match(commit)):
        return []

    def not_verifiable(reason):
        return ("WARNING: generated_from_commit %s names the private "
                "source commit and is not verifiable in this checkout "
                "(%s)" % (commit, reason))
    try:
        inside = subprocess.run(
            ["git", "rev-parse", "--git-dir"], cwd=root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=30)
    except Exception:
        return [not_verifiable("git is unavailable")]
    if inside.returncode != 0:
        return [not_verifiable("not a git checkout")]
    try:
        present = subprocess.run(
            ["git", "cat-file", "-e", commit + "^{commit}"], cwd=root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=30)
    except Exception:
        return [not_verifiable("git is unavailable")]
    if present.returncode != 0:
        return [not_verifiable("commit object is absent")]
    try:
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=30)
    except Exception:
        return [not_verifiable("git is unavailable")]
    if ancestor.returncode != 0:
        return ["WARNING: generated_from_commit %s is not an ancestor "
                "of HEAD in this checkout" % commit]
    return []


def load_json(path, failures):
    if not os.path.isfile(path):
        failures.append("%s: file is missing" % path)
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        failures.append("%s: cannot parse JSON (%s)" % (path, e))
        return None


def check(root):
    failures = []
    registry = load_json(os.path.join(root, "registry.json"), failures)
    aliases_doc = load_json(os.path.join(root, "skill-aliases.json"),
                            failures)
    if registry is None or aliases_doc is None:
        return failures, None, []
    warnings = stamp_warnings(root, registry.get("generated_from_commit"))
    for label, doc in (("registry.json", registry),
                       ("skill-aliases.json", aliases_doc)):
        commit = doc.get("generated_from_commit")
        if not (isinstance(commit, str) and COMMIT_RX.match(commit)):
            failures.append(
                "%s: generated_from_commit %r is not a 40 character "
                "hex string" % (label, commit))
    units = registry.get("units") or []
    canonical_ids = set()
    for u in units:
        if u.get("role") == "canonical":
            canonical_ids.add(u.get("id"))
    all_ids = {u.get("id") for u in units}
    for u in units:
        uid = u.get("id")
        rel = u.get("path") or ""
        main_file = main_file_for(root, rel)
        if main_file is None:
            failures.append(
                "record %s: path %s is absent from the tree" % (uid, rel))
            continue
        actual = sha256_of(main_file)
        if actual != u.get("checksum_sha256"):
            failures.append(
                "record %s: checksum mismatch for %s (registry %s, "
                "file %s)" % (uid, rel, u.get("checksum_sha256"), actual))
    aliases = aliases_doc.get("aliases") or []
    for a in aliases:
        alias = a.get("alias")
        target = a.get("canonical_id")
        rel = a.get("path") or ""
        if alias == target:
            failures.append(
                "alias %s: self-alias (alias equals canonical_id %s)"
                % (alias, target))
        if target not in canonical_ids and target not in all_ids:
            failures.append(
                "alias %s: canonical target %s is missing from the "
                "registry" % (alias, target))
        elif target not in canonical_ids:
            failures.append(
                "alias %s: canonical target %s is not a canonical "
                "record" % (alias, target))
        if not os.path.exists(os.path.join(root, rel)):
            failures.append(
                "alias %s: path %s is absent from the tree" % (alias, rel))
    summary = {
        "records": len(units),
        "aliases": len(aliases),
        "commit": registry.get("generated_from_commit"),
    }
    return failures, summary, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check_registry.py",
        description="Verify registry.json and skill-aliases.json "
                    "against the collection tree at the given root.")
    parser.add_argument("root", help="collection tree root to check")
    args = parser.parse_args(argv)
    root = args.root
    if not os.path.isdir(root):
        print("check_registry: root is not a directory: %s" % root)
        return 1
    failures, summary, warnings = check(root)
    for line in warnings:
        print(line)
    if failures:
        for line in failures:
            print(line)
        print("check_registry: FAIL: %d failure(s)" % len(failures))
        return 1
    print("check_registry: OK: %d records, %d aliases, "
          "generated_from_commit %s"
          % (summary["records"], summary["aliases"], summary["commit"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
