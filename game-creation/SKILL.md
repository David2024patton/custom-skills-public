---
name: game-creation
description: Create games end to end: original games, revivals of defunct games, and retro emulation platforms. Covers the rights and license gate, design (pillars, loops, economy), revival research from archives, prototyping and stage gates, production pipelines, emulator core engineering, playtesting, launch, and live operations. Use when a user wants to make, remake, revive, clone, port, or ship a game, build an emulator or game frontend, or ask how a game should be designed, built, tested, or launched.
---

# Game Creation

One skill for making games at any starting point: a new idea, a dead game worth reviving, or old hardware worth emulating. Work the stages in order. Every stage has a gate, and nothing moves forward on faith.

## The stages

1. Gate zero: rights, licenses, and the constraint sheet. See `references/rights-and-licenses.md`.
2. Design: pillars, loops, economy, and the spec.
3. Revival research, when the game already existed. See `references/revival.md`.
4. Prototype and stage gates. See `references/production.md`.
5. Production: architecture, art, audio, tuning. See `references/production.md`.
6. Retro and emulation engineering, when the game runs old software. See `references/retro-emulation.md`.
7. Playtesting and QA at every gate.
8. Launch: store page, ratings, certification. See `references/launch-and-live.md`.
9. Live operations, telemetry, and end of life. See `references/launch-and-live.md`.
10. Postmortem, folded back into this skill.

## Rules that hold at every stage

- Clear the rights and license gate before building anything, and keep the license ledger in the repo from day one.

- Write the constraint sheet as spec section zero: platforms, weakest target device, frame rate target and frame budget, input set, resolutions, online or offline, and language needs. Design inside it.

- Keep every balance number, limit, and budget in external config or data tables a designer can change without a rebuild, and log every tuning change with its reason.

- Record every decision the user makes in the spec with its date, and keep a risk register reviewed at each stage gate.

- Ship the spec with a sized feature list, an explicit cut list, and a pre-mortem. When time shrinks, cut from the cut list in order instead of renegotiating everything.

- Verify on the real target hardware and in the real app process, and re-run test suites yourself instead of trusting another agent's report. Desktop results do not transfer to weak devices.

- Keep a public capability ledger in the repo: what is proven, on what evidence, what is homebrew-only or test-only, what is known broken, and what is not implemented. Never let one build inherit claims verified only on another.

- At each ship or round end, write a one-page postmortem and fold its lessons back into this skill and the project spec.

## Design

- Write 3 to 5 design pillars, the player fantasy in one sentence, and the target feeling before any systems work, and cut later choices that fight the pillars.

- Name the target player, their motivation, and who the game is not for, and use that profile to settle feature disputes.

- Diagram the loop hierarchy with timing and exit states: moment to moment, core loop, session loop, meta progression. A session loop with no natural stopping point fights its own pacing.

- Design the economy as faucets and sinks per currency with a cross-system influence map, then simulate a new player, a mid player, and a heavy spender over time. Any currency with a faucet and no sink gets a sink before launch.

- Specify progression explicitly: what unlocks when, how difficulty scales, and what visibly marks mastery, tying each unlock to a loop the player already learned.

- Budget game feel as real work: input response, camera behavior, hit feedback, sound cues, and screen feedback for every core action, prototyped before content.

- Give every system a document that ends with acceptance criteria a tester can verify, its edge cases, and its failure states. No criteria, no build start.

- Maintain a systems index with dependencies and priority tiers, check it for cycles before scheduling, and build in dependency order.

## Package and publish

- Keep the project in a GitHub repo with the spec, the mechanics or systems docs, the data tables, the research, and a README index, and verify the remote HEAD equals the local HEAD after pushing.

- Keep large archives, ROMs, and caches out of the repo, and never commit game ROMs, BIOS images, or firmware dumps under any circumstances.

- Report findings first, file links second, open questions last, and keep it short.

## Instance notes

- The iTaK Gaming project (from-scratch emulator cores plus a TV frontend) and the TDZK revival (archive research plus recreation spec) are the worked examples behind this skill. Their lessons are baked into the rules above and the retro chapter.
