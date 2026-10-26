# Troubleshooting

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `python -c "import pm; pm.sync_venv(['stt-whisper'], explicit=True)"` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### Tool not available
1. `hermes tools` - check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` - check config and dependencies
2. `hermes auth` - re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### Page extraction shows a stale page (result caching)
The web search and page extraction tools cache results for 20 minutes (PR #94618): a
repeat fetch of the same URL within the TTL is served from cache, which
can look like "my website changes aren't showing up."

Automatic carveouts (always fetched live, never cached):
- localhost / 127.0.0.1 / `*.local` / `*.localhost` / single-label LAN
  hostnames / private + link-local IP ranges (dev servers, hot-reload
  builds, chat-GUI artifact previews)
- URLs matched by `security.website_blocklist`
- failed responses and keyless-rescue-served responses

Developing a site tested over the PUBLIC internet (Vercel/Netlify
preview, ngrok/cloudflared tunnel, staging domain)? Public DNS isn't
auto-carved-out - list the host in config.yaml:

```yaml
web:
  cache_exempt_hosts:      # always fetched live; effective immediately
    - mysite.vercel.app
    - "*.ngrok-free.app"
    - mysite.dev           # suffix match: also covers preview.mysite.dev
```

Blunt instruments: `web.cache_ttl_minutes: 1` (min) or
`web.cache_enabled: false` disables both caches entirely.

### Skills not showing
1. `hermes skills list` - verify installed
2. `hermes skills config` - check platform enablement
3. Load explicitly: `hermes -s name` (or the skill's own `/<name>` slash command)

### Chats or a workspace "disappeared" (empty session list, missing project)
A profile switch, not data loss. Sessions, projects, skills and memory are
per-profile: the default profile's data lives at the Hermes home root
(`$HERMES_HOME/state.db`, `$HERMES_HOME/projects.db`), while every named
profile keeps its own under `profiles/<name>/` - so the active profile shows
its own empty stores and the other profile's chats vanish from the UI.

1. Read `$HERMES_HOME/active_profile`; `hermes profile list` marks the
   active one with ◆.
2. Prove the data exists before saying anything was lost: open the candidate
   profile's DB read-only and count rows -
   `sqlite3.connect(f"file:{path}?mode=ro", uri=True)`, then `sessions` and
   `messages` in `state.db`, `projects` in `projects.db`. Row counts are the
   receipt; an empty UI is not evidence of deletion.
3. Restore: `hermes profile use <name>`, then restart the desktop app - the
   session list and project switcher read the profile at launch.

Pitfall: never report data loss from an empty workspace - profiles are
isolated by design, so "wrong profile active" is the standing hypothesis
until a read-only count of that profile's own `state.db` disproves it.

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`
- **Gateway logs "skipping unreadable profile.yaml"**: the file holds a multi-line YAML key (the desktop writes wrapped map keys for bot groups); quote the key onto one line, then re-run `hermes gateway list` until the warning clears.

#### Standalone vs multiplexed (plugins 404, profiles "silent")
On current Hermes only ONE host gateway serves every profile; an individual
profile cannot bind its own (the desktop auto-spawning one under a non-default
profile exits `Profile does not get a gateway of its own`). The truth is
`hermes gateway list`: a healthy host shows EVERY profile on ONE PID. If only
one profile is served and the rest read "not running", the gateway is running
STANDALONE, and every desktop plugin 404s, because plugins live under the
default profile a standalone gateway does not serve. Typical trigger: a
`hermes update` wrote new code but did not restart the running gateway (the
log warns of "mixed sys.modules"), or the desktop spawned a gateway under the
wrong profile.

Fix:
```bash
hermes gateway migrate --multiplex --dry-run   # plan + blockers first
hermes gateway migrate --multiplex -y          # converge onto the host gateway
```
Pitfall: `migrate` SIGTERMs the running standalone gateway. If YOUR session
runs through that gateway, do NOT run it synchronously - it kills your own
turn mid-fix. Wait for the gateway to go idle (no active agents/turns), then
migrate, ideally from a background job that polls `live_work()` and fires on
the idle gap. There is no rollback; per-profile gateways are unsupported.

#### Which layer owns a plugin error? (404 vs 502)
`/api/plugins/*` HTTP routes are dispatched by the DESKTOP app, not the
gateway process: curl-ing them against the gateway port returns 404 for
every plugin, healthy ones included, so the gateway is the wrong probe. The
real errors live in `logs/desktop.log`: `502` means the route is mounted
and only its backend or credentials are down, while `Plugin not found`
(or a renderer 404) means the backend was never mounted. Edits to
`desktop-plugins/*/plugin.js` take effect only after a desktop app reload;
restarting the gateway does not pick them up.

#### Unclean death leaves a phantom "running" gateway
When the gateway dies without cleanup, `gateway_state.json` still records
`gateway_state:"running"` with a PID that no longer exists and no listener, so
the desktop reports "Gateway inaccessible" and every profile stalls until a
human intervenes. Diagnosis: the recorded PID is absent from `tasklist`/`ps`
and the `listener_base` port answers nothing.

Durable fix: a health-probe watchdog. The default startup task typically fires
only at logon (no repeat, no restart-on-failure), so it cannot recover a
mid-session death. Register a scheduled task that runs every few minutes,
probes the gateway's `/health` (200 = healthy; note the path is `/health`, not
`/api/health`), and on failure clears the stale `gateway_state.json`, ONLY
when the recorded PID is confirmed dead, then restarts through the registered
startup task. Safety rule: the watchdog must exit silently on a healthy
gateway and never restart one, since that drops in-flight turns (kanban
workers, the current session). A single-instance lock file stops overlapping
ticks from double-restarting. Probe every local port you depend on in the
same task (the gateway `/health` and the dashboard port), restarting each
through its own registered startup mechanism; on this host that ships as
`gateway-service/Hermes_Gateway_Watchdog.ps1` on a 5-minute schedule.

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, line endings): see `references/windows-quirks.md`.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

### "Reset permissions" / auto-approving everything
See `references/security-privacy.md` - wipe the "Always allow" stores, don't touch yolo mode.

