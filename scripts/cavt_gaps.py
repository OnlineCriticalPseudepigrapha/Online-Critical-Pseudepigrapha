#!/usr/bin/env python3
"""Map OCP's static/docs/*.xml to CAVT numbers and rank the CAVT works OCP lacks -> CAVT_GAPS.md.

Reads raw/cavt/cavt_entries.csv (enriched with DiTommaso cross-references).
CAVT_GAPS.md holds numbers, titles, DiTommaso dossier links, and our own notes,
so it can be safely committed to version control.
"""
import collections
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# OCP file -> CAVT number (None = outside CAVT's scope); note describes specific version
OCP_TO_CAVT = {
    "AdamEve.xml": (1, "Greek version = Apocalypsis Moysi, 1.i"),
    "TAdam.xml": (3, "Syriac/Arabic/Greek Testament of Adam"),
    "1En.xml": (61, "Ethiopic 1 Enoch"),
    "Jub.xml": (132, "Ethiopic Jubilees"),
    "Jubi.xml": (132, "Latin Jubilees fragment"),
    "Mois.xml": (134, "Latin Assumption of Moses"),
    "TAbr.xml": (88, "Testament of Abraham"),
    "TAbA.xml": (88, "Long recension (Recension A)"),
    "TAbB.xml": (88, "Short recension (Recension B)"),
    "JosAsen.xml": (105, "Greek Joseph and Aseneth"),
    "T12P.xml": (118, "Greek Testaments of the Twelve Patriarchs"),
    "Amram.xml": (121, "4Q543-547 Visions of Amram"),
    "4Q548.xml": (121, "4Q548 Visions of Amram"),
    "ElMod.xml": (133, "Eldad and Modad (Hermas citation)"),
    "HistRech.xml": (166, "History of the Rechabites / Story of Zosimus"),
    "TSol.xml": (162, "Testament of Solomon (Greek recensions)"),
    "4Ezra.xml": (180, "4 Ezra (Latin Vulgate / Bensly 1895)"),
    "5Ezra.xml": (180, "5 Ezra (4 Ezra 1-2)"),
    "6Ezra.xml": (180, "6 Ezra (4 Ezra 15-16)"),
    "Esdr.xml": (180, "Latin 4 Ezra"),
    "ApEzra.xml": (184, "Greek Apocalypse of Ezra (CAVT 184.i, Tischendorf 1866)"),
    "Sedrach.xml": (184, "Apocalypse of Sedrach (CAVT 184.ii, James 1893)"),
    "Esdl.xml": (184, "Visio beati Esdrae (latine, CAVT 184.iii, Bogaert 1984 / Denis 1993)"),
    "3Macc.xml": (198, "3 Maccabees (LXX)"),
    "4Macc.xml": (199, "4 Maccabees (LXX)"),
    "TJob.xml": (207, "Testament of Job (Greek)"),
    "PssSol.xml": (212, "Psalms of Solomon (Greek)"),
    "LivPro.xml": (213, "Lives of the Prophets (Greek recensions)"),
    "4Bar.xml": (225, "4 Baruch (Paraleipomena Jeremiou)"),
    "2Bar.xml": (233, "2 Baruch (Syriac Apocalypse of Baruch)"),
    "2Bar-Syr.xml": (233, "Syriac 2 Baruch (Ambrosian 7a1)"),
    "3Bar.xml": (235, "3 Baruch (Greek Apocalypse of Baruch)"),
    "ApocrEzek.xml": (244, "Apocryphon of Ezekiel (Greek fragments)"),
    "ApDan.xml": (253, "Greek Apocalypse of Daniel (Diegesis Danielis)"),
    "ApDan_TEI.xml": (253, "Greek Apocalypse of Daniel (TEI P5 draft)"),
    "LetAris.xml": (273, "Letter of Aristeas (Aristeae ad Philocratem Epistula)"),
    "SibOr.xml": (274, "Sibylline Oracles (Books 1-8)"),
    # Judaeo-Hellenistic writers: excluded by CAVT (Introductio), covered by Denis (2000) and DiTommaso (2001)
    "Aristob.xml": (None, "Aristobulus of Alexandria (Exegesis of Law of Moses)"),
    "Artap.xml": (None, "Artapanus (On the Jews)"),
    "ClMal.xml": (None, "Cleodemus Malchus (History of the Jews)"),
    "Eup.xml": (None, "Eupolemus (On the Kings of Judaea)"),
    "Ps-Eup.xml": (None, "Pseudo-Eupolemus (Anonymous Samaritan)"),
    "EzekTrag.xml": (None, "Ezekiel the Tragedian (Exagoge)"),
    "PhEPoet.xml": (None, "Philo the Epic Poet (On Jerusalem)"),
    "Theod.xml": (None, "Theodotus (On the Jews / Shechem)"),
    "ArisEx.xml": (None, "Aristeas the Exegete (On Job)"),
    "DeAdam.xml": (10, "De Adami compositione et nomine (latine, Förster 1908)"),
    "NarrMois.xml": (137, "Narratio de Moyse et Josue (graece, Vassiliev 1893)"),
    "VisEl.xml": (169, "Visio Eliae (latine, De Bruyne 1925)"),
    "OrMan.xml": (178, "Prayer of Manasseh (graece LXX Ode 12 / latine Vulg.)"),
    "ConfEsdr.xml": (181, "Confessio Esdrae / Oratio Esdrae (latine, Mercati 1901)"),
    "PsPhoc.xml": (182, "Sentences of Pseudo-Phocylides (graece, Bergk 1882)"),
    "RevEsdr.xml": (185, "Revelatio Esdrae de qualitatibus anni (latine, Mercati 1901)"),
    "OrJos.xml": (107, "Prayer of Joseph / Oratio Josephi (graece, Denis 1970)"),
    "Ps151.xml": (202, "Psalm 151 (hebraice 11Q5 / graece LXX / latine Vulg.)"),
    "OrMois.xml": (138, "Oratio Moysi in die obitus sui (latine, James 1893)"),
    "VisKenaz.xml": (147, "Visio Kenaz / Visio Zenez (latine, James 1893 / LAB 28)"),
    "ThrenSeila.xml": (148, "Threnus Seilae filiae Iephte (latine, James 1893 / LAB 40)"),
    "CithDavid.xml": (152, "Citharismus regis David contra daemonium Saulis (latine, James 1893 / LAB 60)"),
    "TracSem.xml": (85, "Treatise of Shem / Tractatus Sem (syriace, Mingana 1917)"),
    "AndronAsaph.xml": (None, "Andronicus and Asaph on the Zodiac of the Patriarchs (syriace, Mingana 1917)"),
    "PsOrph.xml": (183, "Testament of Orpheus / Hieroi Logoi (graece, Kern 1922)"),
    "PsHecat.xml": (84, "Pseudo-Hecataeus / De Iudaeis / De Abrahamo (graece, Denis 1970)"),
    "Thallus.xml": (None, "Thallus the Chronographer (graece, Jacoby FGrH 256 / Denis 1970)"),
    "Theoph.xml": (None, "Theophilus (graece, Jacoby FGrH 733 / Denis 1970)"),
    "Demetr.xml": (None, "Demetrius the Chronographer (graece, Jacoby FGrH 722 / Denis 1970)"),
    "Justus.xml": (None, "Justus of Tiberias (graece, Jacoby FGrH 734 / Holladay 1983)")
}

# hand corrections to the automatic tiers (checked against the editions, EDITIONS_CHECK.md):
# "lost" = no text survives; "part" = a section of another CAVT work, not a separate gap
HAND_TIERS = {
    6: ("lost", "testimonia only"),
    69: ("lost", "known only from Michael the Syrian"),
    138: ("part", "= LAB 19 (see 131)"),
    152: ("part", "= LAB 60.2-3 (see 131)"),
    153: ("C", "codex unicus, unedited in 1998"),
    181: ("part", "= 4 Ezra 8:20-36 (180, in OCP)"),
}

OCP_LANGS = {"Greek", "Latin", "Syriac", "Ethiopic", "Aramaic", "Hebrew"}

EXCLUDED_FROM_CAVT = [
    {"author": "Aristeas the Exegete", "work": "Peri Iob (On Job)", "ch": 48,
     "dossier": "Aristeas_the_Exegete.md", "clavis": "Jacoby FGrH 725; Holladay FHJA 1.261-275", "ocp_file": "ArisEx.xml"},
    {"author": "Aristobulus of Alexandria", "work": "Exegesis of the Law of Moses", "ch": 49,
     "dossier": "Aristobulus.md", "clavis": "Holladay FHJA 3.1-250; Denis FPG 217-228", "ocp_file": "Aristob.xml"},
    {"author": "Artapanus", "work": "Peri Ioudaion (On the Jews)", "ch": 50,
     "dossier": "Artapanus.md", "clavis": "Jacoby FGrH 726; Holladay FHJA 1.189-243", "ocp_file": "Artap.xml"},
    {"author": "Cleodemus Malchus", "work": "History of the Jews", "ch": 51,
     "dossier": "Cleodemus_Malchus.md", "clavis": "Jacoby FGrH 727; Holladay FHJA 1.245-259", "ocp_file": "ClMal.xml"},
    {"author": "Demetrius the Chronographer", "work": "On the Kings in Judaea", "ch": 52,
     "dossier": "Demetrius_the_Chronographer.md", "clavis": "Jacoby FGrH 722; Holladay FHJA 1.51-91", "ocp_file": "Demetr.xml"},
    {"author": "Eupolemus", "work": "On the Kings of Judaea", "ch": 53,
     "dossier": "Eupolemus.md", "clavis": "Jacoby FGrH 723; Holladay FHJA 1.93-156", "ocp_file": "Eup.xml"},
    {"author": "Pseudo-Eupolemus", "work": "On the Jews (Anonymous Samaritan)", "ch": 54,
     "dossier": "Pseudo_Eupolemus.md", "clavis": "Jacoby FGrH 724; Holladay FHJA 1.157-187", "ocp_file": "Ps-Eup.xml"},
    {"author": "Ezekiel the Tragedian", "work": "Exagoge (The Exodus drama)", "ch": 55,
     "dossier": "Ezekiel_the_Tragedian.md", "clavis": "TrGF 1.128; Holladay FHJA 2.301-529", "ocp_file": "EzekTrag.xml"},
    {"author": "Pseudo-Hecataeus", "work": "On the Jews / On Abraham", "ch": 56,
     "dossier": "Pseudo_Hecataeus.md", "clavis": "Jacoby FGrH 264/730; Holladay FHJA 1.277-335", "ocp_file": "PsHecat.xml"},
    {"author": "Justus of Tiberias", "work": "Chronicle of Kings / Jewish War", "ch": 57,
     "dossier": "Justus_of_Tiberias.md", "clavis": "Jacoby FGrH 734; Holladay FHJA 1.371-389", "ocp_file": "Justus.xml"},
    {"author": "Pseudo-Orpheus", "work": "Diatheke (Testament of Orpheus)", "ch": 58,
     "dossier": "Pseudo_Orpheus.md", "clavis": "Holladay FHJA 4.1-300; Kern OF 245-248", "ocp_file": "PsOrph.xml"},
    {"author": "Philo the Epic Poet", "work": "Peri Ta Hierosolyma (On Jerusalem)", "ch": 59,
     "dossier": "Philo_the_Epic_Poet.md", "clavis": "Jacoby FGrH 729; Holladay FHJA 2.205-299", "ocp_file": "PhEPoet.xml"},
    {"author": "Thallus", "work": "Histories (Universal Chronography)", "ch": 60,
     "dossier": "Thallus.md", "clavis": "Jacoby FGrH 256; Holladay FHJA 1.343-369", "ocp_file": "Thallus.xml"},
    {"author": "Theodotus", "work": "On the Jews (Epic on Shechem)", "ch": 61,
     "dossier": "Theodotus.md", "clavis": "Jacoby FGrH 732; Holladay FHJA 2.51-204", "ocp_file": "Theod.xml"},
    {"author": "Theophilus", "work": "On Solomon and Hiram of Tyre", "ch": 62,
     "dossier": "Theophilus.md", "clavis": "Jacoby FGrH 733; Holladay FHJA 1.337-341", "ocp_file": "Theoph.xml"},
    {"author": "Hellenistic Synagogal Prayers", "work": "16 Synagogal Prayers in Apostolic Const. 7-8", "ch": 20,
     "dossier": "Hellenistic_Synagogal_Prayers.md", "clavis": "Delling; van der Horst", "ocp_file": "— (Gap)"},
    {"author": "Sentences of Syriac Menander", "work": "Syriac Sapiential Florilegium", "ch": 33,
     "dossier": "Sentences_of_the_Syriac_Menander.md", "clavis": "Baars; Land; Schulthess", "ocp_file": "— (Gap)"},
    {"author": "Sentences of Pseudo-Phocylides", "work": "Gnomological Hexameters", "ch": 37,
     "dossier": "Sentences_of_Pseudo_Phocylides.md", "clavis": "van der Horst; Derron", "ocp_file": "PsPhoc.xml"}
]


def format_dossier_link(row):
    dossier = row.get("ditommaso_dossier")
    ch = row.get("ditommaso_ch")
    if dossier:
        return f"[{dossier}](bibliography/{dossier}) (Ch. {ch})"
    return "—"


def main():
    rows = list(csv.DictReader((ROOT / "raw/cavt/cavt_entries.csv").open(encoding="utf-8")))
    have = {n for n, _ in OCP_TO_CAVT.values() if n}
    docs = sorted(p.name for p in (ROOT / "static/docs").glob("*.xml"))
    unmapped = [d for d in docs if d not in OCP_TO_CAVT]

    def tier(e):
        if int(e["cavt_no"]) in HAND_TIERS:
            return HAND_TIERS[int(e["cavt_no"])][0]
        langs = set(filter(None, (e["title_language"] or e["main_language"]).split("; ")))
        edited = int(e["n_inedita_on_pages"]) == 0
        ocp_lang = not langs or bool(langs & OCP_LANGS)
        if edited and ocp_lang:
            return "A"
        return "B" if edited else "C"

    gaps = [e for e in rows if int(e["cavt_no"]) not in have
            and e["pro_memoria"] != "True" and e["cross_ref_only"] != "True"]
    rec = {int(e["cavt_no"]): e for e in rows}

    def licence(e, depth=0):
        """'PD?' if CAVT lists an edition from 1929 or earlier, 'modern' if only later ones."""
        years = [int(y) for y in e["edition_years"].split()]
        if not years and e["refers_to"] and depth < 2:
            refs = [licence(rec[int(n)], depth + 1) for n in e["refers_to"].split() if int(n) in rec]
            return "PD?" if "PD?" in refs else (refs[0] if refs else "")
        if not years:
            return "none listed"
        return "PD?" if min(years) <= 1929 else "modern"

    order = {"PD?": 0, "modern": 1, "none listed": 2, "": 3}
    by_tier = {t: sorted((e for e in gaps if tier(e) == t), key=lambda e: order[licence(e)])
               for t in "ABC"}
    by_cavt = {}
    for f, (n, note) in OCP_TO_CAVT.items():
        by_cavt.setdefault(n, []).append(f + (f" ({note})" if note else ""))
    title = {int(e["cavt_no"]): e["title"] for e in rows}

    mapped_cavt_count = sum(1 for e in rows if e.get("ditommaso_dossier"))

    out = [
        "# CAVT Gap Analysis and DiTommaso Bibliographic Crosswalk",
        "",
        "Generated by `scripts/cavt_gaps.py` from Haelewyck, *Clavis Apocryphorum Veteris Testamenti* (1998), "
        "enriched with Lorenzo DiTommaso, *A Bibliography of Pseudepigrapha Research, 1850–1999* (2001) "
        "and Albert-Marie Denis, *Introduction à la littérature religieuse judéo-hellénistique* (2000).",
        "",
        f"- **CAVT Works**: {len(rows)} entries in `raw/cavt/cavt_entries.csv`.",
        f"- **CAVT Works mapped to DiTommaso dossiers**: {mapped_cavt_count} entries cross-referenced.",
        f"- **Current OCP Coverage**: {len(have)} CAVT works (represented across {len([k for k, v in OCP_TO_CAVT.items() if v[0] is not None])} XML editions).",
        f"- **Outside CAVT Scope**: {len(EXCLUDED_FROM_CAVT)} Judaeo-Hellenistic & sapiential works (9 published in OCP XML, 9 gap candidates).",
        f"- **Total OCP Gaps within CAVT**: {len(gaps)} (excluding {sum(e['pro_memoria'] == 'True' for e in rows)} pro-memoria and {sum(e['cross_ref_only'] == 'True' for e in rows)} cross-reference entries).",
        "",
        "### Tiers (Automated Classification from CAVT and DiTommaso):",
        "- **Tier A**: No *Inedita* noted; extant in a primary OCP language (Greek, Latin, Syriac, Ethiopic, Aramaic, Hebrew).",
        "- **Tier B**: Edited, but preserved primarily in other linguistic streams (Armenian, Arabic, Slavonic, Coptic, Georgian).",
        "- **Tier C**: Contains *Inedita* (manuscripts remaining unedited or lacking standard critical editions).",
        "",
        "### Editions & Licences:",
        "- **PD?**: CAVT/DiTommaso lists an edition published in 1929 or earlier (likely public domain for OCP digitization).",
        "- **modern**: Critical edition is post-1929 (DJD, Brepols, Brill, OUP, CSCO; check copyright status).",
        "- **none listed**: No independent critical edition found in Haelewyck.",
        "",
        "---",
        "",
        "## 1. OCP Active Texts -> CAVT & DiTommaso Crosswalk",
        "",
        "| CAVT | Title | OCP File(s) | DiTommaso Dossier |",
        "|---|---|---|---|"
    ]

    for n in sorted(k for k in by_cavt if k):
        entry_row = rec.get(n, {})
        dossier_str = format_dossier_link(entry_row)
        out.append(f"| {n} | {title[n]} | {', '.join(by_cavt[n])} | {dossier_str} |")

    out += [
        "",
        "---",
        "",
        "## 2. Judaeo-Hellenistic & Sapiential Works (Outside CAVT Scope)",
        "",
        "Excluded from Haelewyck's *Introductio* (p. xii) as non-apocryphal Hellenistic/sapiential literature; "
        "systematically covered by DiTommaso (2001) and Denis (*Introduction*, 2000):",
        "",
        "| Author / Work | DiTommaso Ch. | Dossier | Standard Clavis / Collections | OCP XML Status |",
        "|---|---|---|---|---|"
    ]

    for item in EXCLUDED_FROM_CAVT:
        out.append(f"| **{item['author']}** — *{item['work']}* | Ch. {item['ch']} | "
                   f"[{item['dossier']}](bibliography/{item['dossier']}) | {item['clavis']} | `{item['ocp_file']}` |")

    if unmapped:
        out += ["", f"**Unmapped OCP Files**: {', '.join(unmapped)}", ""]

    out += ["", "---", ""]

    for t, head in [("A", "Tier A - Edited, Primary OCP Language"),
                    ("B", "Tier B - Edited, Other Language Stream"),
                    ("C", "Tier C - Contains Inedita")]:
        out += [
            f"## 3.{'ABC'.index(t)+1} {head} ({len(by_tier[t])})",
            "",
            "| CAVT | Title | Section | Language | Editions | DiTommaso Dossier | Translations | Qumran |",
            "|---|---|---|---|---|---|---|---|"
        ]
        for e in by_tier[t]:
            lang = e["title_language"] or (e["main_language"] + "?" if e["main_language"] else "")
            dossier_str = format_dossier_link(e)
            out.append(
                f"| {e['cavt_no']} | {e['title']} | {e['section'].title()} | {lang} | "
                f"{licence(e)} | {dossier_str} | {e['translations']} | {'yes' if e['qumran'] == 'True' else ''} |"
            )
        out.append("")

    out += ["## 3.4 Excluded by hand (lost works; parts of other entries)", "",
            "| CAVT | Title | Reason |", "|---|---|---|"]
    out += [f"| {n} | {title[n]} | {why} |" for n, (t, why) in sorted(HAND_TIERS.items()) if t in ("lost", "part")]
    out.append("")

    (ROOT / "CAVT_GAPS.md").write_text("\n".join(out), encoding="utf-8")
    print(f"Generated {ROOT / 'CAVT_GAPS.md'}")
    print(f"Tiers: { {t: len(v) for t, v in by_tier.items()} }")
    print(f"Licences in tiers: { {t: dict(collections.Counter(licence(e) for e in v)) for t, v in by_tier.items()} }")


if __name__ == "__main__":
    main()
