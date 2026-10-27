# RTSP Digest Auth Handshake

Depth for rung 4 of the ladder. Use `scripts/rtsp_probe.py` first; this
reference covers the protocol when the script's verdict needs explaining or
extending.

## Why a manual handshake

ffprobe's RTSP client can stall mid-negotiation (error -138, `Failed reading
RTSP data`) on servers whose digest handling it dislikes, even when the
server and credentials are fine. A raw socket handshake gives an
unambiguous accept/reject without depending on the client's behavior.

## Sequence

1. Connect TCP to host:port (default 554).
2. `OPTIONS * RTSP/1.0` with `CSeq: 1`. Confirms reachability and lists
   supported methods in `Public:`.
3. `DESCRIBE <uri> RTSP/1.0` with `CSeq: 2`, `Accept: application/sdp`, no
   Authorization header.
4. On `401` with `WWW-Authenticate: Digest realm=..., nonce=...`, compute the
   response and resend DESCRIBE with `Authorization: Digest ...`.
5. Interpret the second response with the verdict table below.

## Digest response computation (RFC 2617)

```
HA1 = MD5(username:realm:password)      # raw password, never URL-encoded
HA2 = MD5("DESCRIBE:<request-uri>")     # request-uri exactly as sent, incl. query
response = MD5(HA1:nonce:HA2)           # when no qop offered
```

When the challenge carries `qop="auth"`, add the qop fields:

```
response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
# nc = "00000001", cnonce = random hex string
```

The `uri` field in the Authorization header must match the request-target
byte for byte, including any `?query=`. A mismatch here produces a clean
401 that looks like a wrong password.

## Verdict table

| Second response | Verdict | Meaning |
|---|---|---|
| 200 + SDP body | CREDS-OK | Auth accepted; stream describable |
| 401, `stale="FALSE"` | CREDS-REJECTED | Hash mismatch: wrong password or username, or uri mismatch |
| 401, `stale="TRUE"` | retry once | Nonce expired; recompute with the fresh nonce from this 401, then stop |
| 401 with only Basic challenge | try Basic once | `Authorization: Basic base64(user:pass)`; if rejected, CREDS-REJECTED |
| timeout / connection drop after Authorization | STALLED | Server hung mid-auth; not a credential verdict, report as stalled |
| connection refused / no route | UNREACHABLE | Network problem, not auth |

## Server quirks worth knowing

- **Basic rejected even when offered**: many cameras advertise Basic but
  enforce Digest only. Try Digest first; fall back to Basic only on a
  Basic-only challenge.
- **Realm looks like a serial number**: realm is server-chosen and often the
  device ID. It is not a password hint.
- **`stale="FALSE"` on the retry is the credential verdict.** It means the
  nonce was valid and the response hash did not match. Do not retry with the
  same credentials; ask the user to confirm them with the device.
- **Lockout risk**: cameras and NVRs commonly lock the account after a
  handful of failed attempts. One or two deliberate attempts, then verdict.

## Redaction

Never print or log the password, the full Authorization header, or a URL
with embedded credentials. Report realm, nonce, and status codes; those are
safe. Credentials go through env vars or the vault, never chat or files.
