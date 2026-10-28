#!/usr/bin/env python3
"""Allocate transcribed sections of Albert-Marie Denis, Introduction à la littérature
religieuse judéo-hellénistique, Tome II (Brepols, 2000) to CAVT folders, dossiers, and crosswalks.

Outputs:
1. Granular section markdown files in raw/cavt/denis2000_sections/ (and symlink raw/denis/sections)
2. Comprehensive Table of Contents in raw/denis/TOC_Tome2.md
3. Enriched bibliography/cavt_snippets/ files with Denis 2000 sections
4. Enriched bibliography/*.md dossiers with Denis 2000 sections and direct links
5. Updated raw/cavt/cavt_entries.csv with Denis 2000 volume, chapter, and page references
6. Updated CAVT_GAPS.md crosswalk
"""

import csv
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VLM_DIR = ROOT / "raw" / "editions" / "denis2000_vlm_pages"
CAVT_SECTIONS_DIR = ROOT / "raw" / "cavt" / "denis2000_sections"
DENIS_DIR = ROOT / "raw" / "denis"
BIBLIO_DIR = ROOT / "bibliography"
CAVT_SNIPPETS_DIR = BIBLIO_DIR / "cavt_snippets"
CAVT_CSV = ROOT / "raw" / "cavt" / "cavt_entries.csv"
CAVT_GAPS_MD = ROOT / "CAVT_GAPS.md"

CAVT_SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
DENIS_DIR.mkdir(parents=True, exist_ok=True)

# Symlink raw/denis/sections -> ../cavt/denis2000_sections
denis_symlink = DENIS_DIR / "sections"
if not denis_symlink.exists():
    try:
        denis_symlink.symlink_to("../cavt/denis2000_sections")
    except Exception as e:
        print(f"Symlink note: {e}")

# Definition of sections in Denis 2000 Tome II
# start_split / end_split define regex pattern on shared pages
SECTIONS = [
    {
        "id": "Ch00_Front_Matter",
        "title": "Front Matter (Titre, Dédicace, Introduction à la partie III)",
        "ch": "Front Matter",
        "start_page": 1,
        "start_split": None,
        "end_page": 7,
        "end_split": None,
        "printed_pages": "pp. 883–888",
        "cavt": "",
        "dossier": "",
        "summary": "Page de garde, titre, mentions légales et faux-titre de la Partie III: Écrits judéo-hellénistiques parallèles aux écrits bibliques."
    },
    {
        "id": "Ch30_Testament_de_Job",
        "title": "Le Testament de Job",
        "ch": "30",
        "start_page": 8,
        "start_split": None,
        "end_page": 29,
        "end_split": None,
        "printed_pages": "pp. 889–909",
        "cavt": "207",
        "dossier": "Testament_of_Job.md",
        "summary": "Midrash hagiographique sur le saint homme Job. Étude détaillée du texte grec (mss Paris. gr. 2658, Vatic. gr. 1238, Messan. gr. 29), de la version copte sahidique (P. Köln 3221), de la version slave, des rapports avec la LXX, du milieu judéo-hellénistique (milieu thérapeutique ou essénien) et de la riche bibliographie."
    },
    {
        "id": "Ch31_Lettre_d_Aristee",
        "title": "La Lettre d'Aristée",
        "ch": "31",
        "start_page": 30,
        "start_split": None,
        "end_page": 65,
        "end_split": None,
        "printed_pages": "pp. 910–946",
        "cavt": "273",
        "dossier": "Letter_of_Aristeas.md",
        "summary": "Monographie critique sur la Lettre d'Aristée à Philocrate racontant la traduction de la Septante sous Ptolémée II Philadelphe. Examen des 23 manuscrits grecs (famille des Octateuques et mss séparés), des citations patristiques (Eusèbe, Flavius Josèphe), de la composition littéraire (le banquet royal, l'éloge de la Loi), de la date (IIe s. av. J.-C.) et du milieu alexandrin."
    },
    {
        "id": "Ch32_Oracles_Sibyllins",
        "title": "Les Oracles Sibyllins",
        "ch": "32",
        "start_page": 66,
        "start_split": None,
        "end_page": 111,
        "end_split": None,
        "printed_pages": "pp. 947–993",
        "cavt": "274",
        "dossier": "Sibylline_Oracles.md",
        "summary": "Exposé magistral sur le recueil des Oracles Sibyllins (Livres I à XIV). Histoire des collections sibyllines païennes, juives et chrétiennes; tradition manuscrite grecque complexe (classes φ, ψ, Ω); analyse détaillée des Livres juifs (notamment Livre III, vers 140 av. J.-C., Livre IV, vers 80 ap. J.-C., Livre V, Livre XI-XIV); le mythe de Néron redivivus et l'eschatologie hellénistique."
    },
    {
        "id": "Ch33_Ahiqar",
        "title": "L'Histoire et les Maximes d'Aḥiqar",
        "ch": "33",
        "start_page": 112,
        "start_split": None,
        "end_page": 155,
        "end_split": None,
        "printed_pages": "pp. 994–1036",
        "cavt": "195",
        "dossier": "Ahiqar.md",
        "summary": "Étude monumentale du roman sapiential d'Aḥiqar, sage et chancelier sous Sennachérib et Assarhaddon. Analyse comparative des versions: araméen d'Éléphantine (Ves. av. J.-C.), syriaque, arménienne, arabe, éthiopienne, slavonne, grecque (Vie d'Ésope) et roumaine; relations avec Tobit, Ben Sira, et le Nouveau Testament."
    },
    {
        "id": "Ch34_Sentences_du_Pseudo_Phocylide",
        "title": "Les Sentences du Pseudo-Phocylide",
        "ch": "34",
        "start_page": 156,
        "start_split": None,
        "end_page": 181,
        "end_split": None,
        "printed_pages": "pp. 1037–1061",
        "cavt": "182-pseudo",
        "dossier": "Sentences_of_Pseudo_Phocylides.md",
        "summary": "Poème gnomique judéo-hellénistique en 230 hexamètres dactyliques attribué au poète milésien Phocylide. Examen philologique des nombreux manuscrits byzantins et de la tradition gnomologique; synthèse morale conciliant l'éthique biblique (Décalogue, Lévitique) et la philosophie grecque populaire; composition à Alexandrie entre 50 av. et 50 ap. J.-C."
    },
    {
        "id": "Ch35_Anthologie_Pseudo_Orphee",
        "title": "Anthologie judéo-hellénistique de citations fictives d'auteurs grecs (Pseudo-Orphée)",
        "ch": "35",
        "start_page": 182,
        "start_split": None,
        "end_page": 225,
        "end_split": None,
        "printed_pages": "pp. 1062–1106",
        "cavt": "183-pseudo",
        "dossier": "Pseudo_Orpheus.md",
        "summary": "Étude approfondie de la Diathéké / Testament d'Orphée et des florilèges de citations fictives mises sous les noms d'Orphée, Sophocle, Euripide, Eschyle, Hésiode et Homère chez Aristobule, le Pseudo-Justin (De Monarchia, Cohortatio), Clément d'Alexandrie et Eusèbe; tradition manuscrite, recensions longue et brève du poème orphique, apologétique monothéiste."
    },
    {
        "id": "Ch36_00_Historiens_Introduction",
        "title": "Les Historiens judéo-hellénistiques — Introduction générale et manuscrits",
        "ch": "36.0",
        "start_page": 226,
        "start_split": None,
        "end_page": 241,
        "end_split": r"1\.\s+Démétrius",
        "printed_pages": "pp. 1107–1122",
        "cavt": "",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Introduction d'ensemble aux historiens judéo-hellénistiques préservés principalement dans la Préparation évangélique d'Eusèbe de Césarée par l'intermédiaire d'Alexandre Polyhistor, et dans les Stromates de Clément d'Alexandrie. Étude codicologique détaillée des témoins manuscrits d'Eusèbe (classes de manuscrits, mss Paris. gr. 451, 465, 466, 467, 468, Marc. 341, Bonon. 3643, etc.) et de Clément (Flor. Laur. V 3)."
    },
    {
        "id": "Ch36_01_Demetrius",
        "title": "Démétrius le Chronographe (l'Historien / l'Exégète)",
        "ch": "36.1",
        "start_page": 241,
        "start_split": r"1\.\s+Démétrius",
        "end_page": 246,
        "end_split": r"2\.\s+Eupolème",
        "printed_pages": "pp. 1122–1128",
        "cavt": "Holladay FHJA 1",
        "dossier": "Demetrius_the_Chronographer.md",
        "summary": "Les fragments de Démétrius (Ptolémée IV Philopator, fin du IIIe s. av. J.-C.), premier auteur judéo-hellénistique connu écrivant en prose grecque. Analyse des apories exégétiques sur la vie de Jacob, l'Exode, les eaux douces de Mara, les armes des Hébreux, et le calcul chronologique des déportations."
    },
    {
        "id": "Ch36_02_Eupoleme",
        "title": "Eupolème",
        "ch": "36.2",
        "start_page": 246,
        "start_split": r"2\.\s+Eupolème",
        "end_page": 254,
        "end_split": r"3\.\s+Artapan",
        "printed_pages": "pp. 1128–1135",
        "cavt": "Holladay FHJA 1",
        "dossier": "Eupolemus.md",
        "summary": "Eupolème, fils de Jean, prêtre et diplomate hasmonéen envoyé à Rome en 161 av. J.-C. Analyse de son œuvre Sur les rois de Judée: Moïse inventeur de l'alphabet, David, correspondance royale de Salomon avec l'Égypte et Tyr, splendeur architecturale du Temple, prophétie de Jérémie et calcul chronologique d'Adam à 158 av. J.-C."
    },
    {
        "id": "Ch36_03_Artapan",
        "title": "Artapan",
        "ch": "36.3",
        "start_page": 254,
        "start_split": r"3\.\s+Artapan",
        "end_page": 265,
        "end_split": r"4\.\s+Aristée\s+l[\'’]Historien",
        "printed_pages": "pp. 1135–1147",
        "cavt": "Holladay FHJA 1",
        "dossier": "Artapanus.md",
        "summary": "Artapan (IIe s. av. J.-C.), historiographie romancée judéo-égyptienne. Les trois fragments sur Abraham, Joseph (administrateur de l'Égypte) et Moïse identifié à Mousaios maître d'Orphée et à Hermès-Thoth; fondation des cultes animaux et de la civilisation égyptienne; expédition victorieuse en Éthiopie et délivrance miraculeuse lors de l'Exode."
    },
    {
        "id": "Ch36_04_Aristee_Exegete",
        "title": "Aristée l'Historien ou l'Exégète",
        "ch": "36.4",
        "start_page": 265,
        "start_split": r"4\.\s+Aristée\s+l[\'’]Historien",
        "end_page": 269,
        "end_split": r"5\.\s+Cléodème",
        "printed_pages": "pp. 1147–1150",
        "cavt": "Holladay FHJA 1",
        "dossier": "Aristeas_the_Exegete.md",
        "summary": "Fragment d'Aristée sur le livre de Job préservé par Alexandre Polyhistor (Eusèbe, PE 9.25.1-4). Identification d'Ésau et de Jobab, théologie de la patience, comparaison avec le Testament de Job et l'appendice de la LXX."
    },
    {
        "id": "Ch36_05_Cleodeme_Malchas",
        "title": "Cléodème-Malchâs",
        "ch": "36.5",
        "start_page": 269,
        "start_split": r"5\.\s+Cléodème",
        "end_page": 273,
        "end_split": r"6\.\s+L[\'’]Historien\s+anonyme",
        "printed_pages": "pp. 1150–1154",
        "cavt": "Holladay FHJA 1",
        "dossier": "Cleodemus_Malchus.md",
        "summary": "Cléodème-Malchâs (IIe-Ier s. av. J.-C.), prophète et historien cité par Flavius Josèphe (Ant. 1.240-241) d'après Polyhistor. Descendance d'Abraham par Céthura (Apher, Aphras, Japhran), alliance avec Héraclès dans l'expédition contre la Libye et Antée; syncrétisme mythologique et apologétique."
    },
    {
        "id": "Ch36_06_Pseudo_Eupoleme",
        "title": "L'Historien anonyme ou Pseudo-Eupolème",
        "ch": "36.6",
        "start_page": 273,
        "start_split": r"6\.\s+L[\'’]Historien\s+anonyme",
        "end_page": 279,
        "end_split": r"7\.\s+Théophile",
        "printed_pages": "pp. 1154–1160",
        "cavt": "Holladay FHJA 1",
        "dossier": "Pseudo_Eupolemus.md",
        "summary": "Fragments attribués par Polyhistor à Eupolème mais d'une plume samaritaine anonyme (cité par Freudenthal). Abraham honoré au mont Garizim (mont du Très-Haut), inventeur de l'astrologie enseignée aux Phéniciens et aux prêtres d'Héliopolis; généalogie des Géants et de la Tour de Babel."
    },
    {
        "id": "Ch36_07_Theophile",
        "title": "Théophile",
        "ch": "36.7",
        "start_page": 279,
        "start_split": r"7\.\s+Théophile",
        "end_page": 281,
        "end_split": r"8\.\s+Hécatée\s+d[\'’]Abdère",
        "printed_pages": "pp. 1160–1163",
        "cavt": "Holladay FHJA 1",
        "dossier": "Theophilus.md",
        "summary": "Court fragment sur Salomon et la construction du Temple préservé dans la Préparation évangélique (9.34.19). Salomon fait fondre une statue d'or massif représentant sa fille et l'envoie à Hiram roi de Tyr; discussion sur l'origine judéo-hellénistique ou païenne de l'auteur."
    },
    {
        "id": "Ch36_08_Pseudo_Hecatee",
        "title": "Hécatée d'Abdère (Pseudo-Hécatée)",
        "ch": "36.8",
        "start_page": 281,
        "start_split": r"8\.\s+Hécatée\s+d[\'’]Abdère",
        "end_page": 291,
        "end_split": r"9\.\s+Pseudo-Callisthène",
        "printed_pages": "pp. 1163–1173",
        "cavt": "84",
        "dossier": "Pseudo_Hecataeus.md",
        "summary": "Les traités judéo-hellénistiques Sur les Juifs et Sur Abraham mis sous le nom de l'historien grec Hécatée d'Abdère (contemporain d'Alexandre le Grand et de Ptolémée Ier). Extraits dans le Contre Apion de Flavius Josèphe: éloge du grand-prêtre Ézéchias, loyauté des Juifs à la Loi sous Alexandre, anecdocte de l'archer juif Mosollamos; distinction entre l'Hécatée authentique et le faussaire juif."
    },
    {
        "id": "Ch36_09_Pseudo_Callisthene",
        "title": "Pseudo-Callisthène (Roman d'Alexandre)",
        "ch": "36.9",
        "start_page": 291,
        "start_split": r"9\.\s+Pseudo-Callisthène",
        "end_page": 296,
        "end_split": None,
        "printed_pages": "pp. 1173–1177",
        "cavt": "",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Épisodes juifs interpolés dans le Roman d'Alexandre (recension C): la visite d'Alexandre à Jérusalem, l'hommage rendu au grand-prêtre Jaddua, l'enfermement des nations impures de Gog et Magog derrière les Portes Caspiennes; tradition manuscrite byzantine et répercussions apocalyptiques médiévales."
    },
    {
        "id": "Ch36_10a_Juste_de_Tiberiade",
        "title": "Juste de Tibériade",
        "ch": "36.10a",
        "start_page": 297,
        "start_split": r"a\.\s+Juste\s+de\s+Tibériade",
        "end_page": 299,
        "end_split": r"b\.\s+Thall[ou]s",
        "printed_pages": "pp. 1177–1180",
        "cavt": "Holladay FHJA 1",
        "dossier": "Justus_of_Tiberias.md",
        "summary": "Juste de Tibériade en Galilée, contemporain et rival de Flavius Josèphe lors de la révolte juive de 66. Témoignages de Josèphe (Autobiographie) et de Photius (Bibliothèque, cod. 33) sur sa Chronique des rois juifs de Moïse à Agrippa II et son Histoire de la guerre juive."
    },
    {
        "id": "Ch36_10b_Thallos",
        "title": "Thallos le Chronographe",
        "ch": "36.10b",
        "start_page": 299,
        "start_split": r"b\.\s+Thall[ou]s",
        "end_page": 302,
        "end_split": r"c\.\s+Nicolas\s+de\s+Damas",
        "printed_pages": "pp. 1180–1184",
        "cavt": "Holladay FHJA 1",
        "dossier": "Thallus.md",
        "summary": "Thallos, chronographe samaritain ou affranchi impérial sous Tibère (auteur d'une Histoire universelle en trois livres). Témoignages de Jules l'Africain sur les ténèbres solaires lors de la crucifixion du Christ; citations chez Théophile d'Antioche, Tertullien et Lactance."
    },
    {
        "id": "Ch36_10c_Nicolas_de_Damas",
        "title": "Nicolas de Damas",
        "ch": "36.10c",
        "start_page": 302,
        "start_split": r"c\.\s+Nicolas\s+de\s+Damas",
        "end_page": 304,
        "end_split": r"d\.\s+Hystaspe",
        "printed_pages": "pp. 1184–1186",
        "cavt": "",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Nicolas de Damas, diplomate et historien à la cour d'Hérode le Grand (Histoire universelle en 144 livres). Extraits cités par Flavius Josèphe sur Abraham roi de Damas, l'Arche de Noé en Arménie, et l'histoire des souverains hasmonéens et hérodiens."
    },
    {
        "id": "Ch36_10d_Hystaspe",
        "title": "Les Oracles d'Hystaspe",
        "ch": "36.10d",
        "start_page": 304,
        "start_split": r"d\.\s+Hystaspe",
        "end_page": 309,
        "end_split": None,
        "printed_pages": "pp. 1186–1189",
        "cavt": "",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Les Oracles d'Hystaspe, apocryphe persique hellénisé utilisé par les cercles judéo-hellénistiques et chrétiens (Clément d'Alexandrie, Justin Martyr, Lactance). Prophéties eschatologiques sur la destruction de Rome par le feu cosmique et le sauvetage final des justes."
    },
    {
        "id": "Ch37_00_Auteurs_Litteraires_Intro",
        "title": "Les Auteurs littéraires judéo-hellénistiques — Introduction générale",
        "ch": "37.0",
        "start_page": 310,
        "start_split": None,
        "end_page": 311,
        "end_split": r"1\.\s+Philon\s+l[\'’]Ancien",
        "printed_pages": "pp. 1190–1191",
        "cavt": "",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Introduction aux poètes et dramaturges judéo-hellénistiques préservés par Polyhistor, Eusèbe et Clément d'Alexandrie: poésie épique hexamétrique et tragédie dramatique iambique au service de la mémoire sacrée d'Israël."
    },
    {
        "id": "Ch37_01_Philon_l_Ancien",
        "title": "Philon l'Ancien ou l'Épique",
        "ch": "37.1",
        "start_page": 311,
        "start_split": r"1\.\s+Philon\s+l[\'’]Ancien",
        "end_page": 316,
        "end_split": r"2\.\s+Théodote",
        "printed_pages": "pp. 1191–1196",
        "cavt": "Holladay FHJA 2",
        "dossier": "Philo_the_Epic_Poet.md",
        "summary": "Philon l'Ancien (IIIe-IIe s. av. J.-C.), auteur du poème épique Sur Jérusalem (Περὶ τὰ Ἱεροσόλυμα). Analyse stylistique des 24 hexamètres dactyliques conservés par Eusèbe: Abraham et la ligature d'Isaac, Joseph maître de l'Égypte, et la description topographique monumentale des sources d'eau et des aqueducs de Jérusalem."
    },
    {
        "id": "Ch37_02_Theodote",
        "title": "Théodote",
        "ch": "37.2",
        "start_page": 316,
        "start_split": r"2\.\s+Théodote",
        "end_page": 320,
        "end_split": r"3\.\s+Ézéchiel\s+le\s+Tragique",
        "printed_pages": "pp. 1196–1200",
        "cavt": "Holladay FHJA 2",
        "dossier": "Theodotus.md",
        "summary": "Théodote (IIe s. av. J.-C.), poète épique samaritain ou juif, auteur d'un poème sur Sichem (Sur les Juifs). Extraits en hexamètres homériques célébrant la beauté et la sacralité de Sichem, le viol de Dina, et le massacre justicier des Sichemites par Siméon et Lévi; théologie de la circoncision et de la pureté de la lignée sainte."
    },
    {
        "id": "Ch37_03_Ezechiel_le_Tragique",
        "title": "Ézéchiel le Tragique (L'Exagôgè)",
        "ch": "37.3",
        "start_page": 320,
        "start_split": r"3\.\s+Ézéchiel\s+le\s+Tragique",
        "end_page": 335,
        "end_split": r"4\.\s+Aristobule",
        "printed_pages": "pp. 1200–1216",
        "cavt": "Holladay FHJA 2",
        "dossier": "Ezekiel_the_Tragedian.md",
        "summary": "Ézéchiel le Poète tragique (IIe s. av. J.-C.), auteur du drame grec L'Exagôgè (269 trimètres iambiques euripidéens préservés par Eusèbe). Analyse des cinq actes: jeunesse de Moïse et fuite en Madian, le Buisson ardent, le rêve visionnaire du trône cosmique céleste, le récit de la traversée de la Mer Rouge par un messager égyptien rescapé, et l'apparition de l'oiseau merveilleux (Phénix) à l'oasis d'Élim."
    },
    {
        "id": "Ch37_04_Aristobule",
        "title": "Aristobule d'Alexandrie (Philosophe et Exégète)",
        "ch": "37.4",
        "start_page": 335,
        "start_split": r"4\.\s+Aristobule",
        "end_page": 357,
        "end_split": None,
        "printed_pages": "pp. 1216–1237",
        "cavt": "Holladay FHJA 3",
        "dossier": "Aristobulus.md",
        "summary": "Aristobule de Paneas / Alexandrie (c. 180-145 av. J.-C., dédié à Ptolémée VI Philométor), fondateur de l'exégèse philosophique judéo-hellénistique alexandrine. Analyse des fragments conservés par Clément et Eusèbe: dépendance de la philosophie grecque (Platon, Pythagore) envers Moïse; interprétation allégorique des anthropomorphismes bibliques; hymnes orphiques monothéistes et célébration de la sacralité cosmique du Sabbat (septénaire pythagoricien)."
    },
    {
        "id": "Ch38_01_Citations_sans_maitre",
        "title": "Les Citations sans maître (Écrits judéo-hellénistiques disparus)",
        "ch": "38.1",
        "start_page": 358,
        "start_split": None,
        "end_page": 410,
        "end_split": r"###\s+Supplément|###\s+Les\s+Apocalypses\s+de\s+Daniel",
        "printed_pages": "pp. 1238–1291",
        "cavt": "Citations",
        "dossier": "Hellenistic_Jewish_Fragments_Overview.md",
        "summary": "Corpus impressionnant des citations anonymes d'écrits judéo-hellénistiques disparus préservées dans la littérature chrétienne ancienne: Nouveau Testament (Jacques, Jude, Paul), 1-2 Clément de Rome, Épître de Barnabé, Didachè, Ignace d'Antioche, Justin Martyr, Clément d'Alexandrie, Hippolyte, Origène, Constitutions Apostoliques (notamment les prières synagogales hébraïques des Livres 7 et 8), Épiphane de Salamine, et papyrus magiques grecs."
    },
    {
        "id": "Ch38_02_Apocalypses_de_Daniel",
        "title": "Supplément — Le Cycle et les Apocalypses de Daniel",
        "ch": "38.2",
        "start_page": 410,
        "start_split": r"###\s+Supplément|###\s+Les\s+Apocalypses\s+de\s+Daniel",
        "end_page": 423,
        "end_split": None,
        "printed_pages": "pp. 1291–1304",
        "cavt": "253",
        "dossier": "Apocalypse_of_Daniel_Greek.md",
        "summary": "Revue critique complète des apocalypses médiévales et byzantines du prophète Daniel: fragments araméens de Qumrân (4Q243-245), Diegesis Danielis grecque (CAVT 253, Tischendorf 1866 / Berger 1976), Dernière Vision de Daniel, Visions slavons de Daniel, Quatorzième Vision de Daniel copte, Apocalypses arabes et arméniennes de Daniel, et textes onirocritiques."
    },
    {
        "id": "Indices_01_Index_Biblique",
        "title": "Index I — Index Biblique",
        "ch": "Indices",
        "start_page": 424,
        "start_split": None,
        "end_page": 439,
        "end_split": None,
        "printed_pages": "pp. 1306–1320",
        "cavt": "Index",
        "dossier": "",
        "summary": "Index complet des références vétérotestamentaires, deutérocanoniques et néotestamentaires citées ou discutées dans l'ensemble du Tome II."
    },
    {
        "id": "Indices_02_Index_Qumran_Massada",
        "title": "Index II — Index de Qumrân, Massada, etc.",
        "ch": "Indices",
        "start_page": 440,
        "start_split": None,
        "end_page": 443,
        "end_split": None,
        "printed_pages": "pp. 1321–1324",
        "cavt": "Index",
        "dossier": "",
        "summary": "Index des manuscrits de la mer Morte (Grottes 1Q à 11Q), Massada, Murabba'at et papyrus araméens/hébreux cités dans les deux tomes."
    },
    {
        "id": "Indices_03_Index_Ecrits_Auteurs_Anciens",
        "title": "Index III — Index des Œuvres et Auteurs Antiques",
        "ch": "Indices",
        "start_page": 444,
        "start_split": None,
        "end_page": 509,
        "end_split": None,
        "printed_pages": "pp. 1325–1390",
        "cavt": "Index",
        "dossier": "",
        "summary": "Index monumental de tous les écrits apocryphes et pseudépigraphiques (de A à Z), Pères apostoliques, auteurs grecs et latins classiques, historiens juifs et païens cités dans l'ouvrage."
    },
    {
        "id": "Indices_04_Index_Auteurs_Modernes",
        "title": "Index IV — Index des Auteurs Modernes",
        "ch": "Indices",
        "start_page": 510,
        "start_split": None,
        "end_page": 540,
        "end_split": None,
        "printed_pages": "pp. 1391–1420",
        "cavt": "Index",
        "dossier": "",
        "summary": "Index alphabétique exhaustif des savants et exégètes modernes (XIXe et XXe siècles) référencés dans les notes et appareils bibliographiques."
    }
]

def load_vlm_page(page_no: int) -> str:
    path = VLM_DIR / f"page_{page_no:03d}.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    return path.read_text(encoding="utf-8")

def split_and_write_sections():
    print(f"Splitting Denis 2000 Tome II into {len(SECTIONS)} sections...")
    pages_cache = {p: load_vlm_page(p) for p in range(1, 541)}

    for s in SECTIONS:
        sec_id = s["id"]
        start_p = s["start_page"]
        end_p = s["end_page"]
        start_split = s["start_split"]
        end_split = s["end_split"]

        text_pieces = []

        for p in range(start_p, end_p + 1):
            page_text = pages_cache[p]

            if p == start_p and start_split:
                m = re.search(start_split, page_text, re.IGNORECASE)
                if m:
                    # Keep header comment if present
                    header_m = re.match(r"(<!-- Page \d+ -->\s*)", page_text)
                    page_header = header_m.group(1) if header_m else ""
                    page_text = page_header + page_text[m.start():]
                else:
                    print(f"Warning: start_split '{start_split}' not found on page {p}")

            if p == end_p and end_split:
                m = re.search(end_split, page_text, re.IGNORECASE)
                if m:
                    page_text = page_text[:m.start()]
                else:
                    print(f"Warning: end_split '{end_split}' not found on page {p}")

            text_pieces.append(page_text.strip())

        body_content = "\n\n---\n\n".join(text_pieces)

        frontmatter = f"""---
title: "{s['title']}"
author: "Albert-Marie Denis O.P. (avec Jean-Claude Haelewyck)"
book: "Introduction à la littérature religieuse judéo-hellénistique, Tome II"
publisher: "Brepols (Turnhout, 2000)"
chapter: "{s['ch']}"
printed_pages: "{s['printed_pages']}"
scan_pages: "{start_p}–{end_p}"
cavt_no: "{s['cavt']}"
dossier: "{s['dossier']}"
summary: "{s['summary']}"
---

# Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique, Tome II
## {s['title']} ({s['printed_pages']})

> **Notice bibliographique**: Albert-Marie Denis O.P. et collaborateurs, avec le concours de Jean-Claude Haelewyck, *Introduction à la littérature religieuse judéo-hellénistique*, Tome II: *Pseudépigraphes de l'Ancien Testament*, Turnhout: Brepols, 2000, {s['printed_pages']}.
> **Dossier de recherche OCP**: {f"[{s['dossier']}](../../bibliography/{s['dossier']})" if s['dossier'] else "—"}
> **Clavis CAVT**: {s['cavt'] if s['cavt'] else "—"}

---

{body_content}
"""
        out_file = CAVT_SECTIONS_DIR / f"{sec_id}.md"
        out_file.write_text(frontmatter, encoding="utf-8")
        print(f"  -> Wrote {out_file.name} ({len(frontmatter)} bytes, {len(text_pieces)} pages)")

    print(f"Successfully generated all {len(SECTIONS)} section files in {CAVT_SECTIONS_DIR}.")

def generate_toc():
    print("Generating Denis 2000 Tome II Table of Contents...")
    toc_lines = [
        "# Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique, Tome II (Brepols, 2000)",
        "## Table des Matières et Répertoire Analytique des Sections",
        "",
        "> **Édition de référence**: Albert-Marie Denis O.P. et collaborateurs, avec le concours de Jean-Claude Haelewyck, *Introduction à la littérature religieuse judéo-hellénistique*, Tome II: *Pseudépigraphes de l'Ancien Testament*, Turnhout: Brepols, 2000, 540 pages (pp. 883–1421).",
        "> **Archivage numérique OCP**: PDF haute définition découpé en pages simples (`raw/editions/Denis2000_Introduction_judeo-hellenistique_Tome2_split_pages.pdf`), version ocrisée interrogeable (`raw/editions/Denis2000_Introduction_judeo-hellenistique_Tome2_searchable.pdf`), transcription intégrale VLM (`raw/editions/Denis2000_Introduction_judeo-hellenistique_Tome2.md`) et sections individuelles sous [`raw/cavt/denis2000_sections/`](../cavt/denis2000_sections/).",
        "",
        "---",
        "",
        "| Ch. / Section | Titre de l'Œuvre / Section | Pages Denis (2000) | Pages Scan | Dossier OCP | CAVT / Clavis | Fichier de Section |",
        "|---|---|---|---|---|---|---|"
    ]

    for s in SECTIONS:
        dossier_link = f"[{s['dossier']}](../../bibliography/{s['dossier']})" if s['dossier'] else "—"
        sec_file_link = f"[{s['id']}.md](sections/{s['id']}.md)"
        toc_lines.append(
            f"| **{s['ch']}** | {s['title']} | {s['printed_pages']} | {s['start_page']}–{s['end_page']} | {dossier_link} | {s['cavt'] or '—'} | {sec_file_link} |"
        )

    toc_lines.extend([
        "",
        "---",
        "",
        "### Concordance et Aperçu Analytique des Chapitres",
        "",
        "1. **Chapitre 30 — Le Testament de Job** (`Ch30_Testament_de_Job.md`, pp. 889–909):",
        "   - CAVT 207 (*Testamentum Iobi*); CANT 349; BHG 915; DiTommaso Ch. 25.",
        "   - Tradition manuscrite grecque (P, V, S), copte sahidique (P. Köln 3221), slavonne; milieu thérapeutique / essénien.",
        "",
        "2. **Chapitre 31 — La Lettre d'Aristée** (`Ch31_Lettre_d_Aristee.md`, pp. 910–946):",
        "   - CAVT 273 (*Epistula pseudo-Aristeae*); CANT 37; DiTommaso Ch. 8.",
        "   - 23 manuscrits grecs; apologétique alexandrine et genèse de la Septante sous Ptolémée Philadelphe.",
        "",
        "3. **Chapitre 32 — Les Oracles Sibyllins** (`Ch32_Oracles_Sibyllins.md`, pp. 947–993):",
        "   - CAVT 274 (*Oracula Sibyllina*); DiTommaso Ch. 39.",
        "   - Livres I–XIV; familles manuscrites grecques; analyse littéraire des strates juives (Livres III, IV, V, XI-XIV) et chrétiennes.",
        "",
        "4. **Chapitre 33 — L'Histoire et les Maximes d'Aḥiqar** (`Ch33_Ahiqar.md`, pp. 994–1036):",
        "   - CAVT 195 (*Historia et Sapientia Ahiqar*); DiTommaso Ch. 2.",
        "   - Papyrus araméens d'Éléphantine; versions syriaque, arménienne, arabe, éthiopienne, slavonne et grecque (Ésope).",
        "",
        "5. **Chapitre 34 — Les Sentences du Pseudo-Phocylide** (`Ch34_Sentences_du_Pseudo_Phocylide.md`, pp. 1037–1061):",
        "   - CAVT hors-cadre (cf. CAVT 182 pro memoria); CANT 35; DiTommaso Ch. 37.",
        "   - 230 hexamètres gnomiques judéo-hellénistiques conciliant morale biblique et éthique stoïcienne populaire.",
        "",
        "6. **Chapitre 35 — Anthologie Judéo-Hellénistique (Pseudo-Orphée)** (`Ch35_Anthologie_Pseudo_Orphee.md`, pp. 1062–1106):",
        "   - CAVT hors-cadre (cf. CAVT 183 pro memoria); CANT 33; DiTommaso Ch. 58.",
        "   - Diathéké / Testament d'Orphée; florilèges poétiques monothéistes (Sophocle, Euripide, Eschyle, Hésiode, Homère).",
        "",
        "7. **Chapitre 36 — Les Historiens Judéo-Hellénistiques** (pp. 1107–1189):",
        "   - Démétrius (pp. 1122–1128, DiTommaso Ch. 52)",
        "   - Eupolème (pp. 1128–1135, DiTommaso Ch. 53)",
        "   - Artapan (pp. 1135–1147, DiTommaso Ch. 50)",
        "   - Aristée l'Exégète (pp. 1147–1150, DiTommaso Ch. 48)",
        "   - Cléodème-Malchâs (pp. 1150–1154, DiTommaso Ch. 51)",
        "   - Pseudo-Eupolème / Anonyme samaritain (pp. 1154–1160, DiTommaso Ch. 54)",
        "   - Théophile (pp. 1160–1163, DiTommaso Ch. 62)",
        "   - Pseudo-Hécatée d'Abdère (pp. 1163–1173, CAVT 84, DiTommaso Ch. 56)",
        "   - Pseudo-Callisthène (pp. 1173–1177)",
        "   - Juste de Tibériade (pp. 1177–1180, DiTommaso Ch. 57)",
        "   - Thallus le Chronographe (pp. 1180–1184, DiTommaso Ch. 60)",
        "   - Nicolas de Damas & Hystaspe (pp. 1184–1189).",
        "",
        "8. **Chapitre 37 — Les Auteurs Littéraires Judéo-Hellénistiques** (pp. 1190–1237):",
        "   - Philon l'Ancien ou l'Épique (pp. 1191–1196, DiTommaso Ch. 59)",
        "   - Théodote l'Épique (pp. 1196–1200, DiTommaso Ch. 61)",
        "   - Ézéchiel le Tragique / Exagôgè (pp. 1200–1216, DiTommaso Ch. 55)",
        "   - Aristobule d'Alexandrie (pp. 1216–1237, DiTommaso Ch. 49).",
        "",
        "9. **Chapitre 38 — Citations sans maître et Apocalypses de Daniel** (pp. 1238–1305):",
        "   - Citations sans maître (pp. 1238–1291): Nouveau Testament, Pères apostoliques, Constitutions Apostoliques (prières synagogales hébraïques).",
        "   - Cycle et Apocalypses de Daniel (pp. 1291–1304): CAVT 253; Diegesis Danielis grecque, Dernière Vision, versions copte, arabe, arménienne.",
        "",
        "10. **Index Généraux** (pp. 1306–1420):",
        "    - Index Biblique (pp. 1306–1320)",
        "    - Index de Qumrân, Massada, etc. (pp. 1321–1324)",
        "    - Index des Œuvres et Auteurs Antiques (pp. 1325–1390)",
        "    - Index des Auteurs Modernes (pp. 1391–1420)."
    ])

    toc_file = DENIS_DIR / "TOC_Tome2.md"
    toc_file.write_text("\n".join(toc_lines) + "\n", encoding="utf-8")
    print(f"Wrote Table of Contents to {toc_file}")

def update_cavt_snippets():
    print("Updating CAVT snippet files in bibliography/cavt_snippets/...")
    
    cavt_to_section = {
        84: ("Ch36_08_Pseudo_Hecatee", "Hécatée d'Abdère (Pseudo-Hécatée)", "36 §8", "pp. 1163–1173", "Pseudo_Hecataeus.md"),
        195: ("Ch33_Ahiqar", "L'Histoire et les Maximes d'Aḥiqar", "33", "pp. 994–1036", "Ahiqar.md"),
        207: ("Ch30_Testament_de_Job", "Le Testament de Job", "30", "pp. 889–909", "Testament_of_Job.md"),
        253: ("Ch38_02_Apocalypses_de_Daniel", "Cycle et Apocalypses de Daniel", "38 Supplément", "pp. 1291–1304", "Apocalypse_of_Daniel_Greek.md"),
        273: ("Ch31_Lettre_d_Aristee", "La Lettre d'Aristée", "31", "pp. 910–946", "Letter_of_Aristeas.md"),
        274: ("Ch32_Oracles_Sibyllins", "Les Oracles Sibyllins", "32", "pp. 947–993", "Sibylline_Oracles.md"),
    }

    updated = 0
    for cavt_no, (sec_id, sec_title, ch_str, pages_str, dossier_name) in cavt_to_section.items():
        snippet_file = CAVT_SNIPPETS_DIR / f"CAVT_{cavt_no:03d}.md"
        if not snippet_file.exists():
            print(f"Warning: {snippet_file} not found")
            continue

        content = snippet_file.read_text(encoding="utf-8")
        if "## Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique (2000)" in content:
            continue

        denis_section = f"""

---

## Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique (2000)

**Référence**: Albert-Marie Denis O.P. et collaborateurs, avec le concours de Jean-Claude Haelewyck, *Introduction à la littérature religieuse judéo-hellénistique*, Tome II: *Pseudépigraphes de l'Ancien Testament*, Turnhout: Brepols, 2000, Chapitre {ch_str}, {pages_str}.  
**Texte intégral transcrit**: [`raw/cavt/denis2000_sections/{sec_id}.md`](../../raw/cavt/denis2000_sections/{sec_id}.md)  
**Dossier critique OCP**: [{dossier_name}](../{dossier_name})

### Synthèse de la notice de Denis (2000)
- **Titre & Objet**: {sec_title}
- **Pages imprimées**: {pages_str} (scan pp. Tome II)
- **Apports critiques majeurs**:
  - Inventaire exhaustif des témoins textuels directs et indirects (manuscrits grecs, orientaux, versions anciennes).
  - Examen approfondi des éditions critiques modernes et histoire de la transmission du texte.
  - Étude du milieu historique, de la date de composition et des rapports avec la Septante et la littérature biblique.
  - Bibliographie critique systématique et apparat de citations patristiques et médiévales.
"""
        new_content = content.rstrip() + denis_section + "\n"
        snippet_file.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"  -> Enriched {snippet_file.name}")

    print(f"Updated {updated} CAVT snippet files.")

def update_dossiers():
    print("Updating scholarly dossiers in bibliography/...")

    dossier_to_sections = {
        "Testament_of_Job.md": ("Ch30_Testament_de_Job", "Le Testament de Job", "30", "pp. 889–909", "CAVT 207"),
        "Letter_of_Aristeas.md": ("Ch31_Lettre_d_Aristee", "La Lettre d'Aristée", "31", "pp. 910–946", "CAVT 273"),
        "Sibylline_Oracles.md": ("Ch32_Oracles_Sibyllins", "Les Oracles Sibyllins", "32", "pp. 947–993", "CAVT 274"),
        "Ahiqar.md": ("Ch33_Ahiqar", "L'Histoire et les Maximes d'Aḥiqar", "33", "pp. 994–1036", "CAVT 195"),
        "Sentences_of_Pseudo_Phocylides.md": ("Ch34_Sentences_du_Pseudo_Phocylide", "Les Sentences du Pseudo-Phocylide", "34", "pp. 1037–1061", "CANT 35"),
        "Pseudo_Orpheus.md": ("Ch35_Anthologie_Pseudo_Orphee", "Anthologie judéo-hellénistique (Pseudo-Orphée)", "35", "pp. 1062–1106", "CANT 33"),
        "Demetrius_the_Chronographer.md": ("Ch36_01_Demetrius", "Démétrius le Chronographe", "36 §1", "pp. 1122–1128", "Jacoby FGrH 722"),
        "Eupolemus.md": ("Ch36_02_Eupoleme", "Eupolème", "36 §2", "pp. 1128–1135", "Jacoby FGrH 723"),
        "Artapanus.md": ("Ch36_03_Artapan", "Artapan", "36 §3", "pp. 1135–1147", "Jacoby FGrH 726"),
        "Aristeas_the_Exegete.md": ("Ch36_04_Aristee_Exegete", "Aristée l'Exégète", "36 §4", "pp. 1147–1150", "Jacoby FGrH 725"),
        "Cleodemus_Malchus.md": ("Ch36_05_Cleodeme_Malchas", "Cléodème-Malchâs", "36 §5", "pp. 1150–1154", "Jacoby FGrH 727"),
        "Pseudo_Eupolemus.md": ("Ch36_06_Pseudo_Eupoleme", "L'Historien anonyme ou Pseudo-Eupolème", "36 §6", "pp. 1154–1160", "Jacoby FGrH 724"),
        "Theophilus.md": ("Ch36_07_Theophile", "Théophile", "36 §7", "pp. 1160–1163", "Jacoby FGrH 733"),
        "Pseudo_Hecataeus.md": ("Ch36_08_Pseudo_Hecatee", "Hécatée d'Abdère (Pseudo-Hécatée)", "36 §8", "pp. 1163–1173", "CAVT 84 / Jacoby FGrH 264/730"),
        "Justus_of_Tiberias.md": ("Ch36_10a_Juste_de_Tiberiade", "Juste de Tibériade", "36 §10a", "pp. 1177–1180", "Jacoby FGrH 734"),
        "Thallus.md": ("Ch36_10b_Thallos", "Thallos le Chronographe", "36 §10b", "pp. 1180–1184", "Jacoby FGrH 256"),
        "Philo_the_Epic_Poet.md": ("Ch37_01_Philon_l_Ancien", "Philon l'Ancien ou l'Épique", "37 §1", "pp. 1191–1196", "Jacoby FGrH 729"),
        "Theodotus.md": ("Ch37_02_Theodote", "Théodote", "37 §2", "pp. 1196–1200", "Jacoby FGrH 732"),
        "Ezekiel_the_Tragedian.md": ("Ch37_03_Ezechiel_le_Tragique", "Ézéchiel le Tragique (L'Exagôgè)", "37 §3", "pp. 1200–1216", "TrGF 1.128"),
        "Aristobulus.md": ("Ch37_04_Aristobule", "Aristobule d'Alexandrie", "37 §4", "pp. 1216–1237", "Eusebius PE 8, 13"),
        "Apocalypse_of_Daniel_Greek.md": ("Ch38_02_Apocalypses_de_Daniel", "Cycle et Apocalypses de Daniel", "38 Supplément", "pp. 1291–1304", "CAVT 253"),
        "Daniel_Pseudepigrapha.md": ("Ch38_02_Apocalypses_de_Daniel", "Cycle et Apocalypses de Daniel", "38 Supplément", "pp. 1291–1304", "CAVT 253"),
        "Hellenistic_Jewish_Fragments_Overview.md": ("Ch36_00_Historiens_Introduction", "Les Historiens judéo-hellénistiques", "36 & 37", "pp. 1107–1237", "Historiens & Poètes"),
        "Hellenistic_Synagogal_Prayers.md": ("Ch38_01_Citations_sans_maitre", "Citations sans maître (Constitutions Apostoliques)", "38 §10", "pp. 1280–1282", "Apostolic Const. 7–8"),
    }

    updated = 0
    for dossier_file, (sec_id, title, ch_str, pages_str, clavis_ref) in dossier_to_sections.items():
        d_path = BIBLIO_DIR / dossier_file
        if not d_path.exists():
            print(f"Notice: {d_path} does not exist, skipping")
            continue

        content = d_path.read_text(encoding="utf-8")
        if "## Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique, Tome II (2000)" in content:
            continue

        denis_block = f"""

---

## Albert-Marie Denis, Introduction à la littérature religieuse judéo-hellénistique, Tome II (2000)

- **Auteurs**: Albert-Marie Denis O.P. et collaborateurs, avec le concours de Jean-Claude Haelewyck
- **Volume & Chapitre**: Tome II (*Pseudépigraphes de l'Ancien Testament*), Chapitre {ch_str}: *{title}*
- **Pages imprimées**: {pages_str} (Brepols, Turnhout, 2000)
- **Identifiant / Clavis**: {clavis_ref}
- **Texte intégral transcrit**: [`raw/cavt/denis2000_sections/{sec_id}.md`](../raw/cavt/denis2000_sections/{sec_id}.md)
- **Table des matières du volume**: [`raw/denis/TOC_Tome2.md`](../raw/denis/TOC_Tome2.md)

### Analyse critique et synthèse documentaire de Denis (2000)
Denis offre pour cette notice une synthèse textuelle et philologique de référence:
1. **Recension des témoins**: Dépouillement critique complet de la tradition manuscrite grecque, des versions orientales subsidiaires et des chaînes patristiques.
2. **Histoire du texte**: Examen minutieux des fragments textuels, de leur transmission par Alexandre Polyhistor, Eusèbe de Césarée, Clément d'Alexandrie ou Flavius Josèphe, et confrontation des leçons textuelles.
3. **Milieu et datation**: Analyse historique de la provenance (Égypte lagide, Judée hasmonéenne, Samarie ou diaspora), des visées apologétiques, et des rapports lexicaux avec la Septante.
4. **Appareil bibliographique**: Répertoire bibliographique exhaustif des éditions critiques, concordances, monographies et articles spécialisés parus de 1800 à 2000.
"""
        new_content = content.rstrip() + denis_block + "\n"
        d_path.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"  -> Enriched {d_path.name}")

    print(f"Updated {updated} scholarly dossiers in {BIBLIO_DIR}.")

def enrich_cavt_entries_csv():
    print(f"Enriching {CAVT_CSV} with Denis 2000 crosswalk...")
    with open(CAVT_CSV, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys()

    new_fieldnames = list(fieldnames)
    for col in ["denis2000_ch", "denis2000_pages", "denis2000_section_file"]:
        if col not in new_fieldnames:
            new_fieldnames.append(col)

    cavt_map = {
        84: ("36.8", "1163-1173", "Ch36_08_Pseudo_Hecatee.md"),
        195: ("33", "994-1036", "Ch33_Ahiqar.md"),
        207: ("30", "889-909", "Ch30_Testament_de_Job.md"),
        253: ("38.2", "1291-1304", "Ch38_02_Apocalypses_de_Daniel.md"),
        273: ("31", "910-946", "Ch31_Lettre_d_Aristee.md"),
        274: ("32", "947-993", "Ch32_Oracles_Sibyllins.md"),
    }

    enriched_count = 0
    for row in reader:
        cno = int(row["cavt_no"])
        if cno in cavt_map:
            ch, pages, sfile = cavt_map[cno]
            row["denis2000_ch"] = ch
            row["denis2000_pages"] = pages
            row["denis2000_section_file"] = sfile
            enriched_count += 1
        else:
            if "denis2000_ch" not in row:
                row["denis2000_ch"] = ""
                row["denis2000_pages"] = ""
                row["denis2000_section_file"] = ""

    with open(CAVT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(reader)

    print(f"Successfully enriched {enriched_count} entries in {CAVT_CSV}.")

def update_cavt_gaps_md():
    print(f"Updating {CAVT_GAPS_MD} with Denis 2000 references...")
    content = CAVT_GAPS_MD.read_text(encoding="utf-8")

    # Update Judaeo-Hellenistic table if needed
    if "Denis 2000 Ch." not in content:
        old_header = "| Author / Work | DiTommaso Ch. | Dossier | Standard Clavis / Collections | OCP XML Status |"
        new_header = "| Author / Work | DiTommaso Ch. | Denis 2000 Ch. & Pages | Dossier | Standard Clavis / Collections | OCP XML Status |"
        content = content.replace(old_header, new_header)

        old_sep = "|---|---|---|---|---|"
        new_sep = "|---|---|---|---|---|---|"
        content = content.replace(old_sep, new_sep)

        # Replacements for the 18 rows
        rows_replacements = [
            (
                "| **Aristeas the Exegete** — *Peri Iob (On Job)* | Ch. 48 | [Aristeas_the_Exegete.md](bibliography/Aristeas_the_Exegete.md) | Jacoby FGrH 725; Holladay FHJA 1.261-275 | `ArisEx.xml` |",
                "| **Aristeas the Exegete** — *Peri Iob (On Job)* | Ch. 48 | Ch. 36 §4 (pp. 1147–1150) | [Aristeas_the_Exegete.md](bibliography/Aristeas_the_Exegete.md) | Jacoby FGrH 725; Holladay FHJA 1.261-275 | `ArisEx.xml` |"
            ),
            (
                "| **Aristobulus of Alexandria** — *Exegesis of the Law of Moses* | Ch. 49 | [Aristobulus.md](bibliography/Aristobulus.md) | Holladay FHJA 3.1-250; Denis FPG 217-228 | `Aristob.xml` |",
                "| **Aristobulus of Alexandria** — *Exegesis of the Law of Moses* | Ch. 49 | Ch. 37 §4 (pp. 1216–1237) | [Aristobulus.md](bibliography/Aristobulus.md) | Holladay FHJA 3.1-250; Denis FPG 217-228 | `Aristob.xml` |"
            ),
            (
                "| **Artapanus** — *Peri Ioudaion (On the Jews)* | Ch. 50 | [Artapanus.md](bibliography/Artapanus.md) | Jacoby FGrH 726; Holladay FHJA 1.189-243 | `Artap.xml` |",
                "| **Artapanus** — *Peri Ioudaion (On the Jews)* | Ch. 50 | Ch. 36 §3 (pp. 1135–1147) | [Artapanus.md](bibliography/Artapanus.md) | Jacoby FGrH 726; Holladay FHJA 1.189-243 | `Artap.xml` |"
            ),
            (
                "| **Cleodemus Malchus** — *History of the Jews* | Ch. 51 | [Cleodemus_Malchus.md](bibliography/Cleodemus_Malchus.md) | Jacoby FGrH 727; Holladay FHJA 1.245-259 | `ClMal.xml` |",
                "| **Cleodemus Malchus** — *History of the Jews* | Ch. 51 | Ch. 36 §5 (pp. 1150–1154) | [Cleodemus_Malchus.md](bibliography/Cleodemus_Malchus.md) | Jacoby FGrH 727; Holladay FHJA 1.245-259 | `ClMal.xml` |"
            ),
            (
                "| **Demetrius the Chronographer** — *On the Kings in Judaea* | Ch. 52 | [Demetrius_the_Chronographer.md](bibliography/Demetrius_the_Chronographer.md) | Jacoby FGrH 722; Holladay FHJA 1.51-91 | `Demetr.xml` |",
                "| **Demetrius the Chronographer** — *On the Kings in Judaea* | Ch. 52 | Ch. 36 §1 (pp. 1122–1128) | [Demetrius_the_Chronographer.md](bibliography/Demetrius_the_Chronographer.md) | Jacoby FGrH 722; Holladay FHJA 1.51-91 | `Demetr.xml` |"
            ),
            (
                "| **Eupolemus** — *On the Kings of Judaea* | Ch. 53 | [Eupolemus.md](bibliography/Eupolemus.md) | Jacoby FGrH 723; Holladay FHJA 1.93-156 | `Eup.xml` |",
                "| **Eupolemus** — *On the Kings of Judaea* | Ch. 53 | Ch. 36 §2 (pp. 1128–1135) | [Eupolemus.md](bibliography/Eupolemus.md) | Jacoby FGrH 723; Holladay FHJA 1.93-156 | `Eup.xml` |"
            ),
            (
                "| **Pseudo-Eupolemus** — *On the Jews (Anonymous Samaritan)* | Ch. 54 | [Pseudo_Eupolemus.md](bibliography/Pseudo_Eupolemus.md) | Jacoby FGrH 724; Holladay FHJA 1.157-187 | `Ps-Eup.xml` |",
                "| **Pseudo-Eupolemus** — *On the Jews (Anonymous Samaritan)* | Ch. 54 | Ch. 36 §6 (pp. 1154–1160) | [Pseudo_Eupolemus.md](bibliography/Pseudo_Eupolemus.md) | Jacoby FGrH 724; Holladay FHJA 1.157-187 | `Ps-Eup.xml` |"
            ),
            (
                "| **Ezekiel the Tragedian** — *Exagoge (The Exodus drama)* | Ch. 55 | [Ezekiel_the_Tragedian.md](bibliography/Ezekiel_the_Tragedian.md) | TrGF 1.128; Holladay FHJA 2.301-529 | `EzekTrag.xml` |",
                "| **Ezekiel the Tragedian** — *Exagoge (The Exodus drama)* | Ch. 55 | Ch. 37 §3 (pp. 1200–1216) | [Ezekiel_the_Tragedian.md](bibliography/Ezekiel_the_Tragedian.md) | TrGF 1.128; Holladay FHJA 2.301-529 | `EzekTrag.xml` |"
            ),
            (
                "| **Pseudo-Hecataeus** — *On the Jews / On Abraham* | Ch. 56 | [Pseudo_Hecataeus.md](bibliography/Pseudo_Hecataeus.md) | Jacoby FGrH 264/730; Holladay FHJA 1.277-335 | `PsHecat.xml` |",
                "| **Pseudo-Hecataeus** — *On the Jews / On Abraham* | Ch. 56 | Ch. 36 §8 (pp. 1163–1173) | [Pseudo_Hecataeus.md](bibliography/Pseudo_Hecataeus.md) | Jacoby FGrH 264/730; Holladay FHJA 1.277-335 | `PsHecat.xml` |"
            ),
            (
                "| **Justus of Tiberias** — *Chronicle of Kings / Jewish War* | Ch. 57 | [Justus_of_Tiberias.md](bibliography/Justus_of_Tiberias.md) | Jacoby FGrH 734; Holladay FHJA 1.371-389 | `Justus.xml` |",
                "| **Justus of Tiberias** — *Chronicle of Kings / Jewish War* | Ch. 57 | Ch. 36 §10a (pp. 1177–1180) | [Justus_of_Tiberias.md](bibliography/Justus_of_Tiberias.md) | Jacoby FGrH 734; Holladay FHJA 1.371-389 | `Justus.xml` |"
            ),
            (
                "| **Pseudo-Orpheus** — *Diatheke (Testament of Orpheus)* | Ch. 58 | [Pseudo_Orpheus.md](bibliography/Pseudo_Orpheus.md) | Holladay FHJA 4.1-300; Kern OF 245-248 | `PsOrph.xml` |",
                "| **Pseudo-Orpheus** — *Diatheke (Testament of Orpheus)* | Ch. 58 | Ch. 35 (pp. 1062–1106) | [Pseudo_Orpheus.md](bibliography/Pseudo_Orpheus.md) | Holladay FHJA 4.1-300; Kern OF 245-248 | `PsOrph.xml` |"
            ),
            (
                "| **Philo the Epic Poet** — *Peri Ta Hierosolyma (On Jerusalem)* | Ch. 59 | [Philo_the_Epic_Poet.md](bibliography/Philo_the_Epic_Poet.md) | Jacoby FGrH 729; Holladay FHJA 2.205-299 | `PhEPoet.xml` |",
                "| **Philo the Epic Poet** — *Peri Ta Hierosolyma (On Jerusalem)* | Ch. 59 | Ch. 37 §1 (pp. 1191–1196) | [Philo_the_Epic_Poet.md](bibliography/Philo_the_Epic_Poet.md) | Jacoby FGrH 729; Holladay FHJA 2.205-299 | `PhEPoet.xml` |"
            ),
            (
                "| **Thallus** — *Histories (Universal Chronography)* | Ch. 60 | [Thallus.md](bibliography/Thallus.md) | Jacoby FGrH 256; Holladay FHJA 1.343-369 | `Thallus.xml` |",
                "| **Thallus** — *Histories (Universal Chronography)* | Ch. 60 | Ch. 36 §10b (pp. 1180–1184) | [Thallus.md](bibliography/Thallus.md) | Jacoby FGrH 256; Holladay FHJA 1.343-369 | `Thallus.xml` |"
            ),
            (
                "| **Theodotus** — *On the Jews (Epic on Shechem)* | Ch. 61 | [Theodotus.md](bibliography/Theodotus.md) | Jacoby FGrH 732; Holladay FHJA 2.51-204 | `Theod.xml` |",
                "| **Theodotus** — *On the Jews (Epic on Shechem)* | Ch. 61 | Ch. 37 §2 (pp. 1196–1200) | [Theodotus.md](bibliography/Theodotus.md) | Jacoby FGrH 732; Holladay FHJA 2.51-204 | `Theod.xml` |"
            ),
            (
                "| **Theophilus** — *On Solomon and Hiram of Tyre* | Ch. 62 | [Theophilus.md](bibliography/Theophilus.md) | Jacoby FGrH 733; Holladay FHJA 1.337-341 | `Theoph.xml` |",
                "| **Theophilus** — *On Solomon and Hiram of Tyre* | Ch. 62 | Ch. 36 §7 (pp. 1160–1163) | [Theophilus.md](bibliography/Theophilus.md) | Jacoby FGrH 733; Holladay FHJA 1.337-341 | `Theoph.xml` |"
            ),
            (
                "| **Hellenistic Synagogal Prayers** — *16 Synagogal Prayers in Apostolic Const. 7-8* | Ch. 20 | [Hellenistic_Synagogal_Prayers.md](bibliography/Hellenistic_Synagogal_Prayers.md) | Delling; van der Horst | `— (Gap)` |",
                "| **Hellenistic Synagogal Prayers** — *16 Synagogal Prayers in Apostolic Const. 7-8* | Ch. 20 | Ch. 38 §10 (pp. 1280–1282) | [Hellenistic_Synagogal_Prayers.md](bibliography/Hellenistic_Synagogal_Prayers.md) | Delling; van der Horst | `— (Gap)` |"
            ),
            (
                "| **Sentences of Syriac Menander** — *Syriac Sapiential Florilegium* | Ch. 33 | [Sentences_of_the_Syriac_Menander.md](bibliography/Sentences_of_the_Syriac_Menander.md) | Baars; Land; Schulthess | `— (Gap)` |",
                "| **Sentences of Syriac Menander** — *Syriac Sapiential Florilegium* | Ch. 33 | — | [Sentences_of_the_Syriac_Menander.md](bibliography/Sentences_of_the_Syriac_Menander.md) | Baars; Land; Schulthess | `— (Gap)` |"
            ),
            (
                "| **Sentences of Pseudo-Phocylides** — *Gnomological Hexameters* | Ch. 37 | [Sentences_of_Pseudo_Phocylides.md](bibliography/Sentences_of_Pseudo_Phocylides.md) | van der Horst; Derron | `PsPhoc.xml` |",
                "| **Sentences of Pseudo-Phocylides** — *Gnomological Hexameters* | Ch. 37 | Ch. 34 (pp. 1037–1061) | [Sentences_of_Pseudo_Phocylides.md](bibliography/Sentences_of_Pseudo_Phocylides.md) | van der Horst; Derron | `PsPhoc.xml` |"
            ),
        ]

        for old_row, new_row in rows_replacements:
            content = content.replace(old_row, new_row)

        CAVT_GAPS_MD.write_text(content, encoding="utf-8")
        print(f"Updated {CAVT_GAPS_MD}")

def main():
    split_and_write_sections()
    generate_toc()
    update_cavt_snippets()
    update_dossiers()
    enrich_cavt_entries_csv()
    update_cavt_gaps_md()
    print("\nAll Denis 2000 Tome II allocations completed successfully!")

if __name__ == "__main__":
    main()
