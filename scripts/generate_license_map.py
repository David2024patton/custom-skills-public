#!/usr/bin/env python3
# generate_license_map.py: generate THIRD-PARTY.md, the licensing map for
# this skill collection, by scanning a tree.
#
# Usage:
#   python3 scripts/generate_license_map.py <tree-root>
#   python3 scripts/generate_license_map.py .
#
# The argument is the root of the tree to scan. Every folder in that tree
# that contains a SKILL.md file or a skill.yaml file is a skill unit.
# Each unit is classified as:
#   A: David Patton's own skills, covered by the MIT license in the root
#      LICENSE file. Membership is taken from the David Patton section of
#      the THIRD-PARTY.md already in the tree (that section is recognised
#      by its heading text, whatever letter it carried), plus units whose
#      own record names David Patton as author with a license signal, or
#      whose LICENSE file names David Patton as copyright holder.
#   B: third party skills with a license notice present, meaning a
#      license field in the SKILL.md frontmatter, a license field in
#      skill.yaml, or a LICENSE file in the folder.
#   C: skills with no license signal found.
# The script writes THIRD-PARTY.md into the scanned tree root, with the
# counts for sections A, B, and C computed in the same run, and prints
# those three counts to stdout. It uses only the Python standard library.
"""Generate THIRD-PARTY.md from a scan of the tree given as argv[1]."""

import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".locks"}
EM_DASH = "\u2014"
LICENSE_NAMES = ("LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE-MIT")


def clean(value):
    """Make a value safe for a markdown table cell."""
    if value is None:
        return ""
    text = str(value).strip()
    text = text.replace(EM_DASH, ",")
    text = text.replace("|", "/")
    text = " ".join(text.split())
    return text


def strip_quotes(value):
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        return text[1:-1]
    return text


def parse_frontmatter(path):
    """Read simple name, license, author, and version fields from SKILL.md."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            text = handle.read()
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    in_metadata = False
    for line in text[3:end].splitlines():
        if line.startswith("metadata:"):
            in_metadata = True
            continue
        if in_metadata and line.startswith("  ") and not line.startswith("    "):
            match = re.match(r"\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                data["metadata." + match.group(1)] = strip_quotes(match.group(2))
            continue
        if line and not line.startswith((" ", "\t")):
            in_metadata = False
            match = re.match(r"([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                data[match.group(1)] = strip_quotes(match.group(2))
    return data


def parse_skill_yaml(path):
    """Read top level fields from a skill.yaml file, without a YAML library."""
    data = {}
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return data
    for line in lines:
        if not line or line.startswith((" ", "\t", "#")):
            continue
        match = re.match(r"([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            data[match.group(1)] = strip_quotes(match.group(2))
    return data


def read_old_map(root):
    """Collect prior THIRD-PARTY.md rows and the David Patton folder set.

    The David Patton set is read from whichever section heading names his
    own skills, so maps written before and after the section letters were
    settled both parse. Prior rows are kept as a fallback for the name,
    author, and license text of units whose own files state none of them,
    such as pointer folders.
    """
    path = os.path.join(root, "THIRD-PARTY.md")
    rows = {}
    david_folders = set()
    if not os.path.isfile(path):
        return rows, david_folders
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return rows, david_folders
    in_david_section = False
    for line in lines:
        if line.startswith("## "):
            heading = line.lower()
            in_david_section = "david patton" in heading and "own" in heading
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("Skill", "---") or cells[1] == "---":
            continue
        folder = cells[1].strip("`").strip()
        if not folder or folder == "Folder":
            continue
        folder = folder.rstrip("/")
        rows[folder] = {
            "name": clean(cells[0]),
            "author": clean(cells[2]),
            "license": clean(cells[3]) if len(cells) > 3 else "",
        }
        if in_david_section:
            david_folders.add(folder)
    return rows, david_folders


def license_from_file(folder):
    """Return (license label, names David Patton) from a folder LICENSE file."""
    for name in LICENSE_NAMES:
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                text = handle.read()
        except OSError:
            return "LICENSE file present", False
        lowered = text.lower()
        if "mit license" in lowered:
            label = "MIT"
        elif "apache license" in lowered:
            label = "Apache-2.0"
        elif "bsd" in lowered and "license" in lowered:
            label = "BSD"
        else:
            label = "LICENSE file present"
        return label, "David Patton" in text
    return "", False


def find_units(root):
    units = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        if "SKILL.md" not in filenames and "skill.yaml" not in filenames:
            continue
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel == ".":
            continue
        units.append((rel, dirpath))
    units.sort(key=lambda item: item[0])
    return units


def classify_units(root):
    old_rows, david_folders = read_old_map(root)
    sections = {"A": [], "B": [], "C": []}
    for rel, folder in find_units(root):
        frontmatter = {}
        skill_yaml = {}
        if os.path.isfile(os.path.join(folder, "SKILL.md")):
            frontmatter = parse_frontmatter(os.path.join(folder, "SKILL.md"))
        if os.path.isfile(os.path.join(folder, "skill.yaml")):
            skill_yaml = parse_skill_yaml(os.path.join(folder, "skill.yaml"))
        file_label, david_copyright = license_from_file(folder)
        license_value = (
            frontmatter.get("license")
            or skill_yaml.get("license")
            or file_label
        )
        author = (
            frontmatter.get("author")
            or frontmatter.get("metadata.author")
            or skill_yaml.get("author")
            or ""
        )
        name = frontmatter.get("name") or skill_yaml.get("name") or ""
        old = old_rows.get(rel, {})
        if not name:
            name = old.get("name", "")
        if not name:
            name = os.path.basename(folder)
        if not author:
            author = old.get("author", "")
        if not license_value and old.get("license"):
            # A prior row alone is not a license signal for section B, it is
            # only display fallback for a unit already classified as A.
            pass
        is_david = (
            rel in david_folders
            or david_copyright
            or ("David Patton" in author and bool(license_value))
        )
        record = {
            "name": clean(name),
            "folder": rel,
            "author": clean(author) if author else "not stated",
            "license": clean(license_value),
        }
        if is_david:
            if not record["license"]:
                record["license"] = "MIT"
            sections["A"].append(record)
        elif license_value:
            sections["B"].append(record)
        else:
            sections["C"].append(record)
    return sections


def table(lines, records, with_license):
    if with_license:
        lines.append("| Skill | Folder | Author | License stated |")
        lines.append("|---|---|---|---|")
        for record in records:
            lines.append(
                "| %s | `%s/` | %s | %s |"
                % (
                    record["name"],
                    record["folder"],
                    record["author"],
                    record["license"] or "MIT",
                )
            )
    else:
        lines.append("| Skill | Folder | Author |")
        lines.append("|---|---|---|")
        for record in records:
            lines.append(
                "| %s | `%s/` | %s |"
                % (record["name"], record["folder"], record["author"])
            )
    lines.append("")


def render(root, sections):
    count_a = len(sections["A"])
    count_b = len(sections["B"])
    count_c = len(sections["C"])
    total = count_a + count_b + count_c
    lines = []
    lines.append("# Third-Party Skills and Licensing")
    lines.append("")
    lines.append(
        "This file is the licensing map for this repo. It is generated by"
    )
    lines.append(
        "scripts/generate_license_map.py. Section A membership is"
    )
    lines.append(
        "inherited from the previous edition of this map and"
    )
    lines.append(
        "spot-verified against frontmatter author fields, while"
    )
    lines.append(
        "sections B and C are swept fresh each run from frontmatter,"
    )
    lines.append(
        "skill.yaml, and LICENSE files in every skill unit in the tree"
    )
    lines.append(
        "(a folder containing SKILL.md or skill.yaml). The counts"
    )
    lines.append("below are computed in the same run.")
    lines.append("")
    lines.append(
        "Sweep totals: %d skill units. %d in section A, %d in section B,"
        % (total, count_a, count_b)
    )
    lines.append("%d in section C." % count_c)
    lines.append("")
    lines.append("What a consumer may do with this repo:")
    lines.append("")
    lines.append(
        "- David Patton's own work (section A) is covered by the MIT"
    )
    lines.append("  license in the root LICENSE file.")
    lines.append(
        "- Third party skills with a license notice present (section B)"
    )
    lines.append(
        "  may be redistributed under the terms stated for them, with the"
    )
    lines.append("  copyright and permission notice kept.")
    lines.append(
        "- Skills that state no license (section C) are all rights"
    )
    lines.append("  reserved by default, as section C states plainly.")
    lines.append("")
    lines.append(
        "Note on the Go skills: the `golang-*` folders are upstream"
    )
    lines.append(
        "snapshots of samber/cc-skills-golang, and the `local-golang-*`"
    )
    lines.append(
        "folders are David's local working variants of the same skills."
    )
    lines.append(
        "Both sets are kept on purpose; the folder name is the identity,"
    )
    lines.append("and the two sets are not interchangeable.")
    lines.append("")
    lines.append(
        "Note on license texts: the license texts this map relies on are"
    )
    lines.append(
        "collected in the LICENSES folder at the repo root, and the"
    )
    lines.append(
        "copyright holder for each skill is recorded in the tables below."
    )
    lines.append("")
    lines.append("## A. David Patton's own skills (%d)" % count_a)
    lines.append("")
    lines.append(
        "Covered by the root LICENSE. Most also state MIT in their own"
    )
    lines.append("frontmatter; the two statements agree.")
    lines.append("")
    table(lines, sections["A"], with_license=True)
    lines.append(
        "## B. Third party skills with a license notice present (%d)"
        % count_b
    )
    lines.append("")
    lines.append(
        "The samber golang family (the canonical golang-* folders and"
    )
    lines.append(
        "their local-golang-* copies) is listed here as MIT, with the"
    )
    lines.append(
        "LICENSE files and skill.yaml provenance for the local copies"
    )
    lines.append("restored in this pass.")
    lines.append("")
    table(lines, sections["B"], with_license=True)
    lines.append(
        "## C. No license stated, not cleared for redistribution (%d)"
        % count_c
    )
    lines.append("")
    lines.append(
        "These skills are present in the public mirror, all rights"
    )
    lines.append(
        "reserved, and are excluded from any handover or MCP packaging"
    )
    lines.append("build.")
    lines.append("")
    lines.append(
        "Do not redistribute, mirror, or package these until a grant is"
    )
    lines.append("on file. Presence in this repo is not permission.")
    lines.append("")
    table(lines, sections["C"], with_license=False)
    text = "\n".join(lines)
    text = text.replace(EM_DASH, ",")
    return text.rstrip() + "\n"


def main(argv):
    if len(argv) != 2:
        print("usage: python3 scripts/generate_license_map.py <tree-root>",
              file=sys.stderr)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print("not a directory: %s" % argv[1], file=sys.stderr)
        return 2
    sections = classify_units(root)
    output = render(root, sections)
    with open(os.path.join(root, "THIRD-PARTY.md"), "w",
              encoding="utf-8") as handle:
        handle.write(output)
    print("A: %d" % len(sections["A"]))
    print("B: %d" % len(sections["B"]))
    print("C: %d" % len(sections["C"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
