#!/usr/bin/env python3
"""Integrate DiTommaso bibliographic dossiers into the CAVT structure.

Enriches raw/cavt/cavt_entries.csv with DiTommaso chapter numbers, dossier filenames,
and titles. Updates scripts/cavt_gaps.py to generate an enriched CAVT_GAPS.md with
direct dossier links and a comprehensive Judaeo-Hellenistic fragments section.
"""

import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAVT_CSV = ROOT / "raw/cavt/cavt_entries.csv"
BIB_DIR = ROOT / "bibliography"

# CAVT Entry Number -> (DiTommaso Chapter, Dossier Filename, DiTommaso Title)
CAVT_TO_DITOMMASO = {
    1: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Life of Adam and Eve)"),
    2: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Vita Adae)"),
    3: (6, "Testament_of_Adam.md", "Testament of Adam"),
    4: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Testamentum protoplastorum)"),
    5: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Apocalypse of Moses Greek)"),
    6: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Penitence of Adam)"),
    7: (5, "Apocalypse_of_Adam.md", "Apocalypse of Adam (Gnostic NHC V,5)"),
    8: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Gospel of Eve)"),
    9: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Book of Daughters of Adam)"),
    10: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Composition and Name of Adam)"),
    11: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Cave of Treasures)"),
    12: (5, "Apocalypse_of_Adam.md", "Apocalypse of Adam (Sahidic Coptic)"),
    13: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Sedition of Satan)"),
    14: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Conflict of Adam and Eve)"),
    15: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Mandaean Adam fragments)"),
    16: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Creation and Transgression)"),
    17: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Expulsion from Paradise)"),
    18: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Armenian Penitence)"),
    19: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Words of Adam to Seth)"),
    20: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Death of Adam)"),
    60: (15, "1_Enoch.md", "1 Enoch / Qumran (4Q369 Prayer of Enosh)"),
    61: (15, "1_Enoch.md", "1 Enoch (Ethiopic Enoch / Aramaic 4Q201-212)"),
    62: (15, "1_Enoch.md", "1 Enoch / Book of Giants (4Q203, 4Q530-532, 1Q23)"),
    63: (15, "1_Enoch.md", "1 Enoch / Book of Og the Giant"),
    64: (15, "1_Enoch.md", "1 Enoch / Words of Michael (4Q529, 6Q23)"),
    65: (15, "1_Enoch.md", "1 Enoch / Prayer of Michael (4Q471b)"),
    66: (16, "2_Enoch.md", "2 Enoch (Slavonic Enoch)"),
    67: (17, "3_Enoch.md", "3 Enoch (Hebrew Enoch / Sefer Hekhalot)"),
    68: (15, "1_Enoch.md", "1 Enoch / History of Enoch and Elijah"),
    69: (15, "1_Enoch.md", "1 Enoch / Syriac Apocalypse of Enoch"),
    70: (15, "1_Enoch.md", "1 Enoch / Coptic Enoch fragments I"),
    71: (15, "1_Enoch.md", "1 Enoch / Coptic Enoch fragments II"),
    76: (15, "1_Enoch.md", "1 Enoch / Armenian Giants"),
    78: (16, "2_Enoch.md", "2 Enoch / Priestly Epilogue (Methuselah, Nir, Melchizedek)"),
    79: (29, "Jubilees.md", "Jubilees / Genesis Apocryphon (1Q20)"),
    82: (15, "1_Enoch.md", "1 Enoch / Book of Noah (1Q19, 4Q534-536)"),
    85: (38, "Treatise_of_Shem.md", "Treatise of Shem (Rylands Syr. 44)"),
    88: (3, "Testament_of_Abraham.md", "Testament of Abraham (Greek Recensions A and B)"),
    89: (2, "Apocalypse_of_Abraham.md", "Apocalypse of Abraham (Slavonic)"),
    98: (3, "Testament_of_Abraham.md", "Testament of Isaac (Three Patriarchs Cycle)"),
    99: (3, "Testament_of_Abraham.md", "Testament of Jacob"),
    100: (3, "Testament_of_Abraham.md", "Armenian Testament of Jacob"),
    101: (22, "Ladder_of_Jacob.md", "Ladder of Jacob (Tolkovaja Paleja)"),
    102: (22, "Ladder_of_Jacob.md", "Ladder of Jacob (Slavonic Climax)"),
    103: (23, "Prayer_of_Jacob.md", "Prayer of Jacob (P. Berol. 5527 / PGM XXIIb)"),
    105: (26, "Joseph_and_Aseneth.md", "Joseph and Aseneth (Greek, Syriac, Latin)"),
    106: (28, "Prayer_of_Joseph.md", "Prayer of Joseph / 4Q371-373 Apocryphon of Joseph"),
    107: (28, "Prayer_of_Joseph.md", "Prayer of Joseph (Origen citations)"),
    108: (27, "History_of_Joseph.md", "History of Joseph (P. Lond. 121, Bodl. gr. th. d. 3)"),
    109: (27, "History_of_Joseph.md", "History of Joseph (Syriac)"),
    118: (44, "Testaments_of_the_Twelve_Patriarchs.md", "Testaments of the Twelve Patriarchs"),
    120: (44, "Testaments_of_the_Twelve_Patriarchs.md", "Testaments of Twelve Patriarchs / 4Q542 Testament of Qahat"),
    121: (44, "Testaments_of_the_Twelve_Patriarchs.md", "Testaments of Twelve Patriarchs / 4Q543-548 Visions of Amram"),
    122: (34, "Testament_of_Moses.md", "Testament of Moses / 1Q22, 4Q375-376 Words of Moses"),
    123: (34, "Testament_of_Moses.md", "Testament of Moses / 4Q377 Apocryphon of Moses"),
    124: (34, "Testament_of_Moses.md", "Testament of Moses / 2Q21 Apocryphon of Moses"),
    125: (34, "Testament_of_Moses.md", "Testament of Moses / 4Q385a-390 Pseudo-Moses"),
    129: (24, "Jannes_and_Jambres.md", "Jannes and Jambres"),
    131: (36, "Pseudo_Philo.md", "Pseudo-Philo (Liber Antiquitatum Biblicarum)"),
    132: (29, "Jubilees.md", "Jubilees"),
    133: (13, "Eldad_and_Modad.md", "Eldad and Modad"),
    134: (34, "Testament_of_Moses.md", "Testament/Assumption of Moses"),
    135: (4, "Primary_Adam_Literature.md", "Primary Adam Literature (Apocalypse of Moses)"),
    147: (36, "Pseudo_Philo.md", "Pseudo-Philo / Vision of Kenaz (LAB 25-28)"),
    148: (36, "Pseudo_Philo.md", "Pseudo-Philo / Lament of Seila (LAB 39-40)"),
    153: (44, "Testaments_of_the_Twelve_Patriarchs.md", "Words of Gad the Seer (Cochin Hebrew MS)"),
    155: (53, "Eupolemus.md", "Eupolemus / Letters of Solomon to Hiram and Vaphris"),
    161: (42, "Testament_of_Solomon.md", "Testament of Solomon / Epistle to Rehoboam on Hygromancy"),
    162: (42, "Testament_of_Solomon.md", "Testament of Solomon"),
    166: (46, "History_of_the_Rechabites.md", "History of the Rechabites (Story of Zosimus)"),
    167: (14, "Apocalypse_of_Elijah.md", "Apocalypse of Elijah (Coptic / Chester Beatty 2018)"),
    168: (14, "Apocalypse_of_Elijah.md", "Apocalypse of Elijah (Hebrew Sefer Eliyahu)"),
    169: (14, "Apocalypse_of_Elijah.md", "Vision of Elijah (Latin Epistula Titi)"),
    177: (21, "Ascension_of_Isaiah.md", "Ascension of Isaiah / Testament of Hezekiah"),
    178: (32, "Prayer_of_Manasseh.md", "Prayer of Manasseh"),
    180: (19, "4_Ezra.md", "4 Ezra (Apocalypse of Ezra)"),
    181: (19, "4_Ezra.md", "4 Ezra / Confessio Esdrae (8:20-36)"),
    182: (19, "4_Ezra.md", "5 Ezra (4 Ezra 1-2)"),
    183: (19, "4_Ezra.md", "6 Ezra (4 Ezra 15-16)"),
    184: (19, "4_Ezra.md", "Greek Apocalypse of Ezra"),
    185: (19, "4_Ezra.md", "Revelatio Esdrae (calendar / astromancy)"),
    186: (19, "4_Ezra.md", "Apocalypse of Ezra on the Kingdom of the Arabs"),
    188: (19, "4_Ezra.md", "Armenian Questions of Ezra"),
    189: (19, "4_Ezra.md", "Somnium Esdrae (Dream of Ezra)"),
    195: (7, "Ahiqar.md", "Story and Wisdom of Ahiqar"),
    198: (30, "3_Maccabees.md", "3 Maccabees"),
    199: (31, "4_Maccabees.md", "4 Maccabees"),
    200: (31, "4_Maccabees.md", "5 Maccabees (Arabic/Syriac Maccabees)"),
    202: (43, "Syriac_Apocryphal_Psalms.md", "Syriac Apocryphal Psalms / Psalm 151 (11Q5, LXX)"),
    203: (43, "Syriac_Apocryphal_Psalms.md", "Syriac Apocryphal Psalms / Qumran Psalms (11Q5, 4Q88)"),
    204: (43, "Syriac_Apocryphal_Psalms.md", "Syriac Apocryphal Psalms I-V (Pss 151-155)"),
    205: (40, "Odes_of_Solomon.md", "Odes of Solomon"),
    207: (25, "Testament_of_Job.md", "Testament of Job"),
    212: (41, "Psalms_of_Solomon.md", "Psalms of Solomon"),
    213: (35, "Lives_of_the_Prophets.md", "Lives of the Prophets"),
    216: (45, "Apocalypse_of_Zephaniah.md", "Apocalypse of Zephaniah"),
    218: (21, "Ascension_of_Isaiah.md", "Ascension of Isaiah"),
    225: (11, "4_Baruch.md", "4 Baruch (Paraleipomena Jeremiou)"),
    233: (9, "2_Baruch.md", "2 Baruch (Syriac Apocalypse of Baruch)"),
    234: (9, "2_Baruch.md", "2 Baruch (Latin fragment)"),
    235: (10, "3_Baruch.md", "3 Baruch (Greek Apocalypse of Baruch)"),
    242: (18, "Apocryphon_of_Ezekiel.md", "Apocryphon of Ezekiel / 4Q385-391 Pseudo-Ezekiel"),
    244: (18, "Apocryphon_of_Ezekiel.md", "Apocryphon of Ezekiel (Greek fragments 1-5)"),
    248: (12, "Daniel_Pseudepigrapha.md", "Daniel Pseudepigrapha / 4Q243-245 Pseudo-Daniel"),
    249: (12, "Daniel_Pseudepigrapha.md", "Daniel Pseudepigrapha / 4Q246 Aramaic Apocalypse"),
    250: (12, "Daniel_Pseudepigrapha.md", "Daniel Pseudepigrapha / 4Q552-553 Four Kingdoms"),
    251: (12, "Daniel_Pseudepigrapha.md", "Daniel Pseudepigrapha / 4Q242 Prayer of Nabonidus"),
    252: (12, "Daniel_Pseudepigrapha.md", "Daniel Pseudepigrapha / 4Q551 Daniel and Susanna"),
    253: (12, "Apocalypse_of_Daniel_Greek.md", "Greek Apocalypse of Daniel (Diegesis Danielis)"),
    266: (19, "4_Ezra.md", "Apocalypse of Sedrach"),
    273: (8, "Letter_of_Aristeas.md", "Letter of Aristeas"),
    274: (39, "Sibylline_Oracles.md", "Sibylline Oracles"),
    275: (39, "Sibylline_Oracles.md", "Sibylline Oracles / Tiburtine Sibyl")
}

# Works excluded by CAVT (Judaeo-Hellenistic fragmentists and extra-canonical sapiential)
EXCLUDED_FROM_CAVT = [
    {"author": "Aristeas the Exegete", "work": "Peri Iob (On Job)", "ditommaso_ch": 48,
     "dossier": "Aristeas_the_Exegete.md", "clavis": "Jacoby FGrH 725; Holladay FHJA 1.261-275", "ocp_xml": "ArisEx.xml"},
    {"author": "Aristobulus of Alexandria", "work": "Exegesis of the Law of Moses", "ditommaso_ch": 49,
     "dossier": "Aristobulus.md", "clavis": "Holladay FHJA 3.1-250; Denis FPG 217-228", "ocp_xml": "Aristob.xml"},
    {"author": "Artapanus", "work": "Peri Ioudaion (On the Jews)", "ditommaso_ch": 50,
     "dossier": "Artapanus.md", "clavis": "Jacoby FGrH 726; Holladay FHJA 1.189-243", "ocp_xml": "Artap.xml"},
    {"author": "Cleodemus Malchus", "work": "History of the Jews", "ditommaso_ch": 51,
     "dossier": "Cleodemus_Malchus.md", "clavis": "Jacoby FGrH 727; Holladay FHJA 1.245-259", "ocp_xml": "ClMal.xml"},
    {"author": "Demetrius the Chronographer", "work": "On the Kings in Judaea", "ditommaso_ch": 52,
     "dossier": "Demetrius_the_Chronographer.md", "clavis": "Jacoby FGrH 722; Holladay FHJA 1.51-91", "ocp_xml": "—"},
    {"author": "Eupolemus", "work": "On the Kings of Judaea", "ditommaso_ch": 53,
     "dossier": "Eupolemus.md", "clavis": "Jacoby FGrH 723; Holladay FHJA 1.93-156", "ocp_xml": "Eup.xml"},
    {"author": "Pseudo-Eupolemus", "work": "On the Jews (Anonymous Samaritan)", "ditommaso_ch": 54,
     "dossier": "Pseudo_Eupolemus.md", "clavis": "Jacoby FGrH 724; Holladay FHJA 1.157-187", "ocp_xml": "Ps-Eup.xml"},
    {"author": "Ezekiel the Tragedian", "work": "Exagoge (The Exodus)", "ditommaso_ch": 55,
     "dossier": "Ezekiel_the_Tragedian.md", "clavis": "TrGF 1.128; Holladay FHJA 2.301-529", "ocp_xml": "EzekTrag.xml"},
    {"author": "Pseudo-Hecataeus", "work": "On the Jews / On Abraham", "ditommaso_ch": 56,
     "dossier": "Pseudo_Hecataeus.md", "clavis": "Jacoby FGrH 264/730; Holladay FHJA 1.277-335", "ocp_xml": "—"},
    {"author": "Justus of Tiberias", "work": "Chronicle of Kings / Jewish War", "ditommaso_ch": 57,
     "dossier": "Justus_of_Tiberias.md", "clavis": "Jacoby FGrH 734; Holladay FHJA 1.371-389", "ocp_xml": "—"},
    {"author": "Pseudo-Orpheus", "work": "Diatheke (Testament of Orpheus)", "ditommaso_ch": 58,
     "dossier": "Pseudo_Orpheus.md", "clavis": "Holladay FHJA 4.1-300; Kern OF 245-248", "ocp_xml": "—"},
    {"author": "Philo the Epic Poet", "work": "Peri Ta Hierosolyma (On Jerusalem)", "ditommaso_ch": 59,
     "dossier": "Philo_the_Epic_Poet.md", "clavis": "Jacoby FGrH 729; Holladay FHJA 2.205-299; SH 683-689", "ocp_xml": "PhEPoet.xml"},
    {"author": "Thallus", "work": "Histories (Universal Chronography)", "ditommaso_ch": 60,
     "dossier": "Thallus.md", "clavis": "Jacoby FGrH 256; Holladay FHJA 1.343-369", "ocp_xml": "—"},
    {"author": "Theodotus", "work": "On the Jews (Epic Hexameters on Shechem)", "ditommaso_ch": 61,
     "dossier": "Theodotus.md", "clavis": "Jacoby FGrH 732; Holladay FHJA 2.51-204; SH 757-764", "ocp_xml": "Theod.xml"},
    {"author": "Theophilus", "work": "Notice on Solomon and Hiram of Tyre", "ditommaso_ch": 62,
     "dossier": "Theophilus.md", "clavis": "Jacoby FGrH 733; Holladay FHJA 1.337-341", "ocp_xml": "—"},
    {"author": "Hellenistic Synagogal Prayers", "work": "16 Synagogal Prayers in Apostolic Constitutions 7-8", "ditommaso_ch": 20,
     "dossier": "Hellenistic_Synagogal_Prayers.md", "clavis": "Delling; van der Horst", "ocp_xml": "—"},
    {"author": "Sentences of Syriac Menander", "work": "Syriac Sapiential Florilegium", "ditommaso_ch": 33,
     "dossier": "Sentences_of_the_Syriac_Menander.md", "clavis": "Baars; Land; Schulthess", "ocp_xml": "—"},
    {"author": "Sentences of Pseudo-Phocylides", "work": "Gnomological Hexameters", "ditommaso_ch": 37,
     "dossier": "Sentences_of_Pseudo_Phocylides.md", "clavis": "van der Horst; Derron", "ocp_xml": "—"}
]

def update_cavt_entries():
    print(f"Reading {CAVT_CSV}...")
    with open(CAVT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Add DiTommaso columns if not present
    new_cols = ["ditommaso_ch", "ditommaso_dossier", "ditommaso_title"]
    for col in new_cols:
        if col not in fieldnames:
            fieldnames.append(col)

    mapped_count = 0
    for row in rows:
        c_no = int(row["cavt_no"])
        if c_no in CAVT_TO_DITOMMASO:
            ch, dossier, title = CAVT_TO_DITOMMASO[c_no]
            row["ditommaso_ch"] = str(ch)
            row["ditommaso_dossier"] = dossier
            row["ditommaso_title"] = title
            mapped_count += 1
        else:
            row["ditommaso_ch"] = ""
            row["ditommaso_dossier"] = ""
            row["ditommaso_title"] = ""

    with open(CAVT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Enriched {CAVT_CSV} with {mapped_count} DiTommaso mappings across {len(rows)} entries.")

if __name__ == "__main__":
    update_cavt_entries()
