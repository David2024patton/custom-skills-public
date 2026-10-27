#!/usr/bin/env python3
"""Discover every archived URL for one or more domains via the Wayback CDX API.

Writes a todo list (timestamp url mimetype length) usable by wayback_fetch.py.

Usage:
  wayback_cdx.py OUT_DIR domain1 [domain2 ...] [--only REGEX] [--exclude REGEX]
                 [--max-bytes N] [--from YYYY] [--to YYYY]

Examples:
  wayback_cdx.py work/cdx tdzk.com www.tdzk.com --only '\\.(js|zip|rar|txt)$|topic=|help'
  wayback_cdx.py work/cdx lemmy.redial.net --exclude 'phpbb|simcity|\\.(jpg|png)$'

Outputs:
  OUT_DIR/cdx_<domain>.txt   raw CDX rows (one capture per unique URL, newest kept)
  OUT_DIR/todo.txt           filtered rows across all domains
  Prints a summary by file extension so you can refine filters before fetching.
"""
import argparse, collections, os, re, sys, time, urllib.parse, urllib.request

API = "https://web.archive.org/cdx/search/cdx"


def cdx(domain, frm=None, to=None, retries=4):
    q = {"url": f"{domain}/*", "output": "txt", "fl": "timestamp,original,mimetype,length,statuscode",
         "filter": "statuscode:200", "collapse": "urlkey"}
    if frm: q["from"] = frm
    if to: q["to"] = to
    url = API + "?" + urllib.parse.urlencode(q)
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=240) as r:
                return r.read().decode("utf-8", "replace").splitlines()
        except Exception as e:  # CDX is slow and rate-limits; back off
            print(f"[{domain}] attempt {i+1} failed: {e}", file=sys.stderr)
            time.sleep(10 * (i + 1))
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("domains", nargs="+")
    ap.add_argument("--only")
    ap.add_argument("--exclude")
    ap.add_argument("--max-bytes", type=int, default=20_000_000)
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--to")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    only = re.compile(a.only, re.I) if a.only else None
    excl = re.compile(a.exclude, re.I) if a.exclude else None
    todo, exts = [], collections.Counter()
    for d in a.domains:
        rows = cdx(d, a.frm, a.to)
        open(os.path.join(a.out, f"cdx_{d}.txt"), "w").write("\n".join(rows) + "\n")
        print(f"{d}: {len(rows)} unique URLs")
        for line in rows:
            p = line.split()
            if len(p) < 4: continue
            ts, url, mime, ln = p[0], p[1], p[2], p[3]
            if only and not only.search(url): continue
            if excl and excl.search(url): continue
            if ln.isdigit() and int(ln) > a.max_bytes: continue
            todo.append(f"{ts} {url} {mime} {ln}")
            ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or "(none)"
            exts[ext] += 1
    open(os.path.join(a.out, "todo.txt"), "w").write("\n".join(todo) + "\n")
    print(f"todo.txt: {len(todo)} rows")
    for e, n in exts.most_common(25): print(f"  {e:10} {n}")


if __name__ == "__main__":
    main()
