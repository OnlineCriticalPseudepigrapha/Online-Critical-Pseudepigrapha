#!/usr/bin/env python3
"""Parse the OCR'd Haelewyck CAVT (raw/cavt/cavt.md) into raw/cavt/cavt_entries.csv.

Titles come from the Synopsis materiae (table of contents, PDF pp. 12-21), matched by
entry number. Body pages are assigned to entries by the running head, which carries
the entry number and the printed page (PDF page = printed page + 27). Each entry's
pages are then scanned for Inedita, languages and translations.
Output stays in gitignored raw/cavt/ (Brepols copyright).
"""
import csv
import difflib
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "raw/cavt"
OFFSET = 27            # PDF page = printed page + 27
BODY = range(28, 247)  # PDF pages of entries 1-277 (Concordantia starts after)
N_ENTRIES = 277
OCR_DIGITS = str.maketrans("$SIlO", "55110")

LANGS = {"graece": "Greek", "latine": "Latin", "syriace": "Syriac", "aethiopice": "Ethiopic",
         "armeniace": "Armenian", "georgice": "Georgian", "slauice": "Slavonic", "coptice": "Coptic",
         "sahidice": "Coptic", "bohairice": "Coptic", "arabice": "Arabic", "aramaice": "Aramaic",
         "hebraice": "Hebrew", "persice": "Persian", "mandaice": "Mandaic", "hibernice": "Irish",
         "samaritane": "Samaritan", "karshunice": "Garshuni"}
TITLE_FIXES = [("Adac", "Adae"), ("Euac", "Euae"), ("gracce", "graece"), ("gracca", "graeca"),
               ("gracc", "graec"), ("Daniclis", "Danielis"), ("Macchab", "Maccab"), ("armeniacc", "armeniace"), (" ct ", " et ")]


# title words that name a language without the -e adverb
TITLE_LANG = [(r"\bNHC\b|copt|sahid", "Coptic"), (r"slau", "Slavonic"), (r"syria", "Syriac"),
              (r"graec", "Greek"), (r"latin", "Latin"), (r"aethiop", "Ethiopic"), (r"armen", "Armenian"),
              (r"arab", "Arabic"), (r"persic", "Persian"), (r"hebrai", "Hebrew"), (r"aramai", "Aramaic"),
              (r"georgi", "Georgian"), (r"mandae", "Mandaic")]


def title_language(t):
    found = [lang for pat, lang in TITLE_LANG if re.search(pat, t, re.I)]
    return "; ".join(dict.fromkeys(found))


def main_language(text):
    """Most frequent language adverb in the entry's text."""
    counts = {}
    for k, v in LANGS.items():
        counts[v] = counts.get(v, 0) + len(re.findall(rf"\b{k}\b", text, re.I))
    best = max(counts.items(), key=lambda kv: kv[1])
    return best[0] if best[1] else ""


SKIP_PARA = re.compile(r"^\W*(C[f£]\.?|Notae?|Codd?\.|Translatio|Concordantia|Vide|Inedit|Bibliographia)", re.I)


def editions(text, title):
    """Edition paragraphs (not Cf./Nota/Cod./Translatio...) and the years they cite."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    keep = [p for p in paras[1:] if not SKIP_PARA.match(p) and not p.startswith(title[:15])
            and not re.match(r"^\W*\d{1,3}\s+[A-Z -]{8,}", p)]  # running heads
    years = sorted({int(y) for p in keep for y in re.findall(r"\b(1[5-9]\d\d)\b", p) if int(y) <= 1998})
    return keep, years


# section headings as printed (two-line headings lose their first line in the OCR)
SECTION_NAMES = {
    "ENOSH, HENOCH, LAMECH, NOE, SEM, CHAM": "POSTERI ADAE ET EVAE: ENOSH, HENOCH, LAMECH, NOE, SEM, CHAM",
    "ESDRAS - ESTHER - TOBIT - LV MACCABAEORUM": "ESDRAS - ESTHER - TOBIT - I-V MACCABAEORUM",
    "EZECHIEL": "XII PROPHETAE - ISAIAS - JEREMIAS - BARUCH - EZECHIEL",
    "I-IISAMUEL -I-HREGES - I-IIPARALIPOMENA": "I-II SAMUEL - I-II REGES - I-II PARALIPOMENA",
    "SAPIENTIA — SIRACIDES - PSALMI SALOMONIS": "PSALMI - ODAE SALOMONIS - PROVERBIA - JOB - SAPIENTIA - SIRACIDES - PSALMI SALOMONIS",
    "JOSUE-JUDICES": "JOSUE - JUDICES", "ABRAHAM-ISAAC-JACOB": "ABRAHAM - ISAAC - JACOB",
}

# hand corrections of OCR-garbled TOC titles, checked against the body headings
TITLE_CORRECTIONS = {
    2: "Vita Adae", 12: "Apocalypsis Adae (NHC V,5) (sahidice)",
    13: "Historia seditionis Satanae (fragmentum copticum)",
    18: "Historia paenitentiae Adae et Euae (armeniace)", 22: "Adam. Fragmentum II (armeniace)",
    23: "Adam. Fragmentum III (armeniace)", 35: "Chronologia ab Adamo usque ad Salomonem (armeniace)",
    53: "Liber apocryphus nomine Seth. Mons Victorialis",
    55: "Secundus Tractatus Magni Seth (NHC VII, 2) (coptice)",
    57: "Intelligentia Noreae uxoris Seth (NHC IX, 2) (coptice)", 63: "Liber Og gigantis (Liber de Ogia)",
    64: "Qumran. Dicta Michael (4Q529, 6Q23) (aramaice)", 66: "Henoch slauicus",
    72: "Alius sermo de natiuitate Henoch (aethiopice)", 79: "Qumran. Apocryphon Genesis (1Q20) (aramaice)",
    83: "Qumran. Admonitio de diluuio (4Q370) (hebraice)",
    90: "De commoratione Abrahae et Sarae in Aegypto (aethiopice)", 91: "Inquisitio Abrahae",
    95: "Historia de Melchisedech", 97: "Liber Melchisedech (georgice)", 101: "Scala Jacob (Gradus Jacob)",
    113: "Historia Joseph filii Jacob", 120: "Qumran. Testamentum Qahat (4Q542) (aramaice)",
    121: "Qumran. Visiones Amram (4Q543, 4Q544, 4Q545, 4Q546, 4Q547, 4Q548) (aramaice)",
    122: "Qumran. Apocryphon Moysi (1Q22, 1Q29, 4Q375, 4Q376) (hebraice)",
    125: "Qumran. Pseudo-Moyses (4Q385a, 4Q387a, 4Q388a, 4Q389, 4Q390) (hebraice)",
    126: "Qumran. De Hur et Miriam (4Q549) (aramaice)", 130: "Colloquium Moysi cum Deo",
    133: "Eldad et Modad (fragmentum graecum in citatione)", 145: "Qumran. Psalmi Josue (4Q378, 4Q379) (hebraice)",
    146: "Masada. Apocryphon Josue (Mas1l) (hebraice)", 148: "Threnus Seilae filiae Jephtae (latine)",
    152: "Citharismus Dauid (latine)", 154: "Instructio Dauid ad Salomonem (arabice)",
    169: "Visio Eliae (latine)", 172: "Historia Eliae prophetae et ascensionis eius (arabice)",
    175: "Sermo Elisei prophetae de peccatoribus (arabice)", 179: "3 Esdrae", 182: "5 Esdrae",
    184: "Apocalypsis Esdrae graeca", 192: "Masada. Apocryphon Esther ? (Mas1m) (hebraice)",
    194: "Qumran. Fragmenta Tobit (4Q196, 4Q197, 4Q198, 4Q199, 4Q200?, 4Q478?) (hebraice et aramaice)",
    196: "1 Maccabaeorum", 200: "5 Maccabaeorum", 202: "Psalmus 151",
    203: "Qumran. Psalmi apocryphi (4Q88, 4Q380, 4Q381, 4Q448, 11Q11) (hebraice)",
    206: "Fragmentum cuiusdam Cairensis libri sententiarum (hebraice)", 207: "Testamentum Job",
    208: "De iusto Job quando uenerunt tres amici eius ut uiderent eum (graece)",
    215: "Apocryphon Habacuc", 219: "Historia Isaiae prophetae (arabice)", 226: "Professio Jeremiae et Baruch",
    227: "Apocryphon Jeremiae de captiuitate Babylonis", 228: "Prophetia Jeremiae ad Pashur",
    229: "Legenda Jeremiae (aethiopice)", 234: "Fragmentum latinum Apocalypsis Baruch syriacae",
    239: "Reliqua uerborum Baruch", 240: "Qumran. Lamentationes apocryphae (4Q179, 4Q501) (hebraice)",
    241: "Epistula Jeremiae",
    243: "Qumran. Noua Jerusalem (1Q32, 2Q24, 4Q232?, 4Q554, 4Q555, 5Q15, 11Q18) (hebraice et aramaice)",
    247: "Bel et Draco", 248: "Qumran. Apocryphon Danielis (4Q243, 4Q244, 4Q245) (aramaice)",
    250: "Qumran. Apocryphon de quatuor regnis (4Q552, 4Q553) (aramaice)",
    256: "Visio monachi Danielis de septem collibus et de insulis (graece)",
    257: "Visio Danielis de tempore nouissimo et de fine mundi (graece)", 267: "Passio Danielis et trium puerorum",
    271: "Apocryphi anonymi", 277: "Palaea historica",
}


def pages():
    out, cur = {}, None
    for line in (D / "cavt.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"<!-- page (\d+) -->", line)
        if m:
            cur = int(m.group(1)); out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def clean(s):
    s = s.replace("|", " ")
    s = re.sub(r"(\s*[.,:;'\"‘’°]\s*){2,}.*$", "", s)  # dot leaders + pages
    s = re.sub(r"\s+[\dIS$]{1,3}(\s*-\s*[\dIS$]{1,3})?\s*$", "", s)
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    s = re.sub(r"\s+", " ", s).strip(" .,")
    for a, b in TITLE_FIXES:
        s = s.replace(a, b)
    return s


def toc_titles():
    """Titles from the TOC re-OCR'd with --psm 6 (raw/cavt/toc/). Some pages lost the
    number column, so entries are numbered in sequence: a line ending in a page number closes
    an entry, a line without one wraps into the next, and a printed 'N.' resets the counter."""
    lines = [l.strip() for f in sorted((D / "toc").glob("p-*.txt"))
             for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    # entry 1 is a heading over sub-entries 1.i-1.vi whose sigla OCR as "14", "1.8", "lii"...
    tocpages = {1: (1, 6)}
    titles, sections, section, n, buf = {1: "Vita Adae et Euae (Apocalypsis Moysi)"}, {1: "ADAM"}, "", 0, ""
    ends = re.compile(r"(?<![A-Za-z])[\dIS$sOo]{1,3}(\s*-\s*[\dIS$sOo]{1,3})?\s*$")
    for l in lines:
        if "SYNOPSIS MATERIAE" in l or l.startswith(("INTRODUCTIO", "SIGLA", "CONCORDANTIA")):
            continue
        letters = re.sub(r"[^A-Za-z]", "", clean(l))
        if letters.isupper() and len(letters) > 3 and not buf:
            section = clean(l)
            continue
        if n < 1:
            if re.match(r"^2\s*[.,]\s", l):
                n = 1  # skip front matter and entry 1's sub-entries
            else:
                continue
        if not re.search(r"[A-Za-z]{2}", l) and not buf:
            continue  # stray page range split off a section heading
        m = re.match(r"^(\d{1,3})\s*[.,][\s.|_—-]*(.*)$", l)
        if m and 1 < int(m.group(1)) <= N_ENTRIES and abs(int(m.group(1)) - n) <= 10:
            if buf and int(m.group(1)) == n + 2:  # wrapped title cut off by the next numbered line
                n += 1
                titles.setdefault(n, clean(buf)); sections.setdefault(n, section)
                buf = ""
            n, l = int(m.group(1)) - 1, m.group(2)
        buf += (" " if buf else "") + l
        if ends.search(l) or re.search(r"\.\s*\.", l):
            n += 1
            if n <= N_ENTRIES and n not in titles:
                titles[n], sections[n] = clean(buf), section
            if n <= N_ENTRIES:
                tocpages[n] = toc_range(buf)
            buf = ""
    return titles, sections, tocpages


def toc_range(s):
    """Printed page range at the end of a TOC line: '35-42', '31', or run-together '216217'."""
    num = lambda g: int(g.translate(OCR_DIGITS).replace("s", "5").replace("o", "0"))
    d = r"[\dIS$sOo]"
    m = re.search(rf"(?<![A-Za-z])({d}{{1,3}})\s*-\s*({d}{{1,3}})\s*$", s)
    if m:
        a, b = num(m.group(1)), num(m.group(2))
    elif (m := re.search(rf"(?<![A-Za-z])({d}{{6}})\s*$", s)):
        a, b = num(m.group(1)[:3]), num(m.group(1)[3:])
    elif (m := re.search(rf"(?<![A-Za-z])({d}{{1,3}})\s*$", s)):
        a = b = num(m.group(1))
    else:
        return None
    return (a, b if a <= b <= a + 40 else a)


def head_entries(pg):
    """PDF page -> entry number from the running head ('56 POSTERI ADAE ET EVAE 33')."""
    out = {}
    for p in BODY:
        head = next((l for l in pg.get(p, []) if l.strip()), "")
        nums = [int(x) for x in re.findall(r"\b(\d{1,3})(?:\.[ivx]+)?\b", head.translate(OCR_DIGITS))]
        ent = [n for n in nums if n != p - OFFSET and 1 <= n <= N_ENTRIES]
        out[p] = ent[0] if ent else None
    # fill gaps and reject outliers: entry numbers never decrease through the book
    prev = 1
    for p in BODY:
        n = out[p]
        out[p] = n if n is not None and prev <= n <= prev + 12 else prev
        prev = out[p]
    return out


def _norm(t):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"^\d{1,3}\s*[.,]\s*", "", t).lower().replace("u", "v"))


def _find(lines, t, start=0, floor=0.8, n=None):
    """Index of the entry's heading: a line numbered 'n.' if there is one, else the line(s)
    best matching the whole title (similarity >= floor), skipping lines numbered for other entries."""
    if n is not None:
        for i in range(start, len(lines)):
            if re.match(rf"^\s*{n}\s*[.,]\s+\S", lines[i]) and len(lines[i]) < 90:
                return i
    want, best = _norm(t), (floor, None)
    if not want:
        return None
    for i in range(start, len(lines)):
        if not lines[i].strip() or len(lines[i]) > 90:
            continue
        num = re.match(r"^\s*(\d{1,3})\s*[.,]\s", lines[i])
        if num and n is not None and int(num.group(1)) != n:
            continue
        for span in (1, 2):
            got = _norm(" ".join(lines[i:i + span]))
            r = difflib.SequenceMatcher(None, want, got[:len(want) + 6]).ratio()
            if r > best[0]:
                best = (r, i)
        if best[0] > 0.95:
            break
    return best[1]


def entry_text(n, ps, titles, pg):
    """The entry's own text: from its heading to the next entry's heading (falls back to whole pages)."""
    lines = [l for p in range(ps[0], ps[-1] + 2) for l in pg.get(p, [])]
    a = _find(lines, titles.get(n, ""), n=n)
    if a is None:
        return "\n".join(l for p in ps for l in pg.get(p, []))
    b = _find(lines, titles.get(n + 1, ""), a + 1, 0.9, n + 1) if n < N_ENTRIES else None
    return "\n".join(lines[a:b])


def main():
    pg = pages()
    titles, sections, tocpages = toc_titles()
    titles.update(TITLE_CORRECTIONS)
    sections = {n: SECTION_NAMES.get(v, v) for n, v in sections.items()}
    heads = head_entries(pg)
    body = {}
    for p in BODY:
        body.setdefault(heads[p], []).append(p)
    # an entry that starts mid-page sits on the last page headed by the previous entry
    rows = []
    for n in range(1, N_ENTRIES + 1):
        tp, prev_tp = tocpages.get(n), tocpages.get(n - 1, (1, 1))
        if tp and prev_tp and prev_tp[0] <= tp[0] <= 219:  # TOC page range, when it reads sanely
            ps = list(range(tp[0] + OFFSET, tp[1] + OFFSET + 1))
            rows_src = "toc"
        else:
            ps, rows_src = body.get(n, []), "running head"
        if ps and rows_src == "toc":
            pass
        elif not ps:  # entry wholly inside a page headed by a neighbour
            ps = [max((p for p in BODY if heads[p] <= n), default=28)]
        elif ps[0] > 28 and heads[ps[0] - 1] != n:
            ps = [ps[0] - 1] + ps
        text = entry_text(n, ps, titles, pg)
        blob = (titles.get(n, "") + " " + text).lower()
        rows.append({
            "cavt_no": n, "title": titles.get(n, ""), "section": sections.get(n, ""),
            "pages_from": rows_src, "printed_pages": f"{ps[0] - OFFSET}-{ps[-1] - OFFSET}", "pdf_pages": f"{ps[0]}-{ps[-1]}",
            "title_language": title_language(titles.get(n, "")),
            "main_language": main_language(text),
            "languages_on_pages": "; ".join(sorted({v for k, v in LANGS.items() if k in blob})),
            "n_inedita_on_pages": len(re.findall(r"\binedit", text, re.I)),
            "translations": "; ".join(sorted(set(re.findall(r"Translatio (\w+)", text)))),
            "qumran": bool(re.search(r"\b\dQ\d|Qumran", text)),
            # biblical/deuterocanonical book listed only for completeness
            "pro_memoria": bool(re.search(r"pro\s+memoria\s+tantum", text)),
            "cross_ref_only": len(text) < 200 and bool(re.search(r"\bVide\b", text)),
            "entry_chars": len(text),
            "edition_years": " ".join(map(str, editions(text, titles.get(n, ""))[1])),
            "refers_to": " ".join(re.findall(r"(?:supra|infra) n\W{0,2}\s*(\d{1,3})", text)),
            "no_critical_edition": bool(re.search(r"editio critica nondum", text, re.I)),
        })
    with (D / "cavt_entries.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} entries; untitled: {[r['cavt_no'] for r in rows if not r['title']]}")
    print(f"entries with own body pages: {sum(1 for n in range(1, N_ENTRIES + 1) if n in body)}")


if __name__ == "__main__":
    main()
