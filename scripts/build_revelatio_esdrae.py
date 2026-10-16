#!/usr/bin/env python3
"""
Build Revelatio Esdrae de qualitatibus anni (CAVT 185)
Source: Giovanni Mercati, Note di letteratura biblica e cristiana antica (Studi e Testi 5; Roma: Tipografia Vaticana, 1901), pp. 74-80.
Manuscripts:
- Cod. A: Città del Vaticano, BAV, Palat. lat. 1449, fol. 119v-120 (saec. IX, Abbey of Lorsch)
- Cod. B: Città del Vaticano, BAV, Vatic. lat. 248, fol. IIv (saec. XII, Abbey of Belle-Vaux)
- Cod. C: Città del Vaticano, BAV, Vatic. lat. 4825, fol. 156 (saec. XV, Italy)

Outputs:
  - static/docs/RevEsdr.xml (Grammateus DTD)
  - static/docs/tei/RevEsdr.xml (TEI P5 parallel segmentation)
"""

import os
import subprocess

DAYS = [
    {
        "day_num": 1,
        "name": "Dies Dominicus (Sunday)",
        "a": "Kal. Ianuarii si die dominico venerit, facit hiemem calidum, verem humidum, autunnum ventosum, annonas bonas, habundantiam peccorum, mel sufficienter, vindemias bonas, leguminum ubertatem, fructus hortilares; iuvenes morientur; pugne erunt et latrocinia magna, aliquid novi audietur de regibus vel principibus.",
        "b": "Dominico die si fuerint Kal. Ian., erit hyems calida, vernus humidus, estas et autunnus ventosi, annonas bonas, habundantia pecorum, mel sufficienter, uindemia uberis, leguminis hubertas; hortolares peribunt, iuvenes interibunt; bella dilecta militum, latrocinia erunt, et aliquid novi audietur aut ex regibus aut ex principibus.",
        "c": "Si in die dominico fuerint kalende Ianuarii, hyems calida et ver humidum et estas varia et autumpnus ventosus, spelta bona, habundantia peccorum; mel sufficiet; vindemia uberrima, leguminum ubertas; fructus ortales peribunt, iuvenes interibunt, bella erunt et latrocinia, et nova audientur aut de rege aut de principe, et pax fiet.",
        "en": "If the Kalends of January fall on the Lord's Day (Sunday): it makes a warm winter, a moist spring, and a windy autumn; good grain yields, an abundance of cattle, sufficient honey, a rich vintage, and a plentiful harvest of legumes; garden produce will fail and young people will die; there will be wars and great robberies, and new things will be heard concerning kings and rulers, and peace will be made."
    },
    {
        "day_num": 2,
        "name": "Dies Lunae (Monday)",
        "a": "Dies Lune facit hiemem aestatem communem temperatam; diluvia magna erunt et infirmitas, bella militum, mutationes principum; multae matronae in luctu sedebunt, glaties magnae erunt, reges morientur; vindemia bona; apes moriuntur.",
        "b": "Feria .II.a si fuerint Kal. Ian., erit hyems communis, uernus et estas temperati, diluuia magna erunt, formido infirmitatis, pugne erunt, regum disceptatio, glacies magne erunt, principum altercatio, reges interibunt, ferro mortalitas; vindemia non bona.",
        "c": "Si in die Lune fuerint Kalende Ianuarii, hyems erit aspera, ver communis et estas ventosa et temperata; diluvia erunt, formidines, infirmitates et valitudines principum, altercationes, et multe matrone sedebunt in luctu; glacies magne et vindemia non bona; apes morientur, olei parum erit.",
        "en": "If the Kalends of January fall on Monday: the winter will be harsh, spring normal, and summer moderate; there will be great floods, fear of illnesses, wars among soldiers, disputes and changes among rulers; many matrons will sit in mourning, there will be great frosts, kings will perish by the sword; bees will die, and there will be little oil."
    },
    {
        "day_num": 3,
        "name": "Dies Martis (Tuesday)",
        "a": "Dies Martis facit hiemem magnam et umbrosam, nivem vernalem, aestatem aquosam, autunnum siccum; frumenti caritas, porcorum interitus, peccorum repentinus morbus, navigium periculosum, mel sufficienter, lini raritas, incendia nimia; legumina, fructus hortolares, oleum habundantiam; mulieres morientur et reges; vindemia laboriosa.",
        "b": "Feria .III.a si fuerint K. Ian., erit hyems magnus, diluuia nimia, uernus et estas humidi, autonnus sicus, frumenti raritas, pecorum interitus; repentina mors regnabit, mulieres morientur, pericula erunt in pelago, mel habundabit, incendia erunt, pestilentia nimia, legumina erunt, fructus hortolanis peribunt, turbatio erit Romanis, vindemia laborabit.",
        "c": "Si in die Martis fuerint Kallende Ianuarii, hyems erit magna et umbrosa et nix multa, ver temperatum et ventosum et estas humida, autumnus siccus, frumentum carum et peccora repentini periculi; naves in pellago periclitabunt, mel habundabit; linum carum, incendia multa, pestilencia magna, legumina precipua, oleum satis, turbatio Romanorum; mulieres morientur, reges peribunt, et vindemie laborabunt; perditio peculii.",
        "en": "If the Kalends of January fall on Tuesday: winter will be severe and overcast with much snow, spring windy, summer rainy, and autumn dry; corn will be dear, cattle will suffer sudden sickness, navigation will be perilous; honey will be abundant, flax scarce, fires frequent, pestilence great; garden crops will perish, there will be political disturbance for the Romans; women and kings will die, and the vintage will be laborious."
    },
    {
        "day_num": 4,
        "name": "Dies Mercurii (Wednesday)",
        "a": "Dies Mercurii. Fertilitas annonae, vindemia bona, pomorum inanitas, negocia bona, virorum interitus, hiems calida; autumnus temperatur; pericula ferri, olei copia, ventris et praecordiorum solucio; mulieres morientur, locis diversis fames erit, aestas bona; aliquid novi audietur, mel non erit.",
        "b": "Feria .IIII.a si fuerint K. Ian., erit hyems calidus et asper, vernus malus et humidus, autonnus temperatus, annone uilitas, uindemia abundans, pomorum hubertas, pericula ferri, copia olei, mulieres morientur, diversis locis fames erit et aliquid noui audietur, estas bona erit, vindemia bona, iuuenes morientur, mel non erit.",
        "c": "Si in die Merchurii fuerint Kallende Ianuarii, spelta erit utilis, vindemia bona, vitis interitus, hyems calida, ver humidum, estas bona, autumpnus temperatus, periculum febrium, olei copia, ventris solucio; mulieres morientur, per diversa loca iuvenes cadent; mel non erit, habundabit frumentum et avena, et vindemia bona.",
        "en": "If the Kalends of January fall on Wednesday: corn will be cheap, vintage abundant, winter warm and harsh, spring wet, and summer pleasant; dangers of the sword, abundance of oil, dysentery; women and young men will die in diverse places, there will be localized famines and news of fresh occurrences; there will be no honey."
    },
    {
        "day_num": 5,
        "name": "Dies Jovis (Thursday)",
        "a": "Dies Iovis. Frumenti vilitas, carnis caritas, pomorum habundantia, mel minus erit, hiems temperata, ver ventosus, autunnus bonus, aestas bona, porcorum interitus, pluviae multae; flumina exibunt; oleum sufficiet, annona viciabitur, legumina promiscua erunt, et pax.",
        "b": "Feria .V.a si fuerint K. Ian., hyems temperatus, uernus uentosus, autonnus bonus, estas bona, frumenti uilitas; poma habundabunt, pecora interibunt, pluuie multe erunt, flumina foras exibunt, annone superabundabunt, legumina promiscua erunt, oleum sufficienter erit.",
        "c": "Si in die Iovis fuerint Kallende Ianuarii, frumenti habundantia, carnium et lini carum; poma etiam habundabunt, mellis modicum erit, hyemps temperata, ver ventosum, autumpnus bonus, peccudum interitus, pluvie multe; flumina et fontes exibunt, oleum sufficienter, spelta viciabuntur; legumina promiscua, estas bona, habundantia in illo anno, et reges multi et principes peribunt, et pax fiet, et erit habundantia vini.",
        "en": "If the Kalends of January fall on Thursday: grain will be abundant and cheap, but meat and flax dear; fruit will be plentiful, little honey, winter mild, spring windy, and autumn good; cattle will die, there will be plentiful rains and overflowing rivers; oil will suffice, many kings and rulers will perish, and peace and abundant wine will follow."
    },
    {
        "day_num": 6,
        "name": "Dies Veneris (Friday)",
        "a": "Dies Veneris facit hiemem temperatam, aestatem malam; autunnus siccus, frumenti vilitas, vindemia bona, lippitudo oculorum; infantes morientur; terre motus, periclitationes regum; oleum habundantiam; oves et apes peribunt.",
        "b": "Feria .VI.a si fuerint K. Ian., erit hyems tempestiuus, vernus bonus, estas mala, autonnus siccus, frumenti uilitas, uindemia habundabit, lippitudo oculorum regnabit, infantes interibunt, bella dilecta militum, terre motus per loca, magnus rumor circa principes.",
        "c": "Si in die Veneris fuerint Kalende Ianuarii, hyemps temperata erit, ver bonum et ventosum et estas similiter bona, autumpnus siccus, fructuum et vindemiarum habundantia, lippitudo oculorum; infantes peribunt, bella erunt, destructio militum et regum; peregrinationes erunt, oves et aves peribunt; frumenti copia.",
        "en": "If the Kalends of January fall on Friday: winter will be mild, spring windy, summer unstable, and autumn dry; grain will be cheap and vintage plentiful; eye diseases will prevail, infants will die; earthquakes, military destruction and downfall of kings; migrations will take place, and sheep and bees will perish."
    },
    {
        "day_num": 7,
        "name": "Dies Saturni (Saturday)",
        "a": "Dies Saturni facit hiemem ventosam; ver malus, aestas varia ita ut tempestatibus vexetur, autunnus siccus; frumenti angustia, lini caritas; tertianae dominentur, variis languoribus homines vexabuntur, senes morientur.",
        "b": "Si fuerint Kl. Ianuar. die sabbati, hyemps turbinosa erit et uer uentuosus, et nix erit; oves peribunt; estas bona; fructus laborabit, multi egrotabunt, ueteres morientur et apes, case cremabunt.",
        "c": "Si in die sabati fuerint Kallende Ianuarii, hyemps ventuosa, ver magnum; estas varia tempestatibus vexabitur; autumpnus siccus, frumentum carum; terciane et quartane febres vexabunt, homines senes morientur, incendia multa erunt, fructus laborabunt; annona comoda, peccorum interitus, lini multum; et homines egrotabunt.",
        "en": "If the Kalends of January fall on the Sabbath (Saturday): winter will be tempestuous with snow, spring windy, summer turbulent with storms, and autumn dry; grain will be dear and scarce, tertian and quartan fevers will afflict men, elderly people will die; fires will occur, cattle will perish, and sheep and bees will suffer loss."
    }
]

def build_grammateus_xml():
    bib = "Giovanni Mercati, 'Una Revelatio Esdrae de qualitatibus anni', in Note di letteratura biblica e cristiana antica (Studi e Testi 5; Roma: Tipografia Vaticana, 1901), pp. 74-80. CAVT 185."
    
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="RevEsdr" title="Revelatio Esdrae de qualitatibus anni">',
        '  <version author="Mercati 1901" language="Latin" title="Latin and English">',
        '    <divisions>',
        '      <division delimiter="." label="Day"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="CodA" language="Latin" show="yes">',
        '        <name>Cod. Palat. lat. 1449 (saec. IX, Lorsch)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="CodB" language="Latin" show="yes">',
        '        <name>Cod. Vatic. lat. 248 (saec. XII, Belle-Vaux)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="CodC" language="Latin" show="yes">',
        '        <name>Cod. Vatic. lat. 4825 (saec. XV)</name>',
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

    for d in DAYS:
        v_num = d["day_num"]
        clean_a = d["a"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_b = d["b"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_c = d["c"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en = d["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        lines.append(f'        <div number="{v_num}">')
        lines.append(f'          <unit id="{v_num-1}">')
        lines.append(f'            <reading option="0" mss="CodA ">{clean_a}</reading>')
        lines.append(f'            <reading option="1" mss="CodB ">{clean_b}</reading>')
        lines.append(f'            <reading option="2" mss="CodC ">{clean_c}</reading>')
        lines.append(f'            <reading option="3" mss="Trans ">{clean_en}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')

    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')

    out_path = 'static/docs/RevEsdr.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path} ({len(DAYS)} days)')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Revelatio Esdrae de qualitatibus anni</title>',
        '        <author>Ezra (Pseudepigraphon)</author>',
        '        <editor>Giovanni Mercati</editor>',
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
        '          <witness xml:id="wit-CodA">Codex Palatinus latinus 1449 (saec. IX)</witness>',
        '          <witness xml:id="wit-CodB">Codex Vaticanus latinus 248 (saec. XII)</witness>',
        '          <witness xml:id="wit-CodC">Codex Vaticanus latinus 4825 (saec. XV)</witness>',
        '        </listWit>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>',
        '      <div type="calendar" n="1">'
    ]

    for d in DAYS:
        v_num = d["day_num"]
        clean_a = d["a"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_b = d["b"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_c = d["c"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        clean_en = d["en"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        lines.append(f'        <p n="{v_num}">')
        lines.append('          <app>')
        lines.append(f'            <lem wit="#wit-CodA" xml:lang="lat">{clean_a}</lem>')
        lines.append(f'            <rdg wit="#wit-CodB" xml:lang="lat">{clean_b}</rdg>')
        lines.append(f'            <rdg wit="#wit-CodC" xml:lang="lat">{clean_c}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{clean_en}</rdg>')
        lines.append('          </app>')
        lines.append('        </p>')

    lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')

    out_path = 'static/docs/tei/RevEsdr.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
    subprocess.run(['python3', 'scripts/grammateus_to_tei.py', 'static/docs/RevEsdr.xml', '-o', 'static/docs/tei/RevEsdr.xml'], check=True)
