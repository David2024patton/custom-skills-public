#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Does a SARIF file satisfy SARIF 2.1.0 structure and the frozen critic profile?
# stackDetection: none.
# inputs: findings.sarif, --schema PATH (official SARIF 2.1.0 JSON Schema), --checklists DIR
# effects: read-only
# exits: 0 valid; 1 profile or schema violation; 2 validator dependency missing (jsonschema or schema file); 4 input invalid
# output: summary line first, then one violation per line
# === END MANIFEST ===
"""SARIF post-validator (I-03): profile lint always; official schema check when available."""
import argparse, json, os, sys
REQ_PROPS=["critic:severity","critic:rubricRef","critic:consensus","critic:evidence","critic:smallestFix","critic:confidence"]
def profile_lint(doc,checklists):
    errs=[]
    if doc.get("version")!="2.1.0": errs.append("version is not 2.1.0")
    rule_ids=set()
    for run in doc.get("runs",[]):
        if "critic:verdict" in json.dumps(run.get("properties",{})): errs.append("verdict must never live in SARIF")
        for r in run.get("tool",{}).get("driver",{}).get("rules",[]): rule_ids.add(r.get("id"))
        for res in run.get("results",[]):
            p=res.get("properties",{})
            for k in REQ_PROPS:
                if k not in p: errs.append(f"result {res.get('ruleId')} missing property {k}")
            if not p.get("critic:evidence"): errs.append(f"result {res.get('ruleId')} has no evidence entry")
            f=res.get("partialFingerprints",{})
            if "primaryLocationLineHash" not in f or "critic/findingHash" not in f:
                errs.append(f"result {res.get('ruleId')} missing a partial fingerprint")
            states=[x.get("baselineState") for x in run["results"]]
            if any(s is not None for s in states) and any(s is None for s in states):
                errs.append("baselineState is all-or-nothing per run"); break
        if checklists:
            known=set()
            for fn in os.listdir(checklists):
                if fn.endswith(".checklist.json"):
                    known|={i["id"] for i in json.load(open(os.path.join(checklists,fn))).get("items",[])}
            for res in run.get("results",[]):
                if res.get("ruleId") not in known: errs.append(f"ruleId {res.get('ruleId')} does not resolve to a checklist item")
    return errs
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("sarif"); ap.add_argument("--schema",default=None); ap.add_argument("--checklists",default=None)
    a=ap.parse_args()
    try: doc=json.load(open(a.sarif))
    except Exception as e: print(f"SUMMARY: input invalid: {e}"); return 4
    errs=profile_lint(doc,a.checklists)
    schema_note="schema check not requested"
    if a.schema:
        if not os.path.exists(a.schema): print("SUMMARY: validator missing: schema file not found"); return 2
        try: import jsonschema
        except ImportError: print("SUMMARY: validator missing: python jsonschema package not installed"); return 2
        schema=json.load(open(a.schema))
        v=jsonschema.Draft7Validator(schema); serrs=sorted(v.iter_errors(doc),key=lambda e:e.path)
        errs+=[f"schema: {'/'.join(map(str,e.path))}: {e.message}" for e in serrs]; schema_note=f"schema errors={len(serrs)}"
    print(f"SUMMARY: {'FAIL' if errs else 'PASS'} profile violations={len(errs)} {schema_note}")
    for e in errs: print("VIOLATION:",e)
    return 1 if errs else 0
if __name__=="__main__": sys.exit(main())
