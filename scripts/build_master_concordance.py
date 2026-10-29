#!/usr/bin/env python3
"""Build Master 6-Way Concordance and Registry across:
1. Haelewyck (CAVT, 1998)
2. Denis (1970 & 2000)
3. DiTommaso (2001)
4. Charlesworth (OTP 1 & 2, 1983/1985)
5. Charles (APOT 1 & 2, 1913)
6. Sparks (AOT, 1984)

Outputs:
- raw/cavt/master_crosswalk.csv
- CANON.md (The master canonical registry for pseudepigrapha.org)
"""

import csv
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAVT_CSV = ROOT / "raw" / "cavt" / "cavt_entries.csv"
OUT_CSV = ROOT / "raw" / "cavt" / "master_crosswalk.csv"
CANON_MD = ROOT / "CANON.md"

def build_master_registry():
    print("Building Master 6-Way Concordance Registry...")

    # 1. Load CAVT entries
    with open(CAVT_CSV, "r", encoding="utf-8") as f:
        cavt_rows = list(csv.DictReader(f))

    # Base registry keyed by canonical ID
    registry = []

    # Map of CAVT number to major authorities
    # Authority definitions for major pseudepigrapha and apocrypha:
    # (otp_ref, apot_ref, sparks_ref, cant_ref, ocp_doc)
    cavt_meta = {
        1: ("OTP 2:249-295 (Life of Adam and Eve)", "APOT 2:123-154 (Books of Adam and Eve)", "AOT 141-167 (Life of Adam and Eve)", "CANT 1", "AdamEve.xml"),
        2: ("OTP 2:249-295 (Vita Adae)", "APOT 2:123-154 (Vita Adae et Evae)", "AOT 141-167 (Vita Adae)", "", "AdamEve.xml"),
        3: ("OTP 1:707-728 (Testament of Adam)", "", "AOT 509-515 (Testament of Adam)", "CANT 2", "TAdam.xml"),
        7: ("OTP 1:707-719 (Apocalypse of Adam)", "", "", "", "ApocAdam.xml"),
        10: ("", "", "", "", "DeAdam.xml"),
        11: ("OTP 2:256 (Cave of Treasures)", "", "", "CANT 12", "CavThes.xml"),
        57: ("", "", "", "", ""), # NHC IX.2 Thought of Norea
        61: ("OTP 1:5-89 (1 Enoch / Ethiopic Enoch)", "APOT 2:163-281 (Book of Enoch)", "AOT 169-319 (1 Enoch)", "", "1En.xml"),
        66: ("OTP 1:91-221 (2 Enoch / Slavonic Enoch)", "APOT 2:425-469 (Secrets of Enoch)", "AOT 321-362 (2 Enoch)", "", "2En.xml"),
        67: ("OTP 1:223-315 (3 Enoch / Hebrew Enoch)", "", "", "", "3En.xml"),
        84: ("OTP 2:905-919 (Pseudo-Hecataeus)", "", "", "CANT 28", "PsHecat.xml"),
        85: ("OTP 1:473-486 (Treatise of Shem)", "", "", "", "TracSem.xml"),
        88: ("OTP 1:871-902 (Testament of Abraham)", "", "AOT 393-421 (Testament of Abraham)", "CANT 11", "TAbr.xml"),
        89: ("OTP 1:681-705 (Apocalypse of Abraham)", "", "", "", "ApocAbr.xml"),
        98: ("OTP 1:903-911 (Testament of Isaac)", "", "AOT 423-439 (Testament of Isaac)", "CANT 13", "TIsaac.xml"),
        99: ("OTP 1:913-918 (Testament of Jacob)", "", "AOT 441-452 (Testament of Jacob)", "CANT 14", "TJacob.xml"),
        101: ("OTP 2:401-411 (Ladder of Jacob)", "", "AOT 453-463 (Ladder of Jacob)", "", "LadJac.xml"),
        103: ("OTP 2:715-723 (Prayer of Jacob)", "", "", "", "PrJac.xml"),
        105: ("OTP 2:177-247 (Joseph and Aseneth)", "", "AOT 465-503 (Joseph and Aseneth)", "", "JosAsen.xml"),
        107: ("OTP 2:699-714 (Prayer of Joseph)", "", "", "CANT 351", "OrJos.xml"),
        111: ("OTP 2:515-525 (History of Joseph)", "", "AOT 503", "", "HistJos.xml"),
        118: ("OTP 1:775-828 (Testaments of the Twelve Patriarchs)", "APOT 2:282-367 (Testaments of the XII Patriarchs)", "AOT 505-600 (Testaments of the Twelve Patriarchs)", "CANT 350", "T12Patr.xml"),
        129: ("OTP 2:427-442 (Jannes and Jambres)", "", "", "", "JanJam.xml"),
        131: ("OTP 2:297-377 (Pseudo-Philo / LAB)", "", "AOT 303-377 (Biblical Antiquities of Philo)", "", "LAB.xml"),
        132: ("OTP 2:35-142 (Book of Jubilees)", "APOT 2:1-82 (Book of Jubilees)", "AOT 1-139 (Book of Jubilees)", "", "Jub.xml"),
        134: ("OTP 1:919-934 (Testament of Moses)", "APOT 2:407-424 (Assumption of Moses)", "AOT 601-616 (Assumption of Moses)", "CANT 310", "TMos.xml"),
        137: ("", "", "", "BHG 2277", "NarrMois.xml"),
        138: ("", "", "", "CANT 314", "OrMois.xml"),
        147: ("", "", "", "", "VisKenaz.xml"),
        148: ("", "", "", "", "ThrSeila.xml"),
        152: ("", "", "", "", "CithDav.xml"),
        161: ("", "", "", "", "EpSalRob.xml"),
        162: ("OTP 1:935-987 (Testament of Solomon)", "", "", "CANT 342", "TSol.xml"),
        167: ("OTP 1:735-753 (Apocalypse of Elijah)", "", "", "", "ApocEl.xml"),
        168: ("OTP 2:143-176 (Martyrdom of Isaiah)", "APOT 2:155-162 (Martyrdom of Isaiah)", "AOT 33-51 (Martyrdom of Isaiah)", "CANT 305", "MartIs.xml"),
        169: ("", "", "", "", "VisEl.xml"),
        170: ("", "", "", "", "HistEl.xml"),
        177: ("OTP 2:143-176 (Ascension of Isaiah)", "", "", "CANT 305", "AscIs.xml"),
        178: ("OTP 2:625-637 (Prayer of Manasseh)", "APOT 1:612-624 (Prayer of Manasses)", "AOT 649 (Prayer of Manasses)", "CANT 203", "OrMan.xml"),
        179: ("", "APOT 1:1-58 (1 Esdras / 3 Ezra)", "", "", "1Esd.xml"),
        180: ("OTP 1:517-559 (4 Ezra / 2 Esdras 3-14)", "APOT 2:542-624 (4 Ezra)", "", "", "4Ezra.xml"),
        181: ("", "APOT 2:594-598 (Confessio Esdrae)", "", "", "ConfEsd.xml"),
        182: ("", "APOT 2:542-560 (5 Ezra / 2 Esdras 1-2)", "", "", "5Ezra.xml"),
        183: ("", "APOT 2:613-624 (6 Ezra / 2 Esdras 15-16)", "", "", "6Ezra.xml"),
        184: ("OTP 1:561-579 (Greek Apocalypse of Ezra)", "", "AOT 235-247 (Greek Apocalypse of Ezra)", "CANT 343", "ApEzra.xml"),
        185: ("OTP 1:601-604 (Revelation of Ezra)", "", "", "", "RevEzra.xml"),
        186: ("", "", "", "", "ApEzraArab.xml"),
        187: ("", "", "", "", "ApEzraAeth.xml"),
        188: ("OTP 1:591-599 (Questions of Ezra)", "", "", "", "QuaestEzra.xml"),
        189: ("", "", "", "", "SomnEzra.xml"),
        195: ("OTP 2:479-507 (Ahiqar)", "APOT 2:715-784 (Story of Ahikar)", "AOT 483-507 (Ahiqar)", "", "Ahiqar.xml"),
        196: ("", "APOT 1:59-124 (1 Maccabees)", "", "", "1Macc.xml"),
        197: ("", "APOT 1:125-154 (2 Maccabees)", "", "", "2Macc.xml"),
        198: ("OTP 2:509-529 (3 Maccabees)", "APOT 1:155-173 (3 Maccabees)", "", "", "3Macc.xml"),
        199: ("OTP 2:531-564 (4 Maccabees)", "APOT 2:653-685 (4 Maccabees)", "", "", "4Macc.xml"),
        202: ("OTP 2:609-615 (Psalm 151)", "", "", "CANT 151", "Ps151.xml"),
        203: ("OTP 2:615-624 (More Psalms of David / 152-155)", "", "", "", "Ps152-155.xml"),
        205: ("OTP 2:725-771 (Odes of Solomon)", "", "", "", "OdesSol.xml"),
        207: ("OTP 1:829-868 (Testament of Job)", "", "AOT 617-648 (Testament of Job)", "CANT 349", "TJob.xml"),
        212: ("OTP 2:639-670 (Psalms of Solomon)", "APOT 2:625-652 (Psalms of Solomon)", "AOT 649-682 (Psalms of Solomon)", "", "PssSol.xml"),
        213: ("OTP 2:379-399 (Lives of the Prophets)", "", "AOT 379-399 (Lives of the Prophets)", "CANT 101", "LivProph.xml"),
        216: ("OTP 1:497-515 (Apocalypse of Zephaniah)", "", "", "", "ApocZeph.xml"),
        218: ("OTP 2:143-176 (Martyrdom and Ascension of Isaiah)", "APOT 2:155-162 (Ascension of Isaiah)", "AOT 33-51 (Martyrdom of Isaiah)", "CANT 305", "AscIs.xml"),
        225: ("OTP 2:413-425 (4 Baruch / Paraleipomena Jeremiou)", "", "AOT 813-833 (4 Baruch)", "CANT 308", "4Bar.xml"),
        233: ("OTP 1:615-652 (2 Baruch / Syriac Apocalypse)", "APOT 2:470-526 (2 Baruch)", "AOT 835-895 (2 Baruch)", "", "2Bar.xml"),
        235: ("OTP 1:653-679 (3 Baruch / Greek Apocalypse)", "APOT 2:527-541 (3 Baruch)", "AOT 897-914 (3 Baruch)", "CANT 348", "3Bar.xml"),
        244: ("OTP 1:487-495 (Apocryphon of Ezekiel)", "", "", "", "ApocrEzek.xml"),
        253: ("OTP 1:755-770 (Apocalypse of Daniel)", "", "", "", "ApDan.xml"),
        273: ("OTP 2:7-34 (Letter of Aristeas)", "APOT 2:83-122 (Letter of Aristeas)", "AOT 1-38 (Letter of Aristeas)", "CANT 37", "LetAris.xml"),
        274: ("OTP 1:317-472 (Sibylline Oracles)", "APOT 2:368-406 (Sibylline Oracles)", "", "", "SibOr.xml"),
    }

    # 2. Process all 277 CAVT entries
    for row in cavt_rows:
        cno = int(row["cavt_no"])
        title = row["title"]
        section = row["section"]
        lang = row["main_language"] or row["title_language"] or "Multi/Other"
        
        # DiTommaso
        dt_ch = row.get("ditommaso_ch", "")
        dt_ref = f"Ch. {dt_ch} ({row.get('ditommaso_title', '')})" if dt_ch else ""
        dossier = row.get("ditommaso_dossier", "")
        
        # Denis
        denis_ch = row.get("denis2000_ch", "")
        denis_pages = row.get("denis2000_pages", "")
        denis_ref = f"Denis 2000 Ch. {denis_ch} (pp. {denis_pages})" if denis_ch else ""
        
        # Meta lookups
        meta = cavt_meta.get(cno, ("", "", "", "", ""))
        otp_ref, apot_ref, sparks_ref, cant_ref, ocp_xml = meta
        
        canon_id = f"CAVT-{cno:03d}"
        
        # Determine status
        status = "Live Edition" if ocp_xml and (ROOT / "static" / "docs" / ocp_xml).exists() else ("In Progress / Staged" if ocp_xml else "Gap")

        registry.append({
            "ocp_canon_id": canon_id,
            "cavt_no": str(cno),
            "cant_no": cant_ref,
            "standard_title": title,
            "section": section,
            "primary_language": lang,
            "denis_ref": denis_ref,
            "ditommaso_ref": dt_ref,
            "otp_ref": otp_ref,
            "apot_ref": apot_ref,
            "sparks_ref": sparks_ref,
            "ocp_xml": ocp_xml,
            "dossier": dossier,
            "status": status,
            "category": "CAVT Backbone"
        })

    # 3. Supplemental Range for Judaeo-Hellenica & Sapiential Works (Outside CAVT Scope)
    # 18 Judaeo-Hellenic works + Qumran Damascus Document + Pirke Aboth
    supplements = [
        ("CAVT-JH-01", "Demetrius the Chronographer — On the Kings in Judaea", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §1 (pp. 1122–1128)", "Ch. 52 (Demetrius)", "OTP 2:843-854 (Demetrius)", "", "", "Demetr.xml", "Demetrius_the_Chronographer.md", "Jacoby FGrH 722; Holladay FHJA 1.51-91"),
        ("CAVT-JH-02", "Eupolemus — On the Kings of Judaea", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §2 (pp. 1128–1135)", "Ch. 53 (Eupolemus)", "OTP 2:861-872 (Eupolemus)", "", "", "Eup.xml", "Eupolemus.md", "Jacoby FGrH 723; Holladay FHJA 1.93-156"),
        ("CAVT-JH-03", "Artapanus — Concerning the Jews (Peri Ioudaion)", "HISTORIA / ROMANCE", "Greek",
         "Denis 2000 Ch. 36 §3 (pp. 1135–1147)", "Ch. 50 (Artapanus)", "OTP 2:889-903 (Artapanus)", "", "", "Artap.xml", "Artapanus.md", "Jacoby FGrH 726; Holladay FHJA 1.189-243"),
        ("CAVT-JH-04", "Aristeas the Exegete — On Job (Peri Iob)", "EXEGESIS", "Greek",
         "Denis 2000 Ch. 36 §4 (pp. 1147–1150)", "Ch. 48 (Aristeas the Exegete)", "OTP 2:855-859 (Aristeas the Exegete)", "", "", "ArisEx.xml", "Aristeas_the_Exegete.md", "Jacoby FGrH 725; Holladay FHJA 1.261-275"),
        ("CAVT-JH-05", "Cleodemus Malchus — History of the Jews", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §5 (pp. 1150–1154)", "Ch. 51 (Cleodemus Malchus)", "OTP 2:883-887 (Cleodemus Malchus)", "", "", "ClMal.xml", "Cleodemus_Malchus.md", "Jacoby FGrH 727; Holladay FHJA 1.245-259"),
        ("CAVT-JH-06", "Pseudo-Eupolemus — Anonymous Samaritan Chronographer", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §6 (pp. 1154–1160)", "Ch. 54 (Pseudo-Eupolemus)", "OTP 2:873-882 (Pseudo-Eupolemus)", "", "", "Ps-Eup.xml", "Pseudo_Eupolemus.md", "Jacoby FGrH 724; Holladay FHJA 1.157-187"),
        ("CAVT-JH-07", "Theophilus — On Solomon and Hiram of Tyre", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §7 (pp. 1160–1163)", "Ch. 62 (Theophilus)", "OTP 2:861", "", "", "Theoph.xml", "Theophilus.md", "Jacoby FGrH 733; Holladay FHJA 1.337-341"),
        ("CAVT-JH-08", "Pseudo-Hecataeus — On Abraham / On the Jews", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §8 (pp. 1163–1173)", "Ch. 56 (Pseudo-Hecataeus)", "OTP 2:905-919 (Pseudo-Hecataeus)", "", "", "PsHecat.xml", "Pseudo_Hecataeus.md", "Jacoby FGrH 264/730; Holladay FHJA 1.277-335"),
        ("CAVT-JH-09", "Justus of Tiberias — Chronicle of the Kings / Jewish War", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §10a (pp. 1177–1180)", "Ch. 57 (Justus of Tiberias)", "", "", "", "Justus.xml", "Justus_of_Tiberias.md", "Jacoby FGrH 734; Holladay FHJA 1.371-389"),
        ("CAVT-JH-10", "Thallus the Chronographer — Universal Histories", "HISTORIA", "Greek",
         "Denis 2000 Ch. 36 §10b (pp. 1180–1184)", "Ch. 60 (Thallus)", "", "", "", "Thallus.xml", "Thallus.md", "Jacoby FGrH 256; Holladay FHJA 1.343-369"),
        ("CAVT-JH-11", "Philo the Epic Poet — Peri Ta Hierosolyma (On Jerusalem)", "POESIS", "Greek",
         "Denis 2000 Ch. 37 §1 (pp. 1191–1196)", "Ch. 59 (Philo the Epic Poet)", "OTP 2:781-784 (Philo the Epic Poet)", "", "", "PhEPoet.xml", "Philo_the_Epic_Poet.md", "Jacoby FGrH 729; Holladay FHJA 2.205-299"),
        ("CAVT-JH-12", "Theodotus — Epic on the Shechemites (Peri Ioudaion)", "POESIS", "Greek",
         "Denis 2000 Ch. 37 §2 (pp. 1196–1200)", "Ch. 61 (Theodotus)", "OTP 2:785-793 (Theodotus)", "", "", "Theod.xml", "Theodotus.md", "Jacoby FGrH 732; Holladay FHJA 2.51-204"),
        ("CAVT-JH-13", "Ezekiel the Tragedian — Exagoge (The Exodus Drama)", "DRAMA", "Greek",
         "Denis 2000 Ch. 37 §3 (pp. 1200–1216)", "Ch. 55 (Ezekiel the Tragedian)", "OTP 2:803-819 (Ezekiel the Tragedian)", "", "", "EzekTrag.xml", "Ezekiel_the_Tragedian.md", "TrGF 1.128; Holladay FHJA 2.301-529"),
        ("CAVT-JH-14", "Aristobulus of Alexandria — Exegesis of the Law of Moses", "PHILOSOPHIA", "Greek",
         "Denis 2000 Ch. 37 §4 (pp. 1216–1237)", "Ch. 49 (Aristobulus)", "OTP 2:831-842 (Aristobulus)", "", "", "Aristob.xml", "Aristobulus.md", "Holladay FHJA 3.1-250; Denis FPG 217-228"),
        ("CAVT-JH-15", "Sentences of Pseudo-Phocylides — Gnomological Hexameters", "SAPIENTIA", "Greek",
         "Denis 2000 Ch. 34 (pp. 1037–1061)", "Ch. 37 (Pseudo-Phocylides)", "OTP 2:565-582 (Pseudo-Phocylides)", "", "AOT 683-698 (Pseudo-Phocylides)", "PsPhoc.xml", "Sentences_of_Pseudo_Phocylides.md", "CANT 35; van der Horst; Derron"),
        ("CAVT-JH-16", "Pseudo-Orpheus — Diatheke (Testament of Orpheus)", "POESIS / THEOLOGIA", "Greek",
         "Denis 2000 Ch. 35 (pp. 1062–1106)", "Ch. 58 (Orphica)", "OTP 2:795-801 (Orphica)", "", "", "PsOrph.xml", "Pseudo_Orpheus.md", "CANT 33; Holladay FHJA 4.1-300; Kern OF 245-248"),
        ("CAVT-JH-17", "Hellenistic Synagogal Prayers — 16 Synagogal Prayers in Apostolic Constitutions 7-8", "LITURGICA", "Greek",
         "Denis 2000 Ch. 38 §10 (pp. 1280–1282)", "Ch. 20 (Hellenistic Synagogal Prayers)", "OTP 2:671-697 (Hellenistic Synagogal Prayers)", "", "", "", "Hellenistic_Synagogal_Prayers.md", "Delling; van der Horst"),
        ("CAVT-JH-18", "Sentences of the Syriac Menander — Syriac Sapiential Florilegium", "SAPIENTIA", "Syriac",
         "", "Ch. 33 (Syriac Menander)", "OTP 2:583-606 (Syriac Menander)", "", "", "", "Sentences_of_the_Syriac_Menander.md", "Baars; Land; Schulthess"),
        ("CAVT-JH-19", "Damascus Document (Zadokite Fragments / CD)", "QUMRAN / SECTARIAN", "Hebrew",
         "Denis 2000 Tome I Ch. 10", "Ch. 14 (Damascus Document)", "", "APOT 2:785-834 (Fragments of a Zadokite Work)", "", "CD.xml", "", "CD-A, CD-B; 4Q266-273"),
        ("CAVT-JH-20", "Pirke Aboth (Sayings of the Jewish Fathers)", "RABBINICA", "Hebrew",
         "", "", "", "APOT 2:686-714 (Pirke Aboth)", "", "", "", "Mishna Aboth; Herford 1913"),
        ("CAVT-JH-21", "Apocalypse of Sedrach (independent unit)", "APOCALYPSIS", "Greek",
         "Denis 2000 Ch. 38 §2", "Ch. 40 (Apocalypse of Sedrach)", "OTP 1:605-613 (Apocalypse of Sedrach)", "", "AOT 235-247 (Apocalypse of Sedrach)", "Sedrach.xml", "4_Ezra.md", "CAVT 184.ii / CANT 344"),
        ("CAVT-JH-22", "Visio Beati Esdrae (Latin)", "APOCALYPSIS", "Latin",
         "Denis 2000 Ch. 38 §2 (p. 1300)", "Ch. 19 (Vision of Ezra)", "OTP 1:581-590 (Vision of Ezra)", "", "", "Esdl.xml", "4_Ezra.md", "CAVT 184.iii; ed. Bogaert / Denis"),
    ]

    for item in supplements:
        cid, title, sec, lang, denis, dt, otp, apot, sparks, ocp_xml, dossier, clavis = item
        status = "Live Edition" if ocp_xml and (ROOT / "static" / "docs" / ocp_xml).exists() else ("Gap" if not ocp_xml else "In Progress")
        registry.append({
            "ocp_canon_id": cid,
            "cavt_no": "— (JH / Suppl.)",
            "cant_no": clavis,
            "standard_title": title,
            "section": sec,
            "primary_language": lang,
            "denis_ref": denis,
            "ditommaso_ref": dt,
            "otp_ref": otp,
            "apot_ref": apot,
            "sparks_ref": sparks,
            "ocp_xml": ocp_xml,
            "dossier": dossier,
            "status": status,
            "category": "Judaeo-Hellenica & Canonical Supplements"
        })

    # Write Master CSV
    fieldnames = [
        "ocp_canon_id", "cavt_no", "cant_no", "standard_title", "section",
        "primary_language", "denis_ref", "ditommaso_ref", "otp_ref", "apot_ref",
        "sparks_ref", "ocp_xml", "dossier", "status", "category"
    ]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(registry)
    print(f"Wrote {len(registry)} master entries to {OUT_CSV}")

    # Generate CANON.md
    print("Generating CANON.md master registry document...")
    md = [
        "# OCP Master Canonical Registry & 6-Way Concordance",
        "",
        "> **Consolidated Systematic Numbering Schema for Online Critical Pseudepigrapha (`pseudepigrapha.org`)**",
        "> Combining the taxonomic frameworks of:",
        "> 1. **Haelewyck (1998)** — *Clavis Apocryphorum Veteris Testamenti* (CAVT)",
        "> 2. **Denis (1970 & 2000)** — *Fragmenta Pseudepigraphorum Graeca* & *Introduction à la littérature religieuse judéo-hellénistique* (Tomès I–II)",
        "> 3. **DiTommaso (2001)** — *A Bibliography of Pseudepigrapha Research 1850–1999*",
        "> 4. **Charlesworth (1983, 1985)** — *The Old Testament Pseudepigrapha* (OTP 1 & 2)",
        "> 5. **Charles (1913)** — *The Apocrypha and Pseudepigrapha of the Old Testament* (APOT 1 & 2)",
        "> 6. **Sparks (1984)** — *The Apocryphal Old Testament* (AOT)",
        "",
        "---",
        "",
        "## 1. System Architecture & Numbering Schema",
        "",
        "- **`CAVT-001` through `CAVT-277`**: The primary clavis backbone representing all apocrypha recognized in Haelewyck (1998).",
        "- **`CAVT-JH-01` through `CAVT-JH-22`**: The supplemental clavis series covering the 18 Judaeo-Hellenistic and sapiential works intentionally excluded from CAVT's remit (*Introductio* p. xii), plus major Jewish sectarian/rabbinic documents in Charles APOT (Damascus Document, Pirke Aboth) and segregated Ezra apocalypses (*Apocalypse of Sedrach*, *Visio Beati Esdrae*).",
        "- **Total Unified Corpus**: **299 works** systematically indexed across all six premier scholarly collections.",
        "",
        "---",
        "",
        "## 2. Judaeo-Hellenica & Canonical Supplements (`CAVT-JH`)",
        "",
        "| OCP Canon ID | Title & Attribution | Primary Language | Denis (1970/2000) | DiTommaso (2001) | Charlesworth (OTP) | Charles (APOT) | Sparks (AOT) | OCP Status |",
        "|---|---|---|---|---|---|---|---|---|"
    ]

    for r in registry:
        if r["category"] == "Judaeo-Hellenica & Canonical Supplements":
            dossier_link = f"[{r['standard_title']}](bibliography/{r['dossier']})" if r['dossier'] else r['standard_title']
            ocp_link = f"`{r['ocp_xml']}`" if r['ocp_xml'] else "—"
            md.append(f"| **{r['ocp_canon_id']}** | {dossier_link} | {r['primary_language']} | {r['denis_ref'] or '—'} | {r['ditommaso_ref'] or '—'} | {r['otp_ref'] or '—'} | {r['apot_ref'] or '—'} | {r['sparks_ref'] or '—'} | **{r['status']}** ({ocp_link}) |")

    md.extend([
        "",
        "---",
        "",
        "## 3. Major Pseudepigrapha Active Crosswalk (CAVT Backbone)",
        "",
        "High-priority works represented in Charlesworth OTP, Charles APOT, Sparks AOT, or live OCP editions:",
        "",
        "| OCP Canon ID | CAVT | Standard Title | Language | Denis (2000) | DiTommaso (2001) | Charlesworth (OTP) | Charles (APOT) | Sparks (AOT) | OCP Status |",
        "|---|---|---|---|---|---|---|---|---|---|"
    ])

    for r in registry:
        if r["category"] == "CAVT Backbone" and (r["otp_ref"] or r["apot_ref"] or r["sparks_ref"] or r["status"] == "Live Edition"):
            dossier_link = f"[{r['standard_title']}](bibliography/{r['dossier']})" if r['dossier'] else f"[{r['standard_title']}](bibliography/cavt_snippets/CAVT_{int(r['cavt_no']):03d}.md)"
            ocp_link = f"`{r['ocp_xml']}`" if r['ocp_xml'] else "—"
            md.append(f"| **{r['ocp_canon_id']}** | {r['cavt_no']} | {dossier_link} | {r['primary_language']} | {r['denis_ref'] or '—'} | {r['ditommaso_ref'] or '—'} | {r['otp_ref'] or '—'} | {r['apot_ref'] or '—'} | {r['sparks_ref'] or '—'} | **{r['status']}** ({ocp_link}) |")

    md.extend([
        "",
        "---",
        "",
        "## 4. Full Master Concordance Table (All 299 Works)",
        "",
        "See [`raw/cavt/master_crosswalk.csv`](raw/cavt/master_crosswalk.csv) for the full programmatic 15-column dataset.",
        "",
        "### Summary Statistics",
        f"- **Total Works Registered**: {len(registry)}",
        f"- **Core CAVT Apocrypha (1998)**: {len(cavt_rows)}",
        f"- **Judaeo-Hellenica & Canonical Supplements (`CAVT-JH`)**: {len(supplements)}",
        f"- **Active Live Editions in OCP XML**: {len([r for r in registry if r['status'] == 'Live Edition'])}",
        f"- **Works with DiTommaso Research Dossiers**: {len([r for r in registry if r['dossier']])}",
        f"- **Works Covered in Charlesworth OTP 1 & 2**: {len([r for r in registry if r['otp_ref']])}",
        f"- **Works Covered in Charles APOT 1 & 2**: {len([r for r in registry if r['apot_ref']])}",
        f"- **Works Covered in Sparks AOT**: {len([r for r in registry if r['sparks_ref']])}",
        f"- **Works Covered in Denis (2000 Tome II Sections Allocated)**: {len([r for r in registry if r['denis_ref']])}"
    ])

    with open(CANON_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Wrote master canonical document to {CANON_MD}")

if __name__ == "__main__":
    build_master_registry()
