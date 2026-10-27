---
name: rtsp-diagnostics
description: "Use when probing or troubleshooting an RTSP camera stream."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [RTSP, Cameras, Diagnostics, Networking, Auth]
    related_skills: [systematic-debugging]
---

# RTSP Stream Diagnostics

## When to Use

- The user posts an `rtsp://` URL and asks to view, verify, or check it.
- A camera/NVR stream needs diagnosis: unreachable, auth failure, or ffprobe
  error.
- Credentials were supplied for a stream and a trustworthy accept/reject
  verdict is needed.

## The ladder

Work down this ladder and report the highest rung reached. Never call a
stream viewable without parsed stream metadata (ffprobe JSON) or a frame you
actually captured.

1. Tooling check
2. Reachability and method list
3. Handshake probe
4. Credential verdict
5. Read the stream

## 1. Tooling check

`which ffprobe`. Windows Hermes builds ship ffmpeg/ffprobe in the tools dir.
If absent, steps 2 and 4 still work: the manual probe is stdlib-only.

## 2. Reachability and method list

`nc` is frequently missing on Windows, so probe the port with Python or bash
`/dev/tcp`:

```bash
python3 -c "import socket,sys;s=socket.socket();s.settimeout(5);s.connect((sys.argv[1],int(sys.argv[2])));print('open')" host 554
```

Then ask the server what it speaks:

```bash
curl -sv --max-time 10 "rtsp://host:554/" 2>&1 | grep -iE "public:|rtsp/|failed|refused"
```

A `Public:` line listing DESCRIBE, SETUP, and PLAY means a live RTSP server.

**Pitfall:** curl sends only `OPTIONS` to rtsp:// URLs regardless of the
method you request (`-X DESCRIBE` still goes out as OPTIONS), so a curl
success proves reachability and nothing about whether the stream can be
described or played. Use curl for rung 2 only; ffprobe or the manual probe
own everything below it.

## 3. Handshake probe

```bash
ffprobe -v debug -rtsp_transport tcp -timeout 5000000 -i "rtsp://host:554/path" 2>&1 | tail -30
```

Read the actual RTSP status line in the trace:

- `200 OK` with SDP: jump to rung 5.
- `401` plus `WWW-Authenticate: Digest realm=..., nonce=...`: credentials
  required. Capture realm and nonce, go to rung 4.
- `401` plus `WWW-Authenticate: Basic`: server wants Basic. Percent-encode the
  password, embed `rtsp://user:pass@host:554/path`, retry once.
- Connection refused or connect timeout: network problem. Report that and stop.
- `Failed reading RTSP data` (ffmpeg error -138): the handshake stalled
  mid-exchange. This is not proof the stream is down; isolate with the manual
  probe before reporting anything about the stream's health.

**Pitfall:** `-v debug` prints the full input URL including the password.
Redact credentials before any trace output leaves the terminal: replies,
files, tickets, logs.

## 4. Credentials

Embed them for ffprobe as `rtsp://user:pass@host:554/path?query`.
Percent-encode reserved characters (`@`, `:`, `%`) in the password when
embedding, then percent-decode before hashing; digest auth always uses the
raw password.

When credentials are embedded but ffprobe stalls or returns -138 while the
no-credential run showed a clean 401, suspect the client's digest
negotiation rather than the password. Get a verdict you can trust from the
manual probe:

```bash
python3 scripts/rtsp_probe.py "rtsp://host:554/path?query" --user admin --password "$RTSP_PASSWORD"
```

The env var keeps the secret out of shell history. The script prints one
verdict: `NO-AUTH-REQUIRED`, `CREDS-OK`, `CREDS-REQUIRED`,
`CREDS-REJECTED`, `STALLED`, or `UNREACHABLE`, plus an SDP summary when it
gets one. Protocol details and the verdict table:
`references/digest-auth.md`.

**Pitfall:** never retry-hammer a device that rejects auth. Cameras and NVRs
commonly lock the account after a handful of failures, so make one or two
deliberate attempts, take the verdict, and stop.

## 5. Read the stream

Only after rung 4 returns CREDS-OK (or NO-AUTH-REQUIRED):

```bash
ffprobe -v quiet -print_format json -show_streams -show_format "rtsp://user:pass@host:554/path"
```

Report codec, resolution, and frame rate from that JSON. Capture a frame to
eyeball:

```bash
ffmpeg -rtsp_transport tcp -i "$URL" -frames:v 1 -y frame.jpg
```

Prefer `-rtsp_transport tcp` while diagnosing: UDP media ports are commonly
dropped by NAT and firewalls, which reads like a dead stream. If TCP
handshakes but delivers no data, retry with `-rtsp_transport udp` before
concluding the stream is dead.

## Verdict reporting

State reachability, auth scheme, credential verdict, and stream metadata when
obtained. If credentials were rejected, name the rung that failed and ask the
user to confirm the password with the device or its app. Do not guess
variants.
