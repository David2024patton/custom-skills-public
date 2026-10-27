#!/usr/bin/env python3
"""RTSP reachability and auth probe. Prints one verdict line, exit code 0/1.

Usage:
  python3 rtsp_probe.py rtsp://host:554/path --user USER --password PASS
  RTSP_PASSWORD=... python3 rtsp_probe.py rtsp://host:554/path --user USER

Verdicts: UNREACHABLE, NO-AUTH-REQUIRED, CREDS-REQUIRED, CREDS-OK,
CREDS-REJECTED, STALLED.

Never prints the password, Authorization header, or credential-embedded URL.
stdlib only; no ffprobe dependency.
"""
import argparse
import base64
import hashlib
import re
import socket
import sys
import uuid
from urllib.parse import unquote, urlsplit

TIMEOUT = 10.0


def md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def recv_response(sock: socket.socket) -> str:
    """Read one RTSP message: headers to CRLF CRLF, then Content-Length body."""
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buf += chunk
    head, sep, body = buf.partition(b"\r\n\r\n")
    if not sep:
        return buf.decode("utf-8", "replace")
    text = head.decode("utf-8", "replace")
    m = re.search(r"Content-Length:\s*(\d+)", text, re.I)
    if m:
        need = int(m.group(1))
        while len(body) < need:
            chunk = sock.recv(4096)
            if not chunk:
                break
            body += chunk
        text += "\r\n\r\n" + body[:need].decode("utf-8", "replace")
    return text


def send_request(sock: socket.socket, method: str, uri: str, cseq: int,
                 extra: dict | None = None) -> str:
    lines = [f"{method} {uri} RTSP/1.0", f"CSeq: {cseq}",
             "User-Agent: rtsp-probe/1.0"]
    for k, v in (extra or {}).items():
        lines.append(f"{k}: {v}")
    raw = "\r\n".join(lines) + "\r\n\r\n"
    sock.sendall(raw.encode("utf-8"))
    return recv_response(sock)


def parse_digest_challenge(resp: str) -> dict | None:
    m = re.search(r'WWW-Authenticate:\s*Digest\s+(.+)', resp, re.I)
    if not m:
        return None
    params = {}
    for km in re.finditer(r'(\w+)=(?:"([^"]*)"|([^,\s]+))', m.group(1)):
        params[km.group(1).lower()] = km.group(2) if km.group(2) is not None else km.group(3)
    return params or None


def has_basic_challenge(resp: str) -> bool:
    return bool(re.search(r"WWW-Authenticate:\s*Basic", resp, re.I))


def digest_header(method: str, uri: str, ch: dict, user: str, pw: str) -> str:
    realm, nonce = ch["realm"], ch["nonce"]
    ha1 = md5(f"{user}:{realm}:{pw}")
    ha2 = md5(f"{method}:{uri}")
    if "qop" in ch and "auth" in ch["qop"].split(","):
        nc, cnonce = "00000001", uuid.uuid4().hex[:16]
        resp_hash = md5(f"{ha1}:{nonce}:{nc}:{cnonce}:auth:{ha2}")
        return (f'Digest username="{user}", realm="{realm}", nonce="{nonce}", '
                f'uri="{uri}", qop=auth, nc={nc}, cnonce="{cnonce}", '
                f'response="{resp_hash}"')
    resp_hash = md5(f"{ha1}:{nonce}:{ha2}")
    return (f'Digest username="{user}", realm="{realm}", nonce="{nonce}", '
            f'uri="{uri}", response="{resp_hash}"')


def status_code(resp: str) -> int | None:
    m = re.match(r"RTSP/\d\.\d\s+(\d{3})", resp)
    return int(m.group(1)) if m else None


def sdp_summary(resp: str) -> str:
    codecs = re.findall(r"a=rtpmap:\d+\s+([\w-]+)", resp)
    if not codecs:
        return ""
    return " codecs=" + ",".join(sorted(set(codecs)))


def fail(verdict: str, detail: str = "") -> int:
    print(f"VERDICT: {verdict}" + (f" ({detail})" if detail else ""))
    return 1 if verdict in ("UNREACHABLE", "CREDS-REJECTED", "STALLED") else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="RTSP reachability and auth probe")
    ap.add_argument("url", help="rtsp://[user:pass@]host[:port]/path[?query]")
    ap.add_argument("--user", default=None)
    ap.add_argument("--password", default=None,
                    help="prefer RTSP_PASSWORD env var over this flag")
    args = ap.parse_args()

    parts = urlsplit(args.url)
    host, port = parts.hostname, parts.port or 554
    uri = parts.path or "/"
    if parts.query:
        uri += "?" + parts.query
    user = args.user or (unquote(parts.username) if parts.username else None)
    pw = args.password or __import__("os").environ.get("RTSP_PASSWORD")
    if pw is None and parts.password:
        pw = unquote(parts.password)

    try:
        sock = socket.create_connection((host, port), TIMEOUT)
        sock.settimeout(TIMEOUT)
    except OSError as e:
        return fail("UNREACHABLE", f"{host}:{port} {e.__class__.__name__}")

    try:
        opts = send_request(sock, "OPTIONS", "*", 1)
        if status_code(opts) is None:
            return fail("STALLED", "no valid RTSP response to OPTIONS")

        cseq = 2
        resp = send_request(sock, "DESCRIBE", uri, cseq,
                            {"Accept": "application/sdp"})
        code = status_code(resp)

        if code == 200:
            print("VERDICT: NO-AUTH-REQUIRED" + sdp_summary(resp))
            return 0
        if code != 401:
            return fail("STALLED", f"DESCRIBE returned {code}")

        ch = parse_digest_challenge(resp)
        if ch is None and not has_basic_challenge(resp):
            return fail("STALLED", "401 with no usable challenge")
        if not user or pw is None:
            scheme = "Digest" if ch else "Basic"
            return fail("CREDS-REQUIRED", f"{scheme} auth demanded, no credentials given")

        cseq += 1
        if ch:
            auth = digest_header("DESCRIBE", uri, ch, user, pw)
        else:
            token = base64.b64encode(f"{user}:{pw}".encode()).decode()
            auth = f"Basic {token}"
        resp2 = send_request(sock, "DESCRIBE", uri, cseq, {
            "Accept": "application/sdp", "Authorization": auth})
        code2 = status_code(resp2)

        if code2 == 200:
            print("VERDICT: CREDS-OK" + sdp_summary(resp2))
            return 0
        if code2 == 401:
            if re.search(r'stale\s*=\s*"?TRUE"?', resp2, re.I):
                return fail("STALLED", "nonce went stale; re-run to retry once")
            return fail("CREDS-REJECTED", "401 on authenticated DESCRIBE")
        return fail("STALLED", f"authenticated DESCRIBE returned {code2}")
    except (socket.timeout, OSError) as e:
        return fail("STALLED", e.__class__.__name__)
    finally:
        sock.close()


if __name__ == "__main__":
    sys.exit(main())
