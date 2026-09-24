#!/usr/bin/env python3
"""
Downloads every faculty photo referenced in image_manifest.json into ./images/.

Run this once, on a machine with normal internet access:
    python3 download_images.py

It sets a Referer header of https://iilm.edu/ on each request, which is what
lets the download through IILM's hotlink protection (the same protection that
blocks the images from loading when they're linked to directly from another
site, like a Vercel deployment).

Safe to re-run: it skips any file that's already been downloaded, so if a few
images fail (dead link, timeout, etc.) you can just run it again.
"""

import json
import os
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "image_manifest.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://iilm.edu/",
}


def main():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        items = json.load(f)

    os.makedirs(os.path.join(HERE, "images"), exist_ok=True)

    ok, skipped, failed = 0, 0, []

    for i, item in enumerate(items, 1):
        rel_path = item["file"]           # e.g. "images/sharma.himanshu.jpg"
        url = item["url"]
        dest = os.path.join(HERE, rel_path)

        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped += 1
            continue

        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
            with open(dest, "wb") as out:
                out.write(content)
            ok += 1
            print(f"[{i}/{len(items)}] saved  {rel_path}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            failed.append((rel_path, url, str(e)))
            print(f"[{i}/{len(items)}] FAILED {rel_path} — {e}")

        time.sleep(0.15)  # be polite to the server

    print("\n--- Summary ---")
    print(f"Downloaded : {ok}")
    print(f"Already had: {skipped}")
    print(f"Failed     : {len(failed)}")

    if failed:
        print("\nFailed downloads (site will show initials for these instead):")
        for rel_path, url, err in failed:
            print(f"  {rel_path}  <-  {url}  ({err})")


if __name__ == "__main__":
    main()
