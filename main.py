#!/usr/bin/env python3
"""Copy the entry image to the output directory.

The front page (entry.png, 1024x1024) was drawn during the build; this
program only ships it. Standard library only, so it runs in the
grader's environment. Deterministic: repeated runs write byte-identical
output.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = "entry.png"
OUTPUT = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def check_png(path):
    """Fail unless path is a PNG of the expected size (reads the IHDR)."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR first")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, "
                         f"got {width}x{height}")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    try:
        check_png(src)
    except (OSError, ValueError) as e:
        print(f"entry.png failed checks: {e}", file=sys.stderr)
        sys.exit(1)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, OUTPUT)
    shutil.copyfile(src, dst)
    if sha256_of(src) != sha256_of(dst):
        print("entry.png copy failed verification", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
