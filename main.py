#!/usr/bin/env python3
"""news-image-20261118 entrypoint (Python 3.13, standard library only).

The entry image is rendered ahead of time by draw_news.py and stored in
this repository as entry.png. This program copies it to the output
directory the grader provides, so every run is deterministic and instant:
the same bytes land in /output/entry.png on every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
