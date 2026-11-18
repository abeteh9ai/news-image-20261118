#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261118 bounty.

Writes one image to the output directory: entry.png, a one-page newspaper
summarising the world news of Wednesday, 18 November 2026.

How the image is made (honest method): the image is drawn in advance by
render.py (same repository) with Pillow and DejaVu fonts, and stored in this
repository as entry.png. This program copies those exact bytes to the output
directory. Copying is deterministic by construction: two runs write identical
bytes, and no network, clock, or randomness is involved.

The image itself is original work: a front-page layout (masthead, lead story,
four story cells, bottom strip, sources footer) with six verified stories
from 18 November 2026, drawn with simple flat icons. It is not a screenshot
of any news site and uses no media logos.
"""

import os
import shutil
import sys

# Image rendered by render.py in this repository (1024x1024 PNG).
# sha256: 6bf8fe4a9ecdc853cb6e0795617b3295e37f2834eccb1b926052ba1a9870cc2d
SOURCE_NAME = "entry.png"
TARGET_NAME = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print(f"missing bundled image: {source}", file=sys.stderr)
        sys.exit(1)
    target = os.path.join(out_dir, TARGET_NAME)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")


if __name__ == "__main__":
    main()
