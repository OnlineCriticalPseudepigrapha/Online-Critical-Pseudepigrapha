#!/usr/bin/env python3
"""Write Bensly 5/6 Ezra JSON (from bensly_extract.py) as OCP Grammateus XML: Bensly text + codex C.

Output: raw/editions/bensly_ocr/{5Ezra,6Ezra}.xml (unproofread OCR; move to static/docs after checking).
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

D = Path(__file__).resolve().parent.parent / "raw/editions/bensly_ocr"
BIB = ("R. L. Bensly, The Fourth Book of Ezra: The Latin Version Edited from the MSS, with an introduction "
       "by M. R. James (Texts and Studies 3.2; Cambridge: Cambridge University Press, 1895)")
META = {"5Ezra": ("5 Ezra", "Bensly 1895, cc. I-II (= 4 Esdras 1-2 Vulg.), pp. 1-6"),
        "6Ezra": ("6 Ezra", "Bensly 1895, cc. XV-XVI (= 4 Esdras 15-16 Vulg.), pp. 72-82")}

for name, (title, pages) in META.items():
    vs = json.load(open(D / f"{name}.json", encoding="utf-8"))
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           f'<book title="{title}" language="Latin" filename="{name}">',
           f'  <version title="{title}" language="Latin" author="Anonymous">',
           '    <divisions>', '      <division label="Chapter" delimiter=":"/>', '      <division label="Verse"/>',
           '    </divisions>',
           '    <manuscripts>', '      <ms abbrev="Bensly" language="Latin" show="yes">',
           '        <name>Bensly 1895</name>', f'        <bibliography>{escape(BIB)}, {pages}. '
           'Text from OCR (tesseract), verse division aligned to the Clementine Vulgate; not yet proofread.</bibliography>',
           '      </ms>', '      <ms abbrev="C" language="Latin" show="yes">',
           '        <name>Codex C (Spanish recension)</name>', f'        <bibliography>{escape(BIB)}, Appendix I, '
           'pp. 83-92: text of C (Codex Complutensis) as printed by Bensly; the variants of M are not included. '
           'OCR, verse division from Bensly\'s margin numbers and alignment; not yet proofread.</bibliography>',
           '      </ms>', '    </manuscripts>', '    <text>']
    cv = {(x[0], x[1]): x[2] for x in json.load(open(D / f"{name}_C.json", encoding="utf-8"))}
    ch = None
    for c, v, txt, flags in vs:
        if c != ch:
            if ch is not None: out.append('      </div>')
            out.append(f'      <div number="{c}">'); ch = c
        out += [f'        <div number="{v}">', '          <unit id="1">',
                f'            <reading option="0" mss="Bensly ">{escape(txt)}</reading>',
                *([f'            <reading option="1" mss="C ">{escape(cv[(c, v)])}</reading>'] if cv.get((c, v)) else []),
                '          </unit>', '        </div>']
    out += ['      </div>', '    </text>', '  </version>', '</book>']
    (D / f"{name}.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(name, len(vs), "verses")
