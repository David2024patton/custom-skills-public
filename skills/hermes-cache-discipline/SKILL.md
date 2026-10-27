---
name: hermes-cache-discipline
description: "Use before mid-session edits: preserve the prefix cache."
version: 1.0.0
author: David Patton
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cache, performance, context, compression, skills, memory]
    related_skills: [hermes-agent]
---

# Hermes Cache Discipline

Rules for keeping Hermes prompt-cache hits at 90 percent+. Hermes (the Hermes Agent project by Nous Research) is engineered around a Frozen Prefix Snapshot: SOUL.md, MEMORY.md, USER.md, and AGENTS.md are locked at session start and stay byte-identical, so each turn reuses the previous prefix instead of paying a full prefill. Every rule below protects that invariant. Source references are from this install's Hermes Agent checkout and were verified 2026-10-22.

## When to Use

- Before editing skills, memory, SOUL, AGENTS, config, or plugins mid-session.
- Before adding any proxy, rewriter, or compression layer in front of Hermes.
- When diagnosing poor cache hit rates or expensive prefills.

## Never break the frozen prefix

1. **No external rewording or prompt-compression proxy in front of Hermes.** Anything that rewords or strips tokens mid-message breaks byte-for-byte matching and destroys prefix reuse.
2. **The skills index sits INSIDE the system prompt prefix.** `agent/system_prompt.py:784` says it plainly: an unchanged index stays inside the reused prefix; a changed one re-prefills from there. Therefore: batch skill changes. Stage new SKILL.md files in a scratch folder and install them in ONE operation, instead of one `skill_manage` call per skill (each one re-registers the index and can force a full re-prefill).
3. **Memory writes mid-session shift the injected memory block.** Batch all memory edits into a single `memory` call with an `operations` array at a natural session boundary, never one add per fact across turns.
4. **Never change toolsets or MCP servers mid-session**, and never force a memory reload mid-chat. Disk writes are fine: they take effect next session while the current prefix stays 100 percent cached.
5. **Editing SOUL.md or AGENTS.md on disk mid-session is safe for the CURRENT session** (already frozen in context) but only takes effect at the next session start. Plan changes accordingly: do not expect a soul edit to alter behavior in the running session.
6. **Volatile facts do not belong in frozen files.** CVE numbers, package versions, pricing, and anything that goes stale belong in skills, which load on demand (Level-0 description index at startup, full text via `skill_view` only when triggered). Keep AGENTS.md and SOUL.md lean: they are base footprint paid by every session.

## Compaction status in this build

- Config keys set (2026-10-22): `context.engine: compressor`, `compression.warm_handoff: true`, `compression.progress_notices: true`. NOTE: `compression.warm_handoff` is NOT a recognized key in this checkout (config set warns); it is saved but unread. Do not rely on it as a feature.
- The native compressor already implements warm handoff behavior: `agent/context_compressor.py` splices the `[CONTEXT COMPACTION - REFERENCE ONLY]` summary onto the existing history instead of clearing it, and `tests/agent/test_prompt_cache_prefix_contract.py` contracts that calls reuse the whole previous prefix. So the goal of the warm_compaction plugin is already covered natively here; only install `Elevatormusic/hermes-warm-compaction` if a future regression forces full prefills after compaction.
- Verify after a compaction: `~/.hermes/logs/agent.log` (or the profile's logs dir) should show cached_tokens nearly matching prompt_tokens on the next request.

## Local backends

When routing to local llama.cpp or vLLM (for example the vLLM container on <VLLM_HOST>), the backend must honor the byte-stable prefix: llama-server needs `--cache-reuse`, vLLM needs prefix caching active (`--enable-prefix-caching`, default-on in recent versions; confirm with `docker inspect` args). Without it, Hermes sends a stable prefix and the server throws the KV slot away anyway.

## Pitfalls

- Silently accepting a mid-session skill index notice: count them, they are re-prefill events.
- Putting the latest CVE or library version into a SOUL to keep it handy: it freezes stale data into every future session and bloats the base footprint. It belongs in a skill.
- Chatty one-entry-per-turn memory updates during long sessions: one batched write at the end.
- Consolidating a near-full memory store with several sloppy calls: the `operations` batch is all-or-nothing AND size-checked against the post-batch total, so any over-budget or mismatched op rejects the whole call and nothing applies. Shrink in the same call you add in (remove + rewrite together), and copy every `old_text` verbatim from the injected MEMORY block; one stray character aborts everything. Move the removed detail into a skill and leave a pointer: memory holds who the user is and current state, skills hold how.
