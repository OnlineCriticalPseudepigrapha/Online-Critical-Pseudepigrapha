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
 '1Q17': ['27:19', '27:19', '27:19', '27:20', None],
 '1Q18': ['35:9', '35:9', None, None, None, None, None, None, None],
 '2Q19': ['23:7', '23:7', '23:7', '23:8', None],
 '2Q20': ['46:1', '46:2', '46:2', '46:3', None, None, None, None, None],
 '3Q5': ['23:13', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
 '4Q176a': ['23:21', '23:22', '23:22', '23:23', None, '23:30', '23:31', None],
 '4Q217': [None, None, '1:29', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
 '4Q218': ['2:26', '2:27', None],
 '4Q219': ['21:1', '21:2', '21:7', '21:8', '21:9', '21:10', None, '21:12', '21:12', '21:13', '21:15', '21:16', '21:18', '21:19', '21:20', '21:21', '21:21', '21:22', '21:23', '21:24', '21:25', '21:26', '22:1', None],
 '4Q220': ['21:5', '21:6', '21:7', '21:7', '21:7', '21:8', '21:9', '21:10', '21:10', None],
 '4Q221': ['21:22', '21:22', '21:23', '21:23', '21:24', '21:24', None, '22:22', '22:22', '22:22', None, None, None, '23:10', '23:11', '23:11', '23:12', '23:13', None, '33:12', '33:12', '33:13', '33:13', '33:13', '33:13', '33:13', '33:15', None, '37:11', '37:12', '37:13', '37:14', '37:14', '37:15', None, '38:6', '38:6', '38:7', '38:7', '38:8', None, '39:4', '39:5', '39:5', '39:5', '39:6', '39:6', '39:7', '39:8', '39:8', '39:8', '39:9', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
 '4Q222': ['25:9', '25:10', '25:11', '25:12', None, '27:8', '27:8', '27:8', '27:9', None, '48:5', None, None, None, None, None, None, None],
 '4Q223_224': ['32:18', '32:18', '32:19', '32:19', '32:20', '32:21', None, '34:4', '34:5', '35:7', '35:8', '35:8', '35:9', '35:9', '35:10', '35:10', '35:11', '35:11', '35:12', None, '35:12', '35:12', '35:12', '35:12', '35:13', '35:13', '35:13', '35:14', '35:14', '35:15', '35:15', '35:15', '35:16', '35:17', '35:17', '35:18', '35:19', '35:20', '35:21', '35:22', '35:22', '36:7', '36:8', '36:8', '36:9', '36:10', '36:10', '36:11', '36:12', '36:13', '36:14', '36:14', '36:15', '36:16', '36:17', '36:17', '36:18', '36:18', '36:18', '36:19', '36:20', '36:21', '36:22', '36:23', '36:23', '37:17', '37:18', '37:19', '37:19', '37:20', '37:20', '37:21', '37:22', '37:23', '37:23', '37:24', '37:25', '38:1', '38:1', '38:2', '38:2', '38:4', '38:5', '38:5', '38:6', '38:7', '38:8', '38:8', '38:9', '38:11', '38:12', '38:12', '38:13', '39:9', '39:10', '39:11', '39:12', '39:13', '39:14', '39:14', '39:16', '39:17', '39:18', '40:1', '40:2', '40:3', '40:4', '40:5', '40:5', '40:5', '40:6', '40:6', '40:7', '40:7', '40:7', '40:7', None, '41:8', '41:9', '41:10', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
 '11Q12': ['4:6', '4:7', '4:7', '4:8', '4:9', '4:9', '4:9', '4:10', None, '4:13', '4:14', '4:15', None, '4:16', None, '4:17', '4:18', None, '4:29', '4:30', '4:30', None, '4:31', '4:31', None, '5:1', None, '6:3', None, '12:15', '12:16', '12:17', None, '12:28', '12:29', None, None, None, None, None, None, None, None, None],
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

def fix(t):
    return t.replace('זה ריאש[ון]', 'זה ריאשון]')   # 11Q12: nested bracket in source

def build(tsv, start_id):
    rows = [l.rstrip('\n').split('\t') for l in open(tsv, encoding='utf8')]
    verses = {}
    for scroll, refs in VERSES.items():
        cs = chunks([r for r in rows if r[0] == scroll])
        assert len(cs) == len(refs), (scroll, len(cs), len(refs))
        for c, ref in zip(cs, refs):
            if ref:
                verses.setdefault(ref, {}).setdefault(scroll, []).append(fix(clean(c)))
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
