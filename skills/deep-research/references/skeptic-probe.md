# The Skeptic Probe

The lesson of the October 2026 five AI comparison: the research prompt alone is not the tool. The prompt pair is the tool. A research run that is never attacked ships its weakest claims at full confidence. Run the self audit on your own draft, or hand both prompts to an outside AI and audit what comes back.

## Prompt 1, the research rules (portable, for any AI)

> Research this question under these rules. Open and read primary sources in full, do not work from search snippets alone. Prefer the statute, the agency, the paper, the official docs, and the published price list over summaries and listicles. Tag every claim that comes from a seller as [vendor claim] or [vendor survey] inline. Give a verdict and a dollar value or practical consequence for each item in a decision question. End with what you could not verify, and a list of things the evidence says not to buy or not to rely on. Never claim you did work you did not do.

## Prompt 2, the skeptic follow-up (portable, for any AI)

> Now audit your own report like a hostile reviewer. List every claim you cannot back with a source you actually opened. Which numbers came from sellers? Which came from your background knowledge rather than retrieval? Where did you smooth conflicting sources into a cleaner story than they support? Which famous statistics did you repeat without finding the original study, and how old is it really? Finish with two lists: what survived your audit, and what died.

## Self audit checklist (run on your own draft)

- Walk the claim ledger record by record. Every material claim in the report has a record with importance, status, evidence IDs, tier, locator, freshness, counterevidence checked, access status, and final wording, and the report wording matches the record's status. Cut or relabel anything the ledger cannot support.
- Check citations use evidence IDs only. No numbered references, no mixed systems, and the evidence table, claim ledger, and References section agree on IDs.
- Count the claims resting on sources you only saw as snippets or could only partly access. Either open those sources in full or find the original elsewhere now, or downgrade the claims. No material claim rests solely on a partial or snippet-only source.
- Check user-provided facts are labeled user-provided where they are not independently verified, not presented as externally verified facts.
- List every number that came from an interested party and check whether the report tags it.
- List every claim that came from background knowledge. Either source it or label it as background knowledge in the report.
- Find every place two sources disagreed and confirm the report shows the disagreement instead of picking the tidier number.
- Trace the three most repeated statistics to their original studies and record the year and population measured.
- Check every date, price, and version against the freshest publisher source you can reach.
- Confirm the report never claims an action that did not happen, such as a file written, a test run, a source opened, or a message sent.

## What to publish

- In a report file, publish a short section titled What survived checking and what did not, whenever the audit killed or downgraded a material claim.
- When the audit killed nothing material, say so in one line in the method note and move on.
- Keep a do not rely on list whenever the research found products, statistics, or claims the evidence says to avoid. Name them plainly, with the reason.

## Chain-of-verification (numbered, per high-impact claim)

For every high-impact claim in the draft, run these steps in order and record
the result beside the claim:

1. Re-state the claim in your own words, including its scope and date.
2. Re-derive it independently: a different query, a different source, or the
   arithmetic recomputed, never the page that produced it.
3. Name the strongest evidence AGAINST it that your run found; if none was
   searched for, the claim is not verified.
4. Verdict: HOLDS, WEAKENED (qualify the wording), or DIES (cut or move to
   What could not be verified).
5. Record the verdict in the claims ledger with the evidence IDs that carried it.

A claim that skips steps is unverified by definition, whatever the draft says.

### The Record gate (no proof, no HOLDS)

A HOLDS verdict additionally requires all three, EasyAudit's
Connected-Verified-Current-Traceable pattern adopted 2026-10-26:
(a) a connected primary artifact (evidence ID whose record carries URL plus
locator or exact quote), (b) a freshness check recorded via the ledger's
--freshness field: was this true only when first written, or is it still true
right now? (c) zero reliance on unverified model memory: if the only support is
background knowledge, the verdict caps at WEAKENED. Automated output without
proof never passes.

### Drift scan (tag every finding)

During the pass, scan explicitly for three drift classes and tag findings:
- **AC-DRIFT**: access, permission, or auth-boundary changed or assumed stale.
- **SR-DRIFT**: supply-chain, third-party, or dependency risk introduced or shifted.
- **AU-DRIFT**: policy, spec, or architecture drifted from what the work claims.
Untagged drift that a later reviewer finds is a defect in the review itself.

### Human gate (the system proposes, a person decides)

Emit a structured block before the outcome is written anywhere persistent
(memory, repo, production) when ANY of these hold: a load-bearing claim lands
WEAKENED or DIES; a critical compliance control is GAP; a benchmark score is
under 7; or the next step mutates production or persistent memory. Block shape:
HUMAN_GATE_REQUIRED -> assertion_summary, evidence_ids, proposed_remediation,
who decides (David), when. Execution stops at the block.
