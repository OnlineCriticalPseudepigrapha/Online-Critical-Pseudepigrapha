# Online Critical Pseudepigrapha (OCP)

[![Website](https://img.shields.io/badge/Website-pseudepigrapha.org-gold.svg)](https://pseudepigrapha.org)
[![License: GPL v3](https://img.shields.io/badge/Software-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![License: CC BY 4.0](https://img.shields.io/badge/Texts-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Open Access](https://img.shields.io/badge/Open%20Access-TEI%20XML-green.svg)](https://github.com/OnlineCriticalPseudepigrapha/Online-Critical-Pseudepigrapha/tree/master/static/docs)

The mandate of the **Online Critical Pseudepigrapha (OCP)** is to develop and publish electronic editions of the best critical texts of the "Old Testament" Pseudepigrapha and related literature, complete with textual variants and manuscript witnesses.

---

## 📢 Project Status & Infrastructure Transition (2026)

The original dynamic Web2py application server has been decommissioned. In its place:
1. **Direct Web Access:** A static landing page and interactive text catalog are published directly via GitHub Pages at **[pseudepigrapha.org](https://pseudepigrapha.org)**.
2. **Text Preservation:** All 39 critical edition XML files are preserved and open-access in the [`static/docs/`](file:///home/kmpenner/projects/Research/Online-Critical-Pseudepigrapha/static/docs) directory.
3. **Future Roadmap:** OCP is actively transitioning toward serving textual data through a modern **Distributed Text Services (DTS)** compliant API integrated into [Knowledge Commons Works](https://works.hcommons.org) (InvenioRDM).

---

## 📚 Critical Texts Catalog

The repository includes eclectic critical texts and multi-witness TEI XML editions across Greek, Syriac, Latin, Ethiopic, and Aramaic:

| File | Title | Language | Witnesses / Details |
| :--- | :--- | :--- | :--- |
| [`1En.xml`](static/docs/1En.xml) | 1 Enoch | Ethiopic | Ethiopic, Greek, Latin, Aramaic witnesses |
| [`2Bar.xml`](static/docs/2Bar.xml) | 2 Baruch (Syriac Apocalypse) | Syriac | Syriac, Greek, Latin witnesses |
| [`2Bar-Syr.xml`](static/docs/2Bar-Syr.xml) | 2 Baruch (Syriac Text) | Syriac | Syriac base text |
| [`3Bar.xml`](static/docs/3Bar.xml) | 3 Baruch (Greek Apocalypse) | Greek | Greek manuscripts |
| [`4Bar.xml`](static/docs/4Bar.xml) | 4 Baruch (*Paraleipomena Ieremiou*) | Greek | Greek text |
| [`4Ezra.xml`](static/docs/4Ezra.xml) | 4 Ezra (Syriac) | Syriac | Syriac text & Latin witnesses |
| [`4Macc.xml`](static/docs/4Macc.xml) | 4 Maccabees | Greek | Greek text |
| [`4Q548.xml`](static/docs/4Q548.xml) | 4Q548 | Aramaic | Dead Sea Scrolls fragment |
| [`AdamEve.xml`](static/docs/AdamEve.xml) | Life of Adam and Eve (*Apocalypse of Moses*) | Greek | Greek & Latin witnesses |
| [`Amram.xml`](static/docs/Amram.xml) | Visions of Amram | Aramaic | 4Q543–547 Qumran fragments |
| [`ApocrEzek.xml`](static/docs/ApocrEzek.xml) | Apocryphon of Ezekiel | Greek | Epiphanius (*Panarion*) fragments |
| [`ArisEx.xml`](static/docs/ArisEx.xml) | Aristeas the Exegete | Greek | Eusebius (*Praep. Evang.*) |
| [`Aristob.xml`](static/docs/Aristob.xml) | Aristobulus | Greek | Eusebius & Clement fragments |
| [`Artap.xml`](static/docs/Artap.xml) | Artapanus | Greek | Eusebius (*Praep. Evang.*) |
| [`ClMal.xml`](static/docs/ClMal.xml) | Cleodemus Malchus | Greek | Josephus (*Ant.*) |
| [`ElMod.xml`](static/docs/ElMod.xml) | Eldad and Modad | Greek | *Shepherd of Hermas* citation |
| [`Esdl.xml`](static/docs/Esdl.xml) | Vision of Ezra (*Visio Beati Esdrae*) | Latin | Latin manuscript tradition |
| [`Esdr.xml`](static/docs/Esdr.xml) | 4 Ezra (Latin) | Latin | Latin manuscript tradition |
| [`Eup.xml`](static/docs/Eup.xml) | Eupolemus | Greek | Clement of Alexandria & Eusebius |
| [`EzekTrag.xml`](static/docs/EzekTrag.xml) | Ezekiel the Tragedian (*Exagoge*) | Greek | Drama fragments via Eusebius |
| [`HistRech.xml`](static/docs/HistRech.xml) | History of the Rechabites | Greek | Story of Zosimus |
| [`JosAsen.xml`](static/docs/JosAsen.xml) | Joseph and Aseneth | Greek | Greek text |
| [`Jub.xml`](static/docs/Jub.xml) | Jubilees (Greek & Latin Fragments) | Greek | Greek / Latin citations & fragments |
| [`Jubi.xml`](static/docs/Jubi.xml) | Jubilees (Latin Version) | Latin | Latin version |
| [`LetAris.xml`](static/docs/LetAris.xml) | Letter of Aristeas to Philocrates | Greek | Greek text |
| [`LivPro.xml`](static/docs/LivPro.xml) | Lives of the Prophets | Greek | Greek biographical tradition |
| [`Mois.xml`](static/docs/Mois.xml) | Assumption of Moses (*Testament of Moses*) | Latin | Latin text |
| [`PhEPoet.xml`](static/docs/PhEPoet.xml) | Philo the Epic Poet | Greek | Hexameter epic fragments |
| [`Ps-Eup.xml`](static/docs/Ps-Eup.xml) | Pseudo-Eupolemus | Greek | Hellenistic Jewish fragments |
| [`PssSol.xml`](static/docs/PssSol.xml) | Psalms of Solomon | Greek | 13 Greek witnesses |
| [`SibOr.xml`](static/docs/SibOr.xml) | Sibylline Oracles | Greek | Greek poetic oracles |
| [`TAbA.xml`](static/docs/TAbA.xml) | Testament of Abraham (Recension A) | Greek | Greek text |
| [`TAbB.xml`](static/docs/TAbB.xml) | Testament of Abraham (Recension B) | Greek | Greek text |
| [`TAbr.xml`](static/docs/TAbr.xml) | Testament of Abraham | Greek | Greek text |
| [`TAdam.xml`](static/docs/TAdam.xml) | Testament of Adam | Syriac | Syriac and Greek witnesses |
| [`TJob.xml`](static/docs/TJob.xml) | Testament of Job | Greek | Greek, Coptic, and Slavonic witnesses |
| [`TSol.xml`](static/docs/TSol.xml) | Testament of Solomon | Greek | Greek magical/testamentary tradition |
| [`Theod.xml`](static/docs/Theod.xml) | Theodotus | Greek | Epic poetic fragments on Shechem |

---

## 👥 Editorial Team & Governance

### General Editors
- **Ian W. Scott, PhD** (Co-founder) — Lead Repository Architect, Knowledge Commons Works / Michigan State University
- **Ken M. Penner, PhD** (Co-founder & General Editor) — Professor of Religious Studies, St. Francis Xavier University
- **David M. Miller, PhD** (Co-founder, 2006–2007) — Briercrest College and Seminary

### Scholarly Review Board
- **Judith H. Newman, PhD** — Emmanuel College / University of Toronto
- **James H. Charlesworth, PhD** — Princeton Theological Seminary
- **Robert A. Kraft, PhD †** — University of Pennsylvania
- **Craig A. Evans, PhD** — Houston Christian University

---

## 📖 Citation Format

To cite the OCP editions in academic publications:

> Ian W. Scott and Ken M. Penner, eds. *The Online Critical Pseudepigrapha*. Atlanta: Society of Biblical Literature / Online: pseudepigrapha.org.

When citing specific editions, please include the individual editor named in the document's header metadata along with the OCP project reference.

---

## ⚖️ License

This repository carries two licenses, matching the two kinds of material it holds:

- **Software and reader interface** (the Grammateus3 application, web2py controllers/views, JavaScript, CSS, build scripts) — [GNU General Public License v3.0](LICENSE.GPL) (© Ian W. Scott 2012–2013).
- **Text editions and TEI XML files** in [`static/docs/`](static/docs) — [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE.CC-BY-4.0). You are free to share and adapt these editions, including producing translations and parallel displays, with attribution to the Online Critical Pseudepigrapha and the individual editor named in each document's header metadata.

This dual structure follows the FSF's recommendation against applying software copyleft to non-software works, and brings the repository in line with other open scholarly editions such as the OSHB and SBLGNT (CC BY). The clarification was prompted by issue #34.
