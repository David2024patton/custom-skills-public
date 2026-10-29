#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: What scripts does the critic bundle ship, in manifest-header shape?
# stackDetection: none.
# inputs: --scripts DIR, --out INDEX.json, --check (compare instead of writing)
# effects: mutating (writes the generated --out index only; never hand-kept). With --check: read-only.
# exits: 0 ok (or, with --check, index and tree agree); 1 --check found drift; 2 scripts dir missing
# output: summary line first; generated index at --out
# === END MANIFEST ===
"""Generated bundle script index (I-06). Parses the fixed header block of every bundled script."""
import argparse, glob, json, os, re, sys
def parse(path):
    txt=open(path,errors="ignore").read()[:4000]
    m=re.search(r"=== CRITIC SCRIPT MANIFEST ===\n(.*?)\n# === END MANIFEST ===",txt,re.S)
    if not m:
        m2=re.search(r"# PURPOSE: (.*)",txt)
        return {"file":os.path.basename(path),"legacyHeader":True,"question":(m2.group(1).strip() if m2 else None)}
    fields={}
    for line in m.group(1).splitlines():
        line=line.lstrip("# ").strip()
        if ":" in line:
            k,v=line.split(":",1); fields[k.strip()]=v.strip()
    fields["file"]=os.path.basename(path); fields["legacyHeader"]=False
    return fields
def build_entries(scripts):
    entries=[]
    for p in sorted(glob.glob(os.path.join(scripts,"**","*.sh"),recursive=True)+glob.glob(os.path.join(scripts,"**","*.py"),recursive=True)):
        e=parse(p); e["path"]=os.path.relpath(p,scripts); entries.append(e)
    return entries
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--scripts",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--check",action="store_true",help="compare the shipped index against the tree; exit 1 on drift, write nothing")
    a=ap.parse_args()
    if not os.path.isdir(a.scripts): print("SUMMARY: scripts dir missing"); return 2
    entries=build_entries(a.scripts)
    if a.check:
        if not os.path.isfile(a.out): print("SUMMARY: index DRIFT (index file missing)"); return 1
        try: shipped=json.load(open(a.out))
        except Exception as e: print(f"SUMMARY: index DRIFT (index unreadable: {e})"); return 1
        have={e["path"] for e in shipped.get("scripts",[])}
        want={e["path"] for e in entries}
        missing=sorted(want-have); stale=sorted(have-want)
        if missing or stale:
            print(f"SUMMARY: index DRIFT missing={len(missing)} stale={len(stale)}")
            for p in missing: print("MISSING FROM INDEX:",p)
            for p in stale: print("STALE IN INDEX:",p)
            return 1
        print(f"SUMMARY: index in sync ({len(entries)} scripts)"); return 0
    json.dump({"schemaVersion":1,"generatedBy":"scripts/index-gen.py","scripts":entries},open(a.out,"w"),indent=1)
    print(f"SUMMARY: indexed {len(entries)} scripts to {a.out}"); return 0
if __name__=="__main__": sys.exit(main())
