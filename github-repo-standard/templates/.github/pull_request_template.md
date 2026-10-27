<!--
Pull request template for repos under the github-repo-standard.
The change description standard below is the contract for every PR:
a standalone first line, context, non-goals, and proof links. A PR
whose description cannot stand alone in the PR list is not ready
for review. Delete these comments when the description is filled in.
-->

## Summary

<!-- Standalone first line: one sentence that fully states what this
PR does, readable on its own in the PR list with no other context.
Write that sentence first, on the first line under this heading. -->

<standalone one-line summary of the change>

## Context

<!-- Why this change exists: the problem, the request, or the TODO
item and PLAN section it serves. Link the issue, TODO id, or plan
section instead of restating them. -->

## What changed

<!-- The change itself, module by module. Keep it to what a reviewer
needs to check the diff against the intent. -->

## Non-goals

<!-- What this PR deliberately does not do: the adjacent work it
leaves alone, the follow-ups it parks, and where they are tracked.
If there are no non-goals, say so in one line. -->

## Proof

<!-- Links, not claims: the test run, the gate output, the log line,
the bench note, or the live check that proves the change works.
Name which kind of proof each link is; emulation proof and bench
proof are different claims. -->

- Gates: <link or summary of the run-gates.sh result>
- Tests: <link to the test run or output>
- Other proof: <link, or "none">

## Checks

- [ ] Commit gates run clean (run-gates.sh), or the red gate is named here with its reason.
- [ ] Commit messages follow the commitlint config (commit message gate).
- [ ] No secrets, keys, or tokens in the diff.
- [ ] Standard files touched by this change (TODO, PLAN, STATUS, MAP) are updated in this PR.
