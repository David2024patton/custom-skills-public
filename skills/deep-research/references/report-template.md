# Report Template

Use this skeleton for report files. Drop sections the question does not need. Keep the answer first and the machinery last.

Author rule: use the author the user requested. If none is specified, omit the author line entirely. Never default to a tool, platform, or assistant brand name as the author.

```markdown
# <Question as a plain title>

<One to three short paragraphs that answer the question directly, with the main numbers and verdicts. No preamble.>

## <First concrete topic>

<Findings in prose. Cite evidence IDs beside high impact claims, like [E0007].
Give each decision item its verdict and its dollar value or consequence.>

## <Next concrete topic>

<Findings, same pattern. Show disagreements with both sources named.>

## What survived checking and what did not

<Only when the skeptic pass killed or downgraded something material.
What survived, in one or two lines each. What died, and why.>

## What could not be verified

<Open questions, missing records, and claims labeled single-source, contested, weak, stale, or unknown.
User-provided facts used as context belong here as a note when they were not independently verified: label them user-provided, not verified.>

## Do not rely on

<Only when the research found claims, statistics, or products the evidence says to avoid, each with its reason.>

## Recommended actions

<For decision research. Ranked by value, each action short enough to do on the next working day.>

## Evidence table

| ID | Claim supported | Source | Publisher | Date | Tier | Access | Interest |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E0001 | <claim> | <title> | <publisher> | <date> | A | full | none |

Access is full, partial, or snippet-only. A partial or snippet-only source never solely supports a material claim.

## Claim ledger

<Summary for standard runs, full ledger for deep, exhaustive, or high stakes runs.
One row or record per material claim, using the schema in SKILL.md.>

| Claim | Importance | Status | Evidence | Tier | Locator | Freshness | Counterevidence checked | Final wording |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <exact claim> | high | verified | E0007 | A | Section 4 | <date, rechecked> | yes | <wording used in the report> |

## Gap and risk diagnostic

| Field | Content |
| --- | --- |
| Readiness score | <n/10 from the benchmark sheet> |
| Open gaps | <what could not be verified or remains unbuilt> |
| Dependencies | <what must be true in the environment for this answer to hold> |
| Remediation | <next step; owner: Agent or Human> |

## Method note

Effort level, hop count actually used (planning estimate noted as an estimate, not a quota), source classes used, what was opened in full versus partial or snippet only, tool limitations or substitutions, verification steps, and the stop condition that ended the run.

## References

[E0007]: https://example.com/page "Descriptive source title"
[E0012]: https://example.com/other "Descriptive source title"
```

## Citation rules for report files

- One system only: evidence IDs. Cite claims inline as `[E0007]`. The evidence table and the References section are keyed by the same IDs.
- Never use numbered references such as `[1]` for report claims, and never mix the two systems in one report.
- List a reference once, under its evidence ID, in order of first use, and reuse the same ID for the same source and claim everywhere.
- Give every reference a quoted descriptive title.
- Encode parentheses in URLs, writing %28 for an opening parenthesis and %29 for a closing one, so the link does not break its neighbours.
- Keep citations beside the claims they support, not collected at the end of a paragraph that makes ten claims.

## Visual rules for report files

- Put source attribution and the as of date directly on or directly under every chart or diagram.
- Check labels, legends, axes, scale, and units for readability, sufficient contrast, and color blind readability (never color alone to carry meaning), and readability at phone width.
- Check the scale does not exaggerate or hide differences before delivery.

## Chat reply rules

- Answer in prose, cite with inline links beside the claim, and add no References section.
- Keep it to about three short paragraphs. Anything longer belongs in a report file, with the chat reply reduced to the conclusion and the link.
