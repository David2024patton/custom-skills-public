#!/usr/bin/env python3
# RESEARCH_LEDGER_POINTER: this file is a pointer, never a copy.
"""Pointer to the canonical research ledger script.

This file is a POINTER to skills/deep-research/scripts/research_ledger.py
and never a copy of it. It locates the canonical script by walking up from
this file to the repo root, then runs the canonical script with the same
arguments and exits with the canonical script's exit code. If the canonical
script is absent, it exits 3 with one clear line.
"""

import subprocess
import sys
from pathlib import Path

CANONICAL_REL = Path("skills") / "deep-research" / "scripts" / "research_ledger.py"


def find_canonical():
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / CANONICAL_REL
        if candidate.is_file():
            return candidate
    return None


def main():
    canonical = find_canonical()
    if canonical is None:
        print("research_ledger pointer: canonical script not found at skills/deep-research/scripts/research_ledger.py")
        return 3
    result = subprocess.run([sys.executable, str(canonical)] + sys.argv[1:])
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
