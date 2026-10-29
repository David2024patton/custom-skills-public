#!/usr/bin/env python3
"""Publish gate check: duplicated canonical assets and pointer folders.

Two checks run over the repo tree:

1. Canonical assets. CANONICAL_ASSETS maps a basename to the canonical
   file that owns it, as a path relative to the repo root. For every other
   file in the tree with a listed basename, the file passes only when it
   is byte-identical to the canonical file OR it is a pointer (its bytes
   carry POINTER_MARKER, the marker the pointer shims in this repo use).
   Any other file with a listed basename fails and is named.

2. Pointer folders. For every folder whose SKILL.md frontmatter carries
   a pointer-to: field, the folder passes only when it contains no file
   other than SKILL.md and LICENSE. Any other file fails and is named.

Usage: python3 scripts/check_duplicated_assets.py [repo-root]
The repo root defaults to the parent of this script's folder.
Exit codes: 0 clean, 1 any failure, 2 usage or input error.
Standard library only. No em dashes in this file.
"""

import sys
from pathlib import Path

POINTER_MARKER = "RESEARCH_LEDGER_POINTER"

CANONICAL_ASSETS = {
    "research_ledger.py": "skills/deep-research/scripts/research_ledger.py",
}

ALLOWED_POINTER_FILES = {"SKILL.md", "LICENSE"}
SKIP_DIRS = {".git", "__pycache__", ".locks", ".hub"}


def iter_files(root):
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def frontmatter_has_pointer_to(skill_md):
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        block = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            block.append(line)
    else:
        block = lines[:20]
    return any(line.strip().startswith("pointer-to:") for line in block)


def main(argv):
    if len(argv) > 2:
        print("usage: check_duplicated_assets.py [repo-root]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        root = Path(argv[1]).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"check_duplicated_assets: repo root not found: {root}", file=sys.stderr)
        return 2

    failures = []
    checked_assets = 0
    checked_pointers = 0

    canonical_paths = {}
    for basename, rel in CANONICAL_ASSETS.items():
        canonical = root / rel
        if not canonical.is_file():
            failures.append(f"canonical asset missing: {rel}")
            continue
        canonical_paths[basename] = (canonical, canonical.read_bytes())

    all_files = list(iter_files(root))

    for path in all_files:
        if path.name not in canonical_paths:
            continue
        canonical, canonical_bytes = canonical_paths[path.name]
        if path.resolve() == canonical.resolve():
            continue
        checked_assets += 1
        data = path.read_bytes()
        if data == canonical_bytes:
            continue
        if POINTER_MARKER.encode("utf-8") in data:
            continue
        rel = path.relative_to(root)
        failures.append(
            f"duplicated asset diverged: {rel} is neither byte-identical "
            f"to {CANONICAL_ASSETS[path.name]} nor a pointer to it"
        )

    skill_files = [p for p in all_files if p.name == "SKILL.md"]
    for skill_md in skill_files:
        if not frontmatter_has_pointer_to(skill_md):
            continue
        checked_pointers += 1
        folder = skill_md.parent
        for path in iter_files(folder):
            if path.name not in ALLOWED_POINTER_FILES or path.parent != folder:
                rel = path.relative_to(root)
                failures.append(
                    f"pointer folder violation: {rel} found in pointer "
                    f"folder {folder.relative_to(root)}; pointer folders "
                    "hold only SKILL.md and LICENSE"
                )

    for failure in failures:
        print(f"FAIL: {failure}")
    print(
        f"check_duplicated_assets: {checked_assets} duplicated asset "
        f"candidate(s), {checked_pointers} pointer folder(s), "
        f"{len(failures)} failure(s)"
    )
    if failures:
        print("check_duplicated_assets: FAIL")
        return 1
    print("check_duplicated_assets: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
