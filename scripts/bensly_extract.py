#!/usr/bin/env python3
"""Extract 5 Ezra (Bensly cc. I-II) and 6 Ezra (cc. XV-XVI) from Bensly-James 1895 page OCR.

Input: raw/editions/bensly_ocr/pNN-NNN.txt (tesseract -l lat --psm 4, 400 dpi; printed page = PDF page - 96).
Output: raw/editions/bensly_ocr/{5Ezra,6Ezra}.json  [[chapter, verse, text, flags], ...]

Each line may carry a garbled marginal verse number at its start or end. Bensly capitalizes
the first word of every verse, so a marked line's verse starts at its first capitalized word
after punctuation (or at the line start). Counts are checked against the known verse totals.
"""
import json, re
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "raw/editions/bensly_ocr"
PARTS = {"5Ezra": (range(97, 103), {1: 40, 2: 48}), "6Ezra": (range(168, 179), {15: 63, 16: 78})}
ROMAN = {"I": 1, "II": 2, "III": 3, "XV": 15, "XVI": 16}
MARK = r"(?:[0-9oOsSlIiz?:;»$&gr]{1,3}|[,;:|])"  # garbled marginal number
NAMES = {"Iuda", "Iacob", "Israel", "Sion", "Aegypti", "Aegyptiis", "Moysen", "Aaron", "Babylon", "Asia",
         "Ezra", "Esdra", "Assur", "Sodomae", "Gomorrae", "Ieremiae", "Esaiae", "Danihel"}


SIGLA = re.compile(r"^(?:S|A|C|M|SA|CM|SM|AC|SAM|SAC)[*\u00b0]*[,.;)]?$|^om\.?$|^txt\.?$|^add\.?$")


def apparatus(l):
    toks = l.split()
    return "*" in l or (len(toks) >= 3 and sum(bool(SIGLA.match(t)) for t in toks) >= 2)


def footnote(l):
    """Appendix I foot of page: variants of M, e.g. '14 lucé nubis] ignis Hec 15 signo] cibo'."""
    nums = re.findall(r"(?:^|\s)\d{1,3}(?=[\s\]])", l)
    return (len(nums) >= 2 and ("]" in l or "om." in l or " -" in l or "—" in l)) or \
        bool(re.search(r"(?:^|\s)\d{1,3}\]\s", l)) or (len(nums) >= 1 and "]" in l and "om." in l)


def body(p, appendix=False):
    """Text lines of a page: after the running head, up to the first apparatus line.

    A hand-proofread p{N}.corr.txt (running head + body only) replaces the OCR when present."""
    corr = D / f"p{p}.corr.txt"
    if corr.exists():
        return [l.strip() for l in corr.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    ls = (D / f"p{p}-{p:03d}.txt").read_text(encoding="utf-8").splitlines()
    out = []
    for l in ls[1:]:  # ls[0] = running head
        l = l.strip()
        if not l or re.fullmatch(r"[\d\W]{1,4}", l):
            continue
        if l.startswith("(For") or (footnote(l) if appendix else apparatus(l)):
            break
        out.append(l)
    return out


def strip_marks(l):
    marked = False
    m = re.match(rf"^{MARK}(?=\s|[A-Za-z])\s*(.*)$", l)
    if m and not re.match(r"^(I|II|XV|XVI)\.", l) and not re.match(r"^[a-z]{2,}", l):
        # leading token is a mark only if it contains a digit-like char and is not a real word
        tok = l[: len(l) - len(m.group(1))].strip()
        if re.search(r"[0-9?:;»$&]", tok) or tok in {"i5", "rg", "ro", "ri", "s", "g", "o"} or re.fullmatch(r"[0-9oisSlIz]{1,3}", tok) and not tok.isalpha():
            l, marked = m.group(1), True
    m = re.match(rf"^(.*\S)\s+{MARK}$", l)
    if m and (re.search(r"[0-9?;»$&,|]", l[len(m.group(1)):]) or len(l[len(m.group(1)):].strip()) <= 2):
        l, marked = m.group(1), True
    return l, marked


def split_point(toks):
    for i, t in enumerate(toks):
        w = re.sub(r"^[\"'(]+", "", t)
        if w[:1].isupper() and w.rstrip(".,;:?!") not in NAMES and (i == 0 or re.search(r"[.:;?!,]$", toks[i - 1])):
            return i
    return 0


def extract(pages, expected):
    chapters = list(expected)
    verses, ch, v, cur, flags = [], None, 0, [], []
    for p in pages:
        for raw in body(p):
            raw = re.sub(r"^\W{1,3}\s+(?=(XV|XVI|II|I)\.)", "", raw)
            l, marked = strip_marks(raw)
            toks = l.split()
            h = re.match(r"^(I|II|III|XV|XVI)\.$", toks[0]) if toks else None
            if h:
                if ch is not None and cur:
                    verses.append([ch, v, " ".join(cur), flags])
                ch, v, cur, flags = ROMAN[h.group(1)], 1, [], []
                toks = toks[1:]
                marked = False  # the mark on a heading line is verse 1
                if ch not in chapters:
                    ch = None
            if ch is None:
                continue
            if marked:
                i = split_point(toks)
                cur += toks[:i]
                verses.append([ch, v, " ".join(cur), flags])
                v, cur, flags, toks = v + 1, [], [], toks[i:]
            cur += toks
    if ch is not None and cur:
        verses.append([ch, v, " ".join(cur), flags])
    for x in verses:
        x[2] = re.sub(r"(\w)- (\w)", r"\1\2", x[2])
    return verses


CLEM = D.parent / "vulgate/4Esd_clementina.wiki"  # la.wikisource Vulgata Clementina (PD): verse scaffold


def norm(w):
    w = w.lower().replace("æ", "ae").replace("œ", "oe").replace("v", "u").replace("j", "i")
    return re.sub(r"[^a-z]", "", w)


def clementine(chapters):
    """[(ch, v, [words])] for the given chapters."""
    out, ch = [], None
    for l in CLEM.read_text(encoding="utf-8").splitlines():
        m = re.match(r"==Caput (\d+)==", l)
        if m:
            ch = int(m.group(1)); continue
        if ch in chapters and "<sup>" in l:
            for v, txt in re.findall(r"<sup>(\d+)</sup>(.*?)(?=<sup>|$)", l):
                out.append((ch, int(v), txt.split()))
    return out


APPX = {"5Ezra": (range(179, 184), r"(L|I)\.?", r"Expliciunt"),
        "6Ezra": (range(183, 189), r"XV\.", None)}


def appendix_tokens(name):
    """Codex C (Spanish recension) from Bensly's Appendix I: (tokens, {token index: margin verse no.})."""
    pages, head, stop = APPX[name]
    toks, marks = [], {}
    for p in pages:
        for raw in body(p, appendix=True):
            if raw.startswith(("(The text", "negle", "4 ESDRAS", "Liber Esdre", "Expliciunt")) and stop is None:
                continue
            nums = []
            m = re.match(r"^(\d{1,3})\s*(?=[A-Za-z\[\"'])", raw)      # left-margin verse no.
            if m: nums.append(int(m.group(1))); raw = raw[m.end():]
            m = re.search(r"\s+(\d{1,3})$", raw)                       # right-margin verse no.
            if m: nums.append(int(m.group(1))); raw = raw[:m.start()]
            if nums: marks[len(toks)] = nums[0]
            toks += raw.split()
    # rejoin hyphenated words, keeping the mark indices in step
    t, tm = [], {}
    for i, x in enumerate(toks):
        if i in marks: tm[len(t)] = marks[i]
        if t and t[-1].endswith("-") and len(t[-1]) > 1:
            t[-1] = t[-1][:-1] + x
        else:
            t.append(x)
    start = next(i for i, x in enumerate(t) if re.fullmatch(head, x)) + 1
    end = next((i for i, x in enumerate(t) if i > start and stop and x.startswith(stop)), len(t))
    heads = [i for i in range(start, end) if re.fullmatch(r"(IL|II|XVI)\.", t[i])]
    keep = [i for i in range(start, end) if not re.fullmatch(r"(I|IL|II|XVI|XV)\.", t[i]) and t[i] not in "[|"
            and not (i + 1 in heads and t[i] == "I")]
    newpos = {old: k for k, old in enumerate(keep)}
    chstart = [next(newpos[j] for j in range(h, end) if j in newpos) for h in heads]
    seq = []  # (token index, verse no.) in reading order, restricted to the extracted range
    for i, n in sorted(tm.items()):
        j = next((j for j in range(i, end) if j in newpos), None)
        if j is not None and i >= start - 12:
            seq.append((newpos[j], n))
    return [t[i] for i in keep], seq, chstart


def by_chapter(seq, chapters, chstart):
    """Margin numbers restart each chapter: assign them by position relative to the chapter headings."""
    out, prev = {}, {}
    for idx, (i, n) in enumerate(seq):
        k = sum(i >= c for c in chstart)
        nxt = next((m for j, m in seq[idx + 1:idx + 2] if sum(j >= c for c in chstart) == k), None)
        if n <= prev.get(k, 0) or (nxt is not None and n >= nxt):  # misread (e.g. 39 for 58): skip
            continue
        prev[k] = n
        out[(chapters[k], n)] = i
    for k, c in enumerate(chstart, 1):  # a chapter starts at its heading
        out[(chapters[k], 1)] = c
    return out


def bensly_tokens(pages, chapters):
    toks = []
    for p in pages:
        for raw in body(p):
            raw = re.sub(r"^\W{1,3}\s+(?=(XV|XVI|II|I)\.)", "", raw)
            l, _ = strip_marks(raw)
            toks += l.split()
    t = re.sub(r"(\w)-\s+(\w)", r"\1\2", " ".join(toks)).split()
    # keep from the first chapter heading to the heading after the last chapter
    start = next(i for i, x in enumerate(t) if re.fullmatch(r"(I|XV)\.", x))
    end = next((i for i, x in enumerate(t) if i > start and re.fullmatch(r"(III)\.", x)), len(t))
    return [x for x in t[start:end] if not re.fullmatch(r"(I|II|XV|XVI)\.", x)]


def align(pages, chapters, b=None, margin=None, chstart=None):
    """margin: {verse no.: token index of the printed line on which that verse starts}."""
    import difflib
    b = b if b is not None else bensly_tokens(pages, chapters)
    clem = clementine(chapters)
    c, starts = [], []
    for ch, v, ws in clem:
        starts.append((ch, v, len(c))); c += ws
    bn, cn = [norm(x) for x in b], [norm(x) for x in c]
    sm = difflib.SequenceMatcher(None, cn, bn, autojunk=False)
    cmap = {}
    for a, bb, n in sm.get_matching_blocks():
        for k in range(n):
            cmap[a + k] = bb + k
    def to_b(ci):
        for d in range(0, 8):  # nearest matched clementine token at or after ci
            if ci + d in cmap: return cmap[ci + d] - d, d
        for d in range(1, 8):
            if ci - d in cmap: return cmap[ci - d] + d, d
        return None, 99
    bounds = []
    for ch, v, ci in starts:
        bi, d = to_b(ci)
        flag = [] if d == 0 else [f"approx boundary (±{d})"]
        if bi is not None and d:
            # snap to a capitalized word after punctuation nearby (Bensly capitalizes verse starts)
            near = [k for k in range(max(1, bi - 3), min(len(b), bi + 4))
                    if b[k][:1].isupper() and re.search(r"[.:;?!,|]$", b[k - 1])]
            if near: bi = min(near, key=lambda k: abs(k - bi))
        if margin and (ch, v) in margin and (bi is None or d or abs(bi - margin[(ch, v)]) > 15):
            # the margin number marks the line; take the sentence start on it nearest the estimate
            ls = margin[(ch, v)]
            cand = [k for k in range(ls, min(len(b), ls + 14))
                    if k == 0 or re.search(r"[.:;?!]$", b[k - 1])]
            if cand:
                bi = min(cand, key=lambda k: abs(k - (bi if bi is not None else ls)))
                flag = ["boundary from margin number"]
        if margin and v == 1 and (ch, 1) in margin and chstart:
            bi, flag = margin[(ch, 1)], []
        if chstart and bi is not None:  # keep each verse inside its chapter
            k = chapters.index(ch)
            lo = chstart[k - 1] if k else 0
            hi = chstart[k] if k < len(chstart) else len(b)
            if not lo <= bi <= hi:
                bi, flag = min(max(bi, lo), hi), flag + ["clamped to chapter"]
        bounds.append((ch, v, bi if bi is not None else (bounds[-1][2] if bounds else 0), flag))
    bounds[0] = (bounds[0][0], bounds[0][1], 0, bounds[0][3])
    out = []
    for i, (ch, v, bi, flag) in enumerate(bounds):
        bj = bounds[i + 1][2] if i + 1 < len(bounds) else len(b)
        out.append([ch, v, " ".join(b[bi:bj]), flag])
    ratio = sm.ratio()
    return out, ratio


CONFUSE = [("c", "e"), ("e", "c"), ("1", "i"), ("l", "i"), ("i", "l"), ("rn", "m"), ("o", "e"), ("ii", "u"),
           ("u", "n"), ("n", "u"), ("t", "i"), ("s", "f"), ("l", "t"), ("h", "b"), ("li", "h"), ("f", "s")]


_V = None


def vocab():
    global _V
    if _V is None:
        _V = _vocab()
    return _V


def _vocab():
    """Latin word forms attested in OCP's 4 Ezra Latin (Weber) and the Clementine 4 Esdras."""
    import html
    words = set()
    esdr = (D.parent.parent.parent / "static/docs/Esdr.xml").read_text(encoding="utf-8")
    clem = re.sub(r"<[^>]+>", " ", CLEM.read_text(encoding="utf-8"))
    vul = (D.parent / "vulgate/vul.tsv").read_text(encoding="utf-8")  # whole Clementine Vulgate (PD)
    idx = " ".join(f.read_text(encoding="utf-8") for f in sorted((D / "index").glob("p-*.txt")))  # Bensly's indexes
    for t in (html.unescape(esdr), clem, vul, idx):
        for w in re.findall(r"[A-Za-zæœÆŒ]+", t):
            words.add(norm(w))
    return words


def correct(tok, V):
    """Fix one OCR token if a single confusion (or two) yields an attested form."""
    if V is None:  # hand-proofread pages: leave the text alone
        return tok
    m = re.match(r"^([\"'(|]*)(.*?)([.,;:?!)]*)$", tok)
    pre, w, post = m.groups()
    if not w or norm(w) in V or not re.search(r"[A-Za-z]", w):
        return tok
    cands = set()
    def edits(x):
        for a, b in CONFUSE:
            i = x.find(a)
            while i != -1:
                yield x[:i] + b + x[i + len(a):]
                i = x.find(a, i + 1)
    for e1 in edits(w):
        if norm(e1) in V: cands.add(e1)
    if not cands:
        for e1 in edits(w):
            for e2 in edits(e1):
                if norm(e2) in V: cands.add(e2)
    if len(cands) == 1:
        c = cands.pop()
        if w[:1].isupper(): c = c[:1].upper() + c[1:]
        return pre + c + post
    return tok


# codex C verse starts the margin numbers place wrongly: (chapter, verse) -> first words
MAIN_STARTS = {"5Ezra": {(2, 14): "Testare,"},
               "6Ezra": {(15, 48): "Fornicariam", (15, 50): "Et gloria uirtutis"}}
C_STARTS = {"6Ezra": {(16, 2): "Precingite", (16, 5): "Missa sunt"}}


def fix_starts(cv, starts):
    """Move each listed verse's opening words from the end of the verse before it."""
    for (c, v), w in starts.items():
        i = next(k for k, x in enumerate(cv) if (x[0], x[1]) == (c, v))
        prev = cv[i - 1][2]
        j = prev.rfind(w)
        if j > 0:
            cv[i - 1][2], cv[i][2] = prev[:j].rstrip(), (prev[j:] + " " + cv[i][2]).strip()
            cv[i][3] = ["start set by hand"]


def carry_openers(vs):
    """A verse ending in a lone opening word ('... Et') lent it to the next verse: hand it back."""
    for a, b in zip(vs, vs[1:]):
        w = a[2].split()
        if w and w[-1] in {"Et", "Qui", "Certe"} and b[2]:
            a[2], b[2] = " ".join(w[:-1]), w[-1] + " " + b[2]


def main():
    for name, (pages, expected) in PARTS.items():
        vs, ratio = align(pages, list(expected))
        allp = list(pages) + list(APPX[name][0])
        V = None if all((D / f"p{p}.corr.txt").exists() for p in allp) else vocab()
        fixed = 0
        for x in vs:
            new = " ".join(correct(t, V) for t in x[2].split())
            fixed += sum(a != b for a, b in zip(x[2].split(), new.split()))
            x[2] = re.sub(r"^(XVI?L?|XVL)\s+", "", new)
        fix_starts(vs, MAIN_STARTS.get(name, {}))
        carry_openers(vs)
        print(name, "OCR fixes:", fixed)
        got = {c: sum(1 for x in vs if x[0] == c) for c in expected}
        (D / f"{name}.json").write_text(json.dumps(vs, ensure_ascii=False, indent=0), encoding="utf-8")
        print(name, "verses", got, "expected", expected, f"token match {ratio:.2f};",
              sum(1 for x in vs if x[3]), "approx;", sum(1 for x in vs if not x[2]), "empty")
        ctoks, seq, chstart = appendix_tokens(name)
        cv, ratio = align(None, list(expected), ctoks, by_chapter(seq, list(expected), chstart), chstart)
        for x in cv:
            x[2] = " ".join(correct(t, V) for t in x[2].split())
        fix_starts(cv, C_STARTS.get(name, {}))
        carry_openers(cv)
        (D / f"{name}_C.json").write_text(json.dumps(cv, ensure_ascii=False, indent=0), encoding="utf-8")
        print(name, "codex C", f"token match {ratio:.2f};", sum(1 for x in cv if x[3]), "approx;",
              sum(1 for x in cv if not x[2]), "empty")


if __name__ == "__main__":
    main()
