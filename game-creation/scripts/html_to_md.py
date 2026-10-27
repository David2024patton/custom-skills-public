#!/usr/bin/env python3
"""Convert downloaded archive HTML pages to clean Markdown for grepping/reading.

Usage: html_to_md.py ROOT_DIR [--min-chars 200]
Writes <file>.md next to every .html/.htm/.php/.shtml/extensionless HTML file.
Strips javascript: links, Wayback toolbar remnants, and empty lines.
Requires: pip install html2text
"""
import argparse, os, re, sys

try:
    import html2text
except ImportError:
    sys.exit("pip install html2text")

SKIP = re.compile(r"\.(md|js|css|json|txt|gif|png|jpe?g|bmp|ico|swf|zip|rar|gz|exe|wav|mp3|mid)$", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--min-chars", type=int, default=200)
    a = ap.parse_args()
    h = html2text.HTML2Text(); h.ignore_images = True; h.body_width = 0
    n = 0
    for dp, _, fs in os.walk(a.root):
        for f in fs:
            p = os.path.join(dp, f)
            if SKIP.search(f):
                continue
            raw = open(p, "rb").read()
            if b"<html" not in raw[:3000].lower() and b"<body" not in raw[:5000].lower(): continue
            txt = h.handle(raw.decode("utf-8", "replace"))
            txt = re.sub(r"\(javascript:[^)]*\)+", "", txt)
            txt = "\n".join(l.rstrip() for l in txt.splitlines() if l.strip())
            if len(txt) < a.min_chars: continue
            open(p + ".md", "w").write(txt + "\n"); n += 1
    print(f"converted {n} pages")


if __name__ == "__main__":
    main()
