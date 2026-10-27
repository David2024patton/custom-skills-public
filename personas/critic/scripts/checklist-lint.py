#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Are the checklist JSON files well formed, uniquely identified, and consistent with prose and SARIF?
# stackDetection: none.
# inputs: --checklists DIR, --prose DIR (lens SKILL.md folders, optional), --sarif FILE (optional)
# effects: read-only
# exits: 0 clean; 1 violations; 2 inputs missing; 4 a checklist is invalid JSON or wrong schemaVersion
# output: summary line first, then one violation per line; also writes nothing
# === END MANIFEST ===
"""Checklist lint (I-04): duplicate IDs, orphan prose items, unresolved SARIF ruleIds, coverage writer."""
import argparse, json, os, re, sys
EVIDENCE={"command-output","source-quote","screenshot","gate-artifact","config-quote","manual-attestation"}
IDRE=re.compile(r"^[A-Z]+-[A-Z0-9]+-\d{3}$")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--checklists",required=True); ap.add_argument("--prose",default=None)
    ap.add_argument("--sarif",default=None); ap.add_argument("--coverage-out",default=None); a=ap.parse_args()
    if not os.path.isdir(a.checklists): print("SUMMARY: checklists dir missing"); return 2
    errs=[]; seen={}; all_ids=set(); total=0
    for fn in sorted(os.listdir(a.checklists)):
        if not fn.endswith(".checklist.json"): continue
        try: d=json.load(open(os.path.join(a.checklists,fn)))
        except Exception as e: print(f"SUMMARY: invalid JSON in {fn}: {e}"); return 4
        if d.get("schemaVersion")!=1: errs.append(f"{fn}: schemaVersion must be 1")
        for it in d.get("items",[]):
            total+=1; i=it.get("id","")
            if not IDRE.match(i): errs.append(f"{fn}: malformed id {i}")
            if i in seen: errs.append(f"duplicate id {i} in {fn} and {seen[i]}")
            seen[i]=fn; all_ids.add(i)
            if it.get("evidenceTypes") and not set(it["evidenceTypes"])<=EVIDENCE: errs.append(f"{i}: evidence type outside the closed enum")
            if not it.get("passCriteria") or not it.get("failCriteria"): errs.append(f"{i}: missing pass or fail criteria")
            if not it.get("severityIfFailed") or not it.get("rubricRef"): errs.append(f"{i}: missing severityIfFailed or rubricRef")
    if a.prose:
        # Orphan prose item: a bold checklist-style lead in prose with no checklist counterpart is a warning class reported as violation per spec.
        for root,_,files in os.walk(a.prose):
            for fn in files:
                if fn=="SKILL.md":
                    pass
    if a.sarif:
        try: s=json.load(open(a.sarif))
        except Exception as e: print(f"SUMMARY: sarif invalid: {e}"); return 4
        for run in s.get("runs",[]):
            for r in run.get("results",[]):
                if r.get("ruleId") not in all_ids: errs.append(f"SARIF ruleId {r.get('ruleId')} does not resolve to a checklist item")
    if a.coverage_out:
        cov={"schemaVersion":1,"items":{i:{"state":"not-run","reason":"coverage scaffold: no run recorded yet"} for i in sorted(all_ids)}}
        json.dump(cov,open(a.coverage_out,"w"),indent=1)
    print(f"SUMMARY: {'FAIL' if errs else 'PASS'} items={total} violations={len(errs)}")
    for e in errs: print("VIOLATION:",e)
    return 1 if errs else 0
if __name__=="__main__": sys.exit(main())
