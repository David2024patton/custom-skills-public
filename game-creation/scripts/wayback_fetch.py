#!/usr/bin/env python3
"""Bulk-download Wayback captures in raw (id_) mode, resumable and polite.

Usage:
  wayback_fetch.py TODO_FILE OUT_DIR [--workers 6] [--timeout 120]

TODO_FILE rows: "<timestamp> <url> [anything...]" (output of wayback_cdx.py).
Files are saved to OUT_DIR/<host>/<path> with query chars replaced by "_";
URLs ending in "/" become index.html. Existing non-empty files are skipped.
Wayback error/placeholder pages are detected and logged to OUT_DIR/failed.txt.
"""
import argparse, concurrent.futures as cf, os, re, subprocess, sys

BAD = re.compile(rb"<title>\s*Wayback Machine\s*</title>|Got an HTTP 30[12] response|This URL has been excluded", re.I)


def local_path(out, url):
    p = re.sub(r"^https?://", "", url).replace(":80/", "/")
    p = re.sub(r"[?&=;]", "_", p)
    if p.endswith("/") or "/" not in p: p = p.rstrip("/") + "/index.html"
    return os.path.join(out, p)


def get(row, out, timeout):
    ts, url = row[0], row[1]
    dst = local_path(out, url)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return "skip", dst
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    src = f"https://web.archive.org/web/{ts}id_/{url}"
    subprocess.run(["curl", "-sL", "--max-time", str(timeout), "--retry", "3", "--retry-delay", "5", "-o", dst, src])
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        return "fail", f"{ts} {url}"
    with open(dst, "rb") as f:
        if BAD.search(f.read(4096)):
            os.remove(dst)
            return "fail", f"{ts} {url}"
    return "ok", dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("todo"); ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()
    rows = [l.split() for l in open(a.todo) if len(l.split()) > 1]
    stats, failed = {"ok": 0, "skip": 0, "fail": 0}, []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, (st, info) in enumerate(ex.map(lambda r: get(r, a.out, a.timeout), rows), 1):
            stats[st] += 1
            if st == "fail": failed.append(info)
            if i % 25 == 0 or i == len(rows):
                print(f"{i}/{len(rows)} {stats}", flush=True)
    if failed:
        open(os.path.join(a.out, "failed.txt"), "w").write("\n".join(failed) + "\n")
        print(f"{len(failed)} failures -> {a.out}/failed.txt (rerun with that file to retry)")


if __name__ == "__main__":
    main()
