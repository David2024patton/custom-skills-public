# Persona Bots: Structure and Stand-Up

David runs a roster of Hermes persona bots: a business team (CEO, sales, finance, marketing, support, release) and an SDLC pipeline (planner, analyst, architect, builder, tester, devops, maintainer, researcher, security), plus critics and researchers. Standing up a new persona bot is a recurring task, not a one-off.

## Structural pattern: one SOUL core + lens skills as eyes

A persona is ONE profile with its own SOUL.md. Domain breadth comes from skills, not from multiple SOULs. Build it as:

- **The SOUL core** carries identity, stance, the verdict/output contract, and a routing table that points at the lenses by task type.
- **One lens skill per domain** carries that domain's checklist, source list, output shape, and gotchas. The lens is the "eyes"; the SOUL is the disposition.

Do NOT clone the whole SOUL per domain (it drifts and triples maintenance). Do NOT spawn identical sub-agents when the goal is breaking blind spots: that needs diverse LENSES, not duplicate SOULs. A fan-out of identical reviewers is for self-consistency (defect-finding, where run-to-run variation surfaces different real bugs); a fan-out of different lenses is for coverage of whole classes. The two modes and when to use each live in the persona's own skill (see persona-skeptic), not here.

Example shapes already built: persona-skeptic (core) + critic-lens-{code,claims,ux,growth}; persona-research-specialist (core) + research-lens-{stack,market,horizon}. A future persona should follow the same split.

## Standing up a new persona bot

1. **Clone a source profile that already carries the skills the persona needs.**
 `hermes profile create <name> --clone-from <source> --description "<role>"`
 - Copies config.yaml, .env, SOUL.md, and the whole skills/ tree from the source.
 - Deliberately does NOT copy messaging channels: a copied bot token makes two gateways fight over one. Add the persona's own channels later via `hermes -p <name> setup` (or the dashboard Messaging page).
 - Pick the clone source so the skill tree the persona needs arrives in one step; missing skills mean a manual copy afterward.
2. **Replace the cloned SOUL.md with the persona's own SOUL.** Gotcha: write_file refuses to overwrite a file you have not fully read, and a freshly cloned SOUL counts as unread. Either read it in full first, or `rm` the old SOUL.md via terminal, then write the new one fresh.
3. **Verify the persona's skills actually landed** in the new profile's skills/ dir. A clone from a source that predates a skill leaves a silent gap.
4. **Set the profile.yaml `description`** (the kanban orchestrator reads it to understand the role).
5. **API keys:** the new profile has none of its own; it inherits from the shell env when run. For a self-contained bot, run `hermes -p <name> setup` once.
6. **Confirm** with `hermes profile list` (shows model, gateway status, alias).

## Notes

- Alias defaults to the profile name, so a bot is reachable by that name in chat.
- Profiles are per-profile skill trees; a skill added to one profile does not appear in another. When a persona needs a skill another profile already has, copy the skill dir or re-clone.
- Brand casing for the products the personas serve is exact everywhere: AlphaFlux, AlphaVision, AlphaSafe, iTaK, Patriot Pest Control.
