# Conversation store map (Windows, layout as of 2026-10)

Paths drift between app updates; confirm each root with a quick grep before trusting it. Universal discovery pattern: `timeout 300 grep -rIl -m1 -i <keyword> <root>` with output appended to a scratch file, run in the background for big trees. Classify hits into: chats (primary evidence), plan/research files (secondary evidence), file-edit snapshots (context), credentials (skip; never read or quote).

## Muse / mimocode
- Native store: `%USERPROFILE%\.local\share\mimocode` (subdirs: builtin_skills, compose, log, memory, sessions, storage, tool-output; plus mimocode.db).
- Verbatim user text hides inside `log/*` files: `service=llm` ERROR lines dump the full LLM request body, which embeds David's typed messages verbatim. Each dump is a snapshot, so any date derived from it is an upper bound ("on or before").
- `memory/projects/global/MEMORY.md` holds structured dated decisions when present.
- The main chat export is a per-conversation download from the app UI (can be GBs; zip via Drive when it exceeds chat upload limits). Text format: `[YYYY-MM-DD HH:MM:SS] You:` / `Muse AI:`.

## Buzz (relay platform)
- Workspace: `%USERPROFILE%\.buzz` with PLANS/, RESEARCH/, WORK_LOGS/, OUTBOX/, GUIDES/, REPOS/, archive/, thread_latest.txt.
- Content is plan markdown and work logs; many statements carry dates only in file mtimes (label as file dates).
- `archive/archive.db` is end-to-end encrypted: content fields are ciphertext, unreadable without the key. Name it, give its date window, request the key.

## Cursor / VS Code / VS Code family
- Chat databases: `%APPDATA%\<Editor>\User\workspaceStorage\<hash>\state.vscdb`; read `<hash>\workspace.json` in the same dir to name the project folder. A sweep of all workspace.json files tells which folders even belong to the project.
- Open read-only via Python stdlib sqlite3 (no sqlite3 binary needed): `sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)`; fall back to `mode=ro` if immutable is rejected. Never open for write.
- Chat-bearing keys by editor: Cursor `aiService.prompts` (user prompt list) and `composer.composerData`; Augment `memento/webviewView.augment-chat` (double-encoded JSON: webviewState string, then conversations chatHistory request_message; history-summary items are AI-side); Copilot stores input history only, no transcripts.
- Filter `ItemTable` rows by decoded value containing the keyword; cap extracted output per DB (tens of KB) so a large store cannot flood the reader.
- Assistant replies are almost never stored in these DBs; absence of AI text is normal, not a failed extraction.

## Continue
- `%USERPROFILE%\.continue\dev_data\<version>\chatInteraction.jsonl` and `toolUsage.jsonl`: one JSON object per line; per-project noise unless the keyword appears in the text field.

## Antigravity
- `%APPDATA%\Antigravity`: `User\History` (file-edit snapshots) and `app_storage.json` (workspace/project lists); chat transcripts do not live in state.vscdb form here.

## Hermes
- Own past sessions: use session_search directly; no manual store reads needed for Hermes conversations.

## New tools added later
- Sweep `%APPDATA%`, `%LOCALAPPDATA%`, `%USERPROFILE%\.local\share`, and dot-directories in the home dir for the keyword, then classify hits with the categories above before reading deeply.
