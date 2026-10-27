#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Which stacks, tools, and gates does this target declare, and which stacks are present in a target tree?
# stackDetection: reads personas/critic/critic.manifest.json; no detection logic lives in code.
# inputs: --root DIR, --manifest PATH, --format json|legacy-audit|shell-vars, --lint-manifest
# effects: read-only
# exits: 0 ok; 2 tool or manifest missing; 4 manifest invalid
# output: summary line first, then one record per line (json mode prints one JSON document after the summary on stderr separation: summary to stderr)
# === END MANIFEST ===
"""Single manifest-reading stack detector (I-01, I-02). Replaces all shell detectors."""
import argparse, fnmatch, json, os, re, sys
EXCL={"node_modules",".git","target",".dart_tool","build",".pixi","vendor","__pycache__"}
def load_manifest(p):
    if not os.path.exists(p): print("SUMMARY: manifest missing"); sys.exit(2)
    try: m=json.load(open(p))
    except Exception as e: print(f"SUMMARY: manifest invalid: {e}"); sys.exit(4)
    if m.get("schemaVersion")!=1: print("SUMMARY: manifest invalid: schemaVersion must be 1"); sys.exit(4)
    return m
def lint_manifest(m):
    errs=[]
    for g in m.get("gates",[]):
        if not g.get("evidenceArtifacts"): errs.append(f"gate {g.get('id')} has no declared evidence artifact")
        if g.get("shell") and not g.get("shellReason"): errs.append(f"gate {g.get('id')} uses shell without a recorded reason")
        if not g.get("argv"): errs.append(f"gate {g.get('id')} has no argv")
    ids=[g["id"] for g in m.get("gates",[])]
    if len(ids)!=len(set(ids)): errs.append("duplicate gate ids")
    tids=[t["name"] for t in m.get("tools",[])]
    if len(tids)!=len(set(tids)): errs.append("duplicate tool names")
    return errs
def walk(root,maxdepth):
    for dp,dns,fns in os.walk(root):
        rel=os.path.relpath(dp,root); depth=0 if rel=="." else rel.count(os.sep)+1
        dns[:]=[d for d in dns if d not in EXCL]
        if depth>maxdepth: dns[:]=[]; continue
        for f in fns: yield os.path.join(rel,f) if rel!="." else f
def detect(root,m):
    found={}
    files=list(walk(root,8))
    for s in m["stacks"]:
        name=s["stack"]; det=s["detect"]; hits=[]
        for mk in det["markers"]:
            for rel in files:
                parts=rel.split(os.sep)
                if len(parts)-1<=mk.get("maxDepth",4) and (fnmatch.fnmatch(rel,mk["glob"]) or fnmatch.fnmatch(os.path.basename(rel),mk["glob"])):
                    if mk.get("contains"):
                        try:
                            if mk["contains"] not in open(os.path.join(root,rel),errors="ignore").read(): continue
                        except OSError: continue
                    hits.append(rel)
        neg=False
        for nm in det.get("negativeMarkers",[]):
            for rel in hits:
                try:
                    if nm.get("contains") and nm["contains"] in open(os.path.join(root,rel),errors="ignore").read(): neg=True
                except OSError: pass
        if hits and not neg: found[name]=sorted(set(hits))
        elif hits and neg: found.pop(name,None)
    # flutter refines dart: pubspec containing flutter stays flutter, plain pubspec is dart only
    if "flutter" in found and "dart" in found: del found["dart"]
    return found
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="."); ap.add_argument("--manifest",default=None)
    ap.add_argument("--format",default="json",choices=["json","legacy-audit","shell-vars"]); ap.add_argument("--lint-manifest",action="store_true")
    a=ap.parse_args()
    mp=a.manifest or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","critic.manifest.json")
    m=load_manifest(os.path.normpath(mp))
    errs=lint_manifest(m)
    if a.lint_manifest:
        if errs: print("SUMMARY: manifest lint FAIL"); [print("ERROR:",e) for e in errs]; return 4
        print(f"SUMMARY: manifest lint PASS stacks={len(m['stacks'])} tools={len(m['tools'])} gates={len(m['gates'])}"); return 0
    if errs: print("SUMMARY: manifest invalid"); [print("ERROR:",e) for e in errs]; return 4
    found=detect(a.root,m)
    if a.format=="legacy-audit":
        print(f"SUMMARY: stacks={','.join(sorted(found)) or 'none'}")
        if not found: print(f"STACK none (no markers found under {a.root})")
        for k in sorted(found):
            for h in found[k]: print(f"STACK {k} {os.path.join(a.root,h) if not h.startswith(a.root) else h}")
        import shutil
        for t in m["tools"]:
            cmd=t["probe"]["command"].split()[0]; print(f"TOOL {t['name']} {'ok' if shutil.which(cmd) else 'missing'}")
    elif a.format=="shell-vars":
        print("STACKS="+(" ".join(sorted(found))))
    else:
        print(f"SUMMARY: stacks={','.join(sorted(found)) or 'none'}")
        print(json.dumps({"stacks":found},indent=1))
    return 0
if __name__=="__main__": sys.exit(main())
