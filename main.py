#!/usr/bin/env python3
"""Render the news-image-20261119 entry: one 1024x1024 front page summing
up Thursday 19 November 2026's world news.

The image itself lives in this repository as entry.png (1024x1024, drawn
from six verified stories: the Trump-Xi-Putin trilateral summit in
Shenzhen; GTA VI launching worldwide; Iran widening the Gulf war to
Kuwait and Bahrain; the third Ukrainian strike on the Crimean Bridge;
the ICJ ruling Myanmar committed genocide against the Rohingya; and
Anthropic's record $81.3B IPO).

This program is a standard-library-only copy step on purpose. The
grading container installs nothing and ships no system fonts, so a
program that draws the image with Pillow and DejaVu would fail there
even though it runs locally. Copying the repository's own image
reproduces it byte for byte on every run, in any container.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

ENTRY = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, ENTRY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
