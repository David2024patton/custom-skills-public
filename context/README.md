# Context loading

How to keep the agent's context small and correct while working across languages and domains.

## Load, do not list

- Each language has a curated digest in `knowledge/<lang>/`. Load only the language you are
  currently writing. You never need every language digest at once.
- The per-language skills (`golang`, `rust`, `mojo`, `flutter`, ...) are the source of truth with
  examples. The load command in each skill's header is the load button.
- Loading a skill adds its SKILL.md + frontmatter to context. Reference files are read only when
  asked (`skill_view(name, file_path=...)`). Cheap: read index → read one file.

## Domain fan-out (`skills/domain-fanout`)

When a prompt spans more than one domain/language/framework:

1. Extract the dominant domain prompt from context.
2. Spawn a FRESH agent per domain (context=that prompt). Each does digest → full → compact.
3. Return only a one-line status up; findings already in each child's task file.
4. Orchestrator aggregates compact task-file summaries.

Cost: the main context sees only statuses and one-line digests, not each domain's full content.

Hermes constraint: subagents cannot spawn children or message peers directly. The orchestrator
stays the hub; multi-agent "agent-to-agent chat" is the Hermes **Bot Mode** roster path (peer
messaging between profiles). Use fan-out for per-domain extraction, Bot Mode for true collaboration.

## When to reload a skill

Reload when: (a) context was compressed and the skill shows `[SKILL_PRUNED]`, (b) code review /
validation gate needs it (e.g. `requesting-code-review`), (c) the task switches language/domain
(a new language has its own skill to load). Stale list ≠ fresh instructions: reload first, then act.
