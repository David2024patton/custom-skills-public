# Retro and emulation engineering

Use this chapter when the product runs old software: an emulator, a core, or a frontend for one. The revival chapter recovers how a game worked. This chapter makes the machine that runs it, and proves it runs correctly.

## Core contract

- Target the libretro API first: one dynamically loadable library driven by frontend callbacks, one frame per run call, input polled per frame, no core-owned timers or platform drivers. Treat any non-libretro target as a deliberate exception with a written reason, because the contract decides the architecture before any code exists.

- Ship a correct interpreter first. Add a dynamic recompiler per host architecture only behind profiling evidence, differentially test it against the interpreter, keep an interpreter fallback that is never slower, and budget code-cache memory on the smallest target.

## The two foundations: serialization and determinism

- Design serialization as a versioned state format with a header and migration path, stable offsets, and a reported size that never grows during a loaded game. Test serialize and restore round trips for equivalence. Save states are the mechanism rewind and netplay are built on, not an extra, so never ship a core with stubbed serialization while claiming state, rewind, or netplay support.

- Require determinism: the same initial state plus the same input stream produces the same state hash at every frame checkpoint. Ban wall clocks and ambient entropy from the emulation path, keep threading deterministic or the core single-threaded, and record a state hash in every bug report and test run.

## Proving correctness

- Name an accuracy tier per system (interpreter correctness, then cycle-stepped timing, then cycle-accurate where the hardware demands it), model regional clock ratios (NTSC, PAL, Dendy) as data, and write the tier and its known deviations into the capability ledger before adding features.

- Wire the platform's known test ROM suites (CPU, PPU, APU, mapper suites, golden CPU logs) into CI as pass/fail release gates with suite name and version recorded. A newly failing test is a release blocker, not a known issue.

- Run a golden regression harness: headless fixed-input runs over a fixed matrix of homebrew and legally held test titles, hashing framebuffers at set frames and comparing the emitted audio stream against stored goldens, with the matrix published per build.

- Reproduce every compatibility bug from an input recording plus a state file, and forbid per-game hacks that are not recorded in the capability ledger with their reason.

## Performance on real hardware

- Set written budgets before production: frame-time percentiles on worst-case titles, a memory ceiling including state and rewind buffers, load times, and a sustained 30-minute thermal run, all measured on the weakest supported device. Desktop numbers do not transfer to ARM TV sticks.

- Treat each ABI as a separate product: keep a per-ABI matrix of which cores ship, which backend each uses, and which features are cut, and build and smoke-test every ABI you ship. A 32-bit build must never inherit claims verified only on 64-bit.

- Decide the runtime isolation model up front: one core loaded at a time, separate processes, or a single shared runtime, and unload and reinitialize cleanly between cores. Several independent runtimes in one process can kill the app the first time a game launches, and desktop harnesses do not reproduce it, so include a launch-every-core pass in the real app process in the ship checklist.

## Display, audio, and latency

- Report true geometry and pixel aspect ratio from the core, default to integer scaling with a correct aspect option, handle overscan crop and rotation per system, and offer shader presets in GPU cost tiers measured on the weakest GPU. Treat NTSC and composite effects as an explicit look choice.

- Report exact audio sample rates, prefer batched frame-sized interleaved stereo, use dynamic rate control or equivalent drift correction, and define an underrun policy that never speeds the core up to compensate. Include an audio hash or listening checkpoint in the regression matrix.

- Budget latency end to end (controller, polling, the game's own internal lag, display) and measure it. Run-ahead removes game-internal lag only, is capped at the game's real internal lag (overshooting drops inputs), and spends heavy CPU, so expose it as a per-game setting. No setting fixes a slow display.

## Feature sequencing and netplay

- Sequence enhancement features by dependency: serialization, then save states and rewind, then run-ahead and netplay, then cheats and achievements. Size rewind by state size times retained frames against the memory budget, and define hardcore-style rules that disable state loads, rewind, and cheats while active.

- For netplay choose rollback (predict, advance, restore, re-simulate on late input) for action titles and delay-based only for slow ones. Require per-session state-hash comparison with a desync abort and report, and specify player count, input delay defaults, and NAT and session setup in the feature spec.

## Input and the TV frontend

- Map everything through one pad abstraction with per-core and per-game overrides, analog deadzones, axis-based D-pads, declared port devices for multitaps, light guns, mice, and keyboards, and tested hot-plug and player-order behavior. Keep a tested-pads list with their quirks.

- On TV, require every control reachable by D-pad alone, a visible focus indicator at all times including first launch and idle, and predictable back behavior with no exit gating or menu loops. The full remote-only walkthrough on the real TV device is a release gate.

## Content, saves, and firmware

- Load content from user-picked locations without assuming raw paths, prefer in-memory loading so soft patching works, and identify titles by header and CRC rather than filename.

- Keep battery saves, save states, and firmware in separate backed-up locations. BIOS and firmware are user-supplied dumps or clean-room replacements, never bundled.
