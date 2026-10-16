#!/usr/bin/env python3
"""Build De Adami compositione et nomine (CAVT 10) Grammateus XML and TEI P5.
Source: Max Förster, 'Adams Erschaffung und Namengebung', Archiv für Religionswissenschaft 11 (1908), pp. 477-529.
"""
from xml.sax.saxutils import escape
import subprocess

rec_a_ch1 = [
    "Et ita creavit corpus eius de octo partibus quattuor compositionum:",
    "prima pars de terra figulari, quae deterior est omnibus partibus;",
    "altera de mari, quae est sanguis et sapientia;",
    "tertia de sole, quae est pulchritudo et oculi eius;",
    "quarta de nubibus caelestibus, quae est cogitatio et mollities;",
    "quinta de vento, id est aere, quae est spiritus et invidia;",
    "sexta de lapidibus, quae est firmitas;",
    "septima de lumine huius mundi, qui carne factus est, haec est humilitas et modestia;",
    "octava pars de spiritu sancto, constituta in hominibus ad omnem bonitatem, plena salutis: haec potissima pars est."
]

rec_a_ch2 = [
    "Et ubi Deus Adam creavit, neque nomen ei erat, convocavit quattuor angelos ad se: Michaelem, Gabrielem, Urielem et Raphaelem, quibus dixit: ite et quaerite nomen ei.",
    "Michael versus orientem exiit et stellam, quae Anatole appellatur, vidit, de qua literam A sumpsit et ad Deum attulit.",
    "Gabriel autem versus occidentem ivit et videns stellam, cui Dysis nomen est, sumpsit de ea literam D et ad Deum attulit.",
    "Raphael versus septentrionem profectus est, ubi stellam vidit, quae Arctus appellatur, et sumpsit de ea literam A et ad Deum attulit.",
    "Uriel denique versus meridiem perrexit, ubi stellam, quae Mesembria dicitur, vidit sumpsitque de ea literam M, quam ad Deum attulit.",
    "Tunc Deus Urielem legere iussit, Uriel vero dixit: Adam appellatus est."
]

bib = ("Max Förster, 'Adams Erschaffung und Namengebung: Ein lateinisches Apokryphon des 8. Jahrhunderts', "
       "Archiv für Religionswissenschaft 11 (1908), pp. 477-529. CAVT 10.")

lines = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<!DOCTYPE book SYSTEM "grammateus.dtd">',
    '<book filename="DeAdam" title="De Adami compositione et nomine">',
    '  <version author="Förster 1908" language="Latin" title="Latin">',
    '    <divisions>',
    '      <division delimiter="." label="Chapter"/>',
    '      <division label="Verse"/>',
    '    </divisions>',
    '    <manuscripts>',
    '      <ms abbrev="Förster" language="Latin" show="yes">',
    '        <name>Förster 1908 (Archiv für Religionswissenschaft 11)</name>',
    f'        <bibliography>{escape(bib)}</bibliography>',
    '      </ms>',
    '    </manuscripts>',
    '    <text>',
    '      <div number="1">'
]

unit_id = 0
for v_num, v_text in enumerate(rec_a_ch1, 1):
    lines.append(f'        <div number="{v_num}">')
    lines.append(f'          <unit id="{unit_id}">')
    lines.append(f'            <reading option="0" mss="Förster ">{escape(v_text)}</reading>')
    lines.append('          </unit>')
    lines.append('        </div>')
    unit_id += 1
lines.append('      </div>')

lines.append('      <div number="2">')
for v_num, v_text in enumerate(rec_a_ch2, 1):
    lines.append(f'        <div number="{v_num}">')
    lines.append(f'          <unit id="{unit_id}">')
    lines.append(f'            <reading option="0" mss="Förster ">{escape(v_text)}</reading>')
    lines.append('          </unit>')
    lines.append('        </div>')
    unit_id += 1
lines.append('      </div>')

lines.append('    </text>')
lines.append('  </version>')
lines.append('</book>')

out_path = 'static/docs/DeAdam.xml'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print(f"Wrote {out_path} with 2 chapters and {unit_id} verses.")

# Convert to TEI P5
subprocess.run(['python3', 'scripts/grammateus_to_tei.py', out_path, '-o', 'static/docs/tei/DeAdam.xml'], check=True)
