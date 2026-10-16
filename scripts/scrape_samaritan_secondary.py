#!/usr/bin/env python3
"""Scrape the secondary Samaritan corpora from samaritan-torah.onrender.com.

Six shelf corpora, fetched unit by unit per their own TOCs:
  tm      Tibåt Mårqe / Memar Marqah          tm_chapter?book=I..VI
  asatir  Sefer HaAsatir                      asatir_chapter?chap=1..16
  tz      Tsedaqah al-Hakim (on Genesis)      tz_chapter?chap=1..50
  shyt    Responsa of Jacob ben Aaron         shyt_chapter?q=1..25
  sir     Sir al-Qulub (Secret of Hearts)     sir_chapter?sec=<toc id>
  bhuq    Commentary on Im Behuqotay          bhuq_chapter?part=1..25

Output per corpus: one JSON file per unit + combined <key>.jsonl, plus a
global manifest.json. Resumable: existing unit files are kept (delete to
re-fetch).
Source is copyright Osher Sassoni — research use only, no republication.
"""
import json, pathlib, time, urllib.request, urllib.parse
from typing import Any

BASE = "https://samaritan-torah.onrender.com/api"
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw" / "corpora" / "samaritan_secondary"
DELAY = 0.15
RETRIES = 4

CORPORA: list[dict[str, Any]] = [
    dict(key="tm", label="Tibat Marqe (Memar Marqah)",
         toc="tm_toc", unit_key="book",
         ep=lambda u: f"tm_chapter?book={urllib.parse.quote(u)}",
         fname=lambda u: f"book_{u}.json"),
    dict(key="asatir", label="Sefer HaAsatir",
         toc="asatir_toc", unit_key="chap",
         ep=lambda u: f"asatir_chapter?chap={u}",
         fname=lambda u: f"ch{u:03d}.json"),
    dict(key="tz", label="Tsedaqah al-Hakim (Genesis commentary)",
         toc="tz_toc", unit_key="chap",
         ep=lambda u: f"tz_chapter?chap={u}",
         fname=lambda u: f"ch{u:03d}.json"),
    dict(key="shyt", label="Responsa of Jacob ben Aaron",
         toc="shyt_toc", unit_key="id",
         ep=lambda u: f"shyt_chapter?q={u}",
         fname=lambda u: f"q{u:03d}.json"),
    dict(key="sir", label="Sir al-Qulub (Secret of Hearts)",
         toc="sir_toc", unit_key="id",
         ep=lambda u: f"sir_chapter?sec={u}",
         fname=lambda u: f"sec{u:03d}.json"),
    dict(key="bhuq", label="Commentary on Im Behuqotay",
         toc="bhuq_toc", unit_key="part",
         ep=lambda u: f"bhuq_chapter?part={u}",
         fname=lambda u: f"part{u:03d}.json"),
]


def api(path):
    url = BASE + "/" + path
    last = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            last = e
            wait = min(60, 5 * (attempt + 1) ** 2)  # Render cold starts
            print(f"  retry {attempt+1} {url} ({e}); sleep {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"GET {url} failed after {RETRIES}: {last}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for spec in CORPORA:
        cdir = OUT / spec["key"]
        cdir.mkdir(exist_ok=True)
        toc = api(spec["toc"])
        time.sleep(DELAY)
        units = [t[spec["unit_key"]] for t in toc]
        titles = {t[spec["unit_key"]]: t.get("title") for t in toc}
        n_sec = 0
        rows = []
        for u in units:
            f = cdir / spec["fname"](u)
            if not f.exists():
                data = api(spec["ep"](u))
                time.sleep(DELAY)
                json.dump(data, open(f, "w"), ensure_ascii=False, indent=1)
            data = json.load(open(f))
            secs = data.get("sections") or []
            n_sec += len(secs)
            for s in secs:
                s["_corpus"] = spec["key"]
                s["_unit"] = str(u)
                rows.append(s)
            manifest.append({"corpus": spec["key"], "file": f"{spec['key']}/{spec['fname'](u)}",
                             "unit": str(u), "n_sections": len(secs),
                             "title": titles.get(u)})
        with open(OUT / f"{spec['key']}.jsonl", "w") as fh:
            for s in rows:
                fh.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(f"{spec['key']} ({spec['label']}): {len(units)} units, {n_sec} sections", flush=True)
    with open(OUT / "manifest.json", "w") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    total_sec = sum(m["n_sections"] for m in manifest)
    print(f"DONE: {len(manifest)} unit files across {len(CORPORA)} corpora, {total_sec} sections")


if __name__ == "__main__":
    main()
