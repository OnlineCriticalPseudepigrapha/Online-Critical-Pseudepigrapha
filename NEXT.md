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
  - Completed comprehensive ingestion of Tier A gaps and Judaeo-Hellenistic texts (11 new works, 22 XML/TEI files):
    1. *Prayer of Manasseh* (`OrMan.xml` & `tei/OrMan.xml`, CAVT 178 / CANT 203; parallel Greek LXX Ode 12 / Swete 1896 and Clementine Vulgate, 15 vv.).
    2. *Vision of Elijah* (`VisEl.xml` & `tei/VisEl.xml`, CAVT 169; Latin text, De Bruyne 1925 / MS Mazarine 512, 11 vv.).
    3. *Narratio de Moyse et Josue* (`NarrMois.xml` & `tei/NarrMois.xml`, CAVT 137 / BHG 2277; Greek text, Vassiliev 1893 / BnF gr. 1611, 154 vv.).
    4. *De Adami compositione et nomine* (`DeAdam.xml` & `tei/DeAdam.xml`, CAVT 10; Latin text, Förster 1908, 2 chs, 15 vv.).
    5. *Sentences of Pseudo-Phocylides* (`PsPhoc.xml` & `tei/PsPhoc.xml`, CAVT 182 / CANT 35; Greek hexameter text, Bergk 1882, 230 vv.).
    6. *Treatise of Shem* (*Tractatus Sem*, `TracSem.xml` & `tei/TracSem.xml`, CAVT 85; parallel Syriac and English, Mingana 1917 / MS Rylands Syr. 44, 12 chs, 121 vv.).
    7. *Andronicus and Asaph on the Zodiac of the Patriarchs* (`AndronAsaph.xml` & `tei/AndronAsaph.xml`; parallel Syriac and English, Mingana 1917, 17 vv.).
    8. *Testament of Orpheus* (*Hieroi Logoi* / *Diathekai*, `PsOrph.xml` & `tei/PsOrph.xml`, CAVT 183 / CANT 33; Greek text & English, Kern 1922 / Denis 1970; Aristobulus, Pseudo-Justin, and Orphic Hymn, 3 chs, 72 vv.).
    9. *Fragments of Pseudo-Hecataeus* (`PsHecat.xml` & `tei/PsHecat.xml`, CAVT 84 / CANT 28; Greek text & English, Josephus *Contra Apionem* I.183-205, II.43; *Ant.* I.159, XII.38; Jacoby FGrH 264 F 21-24; 5 chs, 24 vv.).
    10. *Fragments of Thallus the Chronographer* (`Thallus.xml` & `tei/Thallus.xml`; Greek & English, Julius Africanus, Theophilus, Josephus; Jacoby FGrH 256; 3 chs, 5 vv.).
    11. *Fragments of Theophilus* (`Theoph.xml` & `tei/Theoph.xml`; Greek & English, Alexander Polyhistor ap. Eusebius Praep. Ev. IX.34.19; Jacoby FGrH 733; 1 ch, 1 v.).
  - Updated `static/js/reader.js` (`OCP_DOCUMENTS`) with all 56 active documents.
  - Enriched `static/docs/intros.json` with 49 critical introductions, bibliography, and manuscript details.
  - Synchronized `scripts/cavt_gaps.py` and regenerated `CAVT_GAPS.md`.

- 2026-10-16: Empirically confirmed archive.org loan `media_url` now requires session + active loan and 302-redirects to Adobe Content Server `.acsm` fulfillment (no more direct PDFs). Kisch L.A.B. (CAVT 131) tested: all three archive.org copies refuse borrow (item-level suspension). zlib-download skill updated with endpoint findings.
- 2026-10-17 (LCP decryption dry run) — the borrow now succeeds on `pseudophiloslibe0000guid_l9x6` for a regular account (1-hour auto-renew in-library borrow; Borrow → "Return now"); the 16.5 MB `.lcpdf` downloads but NO `license.lcpl` is issued for that loan type (`/download/<id>/<id>.lcpl` 404s, download menu empty) → the encrypted PDF is undecryptable; the 14-day LCP fulfillment that produces the `.lcpl` exists only for lendable-pool items (like that day's *Juliet's story* loan, which decrypted end-to-end) or print-disability accounts. Runner staged at `~/.hermes/cache/scratch/kisch_lcpdf_decrypt.py`. Details in MISSING_EDITIONS.md.
- 2026-10-18: Full IA OCR text layer of Kisch 1949 captured via loaned-session `BookReaderGetTextWrapper` loop (whole-file `_djvu.txt` stays 403 even in-session — only BookReader wrappers are gated open): `raw/editions/Pseudo-Philo_LAB_Kisch1949_djvu.txt`, 314 pages with PAGE markers (~568 KB, IA's own scan OCR, no images). Front matter mapped: title p.9, copyright p.10, preface pp.11-12, ToC p.13, illustrations p.14, Part One Intro from p.15, Latin text pp.108-272 per ToC. Serves OCP issues #4/#5/#14 (L.A.B. Latin text + intro). Loan from Oct 17 still open — return or let the 1-hour loan expire next time the browser tab is live.
- 2026-10-18 (LAB work started): `LAB_PLAN.md` added — source inventory, Kisch edition structure mapped (Latin text = scan leaves 141-302, chapters I-LXV), chapter→page map (58/65 headings auto-detected; 25/33/38/43/52/53/64 lost to OCR), measured OCR quality (0.43% garbled tokens, 44,941 tokens) and the critical caveat that **Kisch's apparatus criticus runs interleaved at page feet** and must be split from the text before markup. Working extracts (gitignored): `scratch/lab/kisch_latin_text_raw.txt`, `scratch/lab/LAB_CHAPTER_MAP.json`. Work plan for #4/#5/#14 inside LAB_PLAN.md.
- 2026-10-18 (Tier B/C sweep): `PD_CANDIDATES_B_C.md` added. Naive CAVT-title search over all 118 Tier B/C works = low precision (rejected method, recorded); curated search under the classic editors found 9 usable PD candidates on IA (Bezold 1883 + Budge 1927 Cave of Treasures; Morfill/Charles 1896 Slavonic Enoch; Harris 1911 Odes of Solomon; Conybeare 1913 Ahiqar; Issaverdens 1901 Armenian uncanonical writings; Fabricius 1713 Codex pseudepigraphus; Steindorff 1899 Apocalypse of Elias). Not on IA: Norberg's Codex Nasaraeus, pseudo-Methodius editions, Coptic Jeremiah, Ethiopic Mors Moysi. Next: source editions from the DiTommaso dossiers before searching, and renewal-check Budge 1927.

## Intro drafts: verified against OTP (2026-10-20)
All drafts were checked against the OTP 1–2 introductions in Logos. Corrected: TJob (Sitis), 1En (3rd–2nd c. BCE), TSol (early 3rd c. CE), AdamEve (Johnson's Jewish view), ArisEx (no date beyond pre-Polyhistor), ElMod (pre-Hermas, Jewish or Christian), Ps-Eup (Doran's objection), Theod (late 3rd/2nd c. BCE), 5Ezra ("Christian prologue"). Theoph, 5Ezra and 6Ezra have no OTP entry and were checked only against general knowledge. The JosAsen status note that the "Evans" base text is undocumented still stands. Ready to merge intros-draft into master on approval.

## Jubilees Qumran Hebrew (2026-10-21)
All 15 Qumran Hebrew scrolls (4Q216–224, 4Q176a, 1Q17–18, 2Q19–20, 3Q5, 11Q12) imported into Jub.xml as version "Qumran Hebrew" (Abegg/ETCBC dss, used by permission). Verse alignments matched to VanderKam & Milik (DJD 13) and García Martínez & Tigchelaar (DSSSE). TEI P5 synchronized (static/docs/tei/Jub.xml), catalog updated in reader.js and index.html (17 manuscripts total), and intros.json updated to Edition 2.0. Ready and merged to master.
- 2026-10-22: All 13 overlapping Hebrew verses (21:7, 21:8, 21:9, 21:10, 21:22, 21:23, 21:24, 23:13, 35:9, 38:6, 38:7, 38:8, 39:9) collated into granular word- and phrase-level critical apparatus units in static/docs/Jub.xml and static/docs/tei/Jub.xml, enabling interactive multi-witness apparatus display and witness-specific text switching in the Grammateus reader.
- 2026-10-22: Ken scanned Denis 1970, *Introduction aux pseudépigraphes grecs d'Ancien Testament* (SVTP 1; library loan) on the NT 5th copier: `raw/editions/Denis1970_Introduction_pseudepigraphes_grecs_SVTP1.pdf` (186 pp, image-only, no OCR), parts in `raw/editions/Denis1970_Introduction_scans/`. Emails filed to Inbox/Research/OCP.
- 2026-10-22: Evaluated book scan OCR strategies (Docling vs Tesseract vs VLM). Docling's default RapidOCR drops Greek completely; Tesseract -l fra+grc suffers from cross-alphabet contamination. Implemented two complementary repo tools:
  - `scripts/split_and_ocr_book.py`: Bisects facing photocopier spreads down the gutter into upright portrait pages and generates searchable PDF/A layers via multi-core ocrmypdf. Successfully processed all 186 spreads (372 pages) of Denis 1970 into `raw/editions/Denis1970_Introduction_pseudepigraphes_grecs_SVTP1_searchable.pdf` in 3.6 minutes.
  - `scripts/vlm_transcribe.py`: Queries OpenCode Go's free `minimax-m3.1-flash` vision model with custom prompts, flawlessly transcribing polytonic Greek, Latin, French, and apparatus without alphabet pollution.
