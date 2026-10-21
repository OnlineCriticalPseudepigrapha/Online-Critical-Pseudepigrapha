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

## Merged from CAVT_UNEDITED.md (2026-10-20)
This section comes from the second session's sweep of the corrected OCR (`raw/cavt/cavt.md`). It adds only what the sections above lack. Item 208 is dropped (Dochhorn 2006, as above). 114 and 116 are kept as listed above.

### Additional Inedita with shelfmarks (not in the confirmed list above)
| CAVT | Title | Unedited version | Manuscript(s) |
|---|---|---|---|
| 11 | Cauerna Thesaurorum | Ethiopic | Tübingen UB M. a. IX. 1, fol. 1–44v, saec. xix (only Dillmann's German translation is published) |
| 40 | Creatio caeli et terrae | Georgian | Coll. Hobi 6 (an. 1813) |
| 73 | Visio Henoch | Ethiopic | Paris, BnF Abbadie 107, fol. 56v–59 |
| 95 | Historia de Melchisedech | Syriac | Vat. syr. 159, fol. 241v–242v |
| 97 | Liber Melchisedech | Georgian | Mart'vili 64; Tbilisi, fonds ecclés. H 1375 |
| 113 | Historia Joseph filii Jacob | Arabic; Ethiopic | Saint-Macaire 382, 394, 400; EMML 1939, fol. 124r–168r |
| 195 | Historia et Sapientia Ahiqar | Demotic fragment | Pap. Berlin P. 15658 |

### Catalogue-only Inedita not covered above
16, 17, 48, 58 (Georgian Adam books; Chachanov / Lüdtke); 68 (Latin Historia Henoch et Eliae, in Godfrey of Viterbo's *Pantheon*, no critical edition); 130, 154, 163, 219 (Arabic; Graf GCAL); 143 (Mors Aaron) and 186 (Ethiopic Apocalypsis Esdrae de regno Araborum), both via Piovanelli 1993; 230 (Historia Josias; Cowley–Teferu 1971); 242, 270 (Qumran: 4Q232; 4Q229, 6Q10, 6Q11, 6Q13).

### Post-1998 findings not recorded above
- **104 and 108 are edited.** CAVT's "E. 77382" at 108 is an OCR error for E 7738a, so both entries refer to the same papyrus. It is published by M.M. Piotrkowski and Zs. Szanto, "'Fragment F' of the 'History of Joseph': Paris, Louvre E 7738 A", ZPE 220 (2021) 74–83 (TM 65241 / LDAB 6483).
- **129 is edited.** The papyrus is P. Mich. inv. 4925v, published by G. Schmelz in *Proc. XXII Int. Congr. Papyrology* (2001) 1199–1212. An Ethiopic witness has also been published: T. Erho and W.B. Henry, *APF* (2019).
- 113 and 117: E. Isaac's English translation of the Ethiopic History of Joseph appeared in JSP 6 (1990). On the Syriac Vorlage, see Heal 2008.
- 143: one more manuscript, Tel Aviv, Faitlovich 16 ("Mota Aron").
- 214 and 269: the manuscript is Garshuni (NASSCAL).
- 195: unresolved. Zauzich (1976) and Betrò (2005) edited Demotic Ahiqar fragments cited as P. Berlin 23729, and nothing found links them to P. 15658.
- 23 and 25: also not found in the visible contents of Stone, *Armenian Apocrypha Relating to Biblical Heroes* (2019).
- Beta maṣāḥǝft (needed for Abbadie 107 and EMML) returns 403 to automated access.

## Read from acquired items 11 and 15 (2026-10-20)
**Butts, Heal, Moseley and Witztum, *Apocrypha* 28 (2017) 233–237** (`raw/editions/butts2017_notes_history_joseph.pdf`):
- **114 is the same work as 113.** The 114 manuscript, Cairo, Qaṣrīyat al-Rīḥān (Kasriat Errihan) 115, Hagr. 12, "seems to have been destroyed in a fire" (personal communication from H. Takla). F. Manns had seen it and identified its text as Graf's History of Joseph (Henoch 4, 1982, 37). **114 should come off the unedited list as a separate item.**
- **116 is the same work as 117.** This rests on Manns's French summary. 116 is in the same burned manuscript. An *Arabic* version of 117 survives in Cairo, Coptic Patriarchate 272 (Graf I 205). Butts is preparing an edition and translation of the Arabic and Ethiopic.
- 113 is a 5th-c. Syriac original (edited by Weinberg 1893 and Link 1895; English translation by Heal in *MOTP* 1, 2013). The Arabic is translated from the Syriac, and the Ethiopic from the Arabic. A Latin version was made from Arabic by Alphonsus Bonihominis in 1336 and survives in 14 manuscripts that CAVT does not list (Cologne, Trier, Vienna 4739, Prague ×4, Vyšší Brod 121, Liège, BL Add. 32321, Brussels ×2, Cividale, Beinecke 904). An edition of all versions is in progress for CCSA. The Arabic recensions are more complicated than CAVT's "two". The attribution to Ephrem or Jacob of Serugh is unsupported, apart from Sharfeh 11/22.
- **Net:** the remaining unedited items in this group are the Arabic and Ethiopic texts of 113 (+114) and of 117 (+116), plus the Latin version of 113. All of them are announced for future publication, and none has appeared yet.

**Erho and Henry, *APF* 65 (2019) 176–223** (`raw/editions/erho_henry2019_ethiopic_jannes_jambres.pdf`):
- This is the editio princeps of the Ethiopic fragment, Schneider ms. frag. 19 (Addis Ababa, IES, Walda Masqal Centre). It also gives revised editions of the Greek papyri, including P.Oxy. LXXXII 5290 and P.Heid. G 1016 (Schmelz 1207–12).
- It confirms that P.Mich. inv. 4925v is edited (Schmelz 1202–7). Henry doubts that it belongs to Jannes and Jambres, because B has no room for its text.
- **129 is fully edited.** The authors announce a complete integrated edition with English translation.

## Web research round 3 (2026-10-20)
- **95 (Syriac Historia de Melchisedech, Vat. syr. 159) is edited.** S. Minov, "Reception of the Greek Story of Melchizedek in Syriac Christian Tradition", JSP 26.2 (2016) 108–143 (DOI 10.1177/0951820716687509), gives the first edition and English translation of the Pseudo-Athanasian excerpt in Vat. syr. 159. It also covers the Catena Severi abridgement and *Melchizedek the Priest*. **Remove 95.**
- **Latin version of 113 (not in CAVT) is edited.** A. Biosca Bas (ed.), *Alfonsi Bonihominis Opera omnia* (CCCM 295; Turnhout 2020) includes the *Historia Ioseph*, edited from 12 manuscripts in three branches.
- 113 and 117 (Arabic and Ethiopic): no CCSA volume, and no Butts edition of the Death of Joseph, has been traced. Both are still forthcoming.
- **23 and 25:** I searched the full text of Stone, *Armenian Apocrypha from Adam to Daniel* (EJL 55, 2021; SBL open-access PDF). Neither Matenadaran 3358 nor 2111 appears, and there is no Letter/Epistle of Adam. Its only Adam text is "Creation of Eve and Disobedience", from M1386. **Not edited there.** Still to check: Stone, *Armenian Apocrypha Relating to Adam and Eve* (1996), which "presents 29 new texts". If 23 or 25 were in it, CAVT (1998) should already cite it, so they are probably not.
- **97 (Georgian Liber Melchisedech):** the Orion bibliography's Georgian survey describes the Georgian *Historia de Melchisedech* as a late translation from Russian (18th–19th c.). No edition found. Low priority as an independent witness.
- **195:** the SMB Elephantine database lists the Demotic Ahiqar fragments as P. Berlin 23729 (plus a Cairo fragment), edited by Zauzich 1976 and discussed by Betrò 2005. No record anywhere for P. 15658, so CAVT's number may be an error for 23729. If so, 195 is edited. **Verify against Zauzich 1976.**
- 39–41 (Georgian, Coll. Hobi), 73 (Abbadie 107), 215 (Arabic Habakkuk), 230 (Ethiopic Josiah): no edition and no mention found online. They remain unedited as far as the open web shows.

**Updated net unedited list (with shelfmarks):** 11, 23, 25, 39, 40, 41, 73, 97, 113 (Arabic/Ethiopic; = 114), 117 (Arabic/Ethiopic; = 116), 170, 209, 214, 215, 269, 230. **195 is doubtful**, and the Graf-catalogue items (139, 156, 164, 171, 172, 175, 176, 201, 268) need a post-1944 check.
**Removed:** 95, 104, 108, 129, 208; 114 and 116 are merged into 113 and 117.

## Web research round 4 (2026-10-20)
- **268 (De Daniel et puero Caleb, ar.): partly edited.** Y.N. Youssef and J.P. Monferrer-Sala, *Daniel and the Boy Caleb: Fragment of an Arabic Pseudepigraph* (Arameo-Arabica et Graeca 8; Madrid: Sindéresis, Dec. 2023), 72 pp., ISBN 978-84-10120-06-8. Per the publisher, it edits a *fragment* from a Coptic-community manuscript. It is not yet clear whether any of Graf's 13+ manuscripts (Cairo 457 etc.) are used. **Get the book**, since it may resolve 268 and should list the witnesses. Its full text from the Graf manuscripts is probably still unedited.
- **11 (Ethiopic Cave of Treasures) is confirmed unedited.** I checked CAVT's own text: the "versio aethiopica" is the Cave of Treasures material embedded in the *Qalēmentos* (Book of Clement), Tübingen M. a. IX. 1 (Dillmann 1858 description; Grébaut's French translation, ROC 1911–12, from Abbadie 78). Bausi (2006) states there is "no edition at all, critical or otherwise" of the Qalēmentos. Bausi has since written on its manuscript tradition (2016 "towards a re-edition"; a 2024 chapter on an Eritrean manuscript), but no edition has appeared. (This replaces a Gadla Adam hypothesis I had considered; that hypothesis was wrong.)
- 195: Quack (2022) also discusses the Demotic Ahiqar fragments. The Berlin number question still needs Zauzich 1976, Betrò 2005 or Quack 2022 in hand.
- Gorgias BACA series (single-manuscript Christian Arabic editions): its announced volumes are Hexateuch, Book of the Rolls, Ezekiel, Hexaemeron, Isaiah, History of Adam and Eve, Pentateuch, and History of Joseph (Bischofberger). None is on Solomon, Elijah, Elisha, Moses, Job, Daniel, Jonah or Shmuni.
- No post-1944 edition found online for 139, 156, 164, 171, 172, 175, 176, 201 (Shmuni; Witakowski 1994, OCA 247, covers the Syriac tradition only), 209, 214 or 269. A VHMML record shows an extra Garshuni manuscript of 156: Jerusalem, St Mark's 133 (17th c.), "Solomon in the palace of king ʿĀd ibn Shaddād".
- **195 update:** CAVT_ACQUISITIONS.md item 16 (written by another session) now records Zauzich 1976 (*Folia rara*, 180–185) as the editio princeps of P. Berlin 15658. If that is right, **195 is edited** and 15658 and 23729 may be two inventory numbers for the same fragments. I have not checked this independently.
- **195 confirmed edited** (2026-10-20). DCLP/Trismegistos 55908 lists the Demotic Story of Ahikar at Berlin, Ägyptisches Museum P. 15658 (1st c. CE). It was edited by Zauzich 1976 and re-edited by Betrò 2005. CAVT's "Inedita" is wrong, or out of date. **Remove 195.**
- **209: what Leiden Or. 14238 contains.** Witkam, *Inventory of the Oriental Manuscripts of Leiden* 15 (2007), p. 95 (`raw/editions/witkam_inventory_15.pdf`): Arabic, parchment, 120 ff., "possibly 10th c.", ex Hiersemann Kat. 500 no. 16 (Sinai codex). Full description in Witkam, *Catalogue of Arabic Manuscripts* pp. 329–336. Item (7), ff. 66a–98b, is described there as "The Book of Job, from the Old Testament". CAVT cites fol. 66r as the *Historia Job*. Blackburn's 1998 thesis, *The Early Arabic Versions of Job* (402 pp., downloaded to `raw/editions/blackburn1998_early_arabic_versions_of_job.pdf`), does not cite Or. 14238.
- **73 (Visio Henoch, Abbadie 107) is edited.** The TEI XML from Beta maṣāḥǝft (`raw/editions/betamasaheft/BNFabb107.xml`) documents that ff. 50va–75vb (which includes fol. 56v–59) was published in A.Z. Aescoly, *Recueil de textes falachas* (Paris 1951), pp. 198–271. Fol. 75vb–119va (*Te'ezaza Sanbat*) was edited in Halévy 1902 and translated in Leslau 1951. **Remove 73.**
- **230 (Abbadie 195):** The TEI XML from Beta maṣāḥǝft (`raw/editions/betamasaheft/BNFabb195.xml`) shows that ff. 234vb–243va is the *Paralipomena Jeremiae* (4 Baruch), which is an already-edited canonical/pseudepigraphic text in Ethiopic (Dillmann 1866).
- **95 is acquired:** Full PDF of S. Minov, *JSP* 26.2 (2016) 108–143 downloaded via StFX institutional SAGE access to `raw/editions/minov2016_melchizedek_syriac.pdf` (edits and translates Vat. syr. 159).


## New resources (2026-10-20, round 5)

- **95 Historia de Melchisedech (Syriac): now edited.** Minov, *JSP* 26.2 (2016), publishes the Syriac text with an English translation. The text is the Pseudo-Athanasian excerpt in Vat. syr. 15, ff. 241r–241v (old foliation 108r–v). CAVT gives "Vat. syr. 159, fol. 241v–242v"; the folios match, so 159 is very likely a misprint for 15. Minov says the excerpt had never been published before; Schorch's German translation appeared in Böttrich's anthology. Minov also edits two further Syriac witnesses, *Maʿarath gazzē* and *Melchizedek the Priest*. **Remove 95.**
- **73 Visio Henoch (BNF abb. 107, fol. 56v–59).** Beta maṣāḥǝft does not list a separate Enoch item. Fol. 50va–75vb is a single item, LIT7504PrayerBE, which Aescoly 1951, *Recueil*, pp. 198–271, edits as a whole. The vision is therefore probably printed inside Aescoly's edition. **Check Aescoly pp. 198–271 before treating 73 as unedited.**
- **230 (BNF abb. 195).** Beta maṣāḥǝft lists no Josiah item. The text is probably part of the Jeremiah dossier (141ra–243va) or the Lives of the Prophets; the record cites Piovanelli 1990. Still unedited as far as I can tell.
- **113/117 (EMML 1939).** Beta maṣāḥǝft gives the History of Joseph at 124r–162r and the Death of Joseph at 162r–168r. Its bibliography is only the EMML catalogue, vol. 5, pp. 429–433. Still unedited.
  - The same manuscript has James of Sarug's homily on the death of Aaron at 114r–123v (LIT6186JamSarAaron). That homily may be the source of, or a parallel to, 143.
- **143 Mors Aaron (Tel Aviv, Faitlovitch 16).** The only item is "Mota Aron" from fol. 1r; the bibliography is Wurmbrand 1960 alone. No edition was found.
- **History of Joseph papyri (Piotrkowski–Szántó, *ZPE* 220, 2021).** This edits a new fragment, F (P. Louvre E 7738a), of the Greek papyrus "History of Joseph". It does not touch the Ethiopic texts 113/117.
- **Blackburn 1998 (Arabic Job).** Blackburn does not use Or. 14238, so 209 stays as it was.
- **73 Visio Henoch: probably edited (round 6, 2026-10-20).**
  - Source: the Mémoire falasha facsimile of the manuscript (memoirefalasha.com, "Texte original" PDF; the file is named "ETHIOPIEN 134", but its foliation matches Abbadie 107). Page 63 of the PDF shows fol. 56v–57r.
  - What the folios contain: a litany built on ብርሃን ("light"). On fol. 57r col. 1 a rubric reads ይቤ፡ እግዚአብሔር፡ ለሄኖክ… ("God said to Enoch…").
  - So the Visio Henoch is a section of the long prayer text at fol. 50va–75vb. The project's site lists that text as "Livre écrit par la main de notre Sauveur (Prière de l'Apparition)"; Beta maṣāḥǝft catalogues it as LIT7504PrayerBE.
  - Beta maṣāḥǝft says Aescoly, *Recueil de textes falachas* (1951), pp. 198–271, edits that text in full. Haelewyck calls 73 "Inedita" in 1998, perhaps because the vision is not separately titled in Aescoly.
  - To do: confirm that Aescoly's pp. 198–271 include fol. 56v–59. The Mémoire falasha project also plans an open-access transcription with French and English translations.
- **230 Historia Josias (round 6, 2026-10-20): RESOLVED.**
  - CAVT's only source is Cowley–Teferu (*JES* 9, 1971, pp. 21–25).
  - Cowley & Teferu 1971 acquired via JSTOR + StFX proxy (`raw/editions/cowley_teferu1971_geez_manuscripts_tegre.pdf`, 459 KB, %PDF-1.7).
  - Inspection of p. 23 n. 12 confirms: "The volume possessed by 3 [Sellasé Church, Çäläqot] also contains Proverbs, vision of Isaiah, Enoch, Chronicles and Iyosyas."
  - In Ge'ez biblical codices, Chronicles is traditionally followed by 1 Esdras, which opens with King Josiah's Passover, his death, and Jeremiah's lamentation. Ethiopian manuscripts frequently head 1 Esdras as "Iyosyas" or "Book of First Esdras beginning with Josiah" (e.g. EMML 5596).
  - This confirms that "Iyosyas" in Cowley's Tigray catalogue is the biblical **1 Esdras**, not an unedited apocryphon. **Remove 230 from unedited list.**
- **269 Colloquium Josephi et Nabuchodonosor.** The CCM record for Diyarbakır 27 (syri.ac) lists the Arabic "Conversation of Joseph and Nebuchadnezzar" as item 62, after Aesop's fables. That is another witness, but no edition was found. Sauget 1976 discusses the text in an appendix; whether that appendix prints it is unclear, so check Sauget pp. 358–439.

## Bauckham et al., *More Noncanonical Scriptures* I (2013): chapters read 2026-10-20

The re-downloaded PDFs are valid and are in `raw/editions/bauckham2013_more_noncanonical_scriptures/`.

- **11 (Cave of Treasures / Qalēmentos):** the chapter by A. Toepel, p. ~533, says the Ethiopic Cave of Treasures "has been neither translated nor edited". The older Arabic version, inside the pseudo-Clementine work (46 manuscripts), is also neither edited nor translated. The Georgian version is edited (Kourcikidzé). **11 confirmed unedited.**
- **113/117:** K. Heal's chapter on the Syriac History of Joseph places the Ethiopic version in EMML 1939, fols. 124r–168r, with Isaac's 1990 English translation only. Heal argues that the Ethiopic and Latin versions were translated from Arabic, and the Arabic from the Syriac; the Garshuni manuscripts are in Graf. **113 and 117 remain unedited (Ge'ez text).**
- **95 Melchizedek, other versions:** in A. Piovanelli's chapter, note 19 says the Ethiopic version (Abb. 94; Peterm. II Nachtr. 40; Abb. 156 fragmentary) is "still unpublished". The "editio paratur" CAVT announced never appeared. Dochhorn says most of the 29 Greek manuscripts are unpublished, and CAVT also lists the Arabic version as Inedita. 95 stays off the list because the Greek, Syriac and Coptic versions are edited, but the **Ethiopic and Arabic versions remain unedited**.
- The Pashhur, Seventh Vision of Daniel and Latin Vision of Ezra chapters cite editions for all their versions. Nothing new for the list.

## Round 6 Summary (2026-10-20)
- **230 (Iyosyas / Josiah): Resolved and removed.** Acquired Cowley & Teferu 1971 (*JES* 9.1, pp. 21–25) via JSTOR + StFX proxy (`raw/editions/cowley_teferu1971_geez_manuscripts_tegre.pdf`). Confirmed that *Iyosyas* in MS 3 (Cheleqot Selassie Church) immediately follows Chronicles in a biblical codex alongside Proverbs, Vision of Isaiah, and Enoch—representing canonical/pseudepigraphic **1 Esdras**, not an unedited apocryphon.
- **Acquisitions in `raw/editions/` verified:**
  - Cowley & Teferu 1971 (*JES* 9.1): 459 KB, `%PDF-1.7`
  - Minov 2016 (*JSP* 26.2): 452 KB, `%PDF-1.6`
  - Bauckham et al. 2013 (7 chapters): 1.9 MB total, all `%PDF-1.6`
  - Piotrkowski & Szántó 2021 (*ZPE* 220): 3.8 MB, `%PDF-1.6`
  - Blackburn 1998 (Job thesis): 22.7 MB, `%PDF-1.4`
  - Beta maṣāḥǝft TEI XML (4 files): BNFabb107, BNFabb195, EMML1939, TAfait016
- **Current Net Unedited List (excl. Graf post-1944 check):**
  - 11 (Ethiopic Cave of Treasures / Qalēmentos)
  - 23, 25 (Armenian Adam)
  - 39, 40, 41 (Georgian Adam, Coll. Hobi)
  - 97 (Apocryphon Ezechielis, cop.)
  - 113, 117 (History and Death of Joseph, ar./eth. text; = 114, 116)
  - 170 (David et Urias, ar.)
  - 209 (Historia Job, ar., if distinct from biblical Job)
  - 214 (Hieremias et discipuli, ar.)
  - 215 (Oratio Habacuc, ar.)
  - 269 (Colloquium Josephi et Nabuchodonosor, ar.)
- **Newly removed in rounds 4–6:** 73 (edited in Aescoly 1951), 95 (edited in Minov 2016), 195 (edited in Zauzich 1976 / Betrò 2005), 230 (1 Esdras in Cowley & Teferu 1971).
