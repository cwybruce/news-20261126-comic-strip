#!/usr/bin/env python3
"""news-image-20261126: The day in four frames.

This program copies the pre-rendered four-panel comic-strip image for
26 November 2026 to the output directory. The image itself was drawn at
build time by draw_comic.py (Pillow + DejaVu fonts); this file is a
pure-stdlib copier so it runs anywhere, with no fonts, no network and
no third-party packages needed.
"""

import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    if not os.path.isfile(SRC):
        print("error: entry.png not found next to main.py "
              "(expected %s)" % SRC, file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("error: entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        if fh.read(8) != PNG_MAGIC:
            print("error: entry.png is not a valid PNG file", file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != size:
        print("error: copied file size mismatch", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
