# Desktop Projects (named workspaces)

Projects group desktop chats into named workspaces. State is per-profile in
`$HERMES_HOME/projects.db`:

- `projects` — id, slug, name, `primary_path`
- `project_folders` — the folders a project claims (a project can span many)
- `project_meta` — key/value; `active_id` holds the app-level active project

When the UI and the tools disagree about what is active, read `project_meta.active_id`
in that DB before theorising.

## Two entry points

- **`desktop_project` tool** (actions: create / switch / list) — the agent-side
  handle the desktop surface exposes. `create` accepts an optional `path` anchor;
  `switch` claims the calling chat for a project; `list` reports which project the
  calling chat is in.
- **`hermes project` CLI** — full management: `create`, `list`, `show`,
  `add-folder`, `remove-folder`, `rename`, `set-primary`, `use`, `archive`,
  `restore`, `bind-board`. Anything beyond create/switch/list lives here.

## Procedure: create a workspace the user can actually use

1. Create the project AND anchor a folder in the same pass. If the user names a
   destination, pass it as `path` on `desktop_project create`; if not, pick a
   sensible default folder, create it on disk, then attach it:
   `hermes project add-folder <slug> <path>` and
   `hermes project set-primary <slug> <path>`.
2. Move the chat: `desktop_project switch <name-or-slug>`.
3. Verify before reporting done: `desktop_project list` must show `active_id`
   set to the project and that project `active: true`;
   `hermes project list` marks the active project with `*`.

## Pitfalls

- **A project with zero folders cannot claim a chat.** `desktop_project switch`
  returns success and sets the app-level active id, yet every chat stays in
  Default and `list` shows `active_id: null`. The desktop only groups a chat into
  a project that claims at least one anchored folder. Always attach a folder
  before switching, even when the user never mentions a path.
- **A success return from `switch` is not proof.** The user reads the sidebar;
  you don't. Verify with `list` (active_id) every time. When the user reports the
  UI still shows Default after a "successful" switch, suspect a missing folder
  binding first, not a stale UI.
- **`desktop_project` cannot manage folders.** Add/remove folders, set the
  primary path, archive, and kanban binding are CLI-only. Check
  `hermes project --help` rather than assuming the tool covers it.
- **Repointing a project's folders unbinds chats already in it.** Changing the
  primary path or swapping the folder list drops the binding: `list` reverts to
  `active_id: null` and the chat falls back to Default. Re-run
  `desktop_project switch` and re-verify after any `add-folder`,
  `remove-folder`, or `set-primary` change.
- **Path convention:** on this user's machine project files stay off the system
  drive entirely. He reinstalls Windows periodically for a clean slate, so C:
  must never hold anything durable: anchor project folders to the G: drive
  (business work under `G:\Business`). Losing C: must never lose project data.
  Never anchor a project inside `$HERMES_HOME` or a profile dir unless asked.