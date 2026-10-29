#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Which required tools and gates can actually run here, and what verdict ceiling does that impose?
# stackDetection: probes come from critic.manifest.json tool entries (command, version regex, minimum).
# inputs: --manifest PATH, --mode quick|full, --out capabilities.json, --root DIR
# effects: read-only, except a pinned install attempt in full mode where the manifest declares one (attempt is logged).
# exits: 0 all required tools present; 1 findings-fail (reserved); 2 a required tool is missing; 3 tool error; 4 manifest invalid; 124 timeout
# output: summary line first; full record written to the --out path (default capabilities.json)
# === END MANIFEST ===
"""Capability contract probe (I-01). Writes capabilities.json per run.

Probe status comes from the subprocess first: a non-zero exit is a
tool-error (exit 3) even when a version string happens to print, and
"ok" requires BOTH exit 0 and a version matched by the manifest's
declared versionRegex. The real subprocess exit code is recorded on
every result.

Required tools are DERIVED from the manifest's required gates, never
from the whole tool list: a tool is required when a required gate's
argv names it, or when it is the primary toolchain of a required
gate's stack (STACK_TOOLS below). The verdict ceiling and this tool's
exit code are computed from the required tools only; optional gaps
are listed separately and never impose the ceiling."""
import argparse, json, os, re, shutil, subprocess, sys
EXIT={"pass":0,"findings":1,"tool_missing":2,"tool_error":3,"manifest_invalid":4,"timeout":124}
STACK_TOOLS={"go":["go"],"rust":["cargo","rustc"],"mojo":["mojo"],
             "dart-flutter":["dart","flutter"],"python":["python3"],
             "javascript":["node"],"typescript":["node"],"react":["node"],
             "nextjs":["node"],"prisma":["node"],"shell":["shellcheck"],
             "common":[],"web":[]}
def required_tools(man):
    req=set()
    toolnames={t["name"] for t in man["tools"]}
    for g in man["gates"]:
        if not g.get("required"): continue
        req.update(STACK_TOOLS.get(g.get("stack"),[]))
        for tok in g.get("argv",[]):
            if tok in toolnames: req.add(tok)
    return req
def ver_key(v):
    return [int(x) if x.isdigit() else 0 for x in re.split(r"[.\-+]",v or "0")]
def probe(t,mode):
    cmd=t["probe"]["command"]; exe=cmd.split()[0]
    if not shutil.which(exe): return {"tool":t["name"],"status":"missing","exit":2}
    try: r=subprocess.run(cmd.split(),capture_output=True,text=True,timeout=15)
    except subprocess.TimeoutExpired: return {"tool":t["name"],"status":"timeout","exit":124}
    except FileNotFoundError: return {"tool":t["name"],"status":"missing","exit":2}
    out=(r.stdout+r.stderr).strip()
    m=re.search(t["probe"].get("versionRegex",""),out)
    ver=m.group(1) if m and m.groups() else (m.group(0) if m else None)
    if r.returncode!=0:
        return {"tool":t["name"],"status":"tool-error","exit":3,"exit_code":r.returncode,"version":ver}
    if not ver:
        return {"tool":t["name"],"status":"tool-error","exit":3,"exit_code":r.returncode,
                "reason":"probe exited 0 but no version matched the declared versionRegex"}
    st={"tool":t["name"],"status":"ok","version":ver,"exit":0,"exit_code":r.returncode}
    if t["probe"].get("minimum") and ver_key(ver)<ver_key(t["probe"]["minimum"]):
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
        # The manifest declares evidence artifacts for this gate; a bare
        # refusal leaves the run's coverage record with a gap a reader
        # cannot distinguish from a lost artifact. Write the declared
        # artifacts as structured not-run records, then exit 2.
        record={"gate":a.gate,"classification":"not-run",
                "reason":"no local runner in this bundle",
                "recorded_by":"capabilities.py --gate (the gate's declared local-runner stand-in)"}
        written=[]
        for rel in g.get("evidenceArtifacts",[]):
            p=os.path.join(a.root,rel); os.makedirs(os.path.dirname(p) or ".",exist_ok=True)
            if rel.endswith(".json"): json.dump(record,open(p,"w"),indent=1)
            else: open(p,"w").write(f"GATE {a.gate} not-run classification=not-run reason=no local runner in this bundle\n")
            written.append(rel)
        print(f"SUMMARY: gate {a.gate} has no local runner in this bundle; classified not-run; evidence written: {', '.join(written) or 'none declared'}")
        print(f"GATE {a.gate} not-run reason=no-local-runner")
        return 2
    req=required_tools(man)
    results=[probe(t,a.mode) for t in man["tools"]]
    for r in results: r["required"]=r["tool"] in req
    missing=[r["tool"] for r in results if r["status"]!="ok" and r["required"]]
    optional_missing=[r["tool"] for r in results if r["status"]!="ok" and not r["required"]]
    gates=[]
    for g in man["gates"]:
        gates.append({"gate":g["id"],"required":g["required"],"classification":"declared","note":"per-gate run state is recorded by the runner; probe covers tools only"})
    cap={"schemaVersion":1,"mode":a.mode,"tools":results,"gates":gates,
         "requiredTools":sorted(req),
         "verdictCeiling":"FIX-FIRST" if missing else "none",
         "untestedLine":("UNTESTED: "+", ".join(missing)) if missing else None,
         "optionalUntestedLine":("OPTIONAL UNTESTED (does not cap the verdict): "+", ".join(optional_missing)) if optional_missing else None}
    if man.get("a11yCeilingDisclosure"):
        # The a11y evidence record carries the disclosure on its face:
        # any reader of this run's capabilities (where the axe result
        # lives) sees what an automated pass does and does not mean.
        cap["a11yCeilingDisclosure"]=man["a11yCeilingDisclosure"]
        for r in results:
            if r["tool"]=="axe": r["a11yCeilingDisclosure"]=man["a11yCeilingDisclosure"]
    json.dump(cap,open(a.out,"w"),indent=1)
    print(f"SUMMARY: tools ok={len(results)-len(missing)-len(optional_missing)} required_missing={len(missing)} optional_missing={len(optional_missing)} out={a.out}")
    if missing: print("UNTESTED: "+", ".join(missing))
    if optional_missing: print("OPTIONAL UNTESTED: "+", ".join(optional_missing))
    return 2 if missing else 0
if __name__=="__main__": sys.exit(main())
