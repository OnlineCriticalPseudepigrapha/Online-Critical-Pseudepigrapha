"""Recompute entry-level fields of raw/cavt/cavt_entries.csv from each entry's own text.
Entry text is located in raw/cavt/cavt.md by cavt_audit.py's title-matching DP (more robust than the
page-based fallback in cavt_parse.py, which leaks neighbouring entries). Only rows whose text is located
are changed; every change is logged to raw/cavt/cavt_entries_fixes.tsv. Usage: python3 scripts/cavt_fix_entries.py"""
import csv, io, re, sys, runpy, contextlib
sys.path.insert(0, 'scripts')
from cavt_parse import editions
sys.argv = ['x', '12000']
with contextlib.redirect_stdout(io.StringIO()):
    A = runpy.run_path('scripts/cavt_audit.py')
starts, ks, L = A['starts'], A['ks'], A['L']
def raw(k):
    j = ks.index(k); e = starts[ks[j+1]] if j+1 < len(ks) else 12000
    return '\n'.join(l for l in L[starts[k]:e] if not l.startswith('<!--'))
P = 'raw/cavt/cavt_entries.csv'
rows = list(csv.DictReader(open(P, encoding='utf-8'))); fields = list(rows[0])
INED = re.compile(r'\b[IlL1|]n[eé]d[il1]t|non(?:dum)? edit', re.I)
log = []
for r in rows:
    n = int(r['cavt_no'])
    if n not in starts: continue
    t = raw(n); flat = re.sub(r'-\s+(?=[a-z])', '', t)
    new = {
        'n_inedita_on_pages': str(len(INED.findall(flat))),
        'edition_years': ' '.join(map(str, editions(t, r['title'])[1])),
        'qumran': str(bool(re.search(r'\b\dQ\d|Qumran', flat))),
        'no_critical_edition': str(bool(re.search(r'editio critica nondum', flat, re.I))),
        'refers_to': ' '.join(re.findall(r'(?:supra|infra) n\W{0,2}\s*(\d{1,3})', flat)),
        'entry_chars': str(len(t)),
    }
    # never drop information on a mere segmentation shortfall: if the located text is much
    # shorter than the parser's own entry text, keep the old row
    # 277 is last: its located text runs into the indices; a short hit without a cross-reference
    # or pro-memoria note matched a TOC/index line, not the heading
    if n == 277 or (len(t) < 200 and not re.search(r'\b[Vv]ide\b|\buide\b|pro memoria', t)):
        continue
    for k, v in new.items():
        if r[k] != v and k != 'entry_chars':
            log.append((n, k, r[k], v)); r[k] = v
    r['entry_chars'] = new['entry_chars']
# hand overrides, read in the entry text (CAVT_AUDIT.md §4-5)
MANUAL = {
    (136, 'pro_memoria'): 'True',      # "pro memoria tantum notatur" (medieval rabbinic work)
    (179, 'edition_years'): '',        # pro memoria; years were a neighbour's
    (190, 'edition_years'): '1877',    # Wesselofsky 1877, with editions and German translation
    (250, 'edition_years'): '1994',    # Beyer 1994, translation "cum textu"
}
for r in rows:
    for (n, k), v in MANUAL.items():
        if int(r['cavt_no']) == n and r[k] != v:
            log.append((n, k, r[k], v)); r[k] = v
w = csv.DictWriter(open(P, 'w', newline='', encoding='utf-8'), fields); w.writeheader(); w.writerows(rows)
with open('raw/cavt/cavt_entries_fixes.tsv', 'w') as f:
    f.write('cavt_no\tfield\told\tnew\n')
    for x in log: f.write('\t'.join(map(str, x)) + '\n')
import collections
print(collections.Counter(k for _, k, _, _ in log), file=sys.stderr)
