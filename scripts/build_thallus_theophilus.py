#!/usr/bin/env python3
"""
Build Thallus the Chronographer (FGrH 256 / Denis PVTG 3, pp. 261-267)
and Theophilus (FGrH 733 / Denis PVTG 3, pp. 203-207)
Outputs:
  - static/docs/Thallus.xml & static/docs/tei/Thallus.xml
  - static/docs/Theoph.xml & static/docs/tei/Theoph.xml
"""

THALLUS_FRAGMENTS = [
    {
        "c": 1,
        "v": 1,
        "grc": "καθ᾽ ὅλου τοῦ κόσμου σκοτία ἐγένετο φοβερωτάτη, σεισμῷ τε αἱ πέτραι διερρήγνυντο, καὶ τὰ πολλὰ Ἰουδαίας καὶ τῆς ἄλλης γῆς κατερρίφη. τοῦτο τὸ σκότος ἔκλειψιν ἡλίου Θάλλος ἀποκαλεῖ ἐν τρίτῃ τῶν ἱστοριῶν, ὡς ἐμοὶ δοκεῖ, ἀλόγως.",
        "en": "Over the whole world there fell a most terrible darkness, and by earthquake rocks were rent, and much of Judaea and the rest of the earth was thrown down. This darkness Thallus calls an eclipse of the sun in the third book of his Histories, without reason, as it seems to me."
    },
    {
        "c": 1,
        "v": 2,
        "grc": "Ἑβραῖοι γὰρ ἄγουσι τὸ πάσχα κατὰ σελήνην ιδʹ, τὰ δὲ περὶ τὸ πάθος τοῦ σωτῆρος πρὸ μιᾶς τοῦ πάσχα συμβαίνει· ἔκλειψις δὲ ἡλίου οὐκ ἂν ἄλλως γένοιτο, εἰ μὴ κατὰ σύνοδον σελήνης πρὸς ἥλιον· πῶς δὲ κατὰ διάμετρον οὔσης τῆς σελήνης ἔκλειψις νομισθείη; (Iulius Africanus, Chronogr. fr. 50 ap. Georg. Syncell. 610)",
        "en": "For the Hebrews celebrate the Passover on the fourteenth day of the moon, and the events of the Passion of the Savior occurred on the eve of the Passover; but an eclipse of the sun cannot happen except at the conjunction of the moon with the sun; how then could an eclipse be supposed to happen when the moon is diametrically opposed to the sun? (Julius Africanus, Chronogr. fr. 50)"
    },
    {
        "c": 2,
        "v": 1,
        "grc": "Θάλλος δὲ μέμνηται Βήλου τοῦ Ἀσσυρίων βασιλεύσαντος καὶ Κρόνου τοῦ Τιτᾶνος, φάσκων τὸν Βῆλον συμπεπολεμηκέναι τοῖς Τιτᾶσι πρὸς Δία καὶ τοὺς σὺν αὐτῷ θεούς, οὓς ἐπικαλεῖ, λέγων· καὶ Ὤγυγος ἡττηθεὶς ἔφυγεν εἰς Ἀκτὴν τότε καλουμένην, νῦν δὲ Ἀττικὴν προσαγορευομένην, ἧς ἐκράτησεν. (Theophilus Antiochenus, Ad Autolycum III.29)",
        "en": "Thallus mentions Belus the king of the Assyrians and Cronus the Titan, asserting that Belus fought along with the Titans against Zeus and the gods with him, whom he invokes, saying: 'And Ogygus, being defeated, fled to Acte then so-called, now named Attica, which he possessed.' (Theophilus of Antioch, Ad Autolycum III.29)"
    },
    {
        "c": 2,
        "v": 2,
        "grc": "καὶ τῶν λοιπῶν δὲ βασιλέων ὧν τὰ ὀνόματα καὶ αἱ κατὰ μέρος πράξεις ἀναγεγραμμέναι εἰσίν, πολλοῖς ἔτεσιν προάγει ὁ κατὰ τὸν Ὤγυγον κατακλυσμός. (Theophilus Antiochenus, Ad Autolycum III.29)",
        "en": "And of the remaining kings whose names and detailed deeds are recorded, the flood in the time of Ogygus antedates them by many years. (Theophilus of Antioch, Ad Autolycum III.29)"
    },
    {
        "c": 3,
        "v": 1,
        "grc": "ἦν δὲ καὶ Θάλλος σαμαρεὺς γένος, Καίσαρος δὲ ἀπελεύθερος, παρʼ οὗ δανείζεται ἑκατὸν μυριάδας, καὶ διαλύει τῇ Ἀντωνίᾳ τὸ χρέος, ταῖς δὲ λοιπαῖς θεραπεύει τὸν Γάϊον, οὐ μετρίως δυνατὸς ὢν ἤδη διὰ τὴν ἐκείνου τιμήν. (Flavius Josephus, Antiquitates Iudaicae XVIII.167)",
        "en": "Now there was also Thallus, a Samaritan by birth and a freedman of Caesar, from whom [Agrippa] borrowed a million drachmae, and repaid his debt to Antonia, and with the remainder paid court to Gaius, being already not a little influential through his favor. (Josephus, Antiquities XVIII.167)"
    }
]

THEOPHILUS_FRAGMENTS = [
    {
        "c": 1,
        "v": 1,
        "grc": "Θεόφιλος δὲ ἱστορεῖ Σολομῶνα τὸν βασιλέα πέμψαι τῷ Τυρίων βασιλεῖ εἰκόνα χρυσῆν, ἀνθʼ ἧς ἐκεῖνον περιθεῖναι τῷ ναῷ κίονα χρυσοῦν, ὃν καὶ ἐπικληθῆναι Χρυσοῦν Κίονα. (Alexander Polyhistor ap. Euseb. Praep. Evang. IX.34.19)",
        "en": "Theophilus relates that King Solomon sent to the king of the Tyrians a golden image, in return for which the latter overlaid a pillar for the Temple with gold, which was also named the Golden Pillar. (Alexander Polyhistor ap. Eusebius, Praep. Evang. IX.34.19)"
    }
]

def build_thallus():
    bib = "Felix Jacoby, Fragmente der griechischen Historiker (FGrH 256); Albert-Marie Denis, Fragmenta Pseudepigraphorum quae supersunt Graeca (PVTG 3; Leiden: Brill, 1970), pp. 261-267."
    # Grammateus
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Thallus" title="Fragments of Thallus the Chronographer">',
        '  <version author="Jacoby / Denis" language="Greek" title="Greek and English">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Denis" language="Greek" show="yes">',
        '        <name>Denis 1970 (PVTG 3) / Jacoby FGrH 256</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>'
    ]
    # Group by chapter
    ch_map = {}
    for frag in THALLUS_FRAGMENTS:
        ch_map.setdefault(frag["c"], []).append(frag)
    
    unit_id = 0
    for c in sorted(ch_map.keys()):
        lines.append(f'      <div number="{c}">')
        for frag in ch_map[c]:
            clean_grc = frag["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            clean_en = frag["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'        <div number="{frag["v"]}">')
            lines.append(f'          <unit id="{unit_id}">')
            lines.append(f'            <reading option="0" mss="Denis ">{clean_grc}</reading>')
            lines.append(f'            <reading option="1" mss="Trans ">{clean_en}</reading>')
            lines.append('          </unit>')
            lines.append('        </div>')
            unit_id += 1
        lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')
    
    with open('static/docs/Thallus.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote static/docs/Thallus.xml ({unit_id} units)')

    # TEI P5
    tei_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Fragments of Thallus the Chronographer</title>',
        '        <author>Thallus</author>',
        '        <editor>Felix Jacoby; Albert-Marie Denis</editor>',
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
        '            <title level="m">Fragmenta pseudepigraphorum quae supersunt graeca</title>',
        '            <editor>Albert-Marie Denis</editor>',
        '            <imprint>',
        '              <publisher>E. J. Brill</publisher>',
        '              <pubPlace>Leiden</pubPlace>',
        '              <date when="1970">1970</date>',
        '              <biblScope unit="page">261-267</biblScope>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>'
    ]
    current_c = 0
    for frag in THALLUS_FRAGMENTS:
        if frag["c"] != current_c:
            if current_c != 0:
                tei_lines.append('      </div>')
            current_c = frag["c"]
            tei_lines.append(f'      <div type="fragment" n="{current_c}">')
        tei_lines.append(f'        <p n="{frag["v"]}">')
        tei_lines.append('          <app>')
        tei_lines.append(f'            <rdg wit="#Denis1970" xml:lang="grc">{frag["grc"]}</rdg>')
        tei_lines.append(f'            <rdg type="translation" xml:lang="en">{frag["en"]}</rdg>')
        tei_lines.append('          </app>')
        tei_lines.append('        </p>')
    if current_c != 0:
        tei_lines.append('      </div>')
    tei_lines.append('    </body>')
    tei_lines.append('  </text>')
    tei_lines.append('</TEI>\n')

    with open('static/docs/tei/Thallus.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tei_lines))
    print('Wrote static/docs/tei/Thallus.xml')

def build_theophilus():
    bib = "Felix Jacoby, Fragmente der griechischen Historiker (FGrH 733); Albert-Marie Denis, Fragmenta Pseudepigraphorum quae supersunt Graeca (PVTG 3; Leiden: Brill, 1970), pp. 203-207."
    # Grammateus
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Theoph" title="Fragments of Theophilus">',
        '  <version author="Jacoby / Denis" language="Greek" title="Greek and English">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Denis" language="Greek" show="yes">',
        '        <name>Denis 1970 (PVTG 3) / Jacoby FGrH 733</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ]
    for v_num, frag in enumerate(THEOPHILUS_FRAGMENTS, 1):
        clean_grc = frag["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en = frag["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        lines.append(f'        <div number="{frag["v"]}">')
        lines.append(f'          <unit id="{v_num-1}">')
        lines.append(f'            <reading option="0" mss="Denis ">{clean_grc}</reading>')
        lines.append(f'            <reading option="1" mss="Trans ">{clean_en}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')
    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')
    
    with open('static/docs/Theoph.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote static/docs/Theoph.xml ({len(THEOPHILUS_FRAGMENTS)} units)')

    # TEI P5
    tei_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Fragments of Theophilus</title>',
        '        <author>Theophilus</author>',
        '        <editor>Felix Jacoby; Albert-Marie Denis</editor>',
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
        '            <title level="m">Fragmenta pseudepigraphorum quae supersunt graeca</title>',
        '            <editor>Albert-Marie Denis</editor>',
        '            <imprint>',
        '              <publisher>E. J. Brill</publisher>',
        '              <pubPlace>Leiden</pubPlace>',
        '              <date when="1970">1970</date>',
        '              <biblScope unit="page">203-207</biblScope>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>',
        '      <div type="fragment" n="1">'
    ]
    for frag in THEOPHILUS_FRAGMENTS:
        tei_lines.append(f'        <p n="{frag["v"]}">')
        tei_lines.append('          <app>')
        tei_lines.append(f'            <rdg wit="#Denis1970" xml:lang="grc">{frag["grc"]}</rdg>')
        tei_lines.append(f'            <rdg type="translation" xml:lang="en">{frag["en"]}</rdg>')
        tei_lines.append('          </app>')
        tei_lines.append('        </p>')
    tei_lines.append('      </div>')
    tei_lines.append('    </body>')
    tei_lines.append('  </text>')
    tei_lines.append('</TEI>\n')

    with open('static/docs/tei/Theoph.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tei_lines))
    print('Wrote static/docs/tei/Theoph.xml')

if __name__ == '__main__':
    build_thallus()
    build_theophilus()
