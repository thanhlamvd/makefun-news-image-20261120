#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120.

Copies the committed front-page image (entry.png, 1024x1024) into the
output directory as entry.png. Pure Python 3.13 standard library;
no network, no clock, no randomness, so two runs write identical
bytes. The output directory comes from MAKEFUN_OUTPUT_DIR and
defaults to /output.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote %s" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
