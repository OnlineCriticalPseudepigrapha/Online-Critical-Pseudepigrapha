#!/usr/bin/env python3
"""
Build Andronicus and Asaph the Historian of the Hebrews (Zodiac of the Patriarchs)
Syriac text and English translation from:
Alphonse Mingana, Some Early Judæo-Christian Documents in the John Rylands Library
(Manchester: The University Press, 1917), pp. 32-35 (translation), 62-64 (Syriac text).
Outputs:
  - static/docs/AndronAsaph.xml (Grammateus DTD)
  - static/docs/tei/AndronAsaph.xml (TEI P5 parallel segmentation)
"""

VERSES = [
    (
        "ܬܘܒ ܡܡܠܠܐ ܕܥܠ ܝܒ ܣܛܘܟܣ̈ܐ ܕܫܡܫܐ ܕܥܒܝܕ ܠܐܢܕܪܘܢܝܩܘܣ ܚܟܝܡܐ ܘܦܝܠܣܘܦܐ ܘܡܗܝܪܐ.",
        "Again a discourse upon the twelve stoicheia of the sun, written by Andronicus the Wise, the Philosopher and the learned."
    ),
    (
        "ܡܛܠ ܕܝܢ ܕܙܕܩ ܕܒܟܠܙܒܢ ܢܬܥܗܕܘܢ ܘܢܣܬܟܠܘܢ ܪ̈ܚܡܝ ܫܪܪܐ ܒܐܝܠܝܢ ܕܫܦܝܪ̈ܢ ܘܡܝܬܪ̈ܢ: ܐܦ ܡܢܗܪ̈ܢ ܬܪܥܝܬܐ ܕܐܝܠܝܢ ܕܒܥܝܢ ܠܗܝܢ: ܐܬܒܛܠ ܠܢ ܐܚ̈ܝ ܠܡܚܘܝܘ ܩܕܡܝܟܘܢ ܐܦ ܗܕܐ ܕܐܝܬܝܗ̇ ܒܥܬܐ ܡܝܬܪܬܐ ܒܪܗܛܐ ܕܕܘܒܪܗ.",
        "Because the lovers of truth must always remember and understand the good and prominent things which enlighten the mind of those who seek after them, I have been anxious, my brethren, to lay down before you the prominent question of the evolution of the course of (the sun),"
    ),
    (
        "ܗܢܘ ܕܝܢ ܬܚܘܡܐ ܘܙܒܢܐ ܘܪܗܛܐ ܟܠܗ ܕܝܘܒܠܗ: ܘܣܗܪܐ ܒܟܠܗܘܢ ܝܘ̈ܡܘܗܝ: ܘܡܥܒܕܢܘܬܐ ܕܬܪܥܣܪ ܣܛܘܟܣ̈ܐ ܗܿܢܘܢ ܕܟܪܟܝܢ ܒܡܢܝܢܐ ܕܬܪܥܣܪ ܝܪ̈ܚܝܢ ܕܫܢ݇ܬܐ: ܘܡܩܕܡܝܢ ܘܡܘܕܥܝܢ ܥܠ ܐܝܠܝܢ ܕܥܬܝܕܢ ܠܡܗܘܐ ܠܘܬܢ ܒܦܘܩܕܢ ܐܠܗܐ ܥܒܘܕܐ ܕܟܠ.",
        "that is to say the limits, the times and all the course of its succession with the days of the moon and the influence of the twelve stoicheia which gravitate circuitously in the number of the twelve months of the year, and which foretell events which happen to us by order of God, creator of everything."
    ),
    (
        "ܟܕ ܡܬܕܠܝܢ ܡܢ ܠܗܿܢܘܢ ܣܛܘܟܣ̈ܐ ܒܝܬ ܝܘܢܝ̈ܐ: ܕܫܡܗ̈ܝܗܘܢ ܘܩܢܘܡ̈ܝܗܘܢ ܬܚܡܘ ܘܣܡܘ ܘܚܘܝܘ: ܟܕ ܟܢܝܘ ܐܢܘܢ ܥܠ ܫܡܗ̈ܐ ܕܐܠܗ̈ܝܗܘܢ.",
        "In investigating these stoicheia the Greeks have defined and shown their names and their entities. They have called them by the names of their gods,"
    ),
    (
        "ܘܪܕܝܢ ܚܕ ܒܬܪ ܚܕ ܒܛܘܟܣܗܘܢ ܕܗܠܝܢ ܩܢܘܢܣ ܕܡܢܝܢܐ ܕܝܢ ܕܝܘ̈ܡܬܐ ܕܝܪ̈ܚܐ: ܗܢܘ ܕܝܢ ܒܚܘܫܒܢܐ ܕܣܗܪܐ.",
        "and they follow one another in the order of the canones of the numbers of the days of the months, that is to say according to the lunar computation."
    ),
    (
        "ܟܕ ܡܫܪܝܢ ܩܕܡܝܐ ܡܢ ܕܝܘܣ ܒܪ ܩܪܢܘܣ ܘܩܪܝܢ ܠܗ ܕܟܪܐ: ܘܒܬܪܗ ܦܘܣܝܕܘܢ ܐܚܘܗܝ ܘܩܪܝܢ ܠܗ ܢܘܢ̈ܐ: ܘܒܬܪܗ ܕܗܢܐ ܐܡܪܝܢ ܐܦܠܘܢ ܘܒܬܪܗ ܕܘܠܐ.",
        "They begin with Dios son of Cronus, and they call him Aries (the Ram). After him comes Poseidon his brother whom they call Pisces (the Fish). After him they say Apollo, and after him Aquarius (the Water-carrier)."
    ),
    (
        "ܘܒܬܪܗ ܕܗܢܐ ܣܝܡܝܢ ܐܪܝܣ ܘܩܪܝܢ ܠܗ ܟܠܒܐ ܕܡܝ̈ܐ: ܒܕܝܠܢ ܕܝܢ ܐܝܠܐ ܗ݇ܘܼ: ܘܡ̣ܢ ܒܬܪܗ ܐܡܪܝܢ ܐܪܡܝܣ ܘܠܗ ܩܪܝܢ ܟܝܪܘܢ.",
        "After this they put Ares, whom they call 'Dog of Water,' but with us it is Capricornus (the Goat). After him they say Hermes, whom they call Chiron (Sagittarius)."
    ),
    (
        "ܘܒܬܪ ܗܢܐ ܐܡܪܝܢ ܦܠܘܛܘܢ ܘܩܪܝܢ ܠܗ ܥܩܪܒܐ: ܘܒܬܪ ܗܢܐ ܐܡܪܝܢ ܐܬܢܐ ܘܩܪܝܢ ܠܗ ܡܣܐܬܐ: ܘܒܬܪ ܗܢܐ ܣܝܡܝܢ ܐܦܪܘܕܝܛܝ ܘܩܪܝܢ ܠܗ̇ ܒܬܘܠܬܐ ܐܘ ܫܒܠܬܐ.",
        "After this they say Pluto, whom they call Scorpio. After this they say Athena, whom they call Libra (the Balance). After this they put Aphrodite, whom they call Virgo who is Spica (the Ear of Corn)."
    ),
    (
        "ܘܡ̣ܢ ܒܬܪܗ ܐܡܪܝܢ ܐܪܛܡܝܣ ܘܠܗ̇ ܡܟܢܝܢ ܐܪܝܐ: ܘܡ̣ܢ ܒܬܪܗ̇ ܐܡܪܝܢ ܕܝܘܢܘܣܝܘܣ ܘܩܪܝܢ ܠܗ ܣܪܛܢܐ.",
        "After this they say Artemis, whom they call Leo (the Lion). After this they say Dionysus, whom they call Cancer (the Crab)."
    ),
    (
        "ܘܒܬܪܗ ܕܝܣܩܘܪܘ ܘܠܗ ܩܪܝܢ ܩܐܣܛܘܪ ܘܦܘܠܘܕܘܟܣ ܕܐܝܬܝܗܘܢ ܒܢܝ̈ ܙܐܘܣ ܡ̣ܢ ܠܝܕܐ ܘܩܪܝܢ ܠܗܘܢ ܬܐܘܡ̈ܐ: ܘܒܬܪܗܘܢ ܗܪܩܠܝܣ: ܘܠܗܢܐ ܩܪܝܢ ܬܘܪܐ.",
        "After this come the Dioscuri, called Castor and Pollux, sons of Zeus by Leda, and they call them Gemini (the Twins). After them comes Hercules, and this they call Taurus (the Bull)."
    ),
    (
        "ܬܫܥܝܬܗܘܢ ܕܗܠܝܢ ܢܗܝܪܐܝܬ ܡܦܫܩ ܐܦ ܡܠܦ ܐܣܦ ܣܦܪܐ ܡܥܗܕܢܐ ܕܥܒܪ̈ܝܐ: ܟܕ ܠܐ ܗ݇ܘܼܐ ܒܫܡܗ̈ܐ ܕܝܘܢܝ̈ܐ ܪܫܡ ܘܡܚܘܐ: ܐܠܐ ܥܠ ܡܢܝܢܐ ܕܫܡܗ̈ܐ ܕܒܢܝ̈ ܝܥܩܘܒ.",
        "Asaph the writer and the historian of the Hebrews explains and teaches clearly the history of all these, but does not write and show them with Greek names, but according to the names of the sons of Jacob."
    ),
    (
        "ܓܒܘܪܘܬܐ ܕܝܢ ܘܟܠܗ̇ ܡܥܒܕܢܘܬܗܘܢ ܕܝܠܗܘܢ ܕܣܛܘܟܣ̈ܐ ܗܠܝܢ ܫܘܝܐܝܬ ܐܡܪ ܐܦ ܗܘܼ: ܟܕ ܡܕܡ ܠܐ ܡܘܣܦ ܐܘ ܡܒܨܪ: ܐܠܐ ܐܢ ܟܕ ܡܫܚܠܦ ܫܡܗ̈ܝܗܘܢ ܠܕܐܒܗ̈ܬܐ ܒܡܠܬܐ ܓܠܝܬܐ.",
        "As to the effects and influences of these stoicheia he, too, enumerates them fully without adding or diminishing anything, but in simply changing in a clear language their names into those of the Patriarchs."
    ),
    (
        "ܟܕ ܡܫܪܐ ܐܦ ܗܘܼ ܐܪܡܐܝܬ: ܘܣܐܡ ܒܪܫܐ ܬܘܪܐ ܘܡܫܡܗ ܪܘܒܝܠ: ܘܒܬܪܗ ܐܡܪܐ ܘܩܪܝܢ ܠܗ ܫܡܥܘܢ: ܘܒܬܪܗ ܢܘܢ̈ܐ ܘܩܪܝܢ ܠܗ ܠܘܝ: ܘܒܬܪܗ ܕܘܠܐ ܘܩܪܝܢ ܠܗ ܐܝܣܟܪ.",
        "He begins them in the Aramaic language and puts at the head Taurus, which he calls 'Reuben'. After it comes Aries, which they call 'Simeon'. After it comes Pisces, which they call 'Levi'. After it comes Aquarius, which they call 'Issachar'."
    ),
    (
        "ܘܒܬܪܗ ܣܝܡ ܓܕܝܐ ܘܠܗ ܩܪܝܢ ܢܦܬܠܝ: ܘܡ̣ܢ ܒܬܪܗ ܪܫܡ ܪܟܒܐ ܟܕ ܩܫܝܕ ܘܩܪܐ ܠܗ ܓܕ: ܘܗܢܘ ܕܝܢ ܟܝܪܘܢ ܕܝܘܢܝ̈ܐ.",
        "After it he puts Capricornus, which they call 'Naphtali'. After it he sketches a rider while shooting, and calls him 'Gad,' and he is the Chiron of the Greeks."
    ),
    (
        "ܘܡ̣ܢ ܒܬܪܗ ܥܩܪܒܐ ܘܠܗ ܩܪܐ ܕܢ: ܡ̣ܢ ܒܬܪܗ ܐܡܪ ܡܣܐܬܐ ܘܩܪܐ ܠܗ̇ ܐܫܝܪ: ܘܬܘܒ ܐܡܪ ܒܬܘܠܬܐ ܘܩܪܐ ܠܗ̇ ܕܝܢܐ: ܘܒܬܪܗ̇ ܐܪܝܐ ܘܩܪܐ ܠܗ ܝܗܘܕܐ: ܘܬܘܒ ܪܫܡ ܣܪܛܢܐ ܘܩܪܐ ܠܗ ܙܒܘܠܘܢ: ܘܒܬܪ ܗܢܐ ܐܡܪ ܬܐܡܐ ܘܩܪܐ ܠܗܘܢ ܐܦܪܝܡ ܘܡܢܫܐ.",
        "After it comes Scorpio, which he calls 'Dan'. After it he mentions Libra, which he calls 'Asher'. After it he mentions Virgo, whom he calls 'Dinah'. After it comes Leo, which he calls 'Judah'. Then he sketches Cancer, which he calls 'Zebulun'. After this he mentions Gemini, whom he calls 'Ephraim' and 'Manasseh'."
    ),
    (
        "ܟܕ ܗܟܝܠ ܒܗܠܝܢ ܕܗܟܢ ܐܬܟܢܝܘ ܒܡܢܝܢܐ ܕܝܘ̈ܡܬܐ ܬܫܟܚܘܢ ܘܬܣܬܟܠܘܢ ܐܝܟ ܪ̈ܚܡܝ ܫܪܪܐ: ܐܡܪ ܐܢܐ ܕܐܢܗܘܼ ܘܐܦ ܢܣܬܩܒܠ ܘܩܠܐ ܕܪܥܡܐ ܢܫܬܡܥ.",
        "As lovers of truth you will see and understand that these (stoicheia) have been named according to the number of days (of lunar computation). I say this, even if it happens that the peal of thunder is heard (in them)."
    ),
    (
        "ܒܟܠ ܝܪܚ ܫܢ݇ܬܐ ܒܟܠ ܚܕ ܡ̣ܢ ܣܛܘܟܣ̈ܐ: ܟܕ ܟܪܟܝܢ ܒܓܘ ܩܢܘܢܣ ܕܝܠܗܘܢ ܕܝܪ̈ܚܐ: ܘܪܗܛܝܢ ܒܡܢܝܢܗ ܕܣܗܪܐ: ܘܡܫܬܡܫܝܢ ܟܠ ܚܕ ܡܢܗܘܢ ܒܬܠܬܐ ܩܢܘܢܣ ܕܝܘܒܠܗ ܕܝܠܗ ܕܣܗܪܐ: ܕܗܕܐ ܗܝ ܬܚܘܝܬܗܘܢ ܘܛܘܟܣܗܘܢ ܘܟܠܗ̇ ܣܝܡܬܕܘܟܬܗܘܢ ܗܝ ܕܡܘܕܥܐ ܠܘܬܢ.",
        "At each month of the year, each one of the stoicheia turns circuitously according to the canones of the months and gravitates according to the number of the moons, each one of them having been brought about by the three canones of the evolution of the moon. This is their exposition, their order, and all their influence of which we are aware."
    )
]

def build_grammateus_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE document SYSTEM "document.dtd">',
        '<document id="AndronAsaph">',
        '    <header>',
        '        <title>Fragment of Andronicus and Asaph the Historian of the Hebrews</title>',
        '        <author>Andronicus / Asaph (Pseudepigraphon)</author>',
        '        <editor>Alphonse Mingana (1917)</editor>',
        '        <description>Syriac text and English translation from Some Early Judæo-Christian Documents in the John Rylands Library (Manchester: The University Press, 1917), pp. 32-35, 62-64. Ancient discourse on the twelve stoicheia of the Zodiac correlating the Greek astrological figures with the twelve sons of Jacob / tribes of Israel according to Asaph the Hebrew historian.</description>',
        '    </header>',
        '    <body>'
    ]
    for v_num, (syr, en) in enumerate(VERSES, 1):
        lines.append(f'        <div c="1" v="{v_num}">')
        lines.append(f'            <line lang="syr">{syr}</line>')
        lines.append(f'            <line lang="en">{en}</line>')
        lines.append('        </div>')
    lines.append('    </body>')
    lines.append('</document>\n')
    
    out_path = 'static/docs/AndronAsaph.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path}')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Fragment of Andronicus and Asaph the Historian of the Hebrews</title>',
        '        <author>Andronicus / Asaph (Pseudepigraphon)</author>',
        '        <editor>Alphonse Mingana</editor>',
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
        '            <title level="m">Some Early Judæo-Christian Documents in the John Rylands Library</title>',
        '            <editor>Alphonse Mingana</editor>',
        '            <imprint>',
        '              <publisher>The University Press</publisher>',
        '              <pubPlace>Manchester</pubPlace>',
        '              <date when="1917">1917</date>',
        '              <biblScope unit="page">32-35, 62-64</biblScope>',
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
    for v_num, (syr, en) in enumerate(VERSES, 1):
        lines.append(f'        <p n="{v_num}">')
        lines.append(f'          <app>')
        lines.append(f'            <rdg wit="#Mingana1917" xml:lang="syr">{syr}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
        lines.append(f'          </app>')
        lines.append(f'        </p>')
    lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')
    
    out_path = 'static/docs/tei/AndronAsaph.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
