---
name: conversation-store-sweep
description: "Use when sweeping AI platform stores for a project's record."
version: 1.0.0
author: David Patton
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [record-alignment, extraction, conversation-history, doc-sync]
    related_skills: [github-repo-standard, commit-gates]
---

# Conversation Store Sweep

David works across many AI tools (Muse, Buzz, Cursor, VS Code with Copilot, Antigravity, Xiaomi MiMo, Continue, Hermes, Opencode) and says things about his projects in all of them. The long-term record lives in the repo standard files, and he periodically asks to reconcile it against every store on the machine. This skill owns that workflow end to end. github-repo-standard owns the target file formats; commit-gates owns the no-red law. Per-platform store map with paths and extraction recipes: references/conversation-stores.md.

## When to Use

- "Make sure the docs are updated and accurate based off my chat conversation."
- "Search my other AI platforms for anything about <project>."
- Any record-alignment pass where conversation history is the source of truth.

## Procedure

1. **Inventory the stores.** Search the known roots for the project keyword using the recipes in the reference. Time-bound every scan (timeout wrappers, output to scratch files) so a several-hundred-thousand-file tree cannot hang the session.
2. **Fan out one reader per store family.** Each brief is self-contained: the keyword, the live repo path, the extraction contract (verbatim user-authored statements only, each with a date and a mapping to a named repo doc or 'new, in none'), a word cap, and explicit skip lists (credential files, key material, encrypted blobs, secret values never read or quoted).
3. **Extract the user's side only.** Assistant replies are context, never evidence. Spawned subagent prompts and pasted reference blocks inside a log are NOT David; only his own sentences are. Dates that come from snapshot files are upper bounds and must be labeled as such.
4. **Dedup against the LIVE repo before folding in.** Readers on a stale clone report already-fixed gaps as new. Every 'not in any doc' finding gets re-checked against HEAD; already-covered items are dropped and the report says so.
5. **Fold in per github-repo-standard**: IDEA entries verbatim with the gloss outside the quotes, ENDFGOAL the same day for end-state restatements, DECISIONS entries with Supersedes lines for reversed calls, TODO items rewritten from open questions into execution tasks once the record settles them.
6. **Gates and commit per commit-gates**, staging explicit paths only.
7. **Report**: what each store held, what was folded in, what was deliberately NOT folded and why (adjacent tracks, superseded ladders, unconfirmed infra calls), security findings surfaced prominently (plaintext credentials in hosted pages, leaked keys), and short open confirmations offered as a list, never as blocking questions.

## Pitfalls

- Never import a non-repo track (infrastructure, side projects, agency-services pricing) into a project's record without David re-dictating it for that repo. Adjacent AlphaFlux work is not console end-state.
- Encrypted or locked stores are named as unread with their date window, and the key is requested. Never guess their contents and never skip them silently.
- A store holding zero relevant statements (predates the project, or stores only assistant text) is reported in one line. That is a finding, not a failure.
- The same statement recovered from two stores is ONE record entry with two sources, not two entries.
- Subagent returns are claims: spot-check one or two quotes per reader against the source file before they enter the record.
- Keep extraction artifacts in scratch, never inside the repo being aligned.
