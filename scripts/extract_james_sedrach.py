#!/usr/bin/env python3
import subprocess, re, os, csv
import pandas as pd

D_IMG = "raw/editions/james_sedrach"
os.environ["TESSDATA_PREFIX"] = os.path.expanduser("~/.local/share/tessdata")

pages_text = {}
for p in range(148, 156):
    png = f"{D_IMG}/p-{p:03d}.png"
    tsv_out = f"/tmp/sedrach_p{p}"
    if not os.path.exists(f"{tsv_out}.tsv"):
        subprocess.run(["tesseract", png, tsv_out, "-l", "grc", "tsv"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    df = pd.read_csv(f"{tsv_out}.tsv", sep="\t", quoting=csv.QUOTE_NONE, on_bad_lines="skip")
    
    body_lines = []
    lines = df[df["level"] == 4]
    for _, l_row in lines.iterrows():
        b = l_row["block_num"]
        p_num = l_row["par_num"]
        l_num = l_row["line_num"]
        words_df = df[(df["level"] == 5) & (df["block_num"] == b) & (df["par_num"] == p_num) & (df["line_num"] == l_num)]
        line_text = " ".join(words_df["text"].dropna().astype(str))
        top = l_row["top"]
        
        # skip running head
        if top < 350 or ("APOCALYPSIS" in line_text and "SEDRACH" in line_text and top < 500):
            continue
        # skip footnote at bottom of page
        if top > 2100:
            continue
        # filter out marginal line numbers (e.g., isolated '5', '10', '15', '20', '25', '30', '35' at right edge)
        # James puts line numbers at the end of every 5th line
        clean_line = re.sub(r'\s+\b(5|10|15|20|25|30|35)\b\s*$', '', line_text).strip()
        if clean_line:
            body_lines.append((top, clean_line))
            
    pages_text[p - 18] = { # printed page = PDF page - 18 (148 -> 130)
        "body": [t for _, t in body_lines]
    }

for p_no in sorted(pages_text.keys()):
    print(f"=== Page {p_no} ({len(pages_text[p_no]['body'])} lines) ===")
    print("\n".join(pages_text[p_no]["body"][:3]))
