# LAB_PLAN — Pseudo-Philo, *Liber Antiquitatum Biblicarum* (CAVT 131)

Plan for open issues **#4, #5, #14** (Latin text and introduction). Written 2026-10-18.

## Source now on disk

| What | Where | Notes |
|---|---|---|
| IA OCR text layer, whole book | `raw/editions/Pseudo-Philo_LAB_Kisch1949_djvu.txt` | 314 leaves, `===== PAGE n =====` markers; gitignored |
| Latin text section extract | `scratch/lab/kisch_latin_text_raw.txt` | leaves 141–302 = Kisch printed pp. 108–272; gitignored |
| Chapter→page map | `scratch/lab/LAB_CHAPTER_MAP.json` | 58 of 65 chapter headings auto-detected; see caveats |

Scans: `pseudophiloslibe0000guid_l9x6` (IA, `inlibrary`/`printdisabled` pool — 1-hour loan,
no LCP license issued; text layer captured via `BookReaderGetTextWrapper`, see
`NEXT.md` 2026-10-18). Captured for research use; no republication.

## Structure of the Kisch edition (scan leaves)

- 137: PART TWO title; 138–140: sigla of manuscripts; **141–302: Latin text** (chapters I–LXV);
  303+: indexes/bibliography rear matter. Front matter: 9–14 title/copyright/preface/ToC/illustrations;
  15–136: PART ONE (Introduction, in English).

## Chapter map (detected)

Complete run **I–XXIV** (pp. 141–208), then XXVI–XXXII, XXXIV–XXXVII, XXXIX–XLII, XLIV–LI,
LIV–LXIII, LXV. Headings for **25, 33, 38, 43, 52, 53, 64** were not matched by the OCR scan
(heading strings damaged); the editor should key those off the printed page ranges in the
map's neighbourhood rather than trusting the gap list. Chapter LXV at p300 is the final chapter —
matches the standard 65-chapter LAB.

## OCR quality (measured, Latin-text pages only)

- 44,941 word-like tokens; **0.43 % garbled** tokens (character–digit mixes). Clean enough to
  work from, not clean enough to publish unverified.
- Regular defects: superscript apparatus sigla interleave into the line (`I. 1. INITIUM MUNDI.®`),
  occasional digit/letter confusions (`2r` for a MS siglum, `Tune` for `Tunc`, `Ihesus autemy`).
- **Crucial**: Kisch prints a full **apparatus criticus at the foot of each page**, and the OCR
  text runs it straight into the chapter text (`5, 4. 5 Gen. 5, 6-7. ... Adm. M; om. A; Phil...`).
  Any extraction must split text vs apparatus before markup — the two streams are interleaved,
  not separated by a marker.

## Work plan for #4 / #5 / #14

1. **Choose the base text policy.**   Kisch's edition is Admont-based with the Melk manuscript and
   the editio princeps (Sichardus 1527, already in `raw/editions/` as `ARes69403`) in the apparatus.
   OCP's existing XML editions (e.g. `Demetr.xml`, `Justus.xml`) show the house style: one `<div>` per
   chapter, `<unit>` per verse, readings attributed by witness sigla. Confirm with Ken whether
   OCP's LAB text should follow Kisch's Admont base or the OCP convention of a majority/eclectic text.
2. **Split text from apparatus** (Kisch pp. 108–272): script a rule — apparatus lines follow the
   verse-number pattern `N, M.` + `<sigla>`; text lines carry the running Latin. Verify against
   the printed page images (available in the loan session while it lasts; otherwise the leaf URIs
   in `scratch/lab/` notes).
3. **Proofread chapter by chapter** against the facsimile (the 0.43 % defect rate means roughly
   one error per ~230 tokens — every chapter needs a pass).
4. **Markup**: build `static/docs/LAB.xml` (+ `static/docs/tei/LAB.xml` twin, per repo convention),
   chapters I–LXV, verse units per Kisch's numbering; sigla from scan pp. 138–140.
5. **Introduction (#14)**: Kisch's English introduction (pp. iii–97 of the printed book) is a
   copyright source — do NOT paste it into the public repo. Draft an original OCP introduction
   citing Kisch, Harrington–Cazeaux (SC 229, ILL pending), and the DiTommaso dossier
   (`bibliography/`); add to `databases/storage.sqlite` + regenerate `static/docs/intros.json`.
6. **Register**: update `OCP_DOCUMENTS` in `static/js/reader.js`, `EDITIONS_CHECK.md`,
   and the CAVT crosswalk row for 131.

## Cautions

- The IA text layer is OCR, not an e-text; every quotation that ships must be facsimile-verified.
- `raw/` and `scratch/` are gitignored by design — the committed artifacts are the XML, the
  intro JSON, and the governance docs; nothing here licenses republication of Kisch's text.
- The 1-hour IA loan is transient: page-image checks must happen during a loan session or from
  the printed copy.
