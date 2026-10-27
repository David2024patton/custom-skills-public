#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: How are findings emitted as SARIF 2.1.0 under the frozen critic profile?
# stackDetection: none; ruleIds resolve against checklists/*.checklist.json when present.
# inputs: findings JSON file (array of finding objects), --out findings.sarif, --baseline present|absent
# effects: mutating (writes the --out file only)
# exits: 0 ok; 1 a finding lacks evidence (invalid under the profile); 4 input invalid
# output: summary line first; SARIF written to --out
# === END MANIFEST ===
"""SARIF 2.1.0 emitter for the critic profile (I-03). Verdicts never live in SARIF."""
import argparse, hashlib, json, sys
SEV={"critical":("error",95),"high":("error",80),"medium":("warning",55),"low":("note",25)}
def fp(f):
    raw="|".join([f.get("path",""),f.get("ruleId",""),str(f.get("line","")),f.get("snippet","")])
    return {"primaryLocationLineHash":hashlib.sha256(raw.encode()).hexdigest()[:32],
            "critic/findingHash":hashlib.sha256(("v1|"+raw).encode()).hexdigest()}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("findings"); ap.add_argument("--out",default="findings.sarif")
    ap.add_argument("--baseline",default="absent",choices=["present","absent"]); a=ap.parse_args()
    try: items=json.load(open(a.findings))
    except Exception as e: print(f"SUMMARY: input invalid: {e}"); return 4
    rules={}; results=[]
    for f in items:
        if not f.get("evidence"): print(f"SUMMARY: finding {f.get('ruleId')} has no evidence entry; invalid"); return 1
        sev=str(f.get("severity","medium")).lower(); level,rank=SEV.get(sev,SEV["medium"])
        rid=f["ruleId"]
        if rid not in rules:
            rules[rid]={"id":rid,"name":rid,"shortDescription":{"text":f.get("title",rid)},
              "properties":{"critic:severity":sev,"critic:rubricRef":f.get("rubricRef","")}}
        r={"ruleId":rid,"level":level,"rank":float(rank),"message":{"text":f.get("message","")},
           "locations":[{"physicalLocation":{"artifactLocation":{"uri":f.get("path","")},"region":{"startLine":int(f.get("line",1))}}}],
           "partialFingerprints":fp(f),
           "properties":{"critic:severity":sev,"critic:rubricRef":f.get("rubricRef",""),
             "critic:consensus":f.get("consensus",{"count":1,"of":5,"band":"flagged"}),
             "critic:evidence":f["evidence"],"critic:smallestFix":f.get("smallestFix",""),
             "critic:confidence":f.get("confidence",5)}}
        if a.baseline=="present": r["baselineState"]=f.get("baselineState","unchanged")
        if f.get("fix"): r["fixes"]=[{"description":{"text":f["fix"].get("text","")},"artifactChanges":[{"artifactLocation":{"uri":f.get("path","")},"replacements":[{"deletedRegion":{"startLine":int(f.get("line",1))},"insertedContent":{"text":f["fix"].get("replacement","")}}]}]}]
        results.append(r)
    doc={"$schema":"https://json.schemastore.org/sarif-2.1.0.json","version":"2.1.0",
      "runs":[{"tool":{"driver":{"name":"critic","version":"1.0.0","rules":list(rules.values())}},
               "results":results,"properties":{"critic:profile":"critic-sarif-1"}}]}
    json.dump(doc,open(a.out,"w"),indent=1)
    print(f"SUMMARY: emitted {len(results)} findings to {a.out}"); return 0
if __name__=="__main__": sys.exit(main())
