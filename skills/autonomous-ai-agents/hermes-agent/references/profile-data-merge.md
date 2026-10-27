# Profile data: locating, merging, and moving it

Use when chats/workspace/notes appear "gone", or the user asks to copy one
profile's data into another. All Hermes data is per-profile; nothing is deleted
by a profile switch, so diagnosis comes before any restore attempt.

## Step 1: Diagnose before restoring

1. Read the active profile: `cat $HERMES_HOME/active_profile` (file at the
   Hermes root, not inside a profile dir), or `hermes profile list` where the
   active profile is marked with the diamond glyph.
2. Count what the user thinks is missing, per profile:
   `sqlite3 "file:<home>/state.db?mode=ro" "select count(*) from sessions"`
   and the same for `messages`. Do the same on the profile they are currently
   in. An empty current profile plus a populated root profile is a profile
   switch, not data loss.
3. Inventory both homes first, so the merge report and backup label are based
   on counts, not impressions.

Per-profile stores (each profile is a full copy of this layout):

| Store | Path under profile home | Merge method |
|---|---|---|
| Sessions + messages + FTS | `state.db` | SQL ATTACH merge (Step 3) |
| Projects / workspaces | `projects.db` | SQL ATTACH merge, per table |
| User + agent memory | `memories/USER.md`, `memories/MEMORY.md` | copy files |
| Request dumps, transcripts | `sessions/` | copy files |
| Kanban board | `kanban.db` | snapshot copy |
| Pasted files, uploads | `attachments/`, `images/`, `pastes/` | copy files |
| Scheduled jobs | `cron/` | do NOT copy (duplicate runs) |
| Session restore receipts | `state_meta` rows `gateway.local_policy.v1:*`, `gateway.local_legacy.v1:*`, `gateway.api.binding.v1.*` | **copy (or re-stamp) — REQUIRED for resume** |
| Plugin consent | `plugins.enabled` / `plugins.disabled` in config | **copy — REQUIRED or every plugin API 404s** |
| Agent scratch, config, identity, skills, secrets | `home/`, `config.yaml`, `SOUL.md`, `skills/`, `.env`, `auth.json` | do NOT copy (but carry `plugins.enabled` across — see above) |

## Step 2: back up the TARGET first

Take snapshots with the SQLite backup API, not a file copy: both databases run
in WAL mode, so a raw `cp state.db` without its `-wal` file is an inconsistent
image. Snapshot `state.db` and `projects.db` of the target profile, and
`shutil.copytree` its `memories/` and `sessions/`, into
`backups/<label>/`. State the backup path in the final report.

## Step 3: merge the databases in one transaction

```python
t = sqlite3.connect(target_state_db, timeout=60)
t.execute("ATTACH DATABASE ? AS src", (source_state_db,))
t.execute("BEGIN IMMEDIATE")
...
t.commit()
```

- **sessions:** build an explicit column list from `PRAGMA table_info` and
  substitute `'orchestrator'` (the target profile name) for `profile_name` in
  the SELECT side, so rows re-homed to the target profile are not stamped with
  the source name.
- **Silent-drop trap:** `INSERT OR IGNORE` will hide rows killed by a unique
  index (Hermes defines `idx_sessions_title_unique` on `sessions.title`).
  Pre-read target titles, compare against source titles, and report collisions
  explicitly. Never let a chat vanish into a changes() count.
- **messages:** primary keys restart at 1 in every database, so offset them:
  `SELECT m.id + (SELECT max(id) FROM messages), ... FROM src.messages m`.
  Check `PRAGMA index_list(messages)` before assuming an auxiliary column such
  as `message_uid` is unique.
- **FTS stays in sync automatically:** the FTS5 tables are external-content
  (`content='messages_...'`) maintained by insert/update/delete triggers, so
  plain INSERTs populate search. Verify after commit:
  `count(messages) == count(messages_fts)`.
- **session_model_usage:** copy rows whose `session_id` is in the migrated set.
  **system_prompts** is keyed by hash: `INSERT OR IGNORE`.
- **Skip gateway runtime state:** `gateway_routing`, `session_turn_leases`,
  `session_admissions`, `runtime_epoch`, `conversation_generations`. Those
  belong to the source profile's running gateways.
- **projects.db:** `INSERT OR IGNORE ... SELECT *` per table; `project_meta` is
  keyed by `key`, so the target's existing value wins by design.

## Step 4: copy the side stores

`copytree` `memories/`, `sessions/`, `attachments/`, `images/`, `pastes/`;
snapshot `kanban.db` with the backup API. Deliberately skip `cron/`,
`config.yaml`, `SOUL.md`, `skills/`, `.env`/`auth.json`, and `home/`, and name
every skipped item in the report so the user can ask for it separately.

## Step 5: verify and report

- `PRAGMA integrity_check` on both merged databases (expect `ok`).
- Spot-read one known row of real content from a migrated session; counts
  alone prove structure, not data.
- Report: per-store before/after counts, what was skipped and why, the backup
  path.
- Writes to a database a running gateway holds open are safe under WAL
  locking, but the desktop app caches its session list: tell the user to
  restart the app to see migrated chats.

## Pitfalls

- **Skipping `state_meta` makes merged chats unresumable.** The session authority only restores a
  cold row through its receipt (`gateway.local_policy.v1:<sid>`), its routing, or an API binding.
  Merged `sessions`/`messages` rows carry none of those, so `session.resume` answers `not_found`
  (4001) while the transcript stays perfectly readable. Symptom: some sessions resume, others
  4001, split by whether the row has a receipt — not by profile or age.
  **Diagnose:** compare `sessions` against `state_meta` per store:
  `select id from sessions where id not in (select substr(key,25) from state_meta where key like 'gateway.local_policy.v1:%')`.
  **Heal without hand-writing receipts:** adopt through the designed path. A row stamped
  `user_id='basic:admin'` is only adoptable by that same principal, so mint a same-user ticket with
  the structured subject and resume once:
  `_session_ticket(home, endpoint, subject='auth:v1:' + json.dumps(["basic","","admin"], separators=(',',':')))`
  then `session.resume` — `adopt_legacy_session` + `commit_local_session` write the receipt and the
  routing identity themselves. Afterwards a plain (no-subject) resume works. Bare labels like
  `admin` are rejected; only the `auth:v1:[provider,issuer,user]` form is nameable. Backup first
  (SQLite backup API — WAL).
- **Skipping `plugins.enabled` breaks every user plugin.** User plugins must be listed there or the
  runtime gate refuses each call with exactly `404 {"detail":"Plugin not found"}` — looks like a
  missing install, but discovery still finds the plugin. Fix with `hermes config set plugins.enabled
  '<json list>'` on the TARGET profile; no restart needed, the config cache re-keys on file change.
- **Leases outlive crashes.** `runtime/active_sessions.json` entries block adoption with
  `runtime_coordination_required` even when the session is not in `session.active_list`. Check
  `updated_at` staleness and the holding pid before assuming the session is live.
- **Check `active_profile` before any restore attempt.** A profile switch
  presents identically to data loss; restoring over the wrong profile writes
  stale data into the live one.
- **Memory tools write only to the running profile.** After a migration, note
  in memory where the data actually lives now, or the next session searches
  the old profile and reports loss again.
- **Copying `cron/` makes every scheduled job fire twice.** Duplicate runs are
  worse than a missing job; leave cron behind and say so.
- **Merge, never overwrite.** The target profile usually holds the current
  session; a wholesale file replacement loses the live conversation.