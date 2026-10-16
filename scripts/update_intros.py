#!/usr/bin/env python3
"""
Update static/docs/intros.json with critical introductions for newly ingested texts.
"""

import json

with open('static/docs/intros.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = data.setdefault('documents', {})

new_intros = {
    "OrMan.xml": {
        "title": "Prayer of Manasseh",
        "author": "Anonymous (Pseudepigraphon)",
        "editor": "Henry Barclay Swete (1896); Clementine Vulgate",
        "description": "<p>The <em>Prayer of Manasseh</em> (CAVT 178 / CANT 203) is a short penitential prayer attributed to King Manasseh of Judah during his Babylonian captivity (2 Chron 33:11-13). Extant in Greek in the Septuagint Odes (Ode 12) and the Didascalia Apostolorum, and in Latin as an appendix to the Vulgate. This edition provides the Greek text from H. B. Swete, <em>The Old Testament in Greek according to the Septuagint</em>, Vol. 3 (Cambridge: Cambridge University Press, 1896), pp. 802-804, in parallel with the Clementine Vulgate Latin text.</p>",
        "sections": {
            "mss": "<p>Greek witnesses include Codex Alexandrinus (A), Codex Turicensis (T), Codex Veronensis (R), and the Didascalia Apostolorum. Latin witnesses include the Clementine Vulgate Appendix and medieval Parisian Bibles.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Prayer of Manasseh.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "VisEl.xml": {
        "title": "Vision of Elijah (Visio Eliae)",
        "author": "Pseudo-Elijah",
        "editor": "Donatien De Bruyne (1925)",
        "description": "<p>The <em>Vision of Elijah</em> (CAVT 169) is an apocryphal Latin vision of the punishment of sinners and the topography of Gehinnom / hell, preserved in a single 11th-century manuscript at the Bibliothèque Mazarine (MS 512, fols. 116v-117r). Critical edition published by Dom Donatien De Bruyne in <em>Revue Bénédictine</em> 37 (1925), p. 58.</p>",
        "sections": {
            "mss": "<p>Paris, Bibliothèque Mazarine, MS 512 (11th century), fols. 116v-117r.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Vision of Elijah (Visio Eliae).\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "NarrMois.xml": {
        "title": "Narratio de Moyse et Josue",
        "author": "Anonymous",
        "editor": "A. Vassiliev (1893)",
        "description": "<p>The <em>Narratio de Moyse et Josue</em> (CAVT 137 / BHG 2277) is an extensive Greek narrative on the life, miracles, and death of Moses and Joshua, preserved in Parisinus gr. 1611 (10th/11th century). Edited by A. Vassiliev in <em>Anecdota Graeco-Byzantina</em>, Vol. 1 (Moscow, 1893), pp. 257-264.</p>",
        "sections": {
            "mss": "<p>Paris, Bibliothèque nationale de France, MS gr. 1611 (10th/11th cent.), fols. 286v-290v.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Narratio de Moyse et Josue.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "DeAdam.xml": {
        "title": "De Adami compositione et nomine",
        "author": "Anonymous",
        "editor": "Max Förster (1908)",
        "description": "<p><em>De Adami compositione et nomine</em> (CAVT 10) is a Latin apocryphon recounting the creation of Adam from the eight cosmic substances (earth, sea, sun, clouds, wind, stones, light, Holy Spirit) and the mystical derivation of his name from the four cardinal directions (Anatole, Dysis, Arktos, Mesembria). Edited by Max Förster in <em>Archiv für Religionswissenschaft</em> 11 (1908), pp. 477-478, from London, British Library, MS Royal 5.E.vii (10th cent.) and Harley 3063 (12th cent.).</p>",
        "sections": {
            "mss": "<p>London, British Library, MS Royal 5.E.vii (10th cent.), fol. 70r; MS Harley 3063 (12th cent.), fol. 12v.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"De Adami compositione et nomine.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "PsPhoc.xml": {
        "title": "Sentences of Pseudo-Phocylides",
        "author": "Pseudo-Phocylides",
        "editor": "Theodor Bergk (1882)",
        "description": "<p>The <em>Sentences of Pseudo-Phocylides</em> (CAVT 182 / CANT 35) is a didactic wisdom poem of 230 dactylic hexameters composed in Hellenistic Jewish circles between 100 BCE and 100 CE, combining Mosaic ethical precepts with traditional Greek gnomic form. Edited by Theodor Bergk, <em>Poetae Lyrici Graeci</em>, 4th ed., Vol. 2 (Leipzig: Teubner, 1882), pp. 361-373.</p>",
        "sections": {
            "mss": "<p>Extant in over 150 Byzantine manuscripts, including Mutinensis (M), Vaticanus (Va), Baroccianus (B), and Parisinus 1603 (P), as well as Sibylline Oracles Book 2 (vv. 56-148).</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Sentences of Pseudo-Phocylides.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "TracSem.xml": {
        "title": "Treatise of Shem",
        "author": "Shem son of Noah (Pseudepigraphon)",
        "editor": "Alphonse Mingana (1917)",
        "description": "<p>The <em>Treatise of Shem</em> (*Tractatus Sem*, CAVT 85) is an ancient astrological and calendrical calendar text in 12 chapters corresponding to the signs of the Zodiac, predicting agricultural yields, politics, weather, and health based on the zodiacal sign in which the year begins. Preserved in Syriac in Manchester, John Rylands Library, MS Cod. Syr. 44 (15th cent.). Edited and translated by Alphonse Mingana, <em>Some Early Judæo-Christian Documents in the John Rylands Library</em> (Manchester: The University Press, 1917), pp. 24-29, 54-61.</p>",
        "sections": {
            "mss": "<p>Manchester, John Rylands Library, MS Cod. Syr. 44 (formerly Harris 165), fols. 13b-18a.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Treatise of Shem.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "AndronAsaph.xml": {
        "title": "Andronicus and Asaph the Historian (Zodiac of the Patriarchs)",
        "author": "Andronicus / Asaph",
        "editor": "Alphonse Mingana (1917)",
        "description": "<p>The fragment of <em>Andronicus and Asaph</em> is a unique Syriac treatise preserved in Rylands MS Cod. Syr. 44 (fols. 18a-19b), setting the Greek pagan deities assigned to the Zodiac signs against the correlation established by 'Asaph the scribe and historian of the Hebrews,' who assigned the 12 signs to the 12 sons of Jacob / tribes of Israel. Edited by Alphonse Mingana (Manchester, 1917), pp. 32-35, 62-64.</p>",
        "sections": {
            "mss": "<p>Manchester, John Rylands Library, MS Cod. Syr. 44, fols. 18a-19b.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Andronicus and Asaph the Historian of the Hebrews.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "PsOrph.xml": {
        "title": "Testament of Orpheus (Hieroi Logoi / Diathekai)",
        "author": "Pseudo-Orpheus",
        "editor": "Otto Kern (1922); Albert-Marie Denis (1970)",
        "description": "<p>The <em>Testament of Orpheus</em> (*Diathēkai* / *Hieroi Logoi*, CAVT 183 / CANT 33) is a Hellenistic Jewish-Orphic poem in dactylic hexameters in which Orpheus recants his former polytheism and instructs Musaeus in the worship of the One True God, explicitly invoking the law of Moses ('the one born of water'). Extant in three recensions: Aristobulus ap. Eusebius (*Praep. Evang.* XIII.12.5), Pseudo-Justin (*Cohortatio ad Graecos* 15; *De Monarchia* 2), and Clement of Alexandria (*Stromata* V.123-125). Edited by Otto Kern, <em>Orphicorum Fragmenta</em> (Berlin, 1922), frr. 245-248.</p>",
        "sections": {
            "mss": "<p>Eusebius, Praeparatio Evangelica XIII.12; Pseudo-Justin, Cohortatio ad Graecos 15 and De Monarchia 2; Clement of Alexandria, Stromata V.123-125; Theosophia Tubingensis 61.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Testament of Orpheus (Hieroi Logoi).\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "PsHecat.xml": {
        "title": "Fragments of Pseudo-Hecataeus",
        "author": "Pseudo-Hecataeus",
        "editor": "Felix Jacoby (FGrH 264 F 21-24); Albert-Marie Denis (1970)",
        "description": "<p>The fragments of <em>Pseudo-Hecataeus</em> (*On the Jews* / *On Abraham*, CAVT 84 / CANT 28) represent a Hellenistic Jewish historical work composed in Egypt under the name of Hecataeus of Abdera (ca. 300-100 BCE). Preserved primarily in Flavius Josephus, <em>Contra Apionem</em> I.183-205; II.43; and <em>Antiquitates</em> I.159; XII.38. Edited by Felix Jacoby (FGrH 264 F 21-24) and Albert-Marie Denis, <em>Fragmenta pseudepigraphorum quae supersunt graeca</em> (PVTG 3; Leiden: Brill, 1970), pp. 49-62.</p>",
        "sections": {
            "mss": "<p>Flavius Josephus, Contra Apionem I.183-205, II.43; Antiquitates Iudaicae I.159, XII.38; Clemens Alexandrinus, Stromata V.113.1-2.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Fragments of Pseudo-Hecataeus.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "Thallus.xml": {
        "title": "Fragments of Thallus the Chronographer",
        "author": "Thallus",
        "editor": "Felix Jacoby (FGrH 256); Albert-Marie Denis (1970)",
        "description": "<p>The fragments of <em>Thallus the Chronographer</em> (FGrH 256) derive from a universal history in three books written by a Samaritan or Jewish chronographer of the 1st century CE. Cited by Julius Africanus (<em>Chronographiae</em> fr. 50 ap. Syncell. 610) regarding the darkness at the Crucifixion, and by Theophilus of Antioch (<em>Ad Autolycum</em> III.29) on the antiquity of Belus and the Ogygian flood.</p>",
        "sections": {
            "mss": "<p>Julius Africanus, Chronographiae fr. 50; Theophilus of Antioch, Ad Autolycum III.29; Flavius Josephus, Antiquitates XVIII.167.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Fragments of Thallus the Chronographer.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "Theoph.xml": {
        "title": "Fragments of Theophilus",
        "author": "Theophilus",
        "editor": "Felix Jacoby (FGrH 733); Albert-Marie Denis (1970)",
        "description": "<p>The fragment of <em>Theophilus</em> (FGrH 733) is an excerpt from a Hellenistic Jewish historian preserved by Alexander Polyhistor and cited by Eusebius, <em>Praeparatio Evangelica</em> IX.34.19, recounting Solomon's gift of a golden image to the king of Tyre in exchange for the gilded pillar of the Temple.</p>",
        "sections": {
            "mss": "<p>Eusebius, Praeparatio Evangelica IX.34.19 (citing Alexander Polyhistor).</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Fragments of Theophilus.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "5Ezra.xml": {
        "title": "5 Ezra (Latin)",
        "author": "Pseudo-Ezra",
        "editor": "Robert L. Bensly (1895)",
        "description": "<p><em>5 Ezra</em> consists of chapters 1-2 of the Latin 4 Ezra, forming a Christian-Jewish prologue condemning the disobedience of Israel and announcing the call of the nations. Critical edition by R. L. Bensly, <em>The Fourth Book of Ezra</em> (Cambridge: Cambridge University Press, 1895).</p>",
        "sections": {
            "mss": "<p>Codex Sangermanensis (S), Codex Ambianensis (A), Codex Complutensis (C), and related Spanish/French Vulgate manuscripts.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"5 Ezra.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "6Ezra.xml": {
        "title": "6 Ezra (Latin)",
        "author": "Pseudo-Ezra",
        "editor": "Robert L. Bensly (1895)",
        "description": "<p><em>6 Ezra</em> consists of chapters 15-16 of the Latin 4 Ezra, an apocalyptic prophecy of wars, famines, and persecutions preceding the final judgment. Critical edition by R. L. Bensly, <em>The Fourth Book of Ezra</em> (Cambridge: Cambridge University Press, 1895).</p>",
        "sections": {
            "mss": "<p>Codex Sangermanensis (S), Codex Ambianensis (A), Codex Complutensis (C), and related Latin witnesses.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"6 Ezra.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "ApDan.xml": {
        "title": "Apocalypse of Daniel (Greek)",
        "author": "Pseudo-Daniel",
        "editor": "K. T. Zervos; F. Macler",
        "description": "<p>The Byzantine <em>Apocalypse of Daniel</em> (CAVT 197 / CANT 208) is a 9th-century Greek historicized apocalypse recounting Byzantine-Arab conflicts, the rise of the Antichrist, and the final judgment. Edited by F. Macler, <em>L'Apocalypse de Daniel</em> (1895); Klaus Berger (1976); and K. T. Zervos in OTP 1 (1983).</p>",
        "sections": {
            "mss": "<p>Oxford, Bodleian Library, MS Baroccianus 145 (15th cent.); Paris, BnF gr. 1295.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Apocalypse of Daniel.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "ApEzra.xml": {
        "title": "Greek Apocalypse of Ezra",
        "author": "Pseudo-Ezra",
        "editor": "Constantin von Tischendorf (1866)",
        "description": "<p>The <em>Greek Apocalypse of Ezra</em> (CAVT 184 / CANT 204) is a Christian-Jewish apocalypse in which Ezra journeys through heaven and Tartarus, pleading for sinners before the throne of God. Edited from Parisinus gr. 929 by C. von Tischendorf, <em>Apocalypses Apocryphae</em> (Leipzig, 1866), pp. 24-33.</p>",
        "sections": {
            "mss": "<p>Paris, Bibliothèque nationale de France, MS gr. 929 (15th cent.), fols. 512-521.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Greek Apocalypse of Ezra.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "Sedrach.xml": {
        "title": "Apocalypse of Sedrach",
        "author": "Pseudo-Sedrach",
        "editor": "Montague Rhodes James (1893)",
        "description": "<p>The <em>Apocalypse of Sedrach</em> (CAVT 184 / CANT 207) is an eschatological dialogue in which Sedrach (associated with Ezra / Shadrach) intercedes for mankind and questions divine justice regarding the fall of Adam and the punishment of sinners. Edited from Bodleian MS Miscell. gr. 56 by M. R. James, <em>Apocrypha Anecdota</em> (T&S 2.3; Cambridge, 1893), pp. 130-137.</p>",
        "sections": {
            "mss": "<p>Oxford, Bodleian Library, MS Miscellaneus gr. 56 (15th cent.), fols. 92-100.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Apocalypse of Sedrach.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    },
    "T12P.xml": {
        "title": "Testaments of the Twelve Patriarchs",
        "author": "Twelve Patriarchs",
        "editor": "Robert Henry Charles (1908)",
        "description": "<p>The <em>Testaments of the Twelve Patriarchs</em> (CAVT 129 / CANT 201) contain the dying farewell discourses of the twelve sons of Jacob, each imparting ethical admonitions and apocalyptic visions of the future of their tribes. Edited by R. H. Charles, <em>The Greek Versions of the Testaments of the Twelve Patriarchs</em> (Oxford: Clarendon Press, 1908).</p>",
        "sections": {
            "mss": "<p>Cambridge Univ. Lib. MS Ff.1.24 (b); Oxford, Bodleian MS Barocci 133 (k); Vatican MS gr. 731 (c); and the primary α and β recensional families.</p>",
            "copyright": "<p>Public domain.</p>"
        },
        "citation": "<p>Penner, Ken M., ed. \"Testaments of the Twelve Patriarchs.\" In <em>The Online Critical Pseudepigrapha</em>. Antigonish, NS: St. Francis Xavier University, 2026.</p>"
    }
}

for doc_id, intro in new_intros.items():
    docs[doc_id] = intro

with open('static/docs/intros.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated static/docs/intros.json: total {len(docs)} documents now documented.")
