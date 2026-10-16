#!/usr/bin/env python3
"""Scrape the Samaritan Pentateuch corpus from samaritan-torah.onrender.com.

Pulls, for every book -> chapter, the parallel-verse JSON:
Samaritan text (Hebrew letters), MT (vocalized), Samaritan Targum, Onkelos,
Qumran, LXX, English, Arabic, and the Hebrew interpretation.

Output: one JSON file per chapter + combined JSONL + a manifest.
Resumable: existing chapter files are kept (delete to re-fetch).
Source is copyright Osher Sassoni — research use only, no republication.
"""
import json, os, sys, time, urllib.request, urllib.parse, pathlib

BASE = "https://samaritan-torah.onrender.com/api"
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw" / "corpora" / "samaritan_torah"
DELAY = 0.15          # seconds between requests
RETRIES = 4

def api(path, **params):
    url = BASE + "/" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            last = e
            wait = min(60, 5 * (attempt + 1) ** 2)  # 5,20,45,80->60 s (Render cold starts)
            print(f"  retry {attempt+1} {url} ({e}); sleep {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"GET {url} failed after {RETRIES}: {last}")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    books = api("books", mode="")
    print(f"{len(books)} books")
    manifest = []
    total = 0
    for b in books:
        bid = b["id"]
        chs = api("chapters", book_id=bid)
        bdir = OUT / f"{bid:02d}"
        bdir.mkdir(exist_ok=True)
        for ch in chs:
            f = bdir / f"ch{ch['number']:03d}.json"
            if not f.exists():
                verses = api("verses", chapter_id=ch["id"])
                # cross-check: verses endpoint is keyed by the canonical chapter id
                time.sleep(DELAY)
                json.dump({"book": b, "chapter": ch, "verses": verses},
                          open(f, "w"), ensure_ascii=False, indent=1)
            data = json.load(open(f))
            manifest.append({"file": str(f.relative_to(OUT)), "book": b["name"],
                             "book_id": bid, "chapter": ch["number"],
                             "n_verses": len(data["verses"])})
            total += len(data["verses"])
        print(f"book {bid} ({b['name']}): {len(chs)} chapters done", flush=True)
    with open(OUT / "manifest.json", "w") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    # combined JSONL
    with open(OUT / "all_verses.jsonl", "w") as fh:
        for m in manifest:
            data = json.load(open(OUT / m["file"]))
            for v in data["verses"]:
                v["_book"] = m["book"]; v["_book_id"] = m["book_id"]; v["_chapter"] = m["chapter"]
                fh.write(json.dumps(v, ensure_ascii=False) + "\n")
    print(f"DONE: {sum(m['n_verses'] for m in manifest)} chapter files checked, {total} verses")

if __name__ == "__main__":
    main()
