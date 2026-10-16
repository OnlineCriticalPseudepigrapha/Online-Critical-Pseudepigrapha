# Plan: CAVT-based expansion of OCP (run on desktop)

Goal: use Haelewyck, *Clavis Apocryphorum Veteris Testamenti* (Brepols, 1998; CAVT) as the master
checklist for a comprehensive OCP, and produce a ranked list of texts OCP does not yet offer.

## Source scan (do NOT commit — Brepols copyright, and this repo is public)
- Zotero: items 2AV8XAID (Early Judaism group) / UB67BHHV (Pseudepigrapha group); same PDF.
  Laptop path: `~/Zotero/storage/CPKGV4ZG/J.-C Haelewyck - 1998 - Clavis apocryphorum veteris testamenti.pdf`
  (270 pp., 8.2 MB, image-only — no text layer).
  **Copy for the desktop: `raw/cavt/Haelewyck_1998_CAVT.pdf`** (Syncthing carries it; gitignored).
- Fallback: OneDrive `Documents/Haelewyck - 0001.png` … `0270.png` (270 page images, presumably the same book; not yet verified).
- Keep all OCR output under `raw/cavt/` (gitignored).

## What the book looks like (checked pp. 60, 150)
- Entry = heading `Title (language)` in bold, e.g. *Visio Eliae (latine)*, *Historia Eliae prophetae (arabice)*;
  then `Cf.:` refs, `Cod./Codd.:` manuscripts, editions, `Translatio anglica/germanica/...:`, `Concordantia:`;
  `Inedita.` marks unedited texts. Running head = biblical section (e.g. `I-II SAMUEL - I-II REGES`);
  CAVT entry numbers in the outer margin (e.g. 33, 123); printed page numbers in the other corner.
- Script: Latin script throughout (Latin headings; FR/DE/EN/IT bibliography; transliteration diacritics
  like *Abū Maqār*; small caps for author surnames). Non-Latin titles are transliterated; expect only
  stray Greek. So: OCR languages `lat+fra+deu+ita+eng`, add `grc` only if Greek turns up.

## Steps
1. **Install** (desktop):
   ```bash
   sudo apt install tesseract-ocr-lat tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-ita tesseract-ocr-grc
   pip install docling
   ```
2. **Pilot on 5 pages** (e.g. 20, 60, 150, 200, 250) with Docling using the Tesseract backend
   (`TesseractCliOcrOptions(lang=["lat","fra","deu","ita","eng"], force_full_page_ocr=True)`),
   export Markdown. Check: headings detected as headings? diacritics kept? margin entry numbers
   captured and not merged into body text? If Docling mangles layout, fall back to plain
   `tesseract page.png out -l lat+fra+deu+ita+eng --psm 4` (300 dpi via `pdftoppm -r 300`).
3. **Full run** → `raw/cavt/cavt.md` (+ per-page files). No API calls; zero cost.
4. **Parse entries** → `raw/cavt/cavt_entries.csv`: `cavt_no, title, language, section, inedita(bool),
   editions (raw), translations (raw), page`. Split on bold headings / `(latine|graece|syriace|...)` pattern.
   Spot-check 20 random entries against the scan.
5. **Gap analysis** → `CAVT_GAPS.md` (fine to commit — titles/numbers/our notes only, no copied text):
   map the 38 `static/docs/*.xml` files to CAVT numbers; list missing texts, ranked by
   (a) a critical edition exists (not *Inedita*), (b) edition is public-domain / openly licensed,
   (c) language OCP already handles (Greek, Latin, Syriac, Ethiopic, Aramaic).
6. Review the ranked list with Ken before acquiring/encoding anything new.

## Notes
- CAVT is from 1998; later editions won't be listed. Second pass later: update with DiTommaso's
  bibliography / MOTP / NASSCAL e-Clavis for post-1998 editions.
- Battifol (1889) OCR pipeline in `ocr_cleanup_scripts/` may be reusable for cleanup.

## Progress
- 2026-10-15: steps 1-3 done (full OCR in `raw/cavt/cavt.md`, per-page files in `pages/`).
- 2026-10-15: step 4 done. `scripts/cavt_parse.py` -> `raw/cavt/cavt_entries.csv` (277 entries).
  Titles from the Synopsis materiae re-OCR'd with `--psm 6` (`raw/cavt/toc/`), numbered in sequence
  where the number column was lost, plus ~70 hand corrections (`TITLE_CORRECTIONS`). Page ranges from the
  TOC (PDF = printed + 27). Each entry's text is cut from its heading to the next entry's heading.
  Checks: all 277 titles found on their pages; scan p. 156 (197-201) matches by eye.
  Known noise: 15 entries fall back to whole-page text (inedita/language counts may include neighbours);
  `languages_on_pages` is keyword-based; `pro_memoria` = "noted for reference only, treated elsewhere".
- 2026-10-15: step 5 first pass. `scripts/cavt_gaps.py` -> `CAVT_GAPS.md` (committable: numbers, titles, notes).
  OCP's 38 texts map to 25 CAVT works; 9 OCP texts (Aristobulus, Artapanus, Cleodemus Malchus,
  Eupolemus, Ps-Eupolemus, Ezekiel the Tragedian, Philo the Epic Poet, Theodotus, Aristeas the Exegete)
  are outside CAVT: its Introductio excludes the Judaeo-Hellenistic writers. 227 gaps, tiered
  A 105 / B 69 / C 53. Open: TSol -> 162? and Esdl -> 180? need checking; 60 entries lack a language
  (mostly multi-version works); edition licences not assessed.
- Structuring authority: CAVT numbers as the backbone identifiers, plus Denis, *Introduction à la
  littérature religieuse judéo-hellénistique* (2000) for the Judaeo-Hellenistic writers CAVT excludes,
  and DiTommaso (2001) / NASSCAL e-Clavis for post-1998 editions. A Denis TOC is needed for that crosswalk (requested by ILL, 2026-10-15).
- 2026-10-15: started EDITIONS_CHECK.md (archive.org verification of PD editions).
- 2026-10-16: Step 5 completed and enriched with Lorenzo DiTommaso, *A Bibliography of Pseudepigrapha Research, 1850–1999* (2001).
  - All 62 DiTommaso chapters extracted and compiled into dedicated scholarly dossiers in `bibliography/` (gitignored).
  - Ambiguities resolved: `TSol.xml` confirmed as CAVT 162 (*Testamentum Salomonis ad Roboam filium suum*); `Esdl.xml` identified as CAVT 184.iii (*Visio beati Esdrae*, Barberini lat. 2318; ed. Bogaert 1984 / Denis 1993, pp. 617–619).
  - `raw/cavt/cavt_entries.csv` enriched via `scripts/integrate_ditommaso_cavt.py` with `ditommaso_ch`, `ditommaso_dossier`, and `ditommaso_title` across all 277 entries (113 CAVT entries directly cross-referenced).
  - `CAVT_GAPS.md` regenerated via `scripts/cavt_gaps.py`: 26 CAVT works covered by 35 OCP XML editions; 18 Judaeo-Hellenistic & sapiential works outside CAVT classified (9 active in OCP, 9 gap candidates); 226 CAVT gap entries ranked across Tier A (105 entries), Tier B (69 entries), and Tier C (52 entries), complete with direct markdown links to DiTommaso dossiers and clavis cross-references.

