#!/usr/bin/env python3
import subprocess, re, os, csv
import pandas as pd

D_IMG = "raw/editions/tischendorf_esdrae"
os.environ["TESSDATA_PREFIX"] = os.path.expanduser("~/.local/share/tessdata")

pages_text = {}
for p in range(97, 107):
    png = f"{D_IMG}/p-{p:03d}.png"
    tsv_out = f"/tmp/esdrae_p{p}"
    if not os.path.exists(f"{tsv_out}.tsv"):
        subprocess.run(["tesseract", png, tsv_out, "-l", "grc", "tsv"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    df = pd.read_csv(f"{tsv_out}.tsv", sep="\t", quoting=csv.QUOTE_NONE, on_bad_lines="skip")
    
    body_lines = []
    app_lines = []
    
    lines = df[df["level"] == 4]
    for _, l_row in lines.iterrows():
        b = l_row["block_num"]
        p_num = l_row["par_num"]
        l_num = l_row["line_num"]
        words_df = df[(df["level"] == 5) & (df["block_num"] == b) & (df["par_num"] == p_num) & (df["line_num"] == l_num)]
        line_text = " ".join(words_df["text"].dropna().astype(str))
        top = l_row["top"]
        
        # skip running head
        if top < 350 or ("APOCALYPSIS" in line_text or "ESDRAE" in line_text or "ΕΒΡΒΛΕ" in line_text):
            continue
            
        # check if apparatus
        if re.search(r"^\d+\s+(cod|codex|pro|ita|supplevimus|priores|sequitur|om\.|add\.|in\s+codice)", line_text) or \
           re.search(r"\b(codex|supplevimus|ante|post|pro|ita prorsus)\b", line_text):
            app_lines.append((top, line_text))
        else:
            if app_lines and top > app_lines[0][0]:
                app_lines.append((top, line_text))
            else:
                body_lines.append((top, line_text))
                
    pages_text[p - 73] = {
        "body": [t for _, t in body_lines],
        "apparatus": [t for _, t in app_lines]
    }

for p_no in sorted(pages_text.keys()):
    print(f"=== Page {p_no} (Body: {len(pages_text[p_no]['body'])} lines, App: {len(pages_text[p_no]['apparatus'])} lines) ===")
    print("\n".join(pages_text[p_no]["body"][:2]))
