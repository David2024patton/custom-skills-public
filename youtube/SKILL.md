---
name: "youtube"
description: "Use Youtube when the user asks for Youtube or this provider's API."
---

# Youtube

## Purpose
Use Youtube with the user-connected `custom.youtube` credential.

## Tooling
CLI: `~/workspace/skills/youtube/bin/youtube.py`. It imports
`/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py` and attaches the
stored key as the `key` query parameter via `url_with_surrogate_query_param`.
Only `www.googleapis.com` and `youtube.googleapis.com` are called.

- `youtube.py channel --id UC...` / `--username NAME`: public channel stats.
- `youtube.py search -q "..." [--max N] [--type video|channel|playlist]`.
- `youtube.py videos --ids VID1,VID2`: video details, up to 50 ids.
- `youtube.py uploads --playlist-id PL...`: latest videos from an uploads list.
- `youtube.py comments --video-id VID`: top-level comment threads.

Verified 2026-09-22: key works. The YouTube Data API v3 was enabled on the key's Cloud project (n8n1) and added to the key's allowed APIs. David's channel: "David Patton" (@david-patton), id UCMw9-yVB5Ag8SNV5k6gYb-A, 198000 subscribers.

## Auth
The credential is already stored; nothing here collects one. Never ask the user to paste a raw key in chat, set a secret environment variable, pass a secret flag, or write an auth file.

A 401 or 403 is a question about the request before it is a question about the key. Check that the credential was attached at all: a request built without the helpers named under Tooling carries nothing, and that looks exactly like a wrong or under-scoped token. Only once a request that did carry the credential is still rejected, call `credentials.request_api_access` with `reconnect` to replace it. The connector is stored as `custom.youtube`.

## Operating Rules
1. Use this skill when the user asks for Youtube or this provider's API.
2. Restrict authenticated requests to: www.googleapis.com, youtube.googleapis.com.
3. Do not print, log, or persist raw credentials.
4. If auth is missing or rejected, follow the Auth section rather than asking for a key.
