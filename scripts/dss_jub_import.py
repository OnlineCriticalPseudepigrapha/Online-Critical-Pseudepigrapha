"""Build the Qumran Hebrew version of Jub.xml from Abegg's ETCBC/dss data.

Input: raw/corpora/etcbc_dss/jubilees_lines.tsv (scripts/dss_tf_lines.py).
Verse identifications are in VERSES below: one entry per sentence chunk
(text split at ׃ and at fragment boundaries), aligned by content to the
VanderKam numbering. Provisional until checked against DJD 13.
"""
import re, sys
from xml.sax.saxutils import escape

VERSES = {
 '4Q216': ['P:1','1:1','1:2','1:3','1:4','1:4','1:5','1:5','1:6','1:7','1:7','1:8','1:9',
           '1:10','1:11','1:12','1:13','1:14','1:15',None,'1:26','1:27','1:28','1:28',None,
           '2:1','2:1','2:2','2:3','2:4',None,'2:7','2:7','2:8','2:9','2:10','2:10','2:11',
           '2:12','2:12',None,'2:13','2:14','2:14','2:14','2:15','2:16','2:17','2:18','2:19',
           '2:20','2:20','2:21','2:21','2:22','2:23','2:23','2:23','2:24',None],
}

def clean(t):
    t = t.replace('׳', '')
    t = re.sub(r'\(\^\s*(.*?)\s*\^\)', r'˹\1˺', t)      # supralinear
    t = re.sub(r'\(<\s*(.*?)\s*>\)', r'⟨\1⟩', t)        # editorial addition
    t = re.sub(r'\(#\s*(.*?)\s*#\)', r'\1', t)
    t = re.sub(r'(\S)(?:##|#\?|#)', '\\1\u05af', t)      # damaged letter → circlet
    t = t.replace('?', '').replace('ε', '…')
    t = re.sub(r'\[\s*\]', '[…]', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\]\s*\[', ' ', t)            # join reconstructions across line breaks
    t = re.sub(r'\[\s+', '[', t); t = re.sub(r'\s+\]', ']', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def chunks(rows):
    out, cur = [], []
    for i, (s, f, ln, t) in enumerate(rows):
        # Abegg's brackets never cross a line: a leading ']' was opened at
        # line start, a trailing '[' closes at line end.
        t = re.sub(r'\[\s*ם\s+#\s+#\s+#\s+\[\s+\^\)', '[ ם … ', t)  # 4Q216 VI 12 markup
        t = re.sub(r'#(\s+#)+', '', t)
        b = re.sub(r'[^\[\]]', '', t)
        if b.startswith(']'): t = '[' + t
        if b.endswith('['): t = t.rstrip() + ' ]'
        parts = t.split('׃')
        for j, p in enumerate(parts):
            cur.append(p.strip())
            if j < len(parts) - 1:
                out.append(cur); cur = []
        nxt = rows[i + 1][1] if i + 1 < len(rows) else None
        if nxt != f and cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    # Re-open/close reconstruction brackets cut at chunk edges, tracking
    # bracket state across the whole scroll.
    res, inside = [], False
    for c in out:
        t = ' '.join(c)
        pre = '[' if inside else ''
        for ch in t:
            if ch == '[': inside = True
            elif ch == ']': inside = False
        res.append(pre + t + (']' if inside else ''))
    return res

def build(tsv, start_id):
    rows = [l.rstrip('\n').split('\t') for l in open(tsv, encoding='utf8')]
    verses = {}
    for scroll, refs in VERSES.items():
        cs = chunks([r for r in rows if r[0] == scroll])
        assert len(cs) == len(refs), (scroll, len(cs), len(refs))
        for c, ref in zip(cs, refs):
            if ref:
                verses.setdefault(ref, {}).setdefault(scroll, []).append(clean(c))
    def key(r):
        c, v = r.split(':'); return (-1 if c == 'P' else int(c), int(v))
    out, uid, chap = [], start_id, None
    for ref in sorted(verses, key=key):
        c, v = ref.split(':'); c = '0' if c == 'P' else c
        if c != chap:
            if chap is not None: out.append('      </div>')
            out.append(f'      <div number="{c}">'); chap = c
        out.append(f'        <div number="{v}">')
        for scroll, parts in verses[ref].items():
            out.append(f'          <unit id="{uid}" group="0" parallel="">')
            out.append(f'            <reading option="0" mss="{scroll} ">{escape(" ".join(parts))}</reading>')
            out.append('          </unit>'); uid += 1
        out.append('        </div>')
    out.append('      </div>')
    return '\n'.join(out), list(VERSES)

if __name__ == '__main__':
    body, scrolls = build(sys.argv[1], int(sys.argv[2]))
    mss = '\n'.join(f'''      <ms abbrev="{s}" language="Hebrew" show="yes">
        <name>{s}</name>
        <bibliography>Transcription: M.G. Abegg, Jr., J.E. Bowley and E.M. Cook, via ETCBC/dss (Text-Fabric), used by permission of M.G. Abegg. Verse identifications provisional (OCP), to be checked against J.C. VanderKam and J.T. Milik, DJD 13 (1994).</bibliography>
      </ms>''' for s in scrolls)
    print(f'''  <version title="Qumran Hebrew" author="Abegg" language="Hebrew">
    <divisions>
      <division label="Chapter" delimiter=":"/>
      <division label="Verse"/>
    </divisions>
    <manuscripts>
{mss}
    </manuscripts>
    <text>
{body}
    </text>
  </version>''')
