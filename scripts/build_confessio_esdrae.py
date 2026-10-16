#!/usr/bin/env python3
"""
Build Confessio Esdrae / Oratio Esdrae (CAVT 181)
The famous independent liturgical prayer extracted from 4 Ezra 8:20-36.
Sources:
- Robert L. Bensly & M. R. James, The Fourth Book of Ezra (Texts and Studies III.2; Cambridge, 1895), pp. 38-41.
- Clementine Vulgate (4 Esdrae 8:20-36).

Outputs:
  - static/docs/ConfEsdr.xml (Grammateus DTD)
  - static/docs/tei/ConfEsdr.xml (TEI P5 parallel segmentation)
"""

import os
import subprocess

VERSES = [
    {
        "v": 20,
        "lat": "Initium verborum Esdrae priusquam assumeretur: et dixi, Domine, qui inhabitas saeculum, cuius oculi elevati in superna et aëre,",
        "en": "The beginning of the words of Ezra, before he was taken up. And I said: O Lord, who inhabitest eternity, whose eyes are exalted toward the heights and the air,"
    },
    {
        "v": 21,
        "lat": "et cuius thronus inaestimabilis, et gloria incomprehensibilis, cui astat exercitus angelorum cum tremore,",
        "en": "and whose throne is beyond estimation, and whose glory is incomprehensible, before whom the host of angels stands with trembling,"
    },
    {
        "v": 22,
        "lat": "quorum servatio in vento et igni convertitur; cuius verbum verum, et dicta perseverantia;",
        "en": "whose service is turned into wind and fire; whose word is true, and whose sayings endure;"
    },
    {
        "v": 23,
        "lat": "cuius iussio fortis, et dispositio terribilis; cuius aspectus arefacit abyssos, et indignatio tabescere facit montes, et veritas testificatur:",
        "en": "whose command is strong, and whose ordinance is fearful; whose look drieth up the depths, and whose indignation maketh the mountains to melt, and whose truth beareth witness:"
    },
    {
        "v": 24,
        "lat": "exaudi orationem servi tui, et auribus percipe precationem figmenti tui.",
        "en": "hearken unto the prayer of thy servant, and give ear to the supplication of thy creature."
    },
    {
        "v": 25,
        "lat": "Dum enim vivo, loquar, et dum sapio, respondebo.",
        "en": "For while I live I will speak, and while I have understanding I will answer."
    },
    {
        "v": 26,
        "lat": "Nec respicias populi tui delicta, sed qui tibi in veritate serviunt.",
        "en": "O look not upon the sins of thy people, but on those who serve thee in truth."
    },
    {
        "v": 27,
        "lat": "Nec intendas impia gentium studia, sed qui tua testimonia cum doloribus custodierunt.",
        "en": "Regard not the impious endeavors of the heathen, but of those who have kept thy testimonies with afflictions."
    },
    {
        "v": 28,
        "lat": "Nec cogites qui in conspectu tuo false conversati sunt, sed memorare qui ex voluntate tua timorem cognoverunt.",
        "en": "Think not upon those that have walked feignedly before thee, but remember those who according to thy will have acknowledged thy fear."
    },
    {
        "v": 29,
        "lat": "Neque volueris perdere qui pecudum mores habuerunt, sed respicias eos qui legem tuam splendide docuerunt.",
        "en": "Desire not to destroy those that have lived like beasts, but look upon those who have clearly taught thy law."
    },
    {
        "v": 30,
        "lat": "Nec indigneris eis qui bestiis peiores iudicati sunt, sed diligas eos qui semper in tua iustitia et gloria confidunt.",
        "en": "Take not indignation at those who are deemed worse than beasts, but love those who always put their trust in thy righteousness and glory."
    },
    {
        "v": 31,
        "lat": "Quoniam nos et patres nostri talibus languoribus morimur; tu autem propter nos peccatores misericors vocaberis.",
        "en": "For we and our fathers have languished through such diseases; but because of us sinners thou shalt be called merciful."
    },
    {
        "v": 32,
        "lat": "Si enim desideraveris nobis misereri, tunc misericors vocaberis, nobis non habentibus opera iustitiae.",
        "en": "For if thou hast a desire to have mercy upon us, then shalt thou be called merciful, unto us, namely, who have no works of righteousness."
    },
    {
        "v": 33,
        "lat": "Iusti enim, quibus sunt opera multa reposita, ex propriis operibus recipient mercedem.",
        "en": "For the righteous, who have many works laid up with thee, shall out of their own deeds receive reward."
    },
    {
        "v": 34,
        "lat": "Quid enim est homo, ut ei indigneris? vel genus corruptibile, ut ita amariceris de eo?",
        "en": "For what is man, that thou shouldest take displeasure at him? or what is a corruptible race, that thou shouldest be so bitter toward it?"
    },
    {
        "v": 35,
        "lat": "In veritate enim nemo est de genitis qui non impie fecerit, et de confitentibus qui non deliquerit.",
        "en": "For in truth there is none among those born who hath not done wickedly, and among those who confess thee none who hath not transgressed."
    },
    {
        "v": 36,
        "lat": "In hoc enim praedicabitur iustitia tua et bonitas tua, Domine, cum misertus fueris his qui non habent substantiam bonorum operum.",
        "en": "For in this thy righteousness and thy goodness shall be declared, O Lord, when thou art merciful unto those who have no substance of good works."
    }
]

def build_grammateus_xml():
    bib = "R. L. Bensly &amp; M. R. James, The Fourth Book of Ezra (Texts and Studies III.2; Cambridge, 1895), pp. 38-41; Biblia Sacra Vulgata (Clementina), 4 Esdrae 8:20-36. CAVT 181."
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="ConfEsdr" title="Confessio Esdrae (Oratio Esdrae)">',
        '  <version author="Bensly 1895" language="Latin" title="Latin and English">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Bensly" language="Latin" show="yes">',
        '        <name>Bensly 1895 (Latin Vulgate tradition)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="8">'
    ]

    for item in VERSES:
        v_num = item["v"]
        clean_lat = item["lat"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en  = item["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        lines.append(f'        <div number="{v_num}">')
        lines.append(f'          <unit id="{v_num-20}">')
        lines.append(f'            <reading option="0" mss="Bensly ">{clean_lat}</reading>')
        lines.append(f'            <reading option="1" mss="Trans ">{clean_en}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')

    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')

    out_path = 'static/docs/ConfEsdr.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path} ({len(VERSES)} verses)')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Confessio Esdrae (Oratio Esdrae)</title>',
        '        <author>Ezra (Pseudepigraphon)</author>',
        '        <editor>Robert L. Bensly</editor>',
        '        <respStmt>',
        '          <resp>TEI P5 Parallel Segmentation edition for Online Critical Pseudepigrapha</resp>',
        '          <name>Ken M. Penner</name>',
        '        </respStmt>',
        '      </titleStmt>',
        '      <publicationStmt>',
        '        <publisher>Online Critical Pseudepigrapha</publisher>',
        '        <pubPlace>St. Francis Xavier University, Antigonish, NS</pubPlace>',
        '        <availability>',
        '          <licence target="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</licence>',
        '        </availability>',
        '      </publicationStmt>',
        '      <sourceDesc>',
        '        <biblStruct type="book">',
        '          <monogr>',
        '            <title level="m">The Fourth Book of Ezra</title>',
        '            <editor>Robert L. Bensly</editor>',
        '            <imprint>',
        '              <publisher>Cambridge University Press</publisher>',
        '              <date when="1895">1895</date>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>',
        '      <div type="chapter" n="8">'
    ]

    for item in VERSES:
        v_num = item["v"]
        clean_lat = item["lat"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en  = item["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        lines.append(f'        <p n="{v_num}">')
        lines.append('          <app>')
        lines.append(f'            <rdg wit="#Bensly" xml:lang="lat">{clean_lat}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{clean_en}</rdg>')
        lines.append('          </app>')
        lines.append('        </p>')

    lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')

    out_path = 'static/docs/tei/ConfEsdr.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
    subprocess.run(['python3', 'scripts/grammateus_to_tei.py', 'static/docs/ConfEsdr.xml', '-o', 'static/docs/tei/ConfEsdr.xml'], check=True)
