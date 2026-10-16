# NEXT — Online-Critical-Pseudepigrapha

Outlook: Inbox/Research/OCP

## Current State (2026-09-04)
- Branch: `master` (PR #35 merged into `master`).
- Live deploy via GitHub Pages: parallel English and French translations published across 100% of active XML editions (38 of 38 documents).
- Reader enhancements: poetic linebreaks (`following`, `doubleFollowing`, `both`) and `.is-indented` verse indentation rendered in client-side reader.
- Dual licensing configured: GNU GPL v3 for software/code, Creative Commons Attribution 4.0 (CC BY 4.0) for critical text editions.
- Closed resolved/obsolete issues: #6, #12, #13, #17, #26, #27, #28, #32.

## What should be done next
- Review remaining open issues:
  - TAdam (#3): Proofreading English introduction.
  - PssSol (#9, #11, #15, #16): Introduction, Greek variants, English markup, and text divisions.
  - LAB (#4, #5, #14): Latin text and introduction.
  - TLevi (#20, #21, #22, #23): Text, variants, and introduction.
  - Amram (#31) / 2Bar (#30) / 4Q548 (#29) / TEI schema (#25): 2018 TEI markup tickets deferred to DTS API roadmap.
- Continue monitoring Dependabot and sitemap crawl status.

## Email history
See `GMAIL-INDEX.md` in this folder.

- 2026-10-05: moved here from the top of `Research/`: `ascenisa corrections.txt.docx` (Ascension of Isaiah Greek corrections by verse; the Greek is mojibake, UTF-8 read as Windows-1252, and needs re-decoding before use).

- 2026-10-05 (Outlook + Sent): site restored Aug 26; Ken fixed the intros (Aug 26) and the per-text citations (Aug 27); Ian approved Ken's GitHub-issue reply Sep 1. Nothing outstanding in email. NEXT: none pending; confirm the GitHub issue is closed.

- 2026-10-15: Samaritan Pentateuch parallel corpus scraped from samaritan-torah.onrender.com into gitignored `raw/corpora/samaritan_torah/` (5,846 verses: SP, MT, Samaritan Targum, Onkelos, Qumran, LXX, EN, AR, Hebrew commentary; 187 chapter files + JSONL + tidy `verses.csv`). Copyright Osher Sassoni — research use only, no republication. Verification record: `raw/corpora/samaritan_torah/VERIFICATION.md`.
- 2026-10-15 (later): secondary Samaritan corpora scraped into gitignored `raw/corpora/samaritan_secondary/` — Tibåt Mårqe (6 books/410 sections), Asatir (16/175), Ṣadaqah al-Ḥakīm on Genesis (50/446), Responsa of Jacob ben Aaron (25), Sīr al-Qulūb (26), ʾIm Beḥuqotay commentary (25/537) = 148 unit files, 1,619 sections + per-corpus JSONL. `verse_id` joins 100% to the main corpus's verse ids (Genesis-anchored). Scraper: `scripts/scrape_samaritan_secondary.py`; verification: `raw/corpora/samaritan_secondary/VERIFICATION.md`. Same copyright regime. Remaining unscraped shelf items: cohen (16), wreschner (9), piyutim (1,126), dara, people.

- 2026-10-15: CAVT gap analysis first pass done (`CAVT_GAPS.md`, plan in `CAVT_PLAN.md`; data in gitignored `raw/cavt/`). WAITING: Denis, *Introduction à la littérature religieuse judéo-hellénistique* (2000) TOC — requested by ILL. When it arrives: OCR the TOC into `raw/denis/` and add the Denis crosswalk, especially for the 9 Judaeo-Hellenistic texts CAVT excludes.

- 2026-10-16: Lorenzo DiTommaso, *A Bibliography of Pseudepigrapha Research, 1850–1999* (2001) fully extracted and integrated:
  - Compiled all 62 chapters into dedicated bibliographic dossiers in `bibliography/` (gitignored).
  - Enriched master CSV `raw/cavt/cavt_entries.csv` with `ditommaso_ch`, `ditommaso_dossier`, and `ditommaso_title` across all 277 CAVT entries (113 CAVT entries directly linked).
  - Regenerated `CAVT_GAPS.md`: all active OCP editions mapped to CAVT/DiTommaso; added dedicated crosswalk table for 18 Judaeo-Hellenistic and sapiential works outside CAVT; mapped and ranked 226 CAVT gap entries across Tier A (105), Tier B (69), and Tier C (52).
  - Resolved text ambiguities: `TSol.xml` = CAVT 162 (*Testamentum Salomonis*); `Esdl.xml` = CAVT 184.iii (*Visio beati Esdrae*, Barberini lat. 2318; ed. Bogaert 1984 / Denis 1993).
  - Ingested Tier A Greek Apocalypses of the Ezra-Sedrach visionary complex:
    - `static/docs/ApEzra.xml` & `static/docs/tei/ApEzra.xml`: *Greek Apocalypse of Ezra* (CAVT 184.i / CANT 343; Tischendorf 1866; 7 chapters, 220 verses).
    - `static/docs/Sedrach.xml` & `static/docs/tei/Sedrach.xml`: *Apocalypse of Sedrach* (CAVT 184.ii / CANT 344; James 1893; 16 chapters, 133 verses).
    - Updated `static/js/reader.js` and `CAVT_GAPS.md` with active editions.

