"""Check license integrity across folders with identical SKILL.md bodies.

Usage: python3 check_license_integrity.py [tree-root]
The root defaults to the repo root (the parent of this script's folder).

Two rules, both fail-closed (exit 1 with one printed line per violation):

1. Local-copy LICENSE rule: when a folder whose name starts with "local-"
   has a SKILL.md body (frontmatter stripped, whitespace normalized)
   identical to another folder's body, and that other (canonical) folder
   declares the MIT license (frontmatter license field, or a LICENSE file
   naming MIT), the local folder must carry its own LICENSE file. A copy
   of MIT-licensed text shipped without the license text breaks the MIT
   condition that the copyright and permission notice travel with copies.

2. Alias rule: any two folders with identical normalized SKILL.md bodies
   must be declared as an alias pair in skill-aliases.json at the tree
   root (an entry whose path is one folder and whose canonical_id
   resolves to the other). Undeclared identical copies drift apart
   silently; declared aliases are data a consumer can resolve.

Folders whose normalized body is empty are ignored. Exit 0 and a clean
line when there are no violations. Exit 2 on usage errors.
"""
import json, os, re, sys


def split_frontmatter(text):
    """Return (frontmatter_text, body_text). Frontmatter is optional."""
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, re.S)
    if m:
        return m.group(1), text[m.end():]
    return "", text


def frontmatter_field(fm, field):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(field), fm, re.M)
    if not m:
        return None
    return m.group(1).strip().strip("\"'").strip()


def license_of(folder_abs, fm):
    """Best available license declaration for a folder, normalized upper."""
    val = frontmatter_field(fm, "license")
    if val:
        return val.upper()
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        p = os.path.join(folder_abs, name)
        if os.path.isfile(p):
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if "MIT" in t:
                return "MIT"
            return t.strip().splitlines()[0].upper() if t.strip() else None
    return None


def has_license_file(folder_abs):
    return any(os.path.isfile(os.path.join(folder_abs, n))
               for n in ("LICENSE", "LICENSE.md", "LICENSE.txt"))


def main(argv):
    if len(argv) > 2:
        sys.stderr.write("usage: python3 check_license_integrity.py [tree-root]\n")
        return 2
    if len(argv) == 2:
        root = os.path.abspath(argv[1])
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(root):
        sys.stderr.write("ERROR: tree root not found: %s\n" % root)
        return 2

    folders = {}  # rel path -> info dict
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        if "SKILL.md" not in files:
            continue
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        try:
            text = open(os.path.join(dirpath, "SKILL.md"),
                        encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        fm, body = split_frontmatter(text)
        folders[rel] = {
            "abs": dirpath,
            "body": " ".join(body.split()),
            "name": frontmatter_field(fm, "name"),
            "license": license_of(dirpath, fm),
            "has_license_file": has_license_file(dirpath),
        }

    # alias map: (alias folder rel, canonical folder rel) pairs
    name_to_folder = {}
    base_to_folder = {}
    for rel, info in folders.items():
        if info["name"]:
            name_to_folder[info["name"]] = rel
        base_to_folder[os.path.basename(rel)] = rel

    def resolve_canonical(canonical_id):
        if not canonical_id:
            return None
        if canonical_id in folders:
            return canonical_id
        if canonical_id in name_to_folder:
            return name_to_folder[canonical_id]
        return base_to_folder.get(canonical_id)

    alias_pairs = set()
    aliases_path = os.path.join(root, "skill-aliases.json")
    if os.path.isfile(aliases_path):
        try:
            data = json.load(open(aliases_path, encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        for entry in data.get("aliases", []):
            alias_folder = entry.get("path")
            canon_folder = resolve_canonical(entry.get("canonical_id"))
            if alias_folder and canon_folder:
                alias_pairs.add((alias_folder, canon_folder))
                alias_pairs.add((canon_folder, alias_folder))

    by_body = {}
    for rel, info in folders.items():
        if info["body"]:
            by_body.setdefault(info["body"], []).append(rel)

    violations = []
    for body, rels in sorted(by_body.items(), key=lambda kv: sorted(kv[1])):
        if len(rels) < 2:
            continue
        rels = sorted(rels)
        for i in range(len(rels)):
            for j in range(i + 1, len(rels)):
                a, b = rels[i], rels[j]
                if (a, b) not in alias_pairs:
                    violations.append(
                        "identical SKILL.md bodies with no alias entry in "
                        "skill-aliases.json: %s and %s" % (a, b))
                for local, canon in ((a, b), (b, a)):
                    if not os.path.basename(local).startswith("local-"):
                        continue
                    lic = folders[canon]["license"]
                    if lic and lic.startswith("MIT"):
                        if not folders[local]["has_license_file"]:
                            violations.append(
                                "local copy of MIT-licensed skill has no "
                                "LICENSE file: %s (canonical: %s)" % (local, canon))
    for v in violations:
        print("VIOLATION: %s" % v)
    if violations:
        print("license integrity: %d violation(s)" % len(violations))
        return 1
    print("license integrity clean: no violations (%d skill folders checked)"
          % len(folders))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
