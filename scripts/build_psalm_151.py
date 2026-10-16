#!/usr/bin/env python3
"""
Build Psalm 151 (CAVT 202 / CANT 151)
Parallel Tri-Lingual Edition:
- Hebrew: 11QPs-a (11Q5) Col. xxviii 3-14 (Psalms 151A and 151B, ed. J. A. Sanders, DJD IV, 1965)
- Greek: Septuagint Psalm 151 (Rahlfs 1935 / Swete 1896)
- Latin: Clementine Vulgate Appendix (Psalmus CLI)

Outputs:
  - static/docs/Ps151.xml (Grammateus DTD)
  - static/docs/tei/Ps151.xml (TEI P5 parallel segmentation)
"""

import os
import subprocess

# Standard 7 verses according to LXX and Vulgate
# Aligned with 11Q5 Hebrew Psalm 151A and 151B
VERSES = [
    {
        "v": 1,
        "heb": "הללויה לדויד בן ישי. קטן הייתי מן אחי וצעיר מבני אבי, וישימני רועה לצונו ומושל בגדיותיו.",
        "grc": "Οὗτος ὁ ψαλμὸς ἰδιόγραφος εἰς Δαυιδ καὶ ἔξωθεν τοῦ ἀριθμοῦ· ὅτε ἐμονομάχησεν τῷ Γολιαδ. Μικρὸς ἤμην ἐν τοῖς ἀδελφοῖς μου καὶ νεώτερος ἐν τῷ οἴκῳ τοῦ πατρός μου· ἐποίμαινον τὰ πρόβατα τοῦ πατρός μου.",
        "lat": "Hic psalmus proprie scriptus est David, et extra numerum, cum pugnavit cum Goliath. Pusillus eram inter fratres meos, et adolescentior in domo patris mei: pascebam oves patris mei.",
        "en": "This psalm is a genuine one of David, though an extra, composed when he fought in single combat with Goliath. I was small among my brothers, and the youngest in my father's house; I tended my father's sheep."
    },
    {
        "v": 2,
        "heb": "ידי עשו עוגב ואצבעותי כנור, ואשימה ליהוה כבוד אמרתי אני בנפשי.",
        "grc": "αἱ χεῖρές μου ἐποίησαν ὄργανον, οἱ δάκτυλοί μου ἥρμοσαν ψαλτήριον.",
        "lat": "Manus meae fecerunt organum: et digiti mei aptaverunt psalterium.",
        "en": "My hands made an instrument, and my fingers fashioned a lyre."
    },
    {
        "v": 3,
        "heb": "ההרים לוא יעידו לו והגבעות לוא יגידו, העצים את דברי והצואן את מעשי. כי מי יגיד ומי ידבר ומי יספר את מעשי? אדון הכול ראה, אלוה הכול הוא שמע והוא האזין.",
        "grc": "καὶ τίς ἀναγγελεῖ τῷ κυρίῳ μου; αὐτὸς κύριος, αὐτὸς εἰσακούει.",
        "lat": "Et quis annuntiabit Domino meo? Ipse Dominus, ipse omnium exaudit.",
        "en": "And who will declare it to my Lord? The Lord himself, he hears."
    },
    {
        "v": 4,
        "heb": "שלח נביאו למושחני, את שמואל לגדלני. וישלח ויקחני מאחר הצואן, וימשחני בשמן הקודש, וישימני נגיד לעמו ומושל בבני בריתו.",
        "grc": "αὐτὸς ἐξαπέστειλεν τὸν ἄγγελον αὐτοῦ καὶ ἦρέν με ἐκ τῶν προβάτων τοῦ πατρός μου καὶ ἔχρισέν με ἐν τῷ ἐλαίῳ τῆς χρίσεως αὐτοῦ.",
        "lat": "Ipse misit angelum suum, et tulit me de ovibus patris mei, et unxit me in misericordia unctionis suae.",
        "en": "He sent forth his angel and took me from my father's sheep, and anointed me with the oil of his anointing."
    },
    {
        "v": 5,
        "heb": "יצאו אחי לקראתו יפי התואר ויפי המראה, הגבהים בקומתם היפים בשערם: לוא בחר יהוה אלוהים בם.",
        "grc": "οἱ ἀδελφοί μου καλοὶ καὶ μεγάλοι, καὶ οὐκ εὐδόκησεν ἐν αὐτοῖς κύριος.",
        "lat": "Fratres mei boni, et magni: et non fuit beneplacitum in eis Domino.",
        "en": "My brothers were handsome and tall, but the Lord took no pleasure in them."
    },
    {
        "v": 6,
        "heb": "תחלת גבורה לדויד משמשחו נביא אלוהים: אז ראיתי פלשתי מחרף מערכות ישראל, יצאתי לקראתו והוא קללני באליליו.",
        "grc": "ἐξῆλθον εἰς συνάντησιν τῷ ἀλλοφύλῳ, καὶ ἐπικατηράσατό με ἐν τοῖς εἰδώλοις αὐτοῦ·",
        "lat": "Exivi obviam alienigenae, et maledixit mihi in simulacris suis.",
        "en": "I went out to meet the Philistine, and he cursed me by his idols."
    },
    {
        "v": 7,
        "heb": "ואנוכי שלפתי את חרבו מלפניו, ואכרות את ראשו, ואסיר חרפה מבני ישראל.",
        "grc": "ἐγὼ δὲ σπασάμενος τὴν παρ’ αὐτοῦ μάχαιραν ἀπεκεφάλισα αὐτὸν καὶ ἦρα ὄνειδος ἐξ υἱῶν Ισραηλ.",
        "lat": "Ego autem evaginato gladio ipsius, decapitavi eum, et abstuli opprobrium de filiis Israel.",
        "en": "But I, drawing his own sword, beheaded him, and removed the reproach from the sons of Israel."
    }
]

def build_grammateus_xml():
    bib_heb = "11QPs-a (11Q5) Col. xxviii 3-14: J. A. Sanders, The Psalms Scroll of Qumrân Cave 11 (11QPs-a) (DJD IV; Oxford: Clarendon Press, 1965), pp. 53-64."
    bib_grc = "Septuaginta: Alfred Rahlfs, Septuaginta (Stuttgart: Privilegierte Württembergische Bibelanstalt, 1935); H. B. Swete, The Old Testament in Greek according to the Septuagint, Vol. II (Cambridge: Cambridge University Press, 1896)."
    bib_lat = "Biblia Sacra Vulgata (Clementina), Appendix: Psalmus CLI."

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Ps151" title="Psalm 151 (Hebrew, Greek, Latin)">',
        '  <version author="Qumran, Septuagint, Vulgate" language="Hebrew" title="Polyglot (Hebrew, Greek, Latin)">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="11Q5" language="Hebrew" show="yes">',
        '        <name>11QPs-a (Qumran Cave 11)</name>',
        f'        <bibliography>{bib_heb}</bibliography>',
        '      </ms>',
        '      <ms abbrev="LXX" language="Greek" show="yes">',
        '        <name>Septuaginta (Rahlfs / Swete)</name>',
        f'        <bibliography>{bib_grc}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Vulg" language="Latin" show="yes">',
        '        <name>Biblia Sacra Vulgata (Clementina)</name>',
        f'        <bibliography>{bib_lat}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib_grc}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ]

    for item in VERSES:
        v_num = item["v"]
        clean_heb = item["heb"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_grc = item["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_lat = item["lat"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en  = item["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        lines.append(f'        <div number="{v_num}">')
        lines.append(f'          <unit id="{v_num-1}">')
        lines.append(f'            <reading option="0" mss="11Q5 ">{clean_heb}</reading>')
        lines.append(f'            <reading option="1" mss="LXX ">{clean_grc}</reading>')
        lines.append(f'            <reading option="2" mss="Vulg ">{clean_lat}</reading>')
        lines.append(f'            <reading option="3" mss="Trans ">{clean_en}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')

    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')

    out_path = 'static/docs/Ps151.xml'
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
        '        <title>Psalm 151 (Hebrew, Greek, Latin)</title>',
        '        <author>David (Pseudepigraphon)</author>',
        '        <editor>J. A. Sanders; Alfred Rahlfs</editor>',
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
        '        <listWit>',
        '          <witness xml:id="wit-11Q5">11QPs-a (11Q5, Hebrew)</witness>',
        '          <witness xml:id="wit-LXX">Septuaginta (Greek)</witness>',
        '          <witness xml:id="wit-Vulg">Biblia Sacra Vulgata (Latin)</witness>',
        '        </listWit>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>',
        '      <div type="psalm" n="151">'
    ]

    for item in VERSES:
        v_num = item["v"]
        clean_heb = item["heb"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_grc = item["grc"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_lat = item["lat"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en  = item["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        lines.append(f'        <p n="{v_num}">')
        lines.append('          <app>')
        lines.append(f'            <rdg wit="#wit-11Q5" xml:lang="heb">{clean_heb}</rdg>')
        lines.append(f'            <rdg wit="#wit-LXX" xml:lang="grc">{clean_grc}</rdg>')
        lines.append(f'            <rdg wit="#wit-Vulg" xml:lang="lat">{clean_lat}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{clean_en}</rdg>')
        lines.append('          </app>')
        lines.append('        </p>')

    lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')

    out_path = 'static/docs/tei/Ps151.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
    # Ensure standard OCP TEI conversion
    subprocess.run(['python3', 'scripts/grammateus_to_tei.py', 'static/docs/Ps151.xml', '-o', 'static/docs/tei/Ps151.xml'], check=True)
