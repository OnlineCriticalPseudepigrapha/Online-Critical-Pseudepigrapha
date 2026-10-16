#!/usr/bin/env python3
"""
Build Prayer of Joseph (Oratio Josephi / CAVT 107 / CANT 351)
Fragments preserved in:
- Fragment A: Origen, Commentarius in Johannem II.31.188-190 (ed. E. Preuschen, GCS 10, pp. 88-89)
- Fragment B: Origen, Philocalia XXIII.15 / Eusebius, Praep. Evang. VI.11.64 (ed. J. A. Robinson 1893, p. 204)
- Fragment C: Origen, Philocalia XXIII.19 (ed. J. A. Robinson 1893, p. 208)

Outputs:
  - static/docs/OrJos.xml (Grammateus DTD)
  - static/docs/tei/OrJos.xml (TEI P5 parallel segmentation)
"""

import os
import subprocess

FRAGMENTS = [
    {
        "frag_num": 1,
        "title": "Fragmentum A (Origenes, Comm. in Joh. II.31.188-190)",
        "source": "Origenes, Commentarius in Johannem II.31.188-190 (ed. E. Preuschen, GCS 10, 1903, pp. 88-89; CPG 1453)",
        "units": [
            {
                "v": 1,
                "grc": "Ὁ γὰρ λαλῶν πρὸς ὑμᾶς ἐγὼ Ἰακὼβ καὶ Ἰσραήλ, ἄγγελος θεοῦ εἰμι ἐγὼ καὶ πνεῦμα ἀρχικόν, καὶ Ἀβραὰμ καὶ Ἰσαὰκ προεκτίσθησαν πρὸ παντὸς ἔργου.",
                "en": "For I, Jacob, who speak to you, and Israel, I am an angel of God and a principal spirit, and Abraham and Isaac were created before every work."
            },
            {
                "v": 2,
                "grc": "ἐγὼ δὲ Ἰακώβ, ὁ κληθεὶς ὑπὸ ἀνθρώπων Ἰακώβ, τὸ δὲ ὄνομά μου Ἰσραήλ, ὁ κληθεὶς ὑπὸ θεοῦ Ἰσραήλ, ἀνὴρ ὁρῶν θεόν, ὅτι ἐγὼ πρωτόγονος παντὸς ζῴου ζωουμένου ὑπὸ θεοῦ.",
                "en": "And I, Jacob, whom men call Jacob, but my name is Israel, called by God Israel, a man seeing God, because I am the firstborn of every creature animated by God."
            },
            {
                "v": 3,
                "grc": "Ἐγὼ δὲ ὅτε ἠρχόμην ἀπὸ Μεσοποταμίας τῆς Συρίας, ἐξῆλθεν Οὐριὴλ ὁ ἄγγελος τοῦ θεοῦ, καὶ εἶπεν ὅτι κατέβην ἐπὶ τὴν γῆν καὶ κατεσκήνωσα ἐν ἀνθρώποις, καὶ ὅτι ἐκλήθην ὀνόματι Ἰακώβ.",
                "en": "And when I was coming from Mesopotamia of Syria, Uriel the angel of God came forth and said that I had descended to earth and tabernacled among men, and that I was called by the name of Jacob."
            },
            {
                "v": 4,
                "grc": "ἐζήλωσε καὶ ἐμαχέσατό μοι, καὶ ἐπάλαιε πρός με, λέγων προτερήσειν ἐπάνω τοῦ ὀνόματός μου τὸ ὄνομα αὐτοῦ καὶ τοῦ πρὸ παντὸς ἀγγέλου.",
                "en": "He envied me and fought with me and wrestled against me, asserting that his name should have precedence over my name and over the angel before all."
            },
            {
                "v": 5,
                "grc": "καὶ εἶπα αὐτῷ τὸ ὄνομα αὐτοῦ καὶ πόσος ἐστὶν ἐν υἱοῖς θεοῦ· Οὐχὶ σὺ Οὐριὴλ ὄγδοος ἐμοῦ, κἀγὼ Ἰσραὴλ ἀρχάγγελος δυνάμεως κυρίου καὶ ἀρχιχιλίαρχός εἰμι ἐν υἱοῖς θεοῦ;",
                "en": "And I told him his name and how great he was among the sons of God: Are you not Uriel, the eighth after me? And am I not Israel, an archangel of the power of the Lord and a chief captain among the sons of God?"
            },
            {
                "v": 6,
                "grc": "οὐχὶ ἐγὼ Ἰσραὴλ ὁ ἐν προσώπῳ θεοῦ λειτουργὸς πρῶτος, καὶ ἐπεκαλεσάμην ἐν ὀνόματι ἀσβέστῳ τὸν θεόν μου;",
                "en": "Am I not Israel, the first minister before the face of God, and did I not invoke my God by an inextinguishable name?"
            }
        ]
    },
    {
        "frag_num": 2,
        "title": "Fragmentum B (Origenes, Philocalia XXIII.15 / Eusebius, Praep. Evang. VI.11.64)",
        "source": "Origenes, Philocalia XXIII.15 (ed. J. A. Robinson 1893, p. 204; CPG 1502) / Eusebius, Praeparatio Evangelica VI.11.64 (ed. K. Mras 1954; CPG 3486)",
        "units": [
            {
                "v": 1,
                "grc": "Διόπερ ἐν τῇ Προσευχῇ τοῦ Ἰωσὴφ δύναται οὕτω νοεῖσθαι τὸ λεγόμενον ὑπὸ τοῦ Ἰακώβ· Ἀνέγνων γὰρ ἐν ταῖς πλαξὶ τοῦ οὐρανοῦ ὅσα συμβήσεται ὑμῖν καὶ τοῖς υἱοῖς ὑμῶν.",
                "en": "Wherefore in the Prayer of Joseph that which is spoken by Jacob can be understood thus: 'For I read in the tablets of heaven whatsoever shall befall you and your sons.'"
            }
        ]
    },
    {
        "frag_num": 3,
        "title": "Fragmentum C (Origenes, Philocalia XXIII.19)",
        "source": "Origenes, Philocalia XXIII.19 (ed. J. A. Robinson 1893, p. 208; CPG 1502)",
        "units": [
            {
                "v": 1,
                "grc": "Καὶ ἄλλως δὲ ὁ Ἰακὼβ μείζων ἢ κατὰ ἄνθρωπον ἦν, πτερνίζων τὸν ἀδελφὸν αὐτοῦ, καὶ ὁμολογῶν ἐν αὐτῇ ταύτῃ τῇ βίβλῳ ἀφ’ ἧς παρεθέμεθα τό· Ἀνέγνων ἐν ταῖς πλαξὶ τοῦ οὐρανοῦ· εἶναι ἀρχιχιλίαρχος δυνάμεως κυρίου, καὶ ὄνομα πάλαι κεκτημένος Ἰσραήλ· ὅπερ ἐν σώματι λειτουργῶν ἀναγνωρίζει, ὑπομιμνήσκοντος αὐτὸν τοῦ ἀρχαγγέλου Οὐριήλ.",
                "en": "Moreover, Jacob was greater than a mere human being, supplanting his brother and confessing in this very book from which we cited, 'I read in the tablets of heaven,' that he was a chief captain of the power of the Lord, and having of old acquired the name Israel, which while serving in the body he recognized, when the archangel Uriel reminded him."
            }
        ]
    }
]

def build_grammateus_xml():
    bib = ("Origen, Commentarius in Johannem II.31.188-190 (ed. E. Preuschen, GCS 10, 1903, pp. 88-89); "
           "Philocalia XXIII.15, 19 (ed. J. A. Robinson, 1893, pp. 204, 208); "
           "Eusebius, Praeparatio Evangelica VI.11.64 (ed. K. Mras, 1954). CAVT 107 / CANT 351.")
    
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="OrJos" title="Prayer of Joseph">',
        '  <version author="Origen / Eusebius" language="Greek" title="Greek and English">',
        '    <divisions>',
        '      <division delimiter="." label="Fragment"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Orig" language="Greek" show="yes">',
        '        <name>Patristic Citations (Origen / Eusebius)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>'
    ]
    
    unit_id = 0
    for frag in FRAGMENTS:
        f_num = frag["frag_num"]
        lines.append(f'      <div number="{f_num}">')
        for u in frag["units"]:
            clean_grc = u["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            clean_en = u["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'        <div number="{u["v"]}">')
            lines.append(f'          <unit id="{unit_id}">')
            lines.append(f'            <reading option="0" mss="Orig ">{clean_grc}</reading>')
            lines.append(f'            <reading option="1" mss="Trans ">{clean_en}</reading>')
            lines.append('          </unit>')
            lines.append('        </div>')
            unit_id += 1
        lines.append('      </div>')
    
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')
    
    out_path = 'static/docs/OrJos.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path} ({unit_id} units)')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Prayer of Joseph (Oratio Josephi)</title>',
        '        <author>Anonymous</author>',
        '        <editor>Erwin Preuschen; J. Armitage Robinson</editor>',
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
        '            <title level="m">Origenes Werke IV (Der Johanneskommentar) / The Philocalia of Origen</title>',
        '            <editor>E. Preuschen; J. A. Robinson</editor>',
        '            <imprint>',
        '              <publisher>J. C. Hinrichs / Cambridge University Press</publisher>',
        '              <date when="1903">1893-1903</date>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>'
    ]
    
    for frag in FRAGMENTS:
        f_num = frag["frag_num"]
        lines.append(f'      <div type="fragment" n="{f_num}">')
        lines.append(f'        <head>{frag["title"]}</head>')
        for u in frag["units"]:
            clean_grc = u["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            clean_en = u["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'        <p n="{u["v"]}">')
            lines.append('          <app>')
            lines.append(f'            <rdg wit="#Origen" xml:lang="grc">{clean_grc}</rdg>')
            lines.append(f'            <rdg type="translation" xml:lang="en">{clean_en}</rdg>')
            lines.append('          </app>')
            lines.append('        </p>')
        lines.append('      </div>')
        
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')
    
    out_path = 'static/docs/tei/OrJos.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
    # Also run grammateus_to_tei to ensure perfect OCP TEI format
    subprocess.run(['python3', 'scripts/grammateus_to_tei.py', 'static/docs/OrJos.xml', '-o', 'static/docs/tei/OrJos.xml'], check=True)
