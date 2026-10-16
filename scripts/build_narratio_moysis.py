#!/usr/bin/env python3
"""Build Narratio de Moyse et Josue (CAVT 137 / BHG 2277)
Source: A. Vassiliev, Anecdota Graeco-Byzantina (Moscow, 1893), pp. 257-264
(Paris, BnF MS gr. 1611, fols. 31v-33v)
"""
import os, subprocess, re, csv
import pandas as pd
from xml.sax.saxutils import escape

D_IMG = "raw/editions/vassiliev_moyses"
os.environ["TESSDATA_PREFIX"] = os.path.expanduser("~/.local/share/tessdata")

pages_lines = []
for p in range(339, 347):
    png = f"{D_IMG}/p-{p:03d}.png"
    tsv_out = f"/tmp/vass_p{p}"
    if not os.path.exists(f"{tsv_out}.tsv"):
        subprocess.run(["tesseract", png, tsv_out, "-l", "grc", "tsv"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Read words
    df = pd.read_csv(f"{tsv_out}.tsv", sep="\t", quoting=csv.QUOTE_NONE, on_bad_lines="skip")
    lines = df[df["level"] == 4]
    for _, l_row in lines.iterrows():
        b = l_row["block_num"]
        p_num = l_row["par_num"]
        l_num = l_row["line_num"]
        top = l_row["top"]
        
        # Skip header/page number (usually top < 250 in 300 dpi)
        if top < 250:
            continue
        # Skip apparatus/footnotes at bottom if any
        if top > 2150:
            continue
            
        w_df = df[(df["level"] == 5) & (df["block_num"] == b) & (df["par_num"] == p_num) & (df["line_num"] == l_num)]
        txt = " ".join(w_df["text"].dropna().astype(str)).strip()
        
        # On p. 339, CAVT 137 starts at line 17: "Μετὰ δὲ τὸ ἀποθανεῖν..."
        if p == 339 and "Μετὰ δὲ τὸ ἀποθανεῖν" not in txt and not pages_lines:
            continue
            
        # On p. 346, CAVT 137 ends at line 2: "καὶ αὐτὸς μετὰ τῶν λοιπῶν προφητῶν."
        if p == 346 and ("XXI" in txt or "ΧΧΙ" in txt or "ΔΙΗΓΗΣΙΣ" in txt):
            break
            
        if txt:
            pages_lines.append(txt)

full_text = " ".join(pages_lines)
full_text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', full_text)
# clean footnote numbers and brackets
full_text = re.sub(r'\s+[0-9]{1,2}\)', '', full_text)
full_text = re.sub(r'\[\d+\]', '', full_text)
full_text = re.sub(r'\s+', ' ', full_text).strip()

print(f"Narratio de Moyse et Josue words: {len(full_text.split())}")
print("Start:", full_text[:150])
print("End:", full_text[-150:])

# Split into coherent sentence units/verses
tokens = re.split(r'(?<=[.·;:])\s+', full_text)
verses = []
buf = ""
for tok in tokens:
    tok = tok.strip()
    if not tok: continue
    if buf: buf += " " + tok
    else: buf = tok
    if len(buf.split()) >= 6 or tok.endswith(('.', ';', '·')):
        verses.append(buf)
        buf = ""
if buf:
    verses.append(buf)

print(f"Total verses: {len(verses)}")

bib = ("A. Vassiliev, Anecdota Graeco-Byzantina, I (Moscow, 1893), pp. 257-264. "
       "Narratio de Moyse et Josue (BHG 2277), based on Paris, Bibliothèque nationale de France, MS grec 1611, fols. 31v-33v.")

xml_lines = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<!DOCTYPE book SYSTEM "grammateus.dtd">',
    '<book filename="NarrMois" title="Narratio de Moyse et Josue">',
    '  <version author="Vassiliev 1893" language="Greek" title="Greek">',
    '    <divisions>',
    '      <division delimiter="." label="Chapter"/>',
    '      <division label="Verse"/>',
    '    </divisions>',
    '    <manuscripts>',
    '      <ms abbrev="Vass" language="Greek" show="yes">',
    '        <name>Vassiliev 1893 (Anecdota Graeco-Byzantina)</name>',
    f'        <bibliography>{escape(bib)}</bibliography>',
    '      </ms>',
    '    </manuscripts>',
    '    <text>',
    '      <div number="1">'
]

for v_num, v_text in enumerate(verses, 1):
    xml_lines.append(f'        <div number="{v_num}">')
    xml_lines.append(f'          <unit id="{v_num-1}">')
    xml_lines.append(f'            <reading option="0" mss="Vass ">{escape(v_text)}</reading>')
    xml_lines.append('          </unit>')
    xml_lines.append('        </div>')

xml_lines.append('      </div>')
xml_lines.append('    </text>')
xml_lines.append('  </version>')
xml_lines.append('</book>')

out_path = 'static/docs/NarrMois.xml'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines) + '\n')
print(f"Wrote {out_path} with {len(verses)} verses.")
