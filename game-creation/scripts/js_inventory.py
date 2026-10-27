#!/usr/bin/env python3
"""Inventory legacy browser JavaScript (fan calculators, simulators, game UI) to
find the game formulas fast.

Usage: js_inventory.py FILE_OR_DIR [...] > inventory.md

For each .js file (and inline <script> in .html) it reports:
  - function definitions with line numbers
  - formula lines: Math.* calls, random rolls, rounding, clamps, % chances
  - large data tables (array/object literals with many entries) = ship/weapon stats
  - version strings / dates / authors in comments
Read the reported lines in context afterwards; this is a map, not the analysis.
"""
import os, re, sys

FUNC = re.compile(r"^\s*(?:function\s+([\w$]+)\s*\(|([\w$.]+)\s*=\s*function\s*\(|(?:var|let|const)\s+([\w$]+)\s*=\s*\([^)]*\)\s*=>)")
FORMULA = re.compile(r"Math\.(random|floor|ceil|round|pow|min|max|sqrt|log|exp|abs)|\b(chance|accuracy|evade|evasion|damage|dmg|crit|armor|armour|shield|hp|speed|turns?|xp|exp|cost|price|level|vis(ibility)?|hide|cloak)\b\s*[*/+\-]?=", re.I)
TABLE = re.compile(r"(new Array\(|=\s*\[|=\s*\{)")
META = re.compile(r"(version|v\d+\.\d+|copyright|\(c\)|author|updated|last modified|19\d\d|20\d\d)", re.I)
SCRIPT = re.compile(r"<script[^>]*>(.*?)</script>", re.S | re.I)


def files(args):
    for a in args:
        if os.path.isdir(a):
            for dp, _, fs in os.walk(a):
                for f in sorted(fs):
                    if f.lower().endswith((".js", ".html", ".htm", ".shtml", ".php")):
                        yield os.path.join(dp, f)
        else:
            yield a


def lines_of(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    if path.lower().endswith(".js"):
        return src.splitlines()
    out = []
    for m in SCRIPT.finditer(src):
        out.extend(m.group(1).splitlines())
    return out


def main():
    for p in files(sys.argv[1:]):
        L = lines_of(p)
        if not L: continue
        funcs, forms, tables, meta = [], [], [], []
        for i, l in enumerate(L, 1):
            m = FUNC.match(l)
            if m: funcs.append(f"{i}:{next(g for g in m.groups() if g)}")
            if FORMULA.search(l) and len(forms) < 120: forms.append(f"{i}: {l.strip()[:160]}")
            if TABLE.search(l):
                commas = l.count(",")
                if commas >= 8: tables.append(f"{i}: ({commas+1} items) {l.strip()[:100]}")
            if ("//" in l or "/*" in l or l.strip().startswith("*")) and META.search(l) and len(meta) < 15:
                meta.append(f"{i}: {l.strip()[:140]}")
        print(f"## {p}  ({len(L)} lines)\n")
        if meta: print("**Meta:**\n```\n" + "\n".join(meta) + "\n```")
        if funcs: print(f"**Functions ({len(funcs)}):** " + ", ".join(funcs) + "\n")
        if tables: print("**Data tables:**\n```\n" + "\n".join(tables[:40]) + "\n```")
        if forms: print("**Formula lines:**\n```\n" + "\n".join(forms) + "\n```")
        print()


if __name__ == "__main__":
    main()
