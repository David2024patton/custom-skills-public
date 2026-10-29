#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Can a run directory be sealed into a verifiable evidence bundle?
# stackDetection: none.
# inputs: --run-dir DIR (findings.sarif, verdict.json, capabilities.json, coverage.json, logs/, evidence/), --manifest critic.manifest.json, --out bundle dir
# effects: mutating (creates the --out bundle directory only)
# exits: 0 bundle built and hashes verified; 1 a required run file is missing; 4 input invalid
# output: summary line first; bundle manifest at <out>/manifest.json
# === END MANIFEST ===
"""Evidence bundle builder (I-05). SLSA-shaped provenance; signing is phase 2, not built."""
import argparse, hashlib, json, os, shutil, sys, time
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--run-dir",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--manifest",default=None); a=ap.parse_args()
    req=["findings.sarif","verdict.json","capabilities.json","coverage.json"]
    missing=[f for f in req if not os.path.exists(os.path.join(a.run_dir,f))]
    if missing: print("SUMMARY: bundle FAIL missing "+", ".join(missing)); return 1
    os.makedirs(a.out,exist_ok=True)
    files={}
    for root,_,fns in os.walk(a.run_dir):
        for fn in fns:
            src=os.path.join(root,fn); rel=os.path.relpath(src,a.run_dir)
            dst=os.path.join(a.out,rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
            # Hash the SOURCE before copying and store the source hash;
            # the final verify compares each destination against the
            # stored source hash, so a corrupted or divergent copy fails.
            files[rel]=sha(src)
            shutil.copy2(src,dst)
    os.makedirs(os.path.join(a.out,"inputs"),exist_ok=True)
    if a.manifest and os.path.exists(a.manifest):
        files["inputs/critic.manifest.json"]=sha(a.manifest)
        shutil.copy2(a.manifest,os.path.join(a.out,"inputs","critic.manifest.json"))
    verdict=json.load(open(os.path.join(a.run_dir,"verdict.json")))
    stale=[]
    now=time.time()
    for feed in verdict.get("feeds",[]):
        age_h=(now-feed.get("fetchedEpoch",now))/3600.0
        if age_h>feed.get("maxAgeHours",24): stale.append(f"STALE FEED: {feed.get('name')} {age_h:.1f}h")
    man={"schemaVersion":1,"files":files,"staleFeedDisclosures":stale,
         "signing":"phase 2: Sigstore keyless signing and VSA attestation are documented, not a launch blocker, not built"}
    json.dump(man,open(os.path.join(a.out,"manifest.json"),"w"),indent=1)
    digest=sha(os.path.join(a.out,"manifest.json"))
    prov={"_type":"https://in-toto.io/Statement/v1","subject":[{"name":"manifest.json","digest":{"sha256":digest}}],
          "predicateType":"https://slsa.dev/provenance/v1",
          "predicate":{"buildDefinition":{"buildType":"critic-run"},"runDetails":{"builder":{"id":"critic/bundle-evidence"}}}}
    json.dump(prov,open(os.path.join(a.out,"provenance.intoto.json"),"w"),indent=1)
    ok=all(sha(os.path.join(a.out,rel))==h for rel,h in files.items())
    print(f"SUMMARY: bundle {'PASS' if ok else 'FAIL'} files={len(files)} manifest_sha256={digest}")
    for s in stale: print(s)
    return 0 if ok else 1
if __name__=="__main__": sys.exit(main())
