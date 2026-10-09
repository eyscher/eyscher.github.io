"""Rebuild index.html and photos.html at the repo root from the sources in _source/.
Run from anywhere:  python3 _source/build.py
Photos live in img/ (name.jpg = 2000px, name-sm.jpg = 900px); list them in _source/photos.json."""
import json, os, html
SRC = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(SRC)
meta = json.load(open(os.path.join(SRC, "photos.json")))
SEQ = ["bethesda-arcade", "broken-wall", "s-special", "lightning", "pigeon", "brooklyn-bowl", "ruin", "camel-trophy", "elevated",
       "papel-picado", "hibiscus", "jet", "van", "silent", "palms", "bench", "window", "manhattan-bridge", "street-cat", "tulum",
       "roys", "ferry", "pinball", "williamsburg", "water-edge", "skeleton", "palapa", "festival", "food-truck", "correos",
       "sleeping-cat", "foliage", "broken-wall-2", "shade-cat", "beach-sunset", "snow"]
PLACE = {"ny": "New York", "mx": "Mexico", "lv": "Las Vegas", "bw": "New York"}
def tags(m): return "bw" if m["series"] == "bw" else ("digital" if m["medium"] == "Digital" else "color")
FILTERS = [("all", "All"), ("color", "Color film"), ("bw", "Black-and-white film"), ("digital", "Digital")]
by = {m["slug"]: m for m in meta}
missing = [m["slug"] for m in meta if m["slug"] not in SEQ]
order = [by[k] for k in SEQ if k in by] + [by[k] for k in missing]
counts = {"all": len(order)}
for m in order:
    counts[tags(m)] = counts.get(tags(m), 0) + 1
filters = "\n".join(f'        <button type="button" data-f="{k}" aria-pressed="{str(k == "all").lower()}">{label} <small>{counts.get(k, 0)}</small></button>' for k, label in FILTERS if counts.get(k))
figs = []
for m in order:
    w, h = m["w"], m["h"]; sw = 900 if w >= h else round(900 * w / h); sh = round(sw * h / w)
    t = html.escape(m["title"]); place = PLACE[m["series"]]; med = html.escape(m["medium"])
    meta_line = f"{place}, {med}"
    figs.append(f'''        <figure data-tags="{tags(m)}" data-ratio="{w / h:.4f}">
          <button type="button" data-full="img/{m["slug"]}.jpg" data-title="{t}" data-meta="{meta_line}" aria-label="Open {t}">
            <img src="img/{m["slug"]}-sm.jpg" srcset="img/{m["slug"]}-sm.jpg 900w, img/{m["slug"]}.jpg 2000w" sizes="(max-width: 600px) 100vw, 33vw" width="{sw}" height="{sh}" alt="{t}" loading="lazy" decoding="async">
          </button>
          <figcaption><span>{t}</span><span>{meta_line}</span></figcaption>
        </figure>''')
photos = open(os.path.join(SRC, "photos.src.html")).read().replace("<!--FILTERS-->", filters).replace("<!--FIGURES-->", "\n".join(figs))

def full_doc(fragment, desc, url, og_title):
    i = fragment.index("<header")
    head, body = fragment[:i], fragment[i:]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0E151D">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://eyscher.com/og.jpg">
<meta name="twitter:card" content="summary_large_image">
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
'''
index = open(os.path.join(SRC, "index.src.html")).read()
open(os.path.join(REPO, "index.html"), "w").write(full_doc(index,
    "Eitan Y. Scher: psychology researcher and research ethics professional studying how meditation, awe and altered states change the experience of time and self.",
    "https://eyscher.com/", "Eitan Y. Scher"))
open(os.path.join(REPO, "photos.html"), "w").write(full_doc(photos,
    "EYS of the World: photographs by Eitan Y. Scher, mostly on 35 mm film.", "https://eyscher.com/photos", "EYS of the World"))
print("rebuilt index.html and photos.html")
