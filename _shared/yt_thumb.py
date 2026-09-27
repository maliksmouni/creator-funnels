#!/usr/bin/env python3
"""Save the creator's latest YouTube upload thumbnail as the video placeholder.

Usage: python3 _shared/yt_thumb.py <slug> <youtube-handle>
Writes {slug}/assets/video-thumb.jpg and records the video in content.json → video.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def curl(url, out=None):
    cmd = ["curl", "-sfL", "-m", "30", "-A", UA, "-H", "Accept-Language: en", "-b", "CONSENT=YES+1", url]
    if out:
        cmd += ["-o", str(out)]
    return subprocess.run(cmd, check=True, capture_output=True).stdout.decode("utf-8", "replace")


def latest_video(handle):
    page = curl(f"https://www.youtube.com/@{handle.lstrip('@')}/videos")
    data = json.loads(re.search(r"var ytInitialData = (\{.*?\});</script>", page).group(1))
    found = []

    def walk(o):
        if isinstance(o, dict):
            if "lockupViewModel" in o:
                found.append(o["lockupViewModel"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    v = found[0]  # the Videos tab is sorted newest first
    return v["contentId"], v["metadata"]["lockupMetadataViewModel"]["title"]["content"]


def main():
    slug, handle = sys.argv[1], sys.argv[2]
    vid, title = latest_video(handle)
    out = ROOT / slug / "assets" / "video-thumb.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    for size in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            curl(f"https://i.ytimg.com/vi/{vid}/{size}.jpg", out)
            if out.stat().st_size > 5000:
                break
        except subprocess.CalledProcessError:
            continue
    cj = ROOT / slug / "content.json"
    c = json.loads(cj.read_text())
    c["video"] = {"thumb": "assets/video-thumb.jpg", "youtubeId": vid, "title": title}
    cj.write_text(json.dumps(c, ensure_ascii=False, indent=2))
    print(f"latest upload: {vid} · {title} → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
