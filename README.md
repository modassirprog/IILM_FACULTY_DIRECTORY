# IILM Greater Noida — Faculty Directory

A single-page faculty directory: search, click-to-call phone numbers,
click-to-email addresses, cabin locations where known, and a "report a
location" button that opens a pre-filled Gmail compose window.

## 1. Download the photos (one-time step)

The photos are **not** included in this folder — they need to be pulled
from iilm.edu onto your own machine first, because that site blocks
images from loading when linked to directly from another domain
(hotlink protection).

Run this once, from inside this folder, on a computer with normal
internet access:

```bash
python3 download_images.py
```

This reads `image_manifest.json` (153 photo URLs) and saves each one into
`images/`, using the request headers that get past IILM's hotlink check.
It takes a minute or two. It's safe to re-run — it skips files it already
downloaded, so if a handful fail (dead link, timeout) just run it again.

Anyone whose photo isn't available (couldn't be matched, or failed to
download) automatically gets a colored initial badge instead of a broken
image — the site never shows a broken-image icon.

## 2. Preview it locally

Once the photos are downloaded, just open `index.html` in a browser —
no server or build step needed.

## 3. Deploy to Vercel

```bash
npm i -g vercel      # if you don't have it already
cd faculty-directory
vercel --prod
```

Or: push this folder to a GitHub repo and import it in the Vercel
dashboard as a static site — no framework or build command required.

## Updating the data

All faculty info lives in one place: the `<script id="facultyData"
type="application/json">` block near the bottom of `index.html`. Each
record looks like:

```json
{
  "n": "Himanshu Sharma",
  "s": "Dr.",
  "e": "sharma.himanshu@iilm.edu",
  "p": "9999618675",
  "c": "Cabin 7 PG Ground floor",
  "i": "images/sharma.himanshu.jpg"
}
```

- `c` (cabin) — leave as `""` if unknown; the site will show "No
  location data available" and a "I know this cabin" button that emails
  modassir.25scs1003003175@iilm.edu.
- `i` (image) — a relative path into `images/`. Leave as `""` if there's
  no photo; the site falls back to an initials badge.

To add a new photo: drop the file into `images/` and set `i` to
`"images/<filename>"`.
