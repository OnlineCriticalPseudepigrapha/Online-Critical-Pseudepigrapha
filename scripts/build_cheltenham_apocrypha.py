#!/usr/bin/env python3
"""
Build 4 Latin Apocrypha from the Cheltenham / Phillipps MS 391 (M. R. James, Apocrypha Anecdota 1, 1893):
  1. Oratio Moysi in die obitus sui (CAVT 138 / CANT 314; James pp. 172-173)
  2. Visio Kenaz / Zenez patris Gothoniel (CAVT 147; James pp. 178-179; cf. LAB 28)
  3. Threnus Seilae filiae Iephte (CAVT 148; James pp. 182-183; cf. LAB 40)
  4. Citharismus regis David contra daemonium Saulis (CAVT 152; James pp. 184-185; cf. LAB 60)

Outputs:
  - static/docs/OrMois.xml & static/docs/tei/OrMois.xml
  - static/docs/VisKenaz.xml & static/docs/tei/VisKenaz.xml
  - static/docs/ThrenSeila.xml & static/docs/tei/ThrenSeila.xml
  - static/docs/CithDavid.xml & static/docs/tei/CithDavid.xml
"""

import os

TEXTS = {
    "OrMois": {
        "cavt": 138,
        "title": "Oratio Moysi in die obitus sui",
        "lang_id": "Latin",
        "lang_code": "lat",
        "mss_id": "Phill",
        "mss_name": "Codex Phillippicus 391 (saec. XI)",
        "units": [
            (
                "Domine Deus, si adhuc potero petere de te iuxta multitudinem misericordiae tuae, non indigneris mihi; et ostende mihi quanta quantitas temporis transiit, et quanta remansit.",
                "Lord God, if I may yet make request of you according to the multitude of your mercy, be not angry with me; and show me how great a quantity of time has passed, and how much remains."
            ),
            (
                "Et dixit ad eum: 'Stigma et apex manus, momenti plenitudo, et cyathi gutta; et omnia complevit tempus. Quatuor enim semis transiit, et duo semis supersunt.'",
                "And he said to him: 'A mark and point of a hand, the fullness of a moment, and a drop from a cup; and time has completed all things. For four and a half has passed, and two and a half remains.'"
            ),
            (
                "Et audiens Moyses repletus est sensu, et mutata est effigies eius in gloria. Et mortuus est in gloria secundum os Domini, et sepelivit eum iuxta quod promiserat ei.",
                "And Moses hearing was filled with understanding, and his appearance was transformed in glory. And he died in glory according to the word of the Lord, and he buried him according as he had promised him."
            ),
            (
                "Et luxerunt angeli in morte eius, et praecedebant eum fulgura et lampades et sagittae omnes unanimes.",
                "And the angels mourned at his death, and lightnings and torches and arrows went before him, all in unison."
            ),
            (
                "Et in illa die non est dictus hymnus militum processu Moysis: nec fuit talis dies ex quo fecit Dominus hominem super terram, nec erit talis adhuc in sempiternum ut humiliet pro hominibus hymnum angelorum: quoniam valde amavit eum. Et sepelivit eum per manus suas super excelsam terram in lumine totius orbis.",
                "And on that day no hymn of the heavenly hosts was chanted at the passing of Moses: nor was there ever such a day since the Lord made man upon the earth, nor shall there be such ever again, that he should suspend the hymn of the angels on account of a man: because he loved him exceedingly. And he buried him with his own hands upon the high land in the light of the whole world."
            )
        ]
    },
    "VisKenaz": {
        "cavt": 147,
        "title": "Visio Kenaz (Visio Zenez patris Gothoniel)",
        "lang_id": "Latin",
        "lang_code": "lat",
        "mss_id": "Phill",
        "mss_name": "Codex Phillippicus 391 (saec. XI)",
        "units": [
            (
                "Cum sederent seniores insiluit spiritus sanctus habitans in Zenez et extulit sensum eius: et coepit prophetare dicens:",
                "While the elders were sitting, the holy spirit dwelling in Kenaz leaped upon him and lifted up his understanding: and he began to prophesy, saying:"
            ),
            (
                "'Ecce nunc video quae non sperabam, et considero quae non cognoscebam. Audite nunc qui habitatis super terram. Sicut commorantes in ea prophetaverunt ante me videntes horam hanc priusquam corrumperetur terra, ut cognoscatis praedestinatas prophetationes omnes vos qui habitatis in ea.",
                "'Behold now I see what I was not hoping for, and contemplate what I did not know. Hear now, you who dwell upon the earth. Just as those who abide in it prophesied before me, seeing this hour before the earth was corrupted, that all you who dwell in it may know the predestined prophecies."
            ),
            (
                "Ecce nunc video flammas non ardentes et audio venas non expergefactas de somno, quibus non est fundamentum, neque fastigia montium nec suspensorium fundamenti considero; sed omnia inapparentia et invisibilia, quibus locus non est in totum: et cum oculus meus non sciat quid videat, cor meum adinveniet quae discat.",
                "Behold now I see flames that do not burn and I hear springs not yet awakened from sleep, for which there is no foundation, neither do I contemplate mountain peaks nor the arch of a firmament; but all things are invisible and without form, having no place at all: and though my eye knows not what it sees, my heart will discover what it may learn."
            ),
            (
                "De flamma autem quam video non ardentem, vidi, et ecce scintilla ascendit, et quasi substravit sibi subdiuum; et erat similitudo substrati eius tamquam aranea ordiens in modum scuti.",
                "From the flame which I see not burning, I looked, and behold, a spark ascended, and spread beneath itself an expanse; and the likeness of its expanse was like a spider weaving in the shape of a shield."
            ),
            (
                "Et dum factum esset fundamentum, vidi de vena illa excitabatur quasi spuma ebulliens, et ecce dum mutavit se tamquam in aliud fundamentum. Inter medium autem fundamentum superioris et inferioris de lumine invisibilis loci advenerunt quasi imagines hominum et perambulabant: et ecce vox dicens: Haec fundamenta erunt hominibus habitantibus in eis annis septem.",
                "And when the foundation was made, I saw that from that spring there was aroused as it were a boiling foam, and behold it transformed itself into another foundation. And between the upper and the lower foundation there arrived from the light of the invisible place likenesses as of men and walked about; and behold a voice saying: These foundations shall be for men dwelling in them for seven thousand years."
            ),
            (
                "Et fundamentum inferius substratum erat, superius autem de spuma erat; et qui processerunt de luce invisibilis loci hi erunt qui habitabunt; et nomen hominis illius [Adam]. Et erit cum peccaverit mihi et completum fuerit tempus, extinguetur scintilla et pausabit vena, et sic mutabuntur.'",
                "And the lower foundation was laid beneath, while the upper was of foam; and those who proceeded from the light of the invisible place, these are they who shall inhabit it; and the name of that man is Adam. And it shall be, when he has sinned against me and the time is fulfilled, the spark will be extinguished and the spring will cease, and thus they will be changed.'"
            ),
            (
                "Et factum est cum locutus fuisset Zenez verba haec expergefactus est et reversus est sensus eius in eum. Ipse autem nesciebat quae locutus fuerat neque quae viderat. Hoc autem solum dixit populo: 'Si sic est requies iustorum posteaquam defuncti fuerint, oportet eos mori corruptibili saeculo, ut non videant peccata.'",
                "And it came to pass when Kenaz had spoken these words, he awoke and his senses returned to him. But he himself did not know what he had spoken nor what he had seen. Only this he said to the people: 'If such is the rest of the righteous after they have departed, it is fitting for them to die to the corruptible age, that they may not see sins.'"
            ),
            (
                "Et cum haec dixisset Zenez, defunctus est et dormivit cum patribus suis: et planxit eum populus triginta diebus.",
                "And when Kenaz had said these things, he died and slept with his fathers: and the people mourned him thirty days."
            )
        ]
    },
    "ThrenSeila": {
        "cavt": 148,
        "title": "Threnus Seilae filiae Iephte in monte Stelac",
        "lang_id": "Latin",
        "lang_code": "lat",
        "mss_id": "Phill",
        "mss_name": "Codex Phillippicus 391 (saec. XI)",
        "units": [
            (
                "Venit filia Iepte in montem Stelac et coepit plorare. Et hic threnus eius in quo plangens ploravit se: et dixit:",
                "The daughter of Jephthah came to Mount Stelac and began to weep. And this is her lamentation in which weeping she lamented herself: and she said:"
            ),
            (
                "'Audite montes threnum meum, et intendite colles lacrimas oculorum meorum, et testes estote petrae in planctu animae meae. Ecce quomodo accusor sed non in vanum recipietur anima mea. Proficiscantur verba mea in caelis et scribantur lacrimae meae ante conspectum firmamenti, ut pater non expugnet filiam quam devovit sacrificare, ut princeps illius unigenitam audiat in sacrificio promissam.",
                "'Hear, O mountains, my lamentation, and give heed, O hills, to the tears of my eyes, and be witnesses, O rocks, to the weeping of my soul. Behold how I am judged, yet not in vain shall my soul be taken. Let my words go forth into the heavens, and let my tears be written before the sight of the firmament, that a father may not overbear the daughter whom he vowed to sacrifice, that the ruler may hear his only daughter promised for a burnt offering."
            ),
            (
                "Ego autem non sum saturata thalamo meo, nec repleta sum coronis nuptiarum mearum. Non enim vestita sum splendore sedens in ingenuitate mea, et non sum usa pretiosi odoramenti mei, nec refecit animam meam oleum unctionis quod praeparatum est mihi.",
                "For I have not been satisfied with my bridal chamber, nor filled with the crowns of my wedding. For I have not been clothed in splendor sitting in my virginity, nor have I used my precious perfume, nor has the oil of anointing which was prepared for me refreshed my soul."
            ),
            (
                "O mater, in vanum peperisti unigenitam tuam et genuisti eam super terram, quoniam factus est infernus thalamus meus. Confectio omnis olei quam praeparavit mihi mater mea effundatur, et albam quam nevit mihi tinea comedat, et corona quam intexuit mea nutrix in tempore marcescat, et stratoria quae texuit mihi de hyacintho et purpura vermis ea corrumpat.",
                "O mother, in vain have you borne your only daughter and brought her forth upon earth, since the underworld has become my bridal chamber! Let all the preparation of oil which my mother prepared for me be poured out, and the white garment which she spun for me let the moth consume, and the garland which my nurse wove in season let it wither, and the bedcoverings which she wove for me of violet and purple let the worm corrupt them."
            ),
            (
                "Et referentes de me convirgines meae cum gemitu per dies plangant me. Inclinate arbores ramos vestros et plangite iuventutem meam: venite ferae silvarum et conculcate supra virginitatem meam, quoniam abscisi sunt anni mei, et tempus vitae meae in tenebris inveteravit.'",
                "And let my maiden companions retelling concerning me with groaning lament me for days. Bend your branches, O trees, and bewail my youth: come, wild beasts of the forests, and trample upon my virginity, for my years are cut short, and the time of my life has grown old in darkness.'"
            ),
            (
                "Et his dictis reversa est Seila ad patrem suum, et ipse fecit omnia quaecumque iuravit, et obtulit holocaustomata. Tunc omnes virgines Israel convenerunt et sepelierunt filiam Iepte et planxerunt eam.",
                "And having said these things Seila returned to her father, and he did all things whatsoever he had sworn, and offered whole burnt offerings. Then all the maidens of Israel assembled and buried the daughter of Jephthah and mourned her."
            )
        ]
    },
    "CithDavid": {
        "cavt": 152,
        "title": "Citharismus regis David contra daemonium Saulis",
        "lang_id": "Latin",
        "lang_code": "lat",
        "mss_id": "Phill",
        "mss_name": "Codex Phillippicus 391 (saec. XI)",
        "units": [
            (
                "Tenebrae et silentium erant antequam fieret saeculum: et locutum est silentium, et apparuerunt tenebrae.",
                "Darkness and silence were before the world was made: and the silence spoke, and darkness appeared."
            ),
            (
                "Et factum est tunc nomen tuum in compaginatione extensionis quod appellatum est superius caelum; inferius vocatum est terra.",
                "And then was your name made in the framework of the expanse, which above was called heaven; below it was named earth."
            ),
            (
                "Et praeceptum est superiori ut plueret secundum tempus eius, et inferiori praeceptum est ut crearet escam omnibus quae facta sunt.",
                "And it was commanded to the upper that it should rain according to its season, and to the lower it was commanded that it should bring forth food for all things that were made."
            ),
            (
                "Et post haec facta est tribus spirituum vestrorum. Et nunc molesta esse noli tamquam secunda creatura: si comminus memorarer artareris in quo ambulas.",
                "And after these things was made the tribe of your spirits. And now be not troublesome, as being a secondary creation: if I should name you to your face, you would be constrained in the place where you walk."
            ),
            (
                "Aut non audire tibi sufficit, quoniam per ea quae consonant in conspectu tuo multis psallo? Aut immemor es quoniam de resultatione in chaomate nata est vestra creatura?",
                "Or does it not suffice you to hear, that through these strings that harmonize before your face I sing to many? Or are you unmindful that from the reverberation in chaos your creation was born?"
            ),
            (
                "Arguent autem tempora nova unde natus sum; de quo nascitur post tempus de lateribus meis qui vos domabit. Et cum hymnizaret David parcebat Sauli spiritus.",
                "Now new seasons shall prove whence I was born; out of whom shall be born after a time from my loins one who will subdue you. And when David played the harp, the spirit spared Saul."
            )
        ]
    }
}

def make_grammateus_xml(key, info):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        f'<book filename="{key}.xml" title="{info["title"]}">'
    ]
    
    # Latin version
    lines.extend([
        f'  <version id="{info["lang_id"]}" title="{info["title"]} ({info["lang_id"]})" lang="{info["lang_code"]}">',
        '    <divisions>',
        '      <division id="1" title="Text" type="section"/>',
        '    </divisions>',
        '    <manuscripts>',
        f'      <manuscript id="{info["mss_id"]}" name="{info["mss_name"]}"/>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ])
    for idx, (lat, _) in enumerate(info["units"], 1):
        uid = f"1.{idx}"
        esc_lat = lat.replace('&', '&amp;')
        lines.append(f'        <unit id="{uid}">')
        lines.append(f'          <reading option="base" mss="{info["mss_id"]}">{esc_lat}</reading>')
        lines.append('        </unit>')
    lines.extend([
        '      </div>',
        '    </text>',
        '  </version>'
    ])
    
    # English translation
    lines.extend([
        f'  <version id="English" title="English Translation" lang="eng">',
        '    <divisions>',
        '      <division id="1" title="Text" type="section"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <manuscript id="Eng" name="English Translation"/>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ])
    for idx, (_, eng) in enumerate(info["units"], 1):
        uid = f"1.{idx}"
        esc_eng = eng.replace('&', '&amp;')
        lines.append(f'        <unit id="{uid}">')
        lines.append(f'          <reading option="base" mss="Eng">{esc_eng}</reading>')
        lines.append('        </unit>')
    lines.extend([
        '      </div>',
        '    </text>',
        '  </version>',
        '</book>'
    ])
    
    return '\n'.join(lines) + '\n'

def main():
    for key, info in TEXTS.items():
        xml_content = make_grammateus_xml(key, info)
        out_xml = f"static/docs/{key}.xml"
        with open(out_xml, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Wrote Grammateus XML: {out_xml} ({len(info['units'])} units)")
        
        out_tei = f"static/docs/tei/{key}.xml"
        ret = os.system(f"python3 scripts/grammateus_to_tei.py {out_xml} -o {out_tei}")
        if ret == 0:
            print(f"Wrote TEI P5 XML: {out_tei}")
        else:
            print(f"Error converting {key} to TEI: {ret}")

if __name__ == '__main__':
    main()
