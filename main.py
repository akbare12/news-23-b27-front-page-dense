#!/usr/bin/env python3
"""news-23 b27 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("main.py: ERROR:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    # Guard: refuse to write inside the repo tree (the grader's /bot is read-only).
    if os.path.commonpath([out_dir_abs, repo_dir]) == repo_dir:
        fail("MAKEFUN_OUTPUT_DIR must be outside the repo directory: %s" % out_dir_abs)
    src = os.path.join(repo_dir, "entry.png")
    if not os.path.isfile(src):
        fail("entry.png not found next to main.py")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over 1 MiB" % len(data))
    # Parse PNG header manually (stdlib struct): signature + IHDR + IEND.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("missing IHDR chunk")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if bit_depth != 8 or color_type not in (2, 6):
        fail("unexpected bit depth %d / colour type %d" % (bit_depth, color_type))
    # IEND trailer: last 12 bytes must be length 0 + 'IEND' + crc.
    # (length field is 4 bytes, then the 4-byte type, then the 4-byte CRC.)
    if len(data) < 12 or struct.unpack(">I", data[-12:-8])[0] != 0 or data[-8:-4] != b"IEND":
        fail("missing or malformed IEND trailer")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    # Re-read output to confirm byte-identical copy.
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output does not match source bytes")
    print("main.py: wrote %s (%d bytes, %dx%d)" % (dst, len(data), width, height))


if __name__ == "__main__":
    main()
