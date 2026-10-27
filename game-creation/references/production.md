# Production: prototype to finished game

The design stage produces a spec. This chapter turns the spec into a shippable game without drift, and it is where most game projects actually die, so the gates are the point.

## Stages and gates

- Run the stages in order: concept, pre-production, prototype, vertical slice, production, alpha (feature complete), beta (content complete, fixes only), release candidate (locked), launch, live.

- End each stage with a written go or no-go against exit criteria set in the spec, and set content lock dates before beta. No new features after beta, ever.

## Prototyping

- Greybox the riskiest mechanic first with placeholder art, one mechanic per prototype, each answering one design question, inside a few weeks at most.

- Playtest the greybox on fresh players. If it is not fun ugly, stop and redesign. Never carry prototype code into production.

## Vertical slice and first milestones

- After the prototype passes, build one short slice (15 to 30 minutes or one full match or level) at shipping quality, exercising art, audio, save, and UI end to end, profiled on the weakest target device. Treat slice failure as a scope signal, not a polishing problem.

- Make milestone one the full shell loop on the weakest target device: launch, title, play, results, save, quit, relaunch, restore, with placeholder content, before any system gets depth.

## Engine and stack selection

- Choose the engine as a scored business decision, not a default: target platforms, 2D or 3D fit, team language, total license cost at expected revenue, ecosystem and hiring pool, source access, and exit cost.

- Prototype the riskiest mechanic in the top candidate before committing, validate again at the vertical slice, record the decision and the license terms in the spec, and re-check terms before launch.

## Architecture

- Run a fixed-timestep simulation decoupled from rendering, with interpolation, so game speed never depends on frame rate.

- Model game state with explicit state machines instead of flag piles.

- Design saves early: versioned format with a migration path, atomic writes, a backup slot, and a corruption recovery story. Test save and load abuse in QA.

- Route all input through one abstraction layer so remapping, multiple devices, and accessibility options come free.

- Keep modules and runtimes isolated behind interfaces so one can be swapped or fail without taking down the rest. Several independent runtimes sharing one process can crash the whole app, so decide the isolation model up front (see the retro chapter for the multi-core case).

- Automate the build and export per platform early, keep a patch pipeline ready before launch, and test the exact build players will download, not the editor build.

## Art and audio pipelines

- Set an asset budget sheet before production: geometry, texture memory, draw calls, build size, and a texel density target, with naming conventions, import presets, and LOD and culling plans from the first asset.

- Write the asset rules down and back them with a validator where the engine allows one. Never hand-edit files the pipeline owns.

- Treat audio as its own system with a spec section: buses for music, effects, dialogue, and ambience, loudness and voice-count budgets, adaptive music and effect variation designed from the start, per-channel volume controls, and defined behavior on interruption (calls, tab switch, mute).

## Tuning

- Model the economy as sources and sinks, run automated simulations to spreadsheet output before human testing, and define difficulty and progression curves explicitly.

- After launch, tune from telemetry (retention funnels, difficulty spike points, currency flow), not anecdotes.

## Playtesting and QA

- Run scheduled playtests from the first prototype: one objective per session, target players plus outsiders, blind tests, and an exploit test where testers try to break the game.

- Observe silently, record stuck points and retries, and separate what players say from what they did. Log everything and retest after fixes.

- Keep bug-hunt QA separate from playtesting: test plans, severity triage, regression passes, a compatibility matrix (minimum device, every supported input type, aspect ratios), long-session soak tests, and crash logging with repro steps. A bug without repro steps is a rumor.

## Onboarding, accessibility, localization

- Design the first five minutes as learn-by-doing, one mechanic at a time, and playtest it blind with someone who never saw the game. Most early quitters quit confused, not bored.

- Work an accessibility checklist from day one: remappable controls, scalable text, no information carried by color alone or by sound alone, subtitles with speaker identification, adjustable difficulty and game speed, photosensitivity care, and playtests that include disabled players.

- Externalize every player-facing string from the first build, never assemble sentences from fragments, and design layouts for text that grows by a third. Retrofit localization is a rewrite.
