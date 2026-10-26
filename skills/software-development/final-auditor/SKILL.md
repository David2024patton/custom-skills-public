---
name: final-auditor
description: "Use to independently verify shipped work before release."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [audit, final-gate, verification, release, sign-off]
    related_skills: [persona-skeptic, commit-gates, security-auditor, ui-visual-check, critic-lens-code]
---

# Final Auditor: The Last, Independent Gate

## When to Use

Run this after the critic fix loop reports zero findings and the UI visual check passes. The final auditor did NOT do the work and did NOT run the first critic pass. Its job is to verify the PROCESS was honest, not to re-review the code from scratch.

## What it verifies (the meta-audit)

1. **Fixes are real, not claimed.** For every Critical/High the loop closed, find the fix in the diff and the re-run output that proves it. A closed finding with no evidence reopens.

2. **Severity was not gamed.** Spot-check that findings were closed by fixing, not by down-labeling. Re-apply the rubric (exploitability x impact) to a sample of the closed findings yourself. If a Critical became a Low without a code change, that is a finding.

3. **The sweep was a sweep.** Confirm the route/handler enumeration is complete (re-run the count) and that no row was left UNTESTED without an owner. Sampling dressed as sweeping is the classic failure.

4. **Untested surface was assigned.** Every item the critic listed as untested is either a closed task or on David's written accepted-risk list. A dead-end untested list reopens it.

5. **The visual report is real.** Screenshots exist, cover the states and widths, and show a working app, not a mock.

6. **Secrets were swept in history,** not just the working tree.

7. **Threat feeds were fresh** at audit time, not cached from a prior run.

## Verdict

- **SHIP**: every Critical/High fixed with evidence, sweep complete, visual report real, feeds fresh.
- **BLOCK**: name exactly what blocks it, with the reopened finding and its evidence.

There is no soft middle. "Mostly ready" is a block with a list.

## Independence rule

The final auditor never audits its own work and never trusts a completion report as proof. A subagent's claim that a fix landed is a claim. Re-run the gate yourself before signing.
