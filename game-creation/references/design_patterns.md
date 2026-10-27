# Modernization Design Patterns (proven in the TDZK revival)

Adapt these to the target game; every number is a configurable default.

## 1. Server-authoritative pacing (the "fast internet broke the game" problem)

Old click-and-refresh games were balanced around 2000s latency. On fiber, the fastest clicker or a script wins. Fix it on the server:

- **Per-action cooldowns:** a "next allowed at" timestamp per player and action. Make them speed-dependent; for example, a move costs `900 ms × 10/speed`, clamped to 600–1500 ms.
- **Arrival ("warp-in") window:** about 1.5 s after arriving, the ship can neither be attacked nor attack.
- **±10% jitter** on every cooldown and window, so scripts can't time actions to the millisecond.
- **Optional latency floor:** hold every action to a common effective round-trip time, for example 250 ms.
- **Keep "refresh to see":** don't auto-push other players' movements, because scouting is a skill. Push only personal alerts.
- **Era presets:** Dial-up 1.8×, DSL 1.0×, Blitz 0.6× multipliers on all timings.
- If the community has a reflex trainer page (for example TDZK's getChief), mine it for the original timings and ship it as a practice page.

## 2. Pixel-faithful UI

Use the official image packs and CSS where they survive. Rebuild the layout as server-rendered HTML that matches the original's structure. Add modern behavior (no-reload updates) without changing how it looks. Use `scripts/contact_sheet.py` to catalog each pack and map image files to UI slots.

## 3. Game-mode family

- **Classic:** the faithful ruleset (the best-documented version).
- **Chaos Round:** an end-of-round tradition. Huge credits and turns, everything unlocked, instant rebuys, no anti-farm limits.
- **Multi-ship / Fleet mode:** see section 4.
- **Planet subgame:** see section 5.
- **AI Agent League:** see section 6.
- Successor-inspired modes are optional and labeled. Check how the community received the successor before borrowing from it; TDZK: Fleets was disliked.

## 4. Single-ship to multi-ship conversion: value conservation

The invariant: **a whole fleet is worth about one classic ship per turn spent.** Scale every reward and cost by `shipShare = value(ship) / value(fleet)`.

| System | Rule |
|---|---|
| Ownership | Grows with level, for example `min(cap, 1 + level/5)` |
| Movement | `1 + ceil(towed/5)` turns; cooldown from the slowest ship |
| Combat | Cap participants per side (for example 6); player-set battle order; reserves swap in; attack cost `base + 1 per extra participant` |
| Death and XP | Classic penalty and kill XP × shipShare; the pod and newbie protection only when the last ship dies |
| Trade | Turn cost scales with holds traded (for example 1 turn per 150 holds), so profit per turn stays the same |
| Upkeep | A small percent of value per day for extra ships; unpaid ships get parked automatically |
| Visibility | Fleets are easier to spot; a fleet is cloaked only if every ship is |

Validate with simulations: a convoy against a single ship over N turns must stay within ±10% on credits and XP per turn.

## 5. Planet subgame with anti-zerg fairness

- **A separate turn pool** (Command Points) for planet actions. Ship turns get you to orbit; Command Points fight on the ground.
- **A living economy:** population, morale, tax curve, food, goods consumption, upkeep, governments, elected offices, treaties.
- **Escalation ladder:** bombardment, then blockade, then raid, sabotage or heist, then occupation, then capture. Never instant permanent deletion.
- **Restock under siege:** shield cells, repair kits, militia, and supply runs that blockaders can intercept.
- **Fairness rules that apply at the target, not per attacker:**
  - landing zones, one pilot each;
  - coordination penalty `1/(1+0.2(n−1))` on attackers;
  - resilience stacks after each hit, in the style of Utopia's multi-attack protection;
  - a daily plunder cap plus reduced rewards when the defender is much smaller, as in Astro Empires;
  - owner-chosen vulnerability windows plus a lockdown when shields fall, as in EVE;
  - solo "Homestead" bonus and NPC militia help when the defender is outnumbered.
- **Clan value:** supply networks, shield relays, clan-only structures, more territory.

## 6. AI Agent mode

- Separate Agent League servers, optional mixed servers with an [AI] tag, and human servers with no automation.
- A line-based text protocol plus JSON plus an MCP wrapper. Verbosity levels: **L0 numbered menu (60 to 120 tokens; the reply is one number, so phone 1B to 4B models can play)**, L1 compact commands, L2 full.
- Owner-set budgets: tokens per observation, hour and day; actions per hour; spending caps. The server enforces what it sends and receives; a reference client (OpenAI-compatible: Ollama, LM Studio, llama.cpp, cloud) enforces the model-side budget.
- Leagues by declared budget class, since the actual model can't be verified.
- Same cooldowns as humans. Optional Arena servers with fixed decision windows, so slow models compete fairly.
- Spectating: a live map with follow-cam, replays in the original report format, a 140-character thought line, Elo leaderboards, AI Chaos events.
- Player-written text is delivered to agents as marked, length-limited untrusted fields, against prompt injection. Owners get a kill switch.

## 7. Anti-cheat ladder

**Prevent:**
- the server is the authority on everything;
- hidden information never reaches the client;
- one-time signed action tokens per page render;
- transactions with row locks;
- rate limits;
- an official outlet for automation (the AI Agent mode).

**Detect, feeding a decaying risk score:**
- refreshers: low spread in reload intervals plus periodicity, reloads with no input in between, reloads while the tab is hidden, and the browser recording the load as `reload`;
- macros: reactions under 150 ms, identical click pixels, no pointer movement, `isTrusted=false`, honeypot links;
- `navigator.webdriver` and headless browser fingerprints;
- 24-hour activity with no sleep gap;
- multi-account links: shared devices or IPs, one-way funnelling, overlapping logins.

**Respond:** quiet logging, then a challenge, then a cooldown multiplier, then an admin review queue with evidence charts, then a human-decided suspension. Allowlist accessibility tools, keep an append-only audit log, and publish the rules.

## 8. Stack defaults

- **TypeScript** on the server, with a dependency-free rules-engine package shared by server, browser and tests. Port the recovered JS almost line for line.
- **PostgreSQL** as the record of truth; Redis only as an add-on.
- Rust or WASM later if wanted.
- SurrealDB and MongoDB are not recommended for contention-heavy game state. SQLite is for development and private servers only.
