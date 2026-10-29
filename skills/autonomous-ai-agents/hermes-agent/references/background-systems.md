# Durable & Background Systems

Four systems run alongside the main conversation loop. Quick reference
here; full developer notes live in `AGENTS.md`, user-facing docs under
`website/docs/user-guide/features/`.

### Delegation (the delegation tool)

Spawn a subagent with an isolated context + terminal session.

- **Single:** one delegation call carrying a goal and context.
- **Batch:** one delegation call carrying a tasks array (each item a goal plus its context) runs children in
  parallel, capped by `delegation.max_concurrent_children` (default 3).
- **Background:** a delegation call with its background flag set returns a handle
  immediately and keeps the parent loop going; the child's result
  re-enters the conversation as a new turn when it finishes.
- **Roles:** `leaf` (default; cannot re-delegate) vs `orchestrator`
  (can spawn its own workers, bounded by `delegation.max_spawn_depth`).
- **Not durable.** A backgrounded child is still process-local -- if the
  parent process exits, the child is lost. For work that must outlive
  the process, use `cronjob` or
  `terminal(background=True, notify_on_complete=True)`.

**Large fan-outs (10+ subagents).** Dispatch in waves that respect the
concurrency cap, and re-dispatch the remainder as slots free up (results
arrive between turns; act on each and top up). For an "all at once" ask,
parallelize as far as the cap allows rather than silently serializing.

Pitfall: a delegation call whose tasks carry a nested `output_schema`
(or many tasks each bundling large `context` plus a big `output_schema`)
can fail to parse and return `tasks must be a JSON array of task objects`
or `Expecting ',' delimiter`. The fragile element is the nested
`output_schema` itself, not just size: a SINGLE task with an
`output_schema` can fail the same way. The reliable fix is to drop the
`output_schema` argument and inline the output contract as plain text in
the goal/context instead (e.g. "RETURN a JSON object shaped like
{\"findings\":[{...}]}"); the identical task then dispatches cleanly.
Splitting into one call per task is a weaker fallback that does not
always help. When the error appears, do not keep re-sending the identical
payload. Splitting Mode-A runs (N identical reviewers) across separate
calls does not reduce their independence, since each child still runs in
an isolated context.

Config: `delegation.*` in `config.yaml`.

### Cron (scheduled jobs)

Durable scheduler -- `cron/jobs.py` + `cron/scheduler.py`. Drive it via
the `cronjob` tool, the `hermes cron` CLI (`list`, `add`, `edit`,
`pause`, `resume`, `run`, `remove`), or the `/cron` slash command.

- **Schedules:** duration (`"30m"`, `"2h"`), "every" phrase
  (`"every monday 9am"`), 5-field cron (`"0 9 * * *"`), or ISO timestamp.
- **Per-job knobs:** `skills`, `model`/`provider` override, `script`
  (pre-run data collection; `no_agent=True` makes the script the whole
  job), `context_from` (chain job A's output into job B), `workdir`
  (run in a specific dir with its `AGENTS.md` / `CLAUDE.md` loaded),
  multi-platform delivery.
- **Zero-token watchdog:** `no_agent=True` plus a `script` that prints
  ONLY when something needs attention (and prints NOTHING when all is
  well) is a free liveness/heartbeat monitor. The scheduler runs the
  script each tick and delivers stdout verbatim with no LLM: empty stdout
  sends nothing, a non-zero exit sends an error alert. Use it for
  stuck-session checks, overdue-job pings, or any "alert me only if X"
  test. Keep the script silent-on-clean (print nothing, not "all clear")
  or it fires every tick. Exclude the job's own delivery-target session from a
  session monitor's watched set: bot-chat delivery lands in an open session that
  idles back into the flag window, and the watchdog then re-triggers delivery
  into itself forever (a self-wakeup loop). For a monitor that should fire only when the
  CONDITION CHANGES, use the `monitor` change-detector field instead (it
  gates any agent run on output diff, so it costs a turn only on change,
  and is incompatible with `no_agent`).
- **Triage the alert before acting on it.** An idle-session flag is a symptom, not a diagnosis: a worker whose run already finished leaves its session row open, so it reads exactly like a wedged one, and idle time alone cannot separate them. Classify each flag against the run record, which is authoritative over the alert's own text: **noise** (its card is `done`, or its `worker_executions` row in the profile `state.db` reads status `terminal`, meaning the run exited), **parked on the user** (the session's last turn is a question or a request for credentials: report it, leave it alone), **real break** (the run is live or its card is `running` with no recent activity). Only the third is work. Fix noise in the detector, never in the session; never restart the parked one.
- **Prove a change to a monitor's filter with both controls.** Negative control: a genuinely stuck run still alerts through the same code path. Positive control: with the filter disabled, the previous alert output comes back line for line. A filter eyeballed only against today's data can be the change that silences the exact signal the monitor exists to catch.
- **Delivery gotcha:** `deliver='origin'` resolves to the session that
  created the job. If that session is CLI/TUI/stateless-HTTP it has no
  live-delivery channel, so output is recorded but never reaches the
  user. For a real notification set `deliver='all'` (gateway channels
  resolved at fire time) or an explicit gateway-connected platform, and
  confirm the job reports a live target before trusting an alert will
  arrive. Two failure modes to check before trusting any live target:
  (1) `deliver='all'` resolves to NOTHING when no messaging platform is
  connected (read `channel_directory.json` -- if `platforms` is empty,
  `all` cannot deliver). (2) `deliver='bot-chat:<profile>'` fails `not_found` in TWO
  distinct states: the Bot Chat does not exist yet (open it once in the
  Bots tab), or a DEAD row still holds the canonical title (a session with
  `end_reason` like `startup_orphan_reap`, often hidden). Delivery resolves
  the title to a dead tip and refuses forever, so re-opening the chat does
  NOT help: the CLI may just resume the dead row. Diagnose with a
  `sessions WHERE title='Bot Chat'` query on that profile checking
  `end_reason`/`hidden`; free the title by renaming the stale row (set
  title + title_source, mirroring the gateway's own displacement UPDATE)
  and the next delivery mints a fresh, bound `local-...` chat
  automatically. VERIFY delivery by reading the target chat's messages
  table for the actual payload: a status of `queued ... completion
  unverified` is normal and is not proof until the message is in the
  store. Cost model: each bot-chat delivery spends one agent turn in that
  receiving chat; for a watchdog that cost is the feature (the receiving
  bot triages the alert instead of just displaying it, looking up the
  flagged sessions and pulling the related cards), but it makes noisy
  detectors expensive, so keep the script quiet-on-clean. With Hermes
  Mobile connected, chat-message notifications carry bot-chat delivery to
  the user's phone with no messaging platform at all. If every live target
  fails, fall back to `deliver='local'` (saved, not pushed) and tell the
  user a platform (Telegram/Discord) must be connected for real push; do
  not silently leave a job on a dead target.
- **Invariants:** 3-minute hard interrupt per run, `.tick.lock` file
  prevents duplicate ticks across processes, cron sessions pass
  `skip_memory=True` by default, and cron deliveries are framed with a
  header/footer instead of being mirrored into the target gateway
  session (keeps role alternation intact).

User docs: the docs site (see SKILL.md), user-guide/features/cron

### Curator (skill lifecycle)

Background maintenance for agent-created skills. Tracks usage, marks
idle skills stale, archives stale ones, keeps a pre-run tar.gz backup
so nothing is lost.

- **CLI:** `hermes curator <verb>` -- `status`, `usage`, `run`, `pause`,
  `resume`, `pin`, `unpin`, `archive`, `restore`, `list-archived`, `prune`,
  `backup`, `rollback`.
- **Slash:** `/curator <subcommand>` mirrors the CLI.
- **Scope:** only touches skills with `created_by: "agent"` provenance.
  Bundled + hub-installed skills are off-limits. **Never deletes** --
  max destructive action is archive. Pinned skills are exempt from
  every auto-transition and every LLM review pass.
- **Cost:** the deterministic inactivity/prune sweep runs for free. The
  aux-model "consolidate overlapping skills into umbrellas" pass is
  **off by default** -- opt in with `curator.consolidate: true` or
  `hermes curator run --consolidate`. Routine background curation costs
  zero tokens.
- **Telemetry:** sidecar at `~/.hermes/skills/.usage.json` holds
  per-skill `use_count`, `view_count`, `patch_count`,
  `last_activity_at`, `state`, `pinned`.

Config: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`,
`stale_after_days`, `archive_after_days`, `backup.*`).
User docs: the docs site (see SKILL.md), user-guide/features/curator

### Kanban (multi-agent work queue)

Durable SQLite board for multi-profile / multi-worker collaboration.
Users drive it via `hermes kanban <verb>`; dispatcher-spawned workers
see a focused `kanban_*` toolset gated by `HERMES_KANBAN_TASK`, and
orchestrator profiles can opt into the broader `kanban` toolset. Normal
sessions still have zero `kanban_*` schema footprint unless configured.

- **CLI verbs (common):** `init`, `create`, `list` (alias `ls`), `show`,
  `assign`, `link`, `unlink`, `comment`, `complete`, `block`, `unblock`,
  `archive`, `tail`. Less common: `watch`, `stats`, `runs`, `log`,
  `dispatch`, `daemon`, `gc`.
- **Worker/orchestrator toolset:** `kanban_show`, `kanban_complete`,
  `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`,
  `kanban_link`; profiles that explicitly enable the `kanban` toolset
  outside a dispatcher-spawned task also get `kanban_list` and
  `kanban_unblock` for board routing.
- **Dispatcher** runs inside the gateway by default
  (`kanban.dispatch_in_gateway: true`) -- reclaims stale claims,
  promotes ready tasks, atomically claims, spawns assigned profiles.
  Auto-blocks a task after `failure_limit` consecutive spawn failures
  (default 2; configurable via `kanban.failure_limit` or per-task
  `max_retries`).
- **Failure blocks are manual to clear.** A task that exhausts
  `failure_limit` lands in `blocked` and the dispatcher does NOT retry it on
  its own; after fixing the underlying cause (usually the gateway), return it
  with `kanban_unblock` / `hermes kanban unblock <id>`. Where it lands
  depends on its parents: **all parents done -> `ready`, so the
  dispatcher respawns the assignee at once; any parent still open ->
  `todo`, parent-gated, promoted only when that parent completes.** So a
  card you unblock to run AFTER a fix will not start until you have first
  linked the fix card as its parent; unblock it with no unsatisfied
  parent and it starts immediately against unfixed work. The underlying
  cause is almost always infrastructure, not the task body: read
  `last_failure_error` and the run history in `kanban_show` before
  requeuing, and never hand-edit the board SQLite to unblock.
- **Isolation:** board is the hard boundary (workers get
  `HERMES_KANBAN_BOARD` pinned in env); tenant is a soft namespace
  within a board for workspace-path + memory-key isolation.

User docs: the docs site (see SKILL.md), user-guide/features/kanban
