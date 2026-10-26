#!/usr/bin/env python3
"""Build a labeled contact sheet of every image in a recovered skin/image pack.

Usage: contact_sheet.py IMAGE_DIR OUT.png [--cell 96] [--cols 14]
Handles gif/png/jpg/bmp (first frame of animations). Requires Pillow.
Use it to view an entire pack in one image instead of opening files one by one.
"""
import argparse, os
from PIL import Image, ImageDraw

EXT = (".gif", ".png", ".jpg", ".jpeg", ".bmp")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("out")
    ap.add_argument("--cell", type=int, default=96); ap.add_argument("--cols", type=int, default=14)
    a = ap.parse_args()
    paths = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(a.dir) for f in fs if f.lower().endswith(EXT))
    if not paths: raise SystemExit("no images found")
    c, lab = a.cell, 14
    rows = (len(paths) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * c, rows * (c + lab)), (24, 28, 36))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(paths):
        x, y = (i % a.cols) * c, (i // a.cols) * (c + lab)
        try:
            im = Image.open(p); im.seek(0); im = im.convert("RGBA"); im.thumbnail((c - 4, c - 4))
            sheet.paste(im, (x + (c - im.width) // 2, y + (c - im.height) // 2), im)
        except Exception:
            d.text((x + 4, y + 40), "ERR", fill=(255, 80, 80))
        d.text((x + 2, y + c), os.path.basename(p)[:15], fill=(170, 190, 210))
    sheet.save(a.out)
    print(f"{len(paths)} images -> {a.out} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
