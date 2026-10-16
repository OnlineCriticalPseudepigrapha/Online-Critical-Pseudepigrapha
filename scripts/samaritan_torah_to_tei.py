#!/usr/bin/env python3
"""Convert the scraped Samaritan Torah corpus (all_verses.jsonl) to one TEI P5 file.

Output stays in gitignored raw/ (copyright Osher Sassoni, research use only).
Usage: python3 scripts/samaritan_torah_to_tei.py
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path(__file__).resolve().parent.parent / "raw/corpora/samaritan_torah"
OUT = SRC / "samaritan_torah_TEI.xml"

BOOKS = {1: ("Gen", "Genesis"), 2: ("Exod", "Exodus"), 3: ("Lev", "Leviticus"),
         4: ("Num", "Numbers"), 5: ("Deut", "Deuteronomy")}

# field -> (witness id, xml:lang, label)
WITNESSES = [
    ("text", "SP", "hbo-Samr", "Samaritan Pentateuch"),
    ("masoretic_text", "MT", "hbo", "Masoretic Text"),
    ("sam_aramaic", "SamTg", "sam", "Samaritan Targum"),
    ("onkelos_text", "TgOnq", "arc", "Targum Onqelos"),
    ("qumran_text", "DSS", "hbo", "Qumran witness"),
    ("lxx_text", "LXX", "grc", "Septuagint"),
    ("english", "EN", "en", "English translation (site)"),
    ("arabic_trans", "AR", "ar", "Arabic translation (site)"),
]


def e(s):
    return escape(str(s).strip(), {'"': "&quot;"})


def main():
    verses = [json.loads(l) for l in (SRC / "all_verses.jsonl").open(encoding="utf-8")]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="en">',
           '<teiHeader><fileDesc>',
           '<titleStmt><title>The Samaritan Torah: parallel corpus</title></titleStmt>',
           '<publicationStmt><p>Unpublished research copy. Source copyright Osher Sassoni '
           '(samaritan-torah.onrender.com); research use only, no republication.</p></publicationStmt>',
           '<sourceDesc><p>Scraped 2026-10-15 via scripts/scrape_samaritan_torah.py; '
           'see raw/corpora/samaritan_torah/VERIFICATION.md.</p>',
           '<listWit>']
    out += [f'<witness xml:id="{w}">{lab}</witness>' for _, w, _, lab in WITNESSES]
    out += ['<witness xml:id="Comm">Samaritan Hebrew commentary (site)</witness>',
            '</listWit></sourceDesc></fileDesc></teiHeader>', '<text><body>']

    book = chap = None
    for v in verses:
        bid, c = v["_book_id"], v["_chapter"]
        if bid != book:
            if chap is not None:
                out.append('</div></div>')
            book, chap = bid, None
            abbr, name = BOOKS[bid]
            out.append(f'<div type="book" n="{abbr}" xml:id="{abbr}"><head>{name}</head>')
        if c != chap:
            if chap is not None:
                out.append('</div>')
            chap = c
            out.append(f'<div type="chapter" n="{c}" xml:id="{BOOKS[bid][0]}.{c}">')
        n = v.get("number") or v.get("verse")
        vid = f"{BOOKS[bid][0]}.{c}.{n}"
        out.append(f'<ab type="verse" n="{n}" xml:id="{vid}">')
        for field, w, lang, _ in WITNESSES:
            if v.get(field):
                extra = f' source="{e(v["qumran_scroll"])}"' if w == "DSS" and v.get("qumran_scroll") else ""
                out.append(f'<seg type="witness" corresp="#{w}" xml:lang="{lang}"{extra}>{e(v[field])}</seg>')
        if v.get("interpretation"):
            out.append(f'<note type="commentary" corresp="#Comm" xml:lang="he">{e(v["interpretation"])}</note>')
        out.append('</ab>')
    out.append('</div></div></body></text></TEI>')
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(verses)} verses -> {OUT}")


if __name__ == "__main__":
    main()
