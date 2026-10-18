# PD candidates: CAVT Tier B & C (sweep 2026-10-18)

First pass over the 118 Tier B (68) + Tier C (50) works in `CAVT_GAPS.md` for
editions already in the public domain. Two methods were run; only the second
produced usable results.

## Method note

1. **Naive title search** (each row's CAVT descriptive Latin title → IA advancedsearch):
   118 queries, 31 raw hits, but low precision — descriptive titles like
   *Historia orientalis* match unrelated printed books, and the hits clustered on
   9 works, almost none of them the intended one. Raw output:
   `scratch/` CSV (gitignored). **Verdict: not a usable method** for these titles;
   the works must be found by their modern editorial names, not the CAVT Latin.
2. **Curated named-edition search** (16 queries against the classic editors): usable.
   Results below. Identifiers are archive.org item ids — none are confirmed PD-US
   by a renewal check yet; all pre-1930 by date.

## Confirmed-looking candidates

| CAVT | Work (Tier) | Edition | Item id | Date | Notes |
|---|---|---|---|---|---|
| 11 | Cauerna Thesaurorum (C) | Bezold, *Die Schatzhöhle* (Syriac text) | `dieschatzhhlea00bezouoft` | 1883 | Syriac original text |
| 11 | Cauerna Thesaurorum (C) | Budge, *The Book of the Cave of Treasures* | `bookofcaveoftrea0000eawa` | 1927 | English; US-PD by date |
| 66 | Henoch slauicus (B) | Morfill/Charles, *The Book of the Secrets of Enoch* | `bookofsecretsofe00morf` | 1896 | 2 Enoch, English from Slavonic |
| 205 | Odae Salomonis (B) | Harris, *The Odes and Psalms of Solomon* | `odespsalmsofsolo00harruoft` | 1911 | with 1909/1910 duplicates on IA |
| 195 | Historia et Sapientia Ahiqar (C) | Conybeare–Harris–Lewis, *The Story of Ahikar* | `storyofahikar0000cony` | 1913 | |
| 18–37 | Armenian Adam/Abel apocrypha (B) | Issaverdens, *The Uncanonical Writings of the O.T.* | `cu31924091353445` | 1901 | covers the Armenian cluster |
| 104–113 | Joseph apocrypha (C) | Fabricius, *Codex pseudepigraphus Veteris Testamenti* | `codexpseudepigr01josegoog` | 1713 | also 1722 vol. `A086B248` |
| 167 | Apocalypsis Eliae (B) | Steindorff, *Die Apokalypse des Elias* | `dieapokalypsede00steigoog` | 1899 | Coptic |
| 216 | Apocalypsis Sophoniae (B) | Steindorff volume above? (Lippl 1910 is the *canonical* Zephaniah — not this) | — | — | **not found**; check Steindorff 1899's companion texts |

## Searched, not found (or false positives only)

- **15 Lib. Adami (Mandaic)** — Norberg's *Codex Nasaraeus* (1815–16) did not surface; the
  hits were unrelated early-modern prints. Worth a direct IA browse of the Norberg
  volumes (they exist in European library collections).
- **254 Apocalypsis pseudo-Methodii** — Bonwetsch hits were other works; the 1897
  *Hippolytus Werke* is not the pseudo-Methodius edition. Sackur 1898 also not on IA.
- **227–228 Jeremiah apocrypha (Coptic)** — false positives (Reusner law disputations).
- **142–143 Mors Moysi / Mors Aaron (Ethiopic)** — zero hits under those names.
- **187 Apocalypsis Esdrae aethiopica** — Box's *Ezra-Apocalypse* (1912/1917) is **4 Ezra**,
  a different work; do not acquire it under this CAVT number.
- **2 Vita Adae (Latin)** — hits were unrelated (herbals, astrolabes).

## Next actions

1. Marshalled acquisitions: the nine candidates above are all readable/downloadable on IA
   as PD; fetch text layers with the `ia-loan-acquisition` workflow (no loan needed when
   the item is not access-restricted).
2. Do the **US renewal check** for the post-1929 ones (Budge 1927) before relying on PD-US.
3. Re-run this sweep as a curated list, not a title search: for each Tier B/C work, name
   its standard edition(s) from the DiTommaso dossier in `bibliography/` first, then hunt
   those names on IA. The dossiers already cite the editions.
4. Tiers still unsearched: the Armenian/Arabic/Ethiopic/Georgian clusters need their own
   repertoires (Issaverdens covers some Armenian; the Arabic and Ethiopic ones largely need
   print ILL).
