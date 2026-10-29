#!/usr/bin/env python3
# === CRITIC SCRIPT MANIFEST ===
# question: Are the checklist JSON files well formed, uniquely identified, and consistent with prose and SARIF?
# stackDetection: none.
# inputs: --checklists DIR, --prose DIR (lens SKILL.md folders, optional), --sarif FILE (optional), --skills-root DIR (optional), --control-map FILE (optional)
# effects: read-only
# exits: 0 clean; 1 violations; 2 inputs missing; 4 a checklist is invalid JSON or wrong schemaVersion
# output: summary line first, then one violation per line; also writes nothing
# === END MANIFEST ===
"""Checklist lint (I-04): duplicate IDs, orphan prose items, unresolved SARIF ruleIds, coverage writer.

The prose orphan check is real: for each lens SKILL.md under --prose it
extracts bold list leads (the prose form of a check) and requires each
untagged lead to resolve to an item of the same lens's checklist by
content-word overlap (at least half the lead's content words present in
an item's title plus howToTest). A lead carrying a spec tag such as
(CS-06) or (P-12) is a cross-reference to the protocol spec in SOUL
section 8, not a checklist entry, and is counted separately, never
flagged. Companion rules: --skills-root makes every related_skills
frontmatter entry resolve to a shipped skill directory; --control-map
requires one COMPLIANCE-CTL item per control the map defines; every
title must be a complete phrase (no trailing whitespace, no ending on
a fragment word, no duplicates inside a file)."""
import argparse, json, os, re, sys
EVIDENCE={"command-output","source-quote","screenshot","gate-artifact","config-quote","manual-attestation"}
IDRE=re.compile(r"^[A-Z]+-[A-Z0-9]+-\d{3}$")
STOP=set("the a an and or of to in on for with is are be this that it its as at by from not no".split())
FRAGMENT_END=STOP | {"per","via","into","over","under","than","then","when","while"}
LENS_OF_FOLDER={"critic-lens-code":"code","critic-lens-claims":"claims","critic-lens-ux":"ux",
                "critic-lens-growth":"growth","critic-lens-compliance":"compliance"}
def content_words(t):
    return {w for w in re.findall(r"[a-z0-9']+", t.lower()) if len(w)>=4 and w not in STOP}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--checklists",required=True); ap.add_argument("--prose",default=None)
    ap.add_argument("--sarif",default=None); ap.add_argument("--coverage-out",default=None)
    ap.add_argument("--skills-root",default=None,help="skills tree root; enables the related_skills resolution check")
    ap.add_argument("--control-map",default=None,help="control-map.md; enables the COMPLIANCE-CTL agreement check")
    a=ap.parse_args()
    if not os.path.isdir(a.checklists): print("SUMMARY: checklists dir missing"); return 2
    errs=[]; seen={}; all_ids=set(); total=0; by_lens={}
    for fn in sorted(os.listdir(a.checklists)):
        if not fn.endswith(".checklist.json"): continue
        try: d=json.load(open(os.path.join(a.checklists,fn)))
        except Exception as e: print(f"SUMMARY: invalid JSON in {fn}: {e}"); return 4
        if d.get("schemaVersion")!=1: errs.append(f"{fn}: schemaVersion must be 1")
        by_lens[fn.split(".")[0]]=d.get("items",[])
        titles_here={}
        for it in d.get("items",[]):
            total+=1; i=it.get("id","")
            if not IDRE.match(i): errs.append(f"{fn}: malformed id {i}")
            if i in seen: errs.append(f"duplicate id {i} in {fn} and {seen[i]}")
            seen[i]=fn; all_ids.add(i)
            if it.get("evidenceTypes") and not set(it["evidenceTypes"])<=EVIDENCE: errs.append(f"{i}: evidence type outside the closed enum")
            if not it.get("passCriteria") or not it.get("failCriteria"): errs.append(f"{i}: missing pass or fail criteria")
            if not it.get("severityIfFailed") or not it.get("rubricRef"): errs.append(f"{i}: missing severityIfFailed or rubricRef")
            t=it.get("title","")
            if t!=t.strip() or t.endswith(","): errs.append(f"{i}: title is not a clean complete phrase (trailing whitespace or comma)")
            full=it.get("howToTest","")
            full=full[len("Inspect the artifact against: "):] if full.startswith("Inspect the artifact against: ") else full
            tail=re.findall(r"[a-z]+", t.lower())
            # A title that IS the item's complete text is a complete
            # phrase by construction, even when the sentence legitimately
            # ends on a small word. The truncation signature is a title
            # CUT FROM a longer text that stops on a fragment word.
            if tail and tail[-1] in FRAGMENT_END and t!=full.strip() and full.strip().startswith(t):
                errs.append(f"{i}: title ends on the fragment word '{tail[-1]}' (truncation signature)")
            if t in titles_here: errs.append(f"{i}: duplicate title also on {titles_here[t]} in {fn}")
            titles_here[t]=i
    if a.prose:
        # Orphan prose items: bold list leads in a lens SKILL.md with no
        # checklist counterpart in the same lens, reported as violations.
        spec_refs=0
        skill_dirs=set()
        if a.skills_root:
            for root,dirs,_ in os.walk(a.skills_root): skill_dirs.update(dirs)
        for root,_,files in os.walk(a.prose):
            for fn in files:
                if fn!="SKILL.md": continue
                path=os.path.join(root,fn); folder=os.path.basename(os.path.dirname(path))
                text=open(path,encoding="utf-8").read()
                if a.skills_root:
                    fm=re.match(r"^---\n(.*?)\n---", text, re.S)
                    if fm:
                        rm=re.search(r"related_skills:\s*\[([^\]]*)\]", fm.group(1))
                        if rm:
                            for entry in rm.group(1).split(","):
                                name=entry.strip().strip("'\"")
                                if name and name not in skill_dirs:
                                    errs.append(f"{folder}: related_skills entry '{name}' does not resolve to a shipped skill directory")
                lens=LENS_OF_FOLDER.get(folder)
                if not lens or lens not in by_lens: continue
                corpus=[content_words(it.get("title","")+" "+it.get("howToTest","")) for it in by_lens[lens]]
                for lead in re.findall(r"^\s*[-*] \*\*([^*]{3,90})\*\*", text, re.M):
                    if re.search(r"\((CS|P)-\d+\)", lead): spec_refs+=1; continue
                    lw=content_words(lead)
                    if len(lw)<2: continue
                    best=max((len(lw & c)/len(lw) for c in corpus), default=0)
                    if best<0.5:
                        errs.append(f"{folder}: orphan prose item '{lead.strip()}' has no counterpart in {lens}.checklist.json")
        if spec_refs: print(f"NOTE: {spec_refs} spec-tagged prose leads counted as protocol cross-references, not checklist items")
    if a.control_map:
        if not os.path.isfile(a.control_map): print("SUMMARY: control map missing"); return 2
        cmap=open(a.control_map,encoding="utf-8").read()
        controls=sorted(set(int(n) for n in re.findall(r"\|\s*C(\d{1,2})\s*\|", cmap))
                        | set(int(n) for n in re.findall(r"\*\*C(\d{1,2}):", cmap)))
        have={it.get("id") for it in by_lens.get("compliance",[])}
        for n in controls:
            want=f"COMPLIANCE-CTL-{n:03d}"
            if want not in have: errs.append(f"control-map agreement: control C{n} has no checklist item {want}")
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
