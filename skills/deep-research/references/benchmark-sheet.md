# Run Benchmark Sheet (score every deep or exhaustive run)

Modeled on enterprise deep-research benchmarks (ServiceNow drbench and the Deep
Research Bench family): score the run in the method note so engine improvements
are measured, not vibes. Score each axis 0 to 2 (0 missing, 1 partial, 2 solid)
and state the total out of 10.

| Axis | What a 2 looks like |
|---|---|
| Coverage | every dimension of the question addressed; gaps named, none silently dropped |
| Citation accuracy | spot-checked: every sampled claim traces to the cited source and the source says it |
| Verdict correctness | decision items carry a real verdict with consequence or dollar value |
| Counterevidence | the strongest opposing view searched, named, and answered |
| Actionability | a reader can act on the next working day without rereading the evidence |

Audience notes: a residential 2 on Actionability means a household can follow it
without jargon; a corporate 2 means the economic buyer can take it to a meeting.
A run scoring under 7 does not ship without saying so in the reply, and it
triggers HUMAN_GATE_REQUIRED (skeptic probe) rather than a silent delivery.

After scoring, append the pre-flight diagnostic block (Gap and Risk
Diagnostic): **Readiness** (the score), **Open Gaps** (unverified or unbuilt),
**Dependencies** (what must be true in the environment for this answer to
hold), **Remediation Actions** (each with owner: Agent or Human).
