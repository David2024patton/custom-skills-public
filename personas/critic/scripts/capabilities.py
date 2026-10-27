#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Which required tools and gates can actually run here, and what verdict ceiling does that impose?
# stackDetection: probes come from critic.manifest.json tool entries (command, version regex, minimum).
# inputs: --manifest PATH, --mode quick|full, --out capabilities.json, --root DIR
# effects: read-only, except a pinned install attempt in full mode where the manifest declares one (attempt is logged).
# exits: 0 all required tools present; 1 findings-fail (reserved); 2 a required tool is missing; 3 tool error; 4 manifest invalid; 124 timeout
# output: summary line first; full record written to the --out path (default capabilities.json)
# === END MANIFEST ===
"""Capability contract probe (I-01). Writes capabilities.json per run."""
import argparse, json, os, re, shutil, subprocess, sys
EXIT={"pass":0,"findings":1,"tool_missing":2,"tool_error":3,"manifest_invalid":4,"timeout":124}
def ver_key(v):
    return [int(x) if x.isdigit() else 0 for x in re.split(r"[.\-+]",v or "0")]
def probe(t,mode):
    cmd=t["probe"]["command"]; exe=cmd.split()[0]
    if not shutil.which(exe): return {"tool":t["name"],"status":"missing","exit":2}
    try: r=subprocess.run(cmd.split(),capture_output=True,text=True,timeout=15)
    except subprocess.TimeoutExpired: return {"tool":t["name"],"status":"timeout","exit":124}
    out=(r.stdout+r.stderr).strip()
    m=re.search(t["probe"].get("versionRegex",""),out)
    ver=m.group(1) if m and m.groups() else (m.group(0) if m else None)
    st={"tool":t["name"],"status":"ok","version":ver,"exit":0}
    if t["probe"].get("minimum") and ver and ver_key(ver)<ver_key(t["probe"]["minimum"]):
        st.update(status="below-minimum",exit=3)
    if mode=="full" and t.get("install"): st["installPolicy"]="pinned attempt allowed in full mode; not attempted by probe"
    return st
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",default=None); ap.add_argument("--mode",default="quick",choices=["quick","full"])
    ap.add_argument("--out",default="capabilities.json"); ap.add_argument("--root",default="."); ap.add_argument("--gate",default=None)
    a=ap.parse_args()
    mp=a.manifest or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","critic.manifest.json"))
    if not os.path.exists(mp): print("SUMMARY: manifest missing"); return 2
    try: man=json.load(open(mp))
    except Exception as e: print(f"SUMMARY: manifest invalid: {e}"); return 4
    if a.gate:
        g=next((x for x in man["gates"] if x["id"]==a.gate),None)
        if not g: print(f"SUMMARY: unknown gate {a.gate}"); return 4
        print(f"SUMMARY: gate {a.gate} has no local runner in this bundle; classified not-run")
        print(f"GATE {a.gate} not-run reason=no-local-runner"); return 2
    results=[probe(t,a.mode) for t in man["tools"]]
    missing=[r["tool"] for r in results if r["status"]!="ok"]
    gates=[]
    toolset={r["tool"]:r["status"] for r in results}
    for g in man["gates"]:
        gates.append({"gate":g["id"],"required":g["required"],"classification":"declared","note":"per-gate run state is recorded by the runner; probe covers tools only"})
    cap={"schemaVersion":1,"mode":a.mode,"tools":results,"gates":gates,
         "verdictCeiling":"FIX-FIRST" if missing else "none",
         "untestedLine":("UNTESTED: "+", ".join(missing)) if missing else None}
    json.dump(cap,open(a.out,"w"),indent=1)
    print(f"SUMMARY: tools ok={len(results)-len(missing)} missing={len(missing)} out={a.out}")
    if missing: print("UNTESTED: "+", ".join(missing))
    return 2 if missing else 0
if __name__=="__main__": sys.exit(main())
