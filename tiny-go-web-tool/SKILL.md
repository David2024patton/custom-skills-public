# tiny-go-web-tool (David's pattern)

The proven recipe for small, single-purpose websites and tools for David,
distilled from building upload.itak.live (the universal photo drop) on
2026-10-19. One job, one small Go program, his server, his colors.

## When this fits

- David wants a little site of his own: upload page, drop page, form,
  viewer, mini dashboard, status page.
- The job is ONE job. If it grows past a few routes, it stops being this
  pattern and becomes a real project.
- The reference implementation is the repo David2024patton/sf-upload.

## Stack law

- Go standard library ONLY. No web framework, no npm, no build step for
  the page. Hand-written HTML and CSS in the Go source.
- Why: nothing sits between the user's tap and the response. David
  noticed the App/Website toggle answered instantly and asked if it was
  Flutter; it is the opposite, plain code is why there is zero delay.
- One Go module, a couple of files at most (main.go, auth.go).
- Gates before any deploy: gofmt clean, go vet clean, go build clean.

## Page design law (David's, do not improvise)

- Mobile first: single column, max width about 560px, generous margins.
- Every step has its label ABOVE its control, on the left. Never put the
  step wording inside the button or bubble itself.
- Two-way choices use a segmented pill control (two halves, selected one
  filled). This is his standing UI standard, not decoration.
- Selects start on a placeholder ("Pick a project"), never pre-picked.
  The primary action stays disabled until the choices are real.
- Primary action button sticks to the bottom of the screen.
- Theme: black background (#060606), panels #141414, borders #333,
  accent Army red #c8102e. His favorite colors are black and red; he
  likes military and Army themes.
- Readability is law: labels bright near-white (#f0f0f0), 15px, weight
  600. Inputs 16px (prevents phone zoom), padding about 11px. No giant
  buttons, no washed-out gray text. He reads these on a phone, outside,
  at work.
- Title in spaced capitals for a light stencil feel.

## Auth pattern

- The bare domain is the front door. Root serves the code page.
- Login is a short code David picks (env PIN). Never invent one for him.
- Correct code issues an HMAC-signed cookie (key = the server token).
  The session is a sliding INACTIVITY timeout: every authenticated
  request re-issues the cookie with a fresh expiry. SESSION_MINUTES env,
  default 120 (2 hours, his choice).
- Throttle failed codes: 10 per IP per 10 minutes, then 429. A short
  code without throttling is an invitation.
- Cookie Path is "/" when the app serves at the root.
- An unguessable token path (/u/<token>) may stay as a second door to
  the same app; the session cookie is site-wide so both doors share it.
- FAIL CLOSED: no TOKEN or no PIN in env, the server refuses to start.
- Constant-time compares for token and code.
- Secrets live in the Dokploy env and a local ACCESS.md (chmod 600) in
  the project folder. Never in the repo, never printed in logs or chat.

## File intake pattern (when the tool collects files)

- Storage root from env DATA_DIR. Layout: <project>/<type>/<section>/.
- Multipart limits as named constants (reference: 30 MB per file,
  600 MB per request, MaxBytesReader on the body).
- Accept by extension allowlist AND content sniffing; HEIC/HEIF are
  exempt from sniffing (DetectContentType cannot read them).
- Saved names are timestamp-prefixed and sanitized; a note field is
  saved as a timestamped .txt sidecar next to the files.
- Reply with small JSON (saved count + names). Log one line per upload.

## Deploy recipe (Dokploy, <DOKPLOY_HOST>)

CLI: python3 ~/workspace/skills/dokploy/bin/dokploy.py -host
<DOKPLOY_HOST> <cmd> (deploys, lists, logs). Creates and updates go
through its call() helper; paths passed to call() are relative to /api
(call prepends it; passing "/api/..." double-prefixes and 404s).

Order that works:
1. Private GitHub repo with the Go source, go.mod, Dockerfile.
   DOCKERFILE GOTCHA: `COPY *.go ./`, never `COPY main.go`, or the
   second file breaks the build with undefined symbols.
2. DNS first (Hostinger CLI): A record to <HOME_PUBLIC_IP>, ttl 300.
   CLI needs PYTHONPATH=/opt/hatch/skills/skill-creator/bin. Verify by
   reading the zone back through the API call(); CLI print output
   truncates and cannot be trusted for verification.
3. Create the host data dir BEFORE the mount matters:
   ssh -F ~/.ssh/ts/config ts-server, use a path the server user owns
   (e.g. /home/server/<tool>). /mnt/alphaflux-data denied writes.
4. application.create {projectId, environmentId, name}. It silently
   DROPS source and build fields; always follow with
   application.update carrying the full github source config, then read
   the app back with application.one (query params go in params, not
   body) before believing anything.
5. Mounts are NOT set by update. POST /mounts.create with
   {serviceId: <appId>, serviceType: "application", type: "bind",
   hostPath, mountPath: "/data"}. Verify on the app record.
6. application.saveEnvironment requires buildArgs, buildSecrets and
   createEnvFile copied from the existing app record. Env: TOKEN, PIN,
   SESSION_MINUTES, DATA_DIR=/data, PORT=8080.
7. domain.create {host, applicationId, domainType: "application",
   certificateType: "letsencrypt", https: true, port: 8080}.
8. Deploy with app-deploy and CONFIRM a new deployment record with the
   new commit title reaches "done". Pushes do not reliably auto-deploy.
   Env-only changes may need app-stop then app-start to take effect.
9. Verify the SERVED thing, never the deployment status (checklist
   below). Deployment "done" has lied before.

## Retrieval pattern (how Lulu gets what the tool collects)

- Files land on the host disk via the bind mount. His home computer is
  never in the path.
- Mirror them to Lulu with a silent 15-minute cron running:
  rsync -rtz --no-owner --no-group --no-perms -e "ssh -F
  /home/hatch/.ssh/ts/config" ts-server:/home/server/<tool>/
  ~/workspace/user/inbox/
  The ownership flags matter: plain -a fails as non-root with chown
  errors (exit 23) even though files copy.
- Cron stays silent on success; failures surface in run history only.

## Verification checklist (run every leg, live, before saying done)

1. GET /healthz returns ok.
2. Root with no session shows the code page; bad token path 404s.
3. Upload with no session returns 401.
4. Wrong code is rejected; right code returns 303 and sets the cookie.
5. Upload with the session succeeds; the file is ON THE HOST DISK under
   the bind dir (ssh and look), not just in an API response.
6. Grep the served HTML for the new markers (a label, a CSS color) to
   prove the new build is what is being served.
7. Slide test: session expiry moves forward after an authenticated
   request (the inactivity promise actually working).

## Traps burned into this skill (all hit on 2026-10-19)

- /tmp is wiped on VM restarts. A missing test file looks exactly like
  a server bug (curl status 000). Regenerate fixtures, then judge.
- A deployment can finish "done" while the OLD container still serves.
  Stop/start or it never picks up env or mounts.
- The first version's Dockerfile copied only main.go; adding auth.go
  failed the whole build. COPY *.go from day one.
- Do not persist the access token anywhere but ACCESS.md and the
  Dokploy env. Rotating it means updating both, plus David's bookmark.
