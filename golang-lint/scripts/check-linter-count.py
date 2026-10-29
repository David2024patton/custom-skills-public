#!/usr/bin/env python3
"""Drift check: the linter count in SKILL.md prose must match the config.

Counts the entries in the `linters.enable` list of assets/.golangci.yml and
compares that number with every bare count stated in SKILL.md in the form
"N linters". A count written as "N+ linters" describes the upstream
golangci-lint catalog size, not this configuration, and is ignored.

Standard library only. Exit codes: 0 when prose and config agree, 1 when
they disagree, 2 when a file cannot be read or parsed.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "assets" / ".golangci.yml"
SKILL = ROOT / "SKILL.md"


def count_enabled_linters(text: str) -> int:
    """Count list items under linters.enable in the golangci YAML.

    The config is machine-generated in a stable shape, so a small
    indentation-aware scan is enough and keeps this script stdlib-only.
    """
    lines = text.splitlines()
    in_linters = False
    in_enable = False
    count = 0
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            in_linters = stripped.startswith("linters:")
            in_enable = False
            continue
        if not in_linters:
            continue
        if indent == 2:
            in_enable = stripped.startswith("enable:")
            continue
        if in_enable and indent >= 4 and stripped.startswith("- "):
            count += 1
    return count


def prose_counts(text: str) -> list:
    """Return bare "N linters" counts from prose, skipping "N+" catalog claims."""
    found = []
    for match in re.finditer(r"(\d+)(\+?)\s+linters\b", text):
        if match.group(2) == "+":
            continue
        found.append(int(match.group(1)))
    return found


def main() -> int:
    try:
        counted = count_enabled_linters(CONFIG.read_text(encoding="utf-8"))
        prose = prose_counts(SKILL.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"check-linter-count: cannot read inputs: {exc}", file=sys.stderr)
        return 2
    if counted == 0:
        print("check-linter-count: no linters.enable entries found in config", file=sys.stderr)
        return 2
    if not prose:
        print("check-linter-count: SKILL.md states no bare linter count; nothing to drift")
        print(f"check-linter-count: config enables {counted} linters")
        return 0
    bad = [n for n in prose if n != counted]
    if bad:
        print(
            f"check-linter-count: DRIFT: config enables {counted} linters "
            f"but SKILL.md states {sorted(set(bad))}",
            file=sys.stderr,
        )
        return 1
    print(f"check-linter-count: OK: SKILL.md and config agree on {counted} linters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
