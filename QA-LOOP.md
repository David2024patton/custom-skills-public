# QA-LOOP.md - The Closed-Loop Quality Pipeline

Instruction header: this is the build law for how work is researched, built,
audited, fixed, and verified in the personas workspace. Every persona and
skill in this system conforms to it. When this document and a persona SOUL
disagree, this document wins on the loop; the SOUL owns the craft.

## The loop, end to end

```
IDEA
  -> Researcher (competitor research, MANDATORY before any SaaS feature)
  -> Ideator (checks idea against competitors + David's existing stack;
              names better routes, gaps, and what to cut)
  -> Owning persona does the work
       code      -> Builder
       copy/ads  -> Marketer / Creator
       design    -> UI Specialist
       data      -> Analyst
  -> Critic loop (the core; runs until ZERO findings)
       |
       +-- has findings? --YES--> route each to owning persona to FIX
       |                          then re-run the full critic checklist
       +-- zero findings? --YES--> UI Visual Check (browser + screenshots)
                                    -> Final Auditor (meta-verify the work
                                       was caught properly; signs off)
                                    -> SHIP
```

Every arrow is a handoff with a required artifact. No phase skips. A phase
exits when its deliverable exists and its gate passes, not when time runs out.

## The Critic Checklist (non-negotiable, nothing skipped)

The critic runs this as an ordered checklist. Every item is answered with
evidence or marked UNTESTED. Nothing is sampled; everything is swept.

### A. Execution (do this FIRST, not last)
- [ ] Build it: language build command, real exit code and output captured.
- [ ] Vet/lint it: the language linter AND the type checker, clean or the
      exact findings listed. Rules are fixed, not silenced without a reason.
- [ ] Test it: full suite with race detector where available. Real output,
      not a claim. A green suite the critic did not run is not green.
- [ ] Run the app: boot it, hit the main flow, read the logs in full. No
      unhandled errors, no unexplained warnings.
- [ ] Error paths: exercise invalid input, missing auth, timeout, upstream
      down, on purpose. Watch for leaks, loops, duplicate work, N+1.

### B. Static attack (after you have run it, read it again)
- [ ] Enumerate EVERY route/handler/export programmatically (grep, AST).
      Produce a matrix: each one marked PASS, FAIL, or UNTESTED against the
      access-control rule. No sampling. The sweep is the deliverable.
- [ ] Access control and tenancy: for every route, can principal A reach
      principal B's data. Two-account probe per route family where possible.
- [ ] The OWASP classes, walked file by file.
- [ ] Correctness under failure, boundaries, concurrency.
- [ ] Performance at scale: N+1, unbounded queries, missing indexes/pagination.
- [ ] Every load-bearing claim in the code's own comments and docs: does the
      code actually do what it says. Contradictions are findings.

### C. Severity (deterministic, not vibes)
- [ ] Score each finding: exploitability (can a real attacker reach it) x
      impact (what they get). Map to Critical/High/Medium/Low by the rubric.
      The same defect always gets the same severity. No upgrading on hunch.

### D. Security grounding (live, not memory)
- [ ] Refresh threat intel THIS run: CISA KEV diff, NVD recency, OSV/GHSA
      per dependency. Record feed freshness in the report header. A clean
      scan on stale feeds is provisional and says so.

### E. Untested surface (a to-do, never a footnote)
- [ ] List everything not covered. Each item becomes an assigned follow-up
      task with an owner, not a paragraph nobody reads.

## Critic dispatch rules (scope proof + fresh-critic fence)

- **Scope proof comes first.** A dispatch brief PINS the exact file paths (or commit) under review. The critic's first output is the inventory of those paths with existence verified, and findings outside that list are out of scope. No git-history wandering: 4 of 6 reviewers on one audit drifted to unrelated upstream commits and returned zero findings about the actual change set.
- **Fresh-critic fence.** A verifying or background critic receives only: the artifact, the brief/spec, and the prior report. NEVER the builder's reasoning or its claimed-fix list. It must find things itself; handed conclusions are how regressions survive.
- **Time box.** Runs over ~60 minutes without a report stop exploring and emit findings with explicit coverage notes. Dispatch in batches of three; re-dispatch rather than letting a stalled run burn time.
- **Evidence marks on every claim.** [OBSERVED] read it this run, [INFERRED] derived from evidence, [ASSUMPTION: high/med/low] a gap. A review where everything is [OBSERVED] of something trivial is not coverage.

## Background reviewer (review while the build runs, not only after)

Promote the critic from a gate that starts AFTER the build to a reviewer that
runs DURING it, the way Meta frames "workers in parallel, reviewers in the
background." The end-of-build gate still runs in full; the background pass
just front-loads discovery so the fix loop starts sooner.

How it works:
1. When a builder starts a module (or the skeleton lands), the orchestrator
   ALSO spawns a skeptic on the SAME scope in parallel. Not instead of the
   final gate. Alongside the build.
2. The background skeptic reviews the diff/skeleton as it exists, runs the
   checklist, and queues findings while the builder keeps working on the next
   slice.
3. When the builder finishes, the background findings are already waiting, so
   the fix loop begins immediately instead of the reviewer starting cold.
4. The definitive critic pass still runs on the completed build and owns the
   verdict. A background review of an in-progress build is PROVISIONAL: it
   re-runs the full checklist (A-E) on the finished work before any finding is
   treated as settled.

Rules:
- Parallel, not nested: spawn builder and background skeptic as siblings via
  delegate_task (both children of the orchestrator). A builder never spawns its
  own reviewer.
- The background skeptic may not block the builder. It queues; it does not
  interrupt. The builder does not wait on it.
- Convergence still rules: findings the background pass and the final pass
  both hit are highest confidence; a final-pass-only finding is still real.
- This shortens the loop without weakening it, because the final gate is
  unchanged and still the only thing that signs off.

## Domain fan-out (keep each context clean)

When work crosses into a new domain/language whose digest or brief is heavy and
this context no longer needs what it carries, spawn a FRESH agent for it
(`domain-fanout`) instead of loading it here. The orchestrator holds the plan
and interfaces, never the digests. Each domain child loads only its own skill
in its own window, returns proof, and is discarded. Results pass through the
orchestrator as compact slices. This is how one job can touch Go, Mojo, and
marketing without any single window stacking all three and blowing the budget.

## The Fix Loop (the part the experiment was missing)

1. Critic produces the defect ledger with severities and smallest fixes.
2. Each finding routes to its owning persona: code -> Builder, copy ->
   Marketer, design -> UI Specialist. The owning persona fixes ONLY its
   findings and returns evidence (the fix, the re-run output).
3. Critic re-runs the FULL checklist A-E on the changed work, not just the
   fixed lines. A fix can break a neighbor.
4. Repeat until the ledger is empty of Critical/High/Medium. Low and Info
   can be accepted as known risks, but only David accepts them, in writing.
5. Zero findings (or accepted-risk list signed by David) is the only exit.
6. **Every round closes with a verification pass** run by a fresh critic: for each prior finding FIXED / PARTLY / STILL PRESENT with proof, plus any NEW defects the fixes introduced, ending in exactly one of SHIP or ONE MORE PASS (at most 3 named fixes). Append round -> artifact -> findings -> changes -> measured result to the round ledger; never overwrite it.
7. **Calibration gates inside the loop:** pre-commitment predictions (3-5, tagged CONFIRMED/REFUTED at the end); Realist Check before any Critical is kept (realistic worst case, mitigations, detection speed; every downgrade carries "Mitigated by:"; never downgrade data loss, security, or financial impact); reachability gate on security findings ([UNCONFIRMED] without a non-privileged exploit path); hard caps of 5 Criticals and 5 improvements per pass; self-audit drops low-confidence claims to Open Questions.
8. **Stop only at zero, a signed risk list, user stop, or stall.** Stall = no full-step improvement in 2 rounds or the same finding named twice -> change the approach, not the wording. At any iteration cap, return reduced confidence plus an enumerated residual-risk list. Measurement law: fixes assert on a computed value re-measured after the last edit, and every zero prints its denominator (0 of N).

## UI Visual Check (required for anything with a screen)

Runs even when the code critic gives the go-ahead, and its screenshots go in
the report so David can see and approve the result himself.

- [ ] Launch the real app in a real browser. Not a description, the app.
- [ ] Signed in as a real user, at desktop, tablet, and phone widths.
- [ ] Click EVERY link, button, form, and route. No dead ends, no console
      errors, no failed requests.
- [ ] Screenshot every screen and every state: loading, empty, error,
      success, disabled, long/odd content. Save each to the report folder.
- [ ] Check: overlap, clipping, overflow, missing images, invisible fonts,
      contrast, keyboard operation, screen-reader labels.
- [ ] Role separation where it applies: admin/agency/customer shells must
      look like different products; no role sees another's data.
- [ ] The 90-year-old test: a capable novice can use it cold.

## Final Auditor (the last gate, independent)

A separate reviewer who did not do the work and did not run the first
critic pass. It verifies the PROCESS, not the code:

- [ ] Every Critical/High from the loop is genuinely fixed, with the fix
      re-run and shown, not just claimed.
- [ ] Nothing was closed by re-labeling severity. The rubric was applied,
      not gamed.
- [ ] The untested-surface follow-ups were actually assigned, or are
      explicitly on David's accepted-risk list.
- [ ] The visual report exists, has real screenshots, and covers the states.
- [ ] Secrets scanned across git history, not just the working tree.
- [ ] Verdict: SHIP, or name exactly what blocks it.

## The idea route (before anything is built)

David's idea -> Researcher (mandatory competitor research for any SaaS
feature: Set A the customer compares, Set B the platform is judged on, with
pricing and a named parity target) -> Ideator (checks the researched
landscape against what David already has; names the better route, the gaps,
the things to cut, and whether it is novel or a clone) -> then the build
loop. No SaaS feature reaches a Builder without the competitor research in
hand.

## Ready-to-run scripts (the critic's instruments)

Every critic loads a stack-specific script pack so execution is one command,
not a guess. Per stack (Go, Flutter/Dart, Rust, Mojo, web):

- build, vet/lint, test (with race), run, and a smoke probe.
- A browser driver for the visual check (launch, navigate, screenshot,
  click-everything) wired to the report folder.
- A threat-feed fetcher (KEV + NVD + OSV) that stamps feed freshness.

The scripts live with the stack skills; the critic invokes them and captures
real output. A critic without its instruments does not start.

## The collaboration rule (ask each other, or research online)

When any persona or skill is unsure, it does NOT stall or guess. Two exits,
in order:

1. **Ask a peer.** The named peer is a Bot/profile: mention it in a group
   chat, route a question via kanban (`hermes kanban create`), or spawn it.
   The researcher asks the ideator; the skeptic asks the security auditor.
   Bots messaging each other is native in Hermes Bot Mode, so this needs no
   custom wiring, only the habit.
2. **Research it live.** If no peer knows, run a live search (deep-research /
   SearXNG at https://search.itak.live/ first, then web tools) and cite the
   source. Never answer a factual question from memory when a lookup is one
   call away.

The harness anatomy (profiles, bots, SOUL vs AGENTS, skills, plugins) lives
in the `hermes-harness` skill with worked examples and official doc links.

## Every skill ships with examples (standing rule)

A skill with no worked example is not done. Each skill carries an Examples
section with a real invocation and its real output, so the next agent copies
a proven pattern instead of guessing. The QA script packs under
`scripts/<lang>/qa.sh` are themselves executable examples of this rule.
