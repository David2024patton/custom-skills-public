# Run Evaluation Checklist

Use this to audit a finished run, your own or another agent's, before the result is trusted or merged. Score each line pass, fail, or not applicable, and attach the run folder as evidence.

## Coverage

- The run answered the question that was asked, at the scope in the contract, and did not quietly substitute an easier question.
- Every dimension on the outline has findings, or a named reason it has none.
- Fan out work reports its coverage as successes out of total, with failures listed rather than absorbed silently.

## Evidence

- Every high impact claim traces to an evidence ID, a source, and a locator such as a page, section, or line.
- Citations use evidence IDs only (`[E0007]`). No numbered references (`[1]`) appear for report claims, and the evidence table, claim ledger, and References section are all keyed by the same IDs.
- No decisive claim rests on a snippet alone. Sources that could not be opened in full are marked partial or snippet-only, an original or equivalent primary source was sought elsewhere, and no material claim rests solely on a partial or snippet-only source.
- Vendor and interested party claims are tagged, and no market truth rests on Tier C alone.
- The three most load bearing statistics trace to original studies with years attached.
- Prices, rules, and versions carry as of dates and were rechecked against the freshest publisher source.

## Claim ledger

- A claim ledger exists for the run, one record per material claim, with importance, status (verified, probable, contested, unsupported), evidence IDs, source tier, locator, freshness, counterevidence checked, access status, and final wording.
- No report paragraph mixes a verified fact, an inference, and an unsupported assumption at one confidence level. Unsupported claims are cut or in What could not be verified. Contested claims name both sides.
- User-provided facts are labeled user-provided, not independently verified, unless a source in the run verified them. They are not silently contradicted by generic web data.

## Honesty

- The report separates what was verified firsthand, read in full, seen only as a snippet, and accepted from another report.
- Nothing claims work that did not happen. No invented files, tests, sources, or sends.
- Conflicts appear with both sources named. Nothing was smoothed into a tidier story.
- Uncertainty labels are used where the evidence is thin, and the could not verify section is present and specific.

## Usefulness

- Decision items carry verdicts and consequences, and the actions are ranked by value.
- A reader who only reads the first three paragraphs and the actions still gets the answer right.
- The author line, if any, is the author the user requested. No default tool, platform, or assistant brand name is used as author.
- The findings are saved somewhere findable after the chat scrolls away, and only where saving is useful and permitted. No sensitive personal, medical, financial, credential, or confidential business information is stored in notes or memory unless the user explicitly requested it.

## Visuals (when the report has any)

- Labels, legends, axes, scale, and units are readable and explicit.
- Contrast is sufficient and the visual reads for color blind readers; color alone does not carry meaning.
- The visual is readable at phone width.
- Source attribution and the as of date appear directly on or under the chart.
- The scale does not exaggerate or hide differences (no misleading truncated axes, cherry picked ranges, or 3D distortion).

## Process

- Hop counts are treated as planning estimates only. The method note names the real stop condition (material claims supported, contradictions resolved or labeled, further research unlikely to change the conclusion), not a hop quota.
- Tool names in the run are mapped to the tools actually available in that environment. Any unavailable tool, substitution, or ledger fallback is disclosed in the method note.
- Parallel drafting, if used, was justified by high stakes, unusual breadth, or a contested topic, not used merely to lengthen an ordinary report.

## Failure patterns this checklist exists to catch

- Depth without an operator lens, meaning a long report with nothing the reader can do next.
- A tidy outline presented as research, with no primary source opened.
- Hallucinated labour, where the writer claims it built, ran, or checked things it never touched.
- One AI's unverified output copied into another report as if it were a source.
- Enterprise framing on a small operator's question, or generic framing on a question with a specific person, place, and budget.
