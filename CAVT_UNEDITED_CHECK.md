# CAVT gaps: "shelfmark but no edition" — manual check (2026-10-20)

Automated list (`edition_years` empty + "cod. ..." regex hit + not in OCP) gave 39 works.
Each was checked by reading its entry in `raw/cavt/pages/`. Both automated signals were unreliable:
`edition_years` missed many editions, and the shelfmark regex picked up neighbouring entries on the same page.

## Confirmed: shelfmark given in CAVT, unedited ("Inedita") as of 1998

| CAVT | Work | Manuscript(s) | Note |
|---|---|---|---|
| 23 | Adam. Fragmentum III (arm.) | Erevan, Matenadaran 3358, fol. 3v | |
| 25 | Epistula Adae ad Deum (arm.) | Erevan, Matenadaran 2111, fol. 229v; Venezia, S. Lazzaro 240 | |
| 39 | Eiectio Adae et Euae (georg.) | Coll. Hobi 6; Tbilisi, fonds ecclés. A 153 | identification uncertain |
| 41 | Reuelationes de creatione (georg.) | Coll. Hobi 6; Tbilisi, fonds ecclés. H 1284 | perhaps = Cave of Treasures (11) |
| 114 | Historia Joseph filii Jacob (ar.) | Cairo, Kasriat Errihan 115 | ed. announced (Manns) |
| 116 | Dormitio Joseph (ar.) | Cairo, Kasriat Errihan 115 | ed. announced (Bagatti–Battista) |
| 117 | Mors Joseph (eth.) | EMML 1939, fol. 124r–168r (codex unicus) | Eng. tr. E. Isaac, JSP 6 (1990) |
| 170 | Historia Eliae prophetae (ar.) | Dayr Abū Maqār 414 (Hag. 48) | also Graf refs |
| ~~208~~ | De iusto Job (gr., BHG 939t) | Oxford, Bodl., Holkham gr. 24, fol. 173v–175v (codex unicus) | **Withdrawn**: per Pinakes (recension 647) an anonymous abridgement of Ps.-Chrysostom, In Iob sermo 4 (PG 56, 576–582); Datema, AnBoll 103 (1985) 303f.; **edited** with German tr. by J. Dochhorn, ZAC 10 (2006) 187–194 (fol. 173v–175r) — confirmed from `raw/editions/dochhorn2006_de_iusto_job.pdf` |
| 209 | Historia Job (ar.) | Leiden 14238; Dayr Abū Maqār 394, 414 | |
| 214 | Historia Jonae (syr./ar.) | Sbath 125 + Mingana syr. 88 (syr.) | Arabic: Graf refs only |
| 215 | Apocryphon Habacuc (ar./eth.) | Dayr Abū Maqār 408 | It. tr. Conti Rossini 1945 |
| 269 | Colloquium Josephi et Nabuchodonosor (ar.) | Sbath 125 + Mingana syr. 88 | |

## Post-1998 check (web search, 2026-10-20; inconclusive unless stated)
- 208: withdrawn (see table).
- 114/116: Isaac 1990 (p. ~43 n.) cites Manns, says Battista–Bagatti would publish an Arabic Joseph life, and adds that its identity with the Ethiopic History "has yet to be demonstrated". Otherwise only Manns, "Note sur la 'Dormition de Joseph'", Henoch 4 (1982) 37–40, and Isaac (JSP 1990) reporting the Battista–Bagatti edition as forthcoming. No sign it ever appeared (syri.ac still lists only the MS). Next step: check the SBF (Franciscan Printing Press, Jerusalem) catalogue.
- 117: confirmed from `raw/editions/isaac1990_history_of_joseph.pdf`: Isaac, JSP 6 (1990), gives an English translation only, no Ge‘ez text, from EMML 1939, fols. 124a–168a (late 14th/early 15th c.). Still unedited.
- 25: Stone's survey lists "letter which God gave to Adam" as unpublished; it may be in Stone, *Armenian Apocrypha from Adam to Daniel* (2021). Check that volume's contents.
- 215: syri.ac OT Pseudepigrapha lists it (MSS via Zanetti 1988, pp. 54, 58–59) with no edition. Check the Gorgias "Biblical and Apocryphal Christian Arabic Texts" series.
- 214/269: only Sauget 1976 (reconstruction of Sbath 125 + Mingana syr. 88; Aesopic fables in the Joseph–Nebuchadnezzar frame, numbered by Sauget). No separate edition found.
- 23: Stone 2021 (*Armenian Apocrypha from Adam to Daniel*, EJL 55) has only "Creation of Eve and Disobedience" in its Adam section; no match to Matenadaran 3358 found. Check the volume's MS-sources list.
- 39, 41: no edition found. Georgian Adam literature (K'urc'ikidze 1964; Kochlamazashvili 2003 *Life of Adam*) covers the Georgian Vita, not these. "Coll. Hobi" did not come up in any search.
- 170: syri.ac marks the Arabic Elijah histories (incl. History of the Prophet Elijah) "unedited"; refs only to Zanetti 1988 and Graf.
- 209: syri.ac lists "History of Job (Arabic)" (from CAVT); no edition found.

- **Lead for 114:** Gorgias BACA series lists "History of Joseph, son of Jacob", ed. Aurélie Bischofberger (announced 2021). Publication not confirmed; nor is it confirmed that it uses Kasriat Errihan 115. Verify before removing 114.

- Follow-up (2026-10-20): the Bischofberger volume is listed on the Gorgias series page only, with no ISBN or catalogue record found, so it is probably still forthcoming. A user-compiled list distinguishes Arabic "History of Joseph son of Jacob" Versions A and B, which may be 114 and 116. The only Bagatti–Battista Arabic edition traced is *La caverna dei tesori* (SBF Collectio Minor 26, 1979/80); no Joseph volume appears in SBF listings. Stone 2021: online only the cover blurb is available; the MS index needs the book itself (JSTOR j.ctv256d6c8).

**Net (2026-10-20):** of the 12 remaining works, none has a post-1998 edition that turns up in a web search. Concrete checks left: Stone 2021 MS index (23, 25); SBF Jerusalem catalogue (114, 116); Gorgias Christian Arabic series (209, 215, 170).

## Unedited, but manuscripts cited only via a catalogue (Graf, GCAL I): shelfmarks from Graf (2026-10-20)
Source: `raw/editions/graf_gcal.1.pdf` (printed p. = PDF p. − 42). Read from OCR; all nine entries have been checked against the scan. Graf gives no edition for any of these unless noted.

| CAVT | Work | Graf | Manuscripts (Graf) |
|---|---|---|---|
| 139 | Vita Moysi (ar.) | p. 207 | Mingana ar. christ. 96 [85] (1643), ff. 143r–150r; Sin. ar. O, 11 (sic, Graf); Šarfeh syr. 11/14,1 (karš., 16th c.) |
| 156 | De palatio Salomonis (ar.) | p. 210 | Vat. syr. 199 (karš., 1545), ff. 281r–299r; Gotha ar. 2652, ff. 35r–47v; Mingana syr. 299 (1551), ff. 33v–51v; 411 (19th c.), ff. 121v–140v; 439 (1901), ff. 70r–94v; 463 (1819), ff. 59v–78r; Diyarbakr 148,4 (1600); Sbath 25 (12th c.), pp. 98–181; Sbath 1122, 1 (18th c., beginning missing) |
| 164 | Mors Salomonis (ar.) | p. 209 | Par. ar. 153 (17th c.), ff. 92r–96r; Cairo 272 (17th c.), ff. 133r–138r; Cairo 611 (1787), ff. 207r–215r; Cairo 456 (18th c.), ff. 80v–153r (Life and Death); fragm. Brit. Mus. karš. 4, ff. 206v–210r |
| 171 | Historia Eliae et filii uiduae (ar.) | p. 212 | Šarfeh syr. 11/6, 11 (karš., 17th c.) (Graf's general *History of Elijah* MSS, which CAVT does not number, are Beirut 615 (1677), pp. 109–124; Beirut 624 (1658); Sbath 246 (1615), pp. 131–156; Sin. ar. 407, 5 (1335)) |
| 172 | Historia Eliae et ascensionis eius (ar.) | pp. 212–213 | Mingana ar. christ. 44 [83] (13th c.), ff. 101r–113r; Sin. ar. 522; listed in the index of a 9th-c. Sinai parchment MS (Or. christ. N.S. 4 (1914) 339) |
| 175 | Sermo Elisei de peccatoribus (ar.) | p. 213 | Mingana syr. 562 (karš., 1723), ff. 337r–340r (codex unicus) |
| 176 | Sermo Elisei de necessitate purificationis (ar.) | p. 213; II p. 487 | Mingana syr. 225 (karš., 15th c.), ff. 87r–89r; Bodl. syr. 159 (karš., 1643), ff. 80–84; Gotha ar. 27, ff. 95r–101r (karš.) |
| 201 | Historia sanctae Shamuni (ar.) | pp. 223–224 | Karš.: Vat. syr. 202 (1672), ff. 129v–138r; Bodl. syr. 149 (1549), ff. 120r–129r; 165 (17th c.), ff. 42–51; Mingana syr. 369 (1474), ff. 15v–18r; 446 (18th c.), ff. 65v–74r; 562 (1723), ff. 354r–364r; Berl. syr. 110 (1699), ff. 28v–35r; 245 (1823), ff. 168v–186r; Šarfeh syr. 11/15, 1; 11/26, II, 1 (1670); Diyarbakr 145, 18 (15th c.). Arabic: Sbath 566 (16th c.), pp. 245–276; Šarfeh ar. 2/34, 22 (17th c.); 7/31, 5 (18th c.); Hiersemann cat. 500 no. 17 (15th c.); cat. 581 no. 1372 (karš., 1723/4). Cf. Mašriq 13 (1910) 778 |
| 268 | De Daniel et puero Caleb (ar.) | pp. 215–216 | Cairo 457 (17th/18th c.), ff. 99r–117r; Šarfeh ar. 1/36, II, 7; 6/17, 3. Karš.: Vat. syr. 159, ff. 299v–301r; Bodl. syr. 137 (16th c.), ff. 31–33 (?); 159 (1643), ff. 57–62 (?); Cambridge Add. 2881 (1484), ff. 140v–148r; 2885 (1771), ff. 67v–73v; Mingana syr. 22 (1527), ff. 136v–141r; 146 (c. 1700), ff. 221r–226r; 257 (17th c.), ff. 1–3 (incompl.); 263 (17th c.), ff. 11v–17v; 295 (c. 1500), ff. 86r–88r; 446 (18th c.), ff. 61r–65v; Diyarbakr 149, 4 (16th c.); Se'ert 64, 10 (16th c.) |

Graf (1944) lists no edition for any of the nine. All nine therefore have catalogued shelfmarks and can join the confirmed list above, subject to a post-1944 edition check. One exception: CAVT says 156 has "no codd.", but Graf lists 9 manuscripts.

## False positives: actually edited
22 (Stone 1982); 43 (Andersen, Interchange 33, cited); 59 (Tichonravov, Pamjatniki I); 74 (Yovsēpʻeancʻ 1896); 75, 81 (Stone 1996); 78 (Gaster, Romanian; Slavonic = 2 En 68–73); 80 (Tichonravov); 259 (Klostermann 1895); 226 (= Paralipomena Jeremiae, 225).

## False positives: no manuscript / not a separate text
4, 53 (patristic testimonia only); 54 (lost); 217 (Deperdita); 140 (no codd.; shelfmark hit was a neighbour); 138 (= LAB 19).
223, 224 (4Q387b, 4Q389a): "editio paratur" in 1998; since published (Dimant, DJD 30, 2001).

## Reverse error (not yet swept)
Some entries the parser counted as *edited* are in fact Inedita with shelfmarks, e.g. 73 Visio Henoch (Paris, BnF Abbadie 107) and 153 Dicta Gad (Cambridge UL Oo.1.20, codex unicus). The Tier C entries in CAVT_GAPS.md should be checked the same way.

## Entry-level audit (scripts/cavt_audit.py → CAVT_AUDIT.md, 2026-10-20)
- Neighbour leak of the Inedita flag: 15, 96, 100, 142 are edited. They were moved out of Tier C via HAND_TIERS in cavt_gaps.py (Tiers now A 92 / B 71 / C 46).
- Inedita in the entry but page flag 0: 129 (an unedited Michigan papyrus beside the edited text) and 242 (4Q232, unedited) are partial inedita and stay in Tier A. 88's hit is a false positive ("unpublished mss" in a thesis title).
- (Superseded by the second pass below: edition-year errors corrected by cavt_fix_entries.py.)
- 54 entries mention "paratur" (edition in preparation in 1998); mostly Qumran, now in DJD. They are a checklist for post-1998 editions.
- The CAVT_GAPS.md header now reports 209 in tiers + 2 hand-excluded (previously an unexplained 211).

## Corrections applied (2026-10-20, second pass)
- `scripts/cavt_fix_entries.py` recomputed n_inedita_on_pages, edition_years, qumran, refers_to and no_critical_edition for each entry from its own text (not the whole page). It also applies 4 hand overrides: 136 is pro memoria; 179 years cleared; 190 = 1877; 250 = 1994. The 63 changes are logged in `raw/cavt/cavt_entries_fixes.tsv`. Entry 277 and short mismatched hits are skipped.
- `raw/cavt/post1998_editions.csv`: post-1998 DJD/Masada editions for 23 Qumran/Masada entries, from memory and **not yet verified**. `cavt_gaps.py` now marks them "modern" instead of "none listed".
- HAND_TIERS now also covers 15, 96, 100 → B; 142, 129, 242 → A; 208 → part (abridgement). Tiers are now A 92, B 71, C 45.
- Still open: the non-Qumran "editio paratur" entries in CAVT_AUDIT.md §3, such as 73, 95, 102, 114, 116, 153, 230 and 254; the entries 194 and 243 that the script could not locate; and Tier C after these fixes.

## Editions announced in 1998 ("editio paratur"), works outside Qumran: follow-up (2026-10-20, web search)
| CAVT | Work | Announced 1998 | Found |
|---|---|---|---|
| 73 | Visio Henoch (eth.), Paris BnF Abbadie 107, fol. 56v–59 | Haelewyck | Nothing found; probably still unedited |
| 95 | Historia de Melchisedech | (Syriac version Inedita: Vat. syr. 159, fol. 241v–242v) | Not checked; Greek and Coptic versions are already edited |
| 102 | Scala Jacob (slav.) | new ed. by R. Rubinkiewicz | No Rubinkiewicz edition found. **New**: S. Fahl and Ch. Böttrich (with D. Fahl), *Leiter Jakobs* (JSHRZ.NF I/6; Gütersloh 2015). It is a German translation (pp. 105–247) made from a fresh collation of the manuscripts (sigla, pp. 19–23; recensions, pp. 23–28), with no Slavonic text printed (per the table of contents). Older editions already exist (Pypin, Tichonravov, Porfir'ev). |
| 153 | Dicta Gad uidentis (hebr.), Cambridge UL Oo.1.20 | M. Bar-Ilan | **Edited**: M. Bar-Ilan, Hebrew edition with English introduction and translation (2015; NLI record NNL_ALEPH003844968); English tr. Bar-Ilan, *Words of Gad the Seer* (CreateSpace 2016). The 2015 edition runs to 377 pp. (NLI); its publisher is still to be confirmed (the NLI page blocks automated access). |
| 230 | Historia Josias (eth.) | Haelewyck | Nothing found; probably still unedited |
| 254 | Apocalypsis Ps.-Methodii | Aerts–Kortekaas | **Published**: W.J. Aerts and G.A.A. Kortekaas, *Die Apokalypse des Pseudo-Methodius*, CSCO 569–570, Subsidia 97–98 (Leuven 1998). Confirmed by web search; some bibliographies give 1997. |

**New source for 114/116:** A. M. Butts, K. S. Heal, S. Moseley and J. Witztum, "Notes on the History of Joseph (CAVT 113, 114) and the Death of Joseph (CAVT 116, 117)", *Apocrypha* 28 (2017) 233–237. The article revises CAVT's entries for these four works, so it may resolve the Kasriat Errihan 115 question. Brepols DOI 10.1484/J.APOCRA.5.115432 (paywalled; the BYU record has no PDF). The abstract does not say what the revisions are, so the article itself is needed.
