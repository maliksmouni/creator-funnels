#!/usr/bin/env python3
"""Assemble the public site for Cloudflare Pages into dist/.

Usage: python3 _shared/publish.py   (Cloudflare build command; output directory: dist)

Only an allowlist is copied, so internal files never reach the host:
- site root: 404.html, _headers (noindex for every page), assets/ (fonts, case-study screenshots)
- each creator with status "live": everything except PRIVATE_PER_CREATOR (dossier, content.json, notes)
Draft creators, HOUSE.md, CLAUDE.md, _shared/, .claude/ and the Netlify _redirects stay out.
"""
import json
import shutil
from pathlib import Path

from build import PRIVATE_PER_CREATOR, ROOT

DIST = ROOT / "dist"
ROOT_FILES = ["404.html", "_headers"]
ROOT_DIRS = ["assets"]


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    for f in ROOT_FILES:
        shutil.copy2(ROOT / f, DIST / f)
    for d in ROOT_DIRS:
        shutil.copytree(ROOT / d, DIST / d)
    for cj in sorted(ROOT.glob("*/content.json")):
        src = cj.parent
        status = json.loads(cj.read_text()).get("status")
        if status != "live":
            print(f"skip {src.name} ({status})")
            continue
        shutil.copytree(src, DIST / src.name, ignore=shutil.ignore_patterns(*PRIVATE_PER_CREATOR, ".*"))
        print(f"copy {src.name}")
    print(f"wrote {DIST.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
