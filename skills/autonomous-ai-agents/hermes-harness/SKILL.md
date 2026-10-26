---
name: hermes-harness
description: "Use when building or wiring Hermes profiles, bots, skills."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [hermes, profiles, bots, skills, soul, agents, plugins, harness]
 related_skills: [hermes-agent, hermes-agent-skill-authoring, persona-skeptic, qa-loop]
---

# Hermes Harness: Profiles, Bots, Skills, Context, Plugins

## When to Use

When creating or wiring anything in the Hermes runtime itself: a new persona profile, a bot roster entry, a SOUL or AGENTS file, a skill, or a plugin. This is the anatomy reference with the official doc links and worked examples, so you build against the real primitive instead of guessing.

Primary docs: https://hermes-agent.nousresearch.com/docs (index: /docs/llms.txt). This skill summarizes and links; the docs win on any detail that changes.

## The core primitive: a Profile is everything

A profile is a separate Hermes home directory with its OWN config.yaml, .env, SOUL.md, memories, sessions, skills, cron jobs, and state database. A persona IS a profile. There is no separate "bot" object: a Bot (Bot Mode) is just a profile with a UI over it.

Key rule: NEVER point two live agents at the same profile. Both auto-write memory and load each other's writes, so two writers on one home corrupt each other's state. Agents that need shared memory use an external memory provider instead.

Doc: https://hermes-agent.nousresearch.com/docs/user-guide/profiles

### Example: create a persona profile

```bash
# Fresh specialist with a role description the kanban orchestrator can route to
hermes profile create uispecialist --description "UI/UX specialist. Owns design and the visual check."

# Clone an existing one (config, .env, SOUL.md, skills, memory) then edit its SOUL
hermes profile create ideator --clone-from orchestrator

# Its own command exists immediately:
uispecialist chat
hermes -p uispecialist chat -q "hello"
```

Each profile lives at ~/.hermes/profiles/<name>/ (on this machine: C:/Users/David/AppData/Local/hermes/profiles/<name>/).



## Bot Mode: the roster where bots message each other

Bot Mode turns profiles into a roster of named Bots, each with its own chat, role, model, memory, skills, and avatar. It is built into the desktop app, on by default, as the Bots tab.

What it enables (this is the collaboration layer):
- Each Bot has a canonical persistent Bot Chat.
- Bots run recurring routines (cron jobs, shown as `hermes cron list`, jobs named `[bot:<name>]`).
- Bots deliberate together in GROUP CHATS and MESSAGE EACH OTHER directly. This is the native way one persona asks another for help, no custom wiring needed.
- Create a Bot in seconds: Name, Title, Description. Advanced lets you clone from a profile, pin a model, set a custom SOUL.md, and toggle per-skill / per-toolset / per-MCP enablement.

Doc: https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode

### Example: two bots collaborating

Put the skeptic and the builder in a group chat, or have the researcher @mention the ideator. Because each Bot is a profile, `hermes -p skeptic chat` and the Bot roster are the same agent. Routines and group membership persist.

## Context files: SOUL vs AGENTS

Two different jobs. Do not mix them.

| File | Job | Where it loads from |
|---|---|---|
| SOUL.md | The agent IDENTITY: personality, mission, standing instructions. Global to the instance. | HERMES_HOME/SOUL.md only |
| AGENTS.md | PROJECT instructions: structure, conventions, architecture. | Discovered from CWD/git root |
| .hermes.md / HERMES.md | Project instructions, highest priority | Walks to git root |
| AGENTS.override.md | Personal per-directory override of AGENTS.md (gitignored) | CWD + subdirs |
| CLAUDE.md | Claude Code context (also detected) | CWD + subdirs |
| .cursorrules, .cursor/rules/*.mdc | Cursor conventions | CWD only |

Priority: only ONE project context loads per session (.hermes.md -> AGENTS.override.md -> AGENTS.md -> CLAUDE.md -> .cursorrules). SOUL.md ALWAYS loads separately as identity slot #1.

AGENTS.md chains git-root -> working dir; deeper files load later and win. Keep SOUL.md free of volatile facts (no versions, prices, CVEs) because it is a frozen prefix file loaded every session; put those in skills.

Doc: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

## Skills: on-demand knowledge with examples

Skills live in ~/.hermes/skills/, use progressive disclosure (short SKILL.md loads first, linked files load on demand), and follow the agentskills.io open standard.

EVERY skill we author MUST carry worked examples (David's standing rule). A skill with no example is not done. The example section shows a real invocation and its real output, so the next agent copies a proven pattern instead of guessing.

Skill authoring rules that matter:
- description is under 60 chars, trigger-first, ends with a period (the index truncates at 57 chars).
- Frontmatter: name, description, version, author, license, platforms, metadata.hermes.{tags, related_skills}.
- Include a When to Use section near the top, and an Examples section with real invocations.
- ASCII only, zero em dashes in anything we ship.

Pitfall (skill resolution): the loader resolves skills BY NAME within a profile. If one skill name exists in TWO directories under a profile's skills/ (a clone put it in a category subdir, a later sync wrote a top-level copy), the loader may pick either and the stale copy shadows the current one. After cloning a profile or syncing skills into it, verify each skill name maps to exactly ONE file before trusting the agent loads the up-to-date version. Verification and repair rules:

- Check FLEET-WIDE, not just the profile you touched: a template clone replicates the same duplication into every profile it spawns, so one bad template means the same duplicated names in 20+ profiles.
- When the copies DIFFER, keep the NEWER by mtime and remove the stale stray. This resolves both directions correctly: clones carry old category copies (older mtime), while later syncs write fresh top-level copies (newer mtime). Byte-identical duplicates are harmless housekeeping, not urgent.
- A NESTED duplicate (skills/mojo/mojo/SKILL.md beside skills/mojo/SKILL.md) is UNLOADABLE: the loader only looks at <skillsdir>/<name>/SKILL.md, so the nested copy is invisible even when it is the newer file. Move the newer content UP to the loadable path first, then delete the nested dir, or the newer version is lost.
- Automate the check: this skill ships `scripts/fleet-heartbeat.py`, which walks every profile and reports waiting sessions (open, quiet 2-12h), missing/truncated SOUL.md, differing duplicate skills GROUPED by root cause (same name + same byte pattern collapses to one line instead of one line per profile), and overdue cron jobs. Wire it as a no_agent hourly cron (watchdog pattern: see the Cron section of the hermes-agent skill's background-systems reference): print only when something is wrong, empty stdout when the fleet is healthy.
- Pitfall (watchdog crying wolf): a kanban worker's `sessions` row stays OPEN with `ended_at` NULL after its run exits, so idle time alone flags every FINISHED job as stuck, every hour, forever. Filter on `worker_executions.status='terminal'` read across every profile's state.db: terminal means the run exited, skip it. A session with no worker row at all is an interactive thread (the user's own) and must still be reported, and an unrecognized status must never silence a session or a live stall is lost. The 2-12h window is deliberate: anything quiet longer reads as parked, so work that must stay visible belongs on a kanban card, not in a session.
- Keep both copies in sync: the script exists twice, here under `scripts/` and live under `profiles/<owner>/scripts/` where the cron job points. Patch both in the same pass, or the skill documents behavior the running watchdog does not have.

Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
Authoring companion: skill hermes-agent-skill-authoring.

### Example: minimal skill skeleton

```markdown
---
name: my-skill
description: "Use when <trigger>. <value>." # under 60 chars
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [tag1, tag2]
 related_skills: [other-skill]
---

## When to Use
<when this loads>

## Examples
$ real-command --flag
real output proving it worked
```

## Plugins: custom tools without touching core

A plugin is a directory in ~/.hermes/plugins/ with plugin.yaml + __init__.py (register()) + schemas.py (tool schemas the LLM sees) + tools.py (handlers that run).

Doc: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins

### Example: minimal plugin (registers a tool + a hook)

~/.hermes/plugins/hello-world/plugin.yaml:
```yaml
name: hello-world
version: "1.0"
description: A minimal example plugin
```

~/.hermes/plugins/hello-world/__init__.py:
```python
import json
def register(ctx):
 schema = {"name": "hello_world", "description": "Greets a name.",
 "parameters": {"type": "object",
 "properties": {"name": {"type": "string"}},
 "required": ["name"]}}
 def handle(params, **kw):
 return json.dumps({"greeting": "Hello, %s!" % params.get("name", "World")})
 ctx.register_tool(name="hello_world", toolset="hello_world", schema=schema, handler=handle)
 ctx.register_hook("post_tool_call", lambda tn, p, r: print("[hello]", tn))
```

Restart Hermes and the model can call hello_world immediately.

## The collaboration rule (ask each other, or research online)

When any persona or skill is unsure, it does NOT stall or guess. Two exits, in order:
1. **Ask a peer.** The named peer is a Bot/profile: mention it in a group chat, or route a question via kanban (`hermes kanban create`), or spawn it. The researcher asks the ideator; the skeptic asks the security auditor.
2. **Research it live.** If no peer knows, run a live search (deep-research / SearXNG at https://search.itak.live/ first, then web tools) and cite the source. Never answer a factual question from memory when a lookup is one call away.

This is native: Bots message each other (Bot Mode), and every profile has the search tools. The rule just makes it a habit instead of an accident.

## Portable package: rebuild this setup elsewhere

When David wants the Hermes setup reproducible in another harness (the harness) or a fresh install, ship it as one self-contained package directory:

1. `skills/` - copy the profile's whole skills tree wholesale (it is the working set; do not curate by hand).
2. `personas/<name>/SOUL.md` - one dir per profile; SOUL is the identity, nothing else is needed to recreate a persona.
3. `scripts/` + `knowledge/` - QA packs and per-language digests, staged at a workspace path.
4. `QA-LOOP.md` (build law) + `IDEA.md` at the package root.
5. `HANDOFF.md` - the portable writeup: phases, persona roster, critic method (Mode A/B/C, checklist, fix loop), context management (domain fan-out), and a mapping to the target harness's phase model.
6. `MANIFEST.md` - inventory with real counts and per-part source paths (generate from the filesystem, never by hand - counts drift).
7. `bootstrap.sh` - copies skills into a target hermes_home, stages the workspace, and PRINTS the follow-up commands a script cannot safely run (profile creation, credential entry, verification runs). Never moves credentials.

Verification before trusting the package: run one critic on a real file and one script pack against known buggy code; both must reproduce/behave as documented, or the package is not honest yet.

The package drifts the moment the live fleet changes: regenerate it in the same pass as any fleet fix, and fingerprint-compare a sample of live vs packaged files before trusting it (a package built before a later fix re-seeds the exact bug it was meant to end). Export cron jobs and monitor scripts as part of the package with their recreation among the printed follow-ups, and have MANIFEST name what is NOT automated, so rebuild gaps are visible instead of discovered.

## Quick reference (CLI)

```bash
hermes profile create <name> [--clone-from <src>] --description "<role>"
hermes profile list / show <name> / describe <name>
hermes -p <name> chat -q "..." # run a profile headless
hermes cron list # bot routines
hermes skills opt-out / opt-in --sync # bundled-skill seeding
```

## Source

- Profiles: https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- Bot Mode: https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
- Context Files: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- Skills System: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Docs index: https://hermes-agent.nousresearch.com/docs/llms.txt
