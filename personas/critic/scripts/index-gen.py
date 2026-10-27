#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: What scripts does the critic bundle ship, in manifest-header shape?
# stackDetection: none.
# inputs: --scripts DIR, --out INDEX.json
# effects: mutating (writes the generated --out index only; never hand-kept)
# exits: 0 ok; 2 scripts dir missing
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
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--scripts",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    if not os.path.isdir(a.scripts): print("SUMMARY: scripts dir missing"); return 2
    entries=[]
    for p in sorted(glob.glob(os.path.join(a.scripts,"**","*.sh"),recursive=True)+glob.glob(os.path.join(a.scripts,"**","*.py"),recursive=True)):
        e=parse(p); e["path"]=os.path.relpath(p,a.scripts); entries.append(e)
    json.dump({"schemaVersion":1,"generatedBy":"scripts/index-gen.py","scripts":entries},open(a.out,"w"),indent=1)
    print(f"SUMMARY: indexed {len(entries)} scripts to {a.out}"); return 0
if __name__=="__main__": sys.exit(main())
