#!/usr/bin/env python3
"""
Build Pseudo-Orpheus (Testament of Orpheus / Diathēkai / Hieroi Logoi, CAVT 183 / CANT 33)
Greek text from:
Otto Kern, Orphicorum Fragmenta (Berlin: Weidmann, 1922), frr. 245-248, pp. 255-266.
Denis, Fragmenta pseudepigraphorum quae supersunt graeca (PVTG 3, 1970), pp. 163-174.

Contains:
  - Chapter 1: Recensio Aristobuliana (ap. Euseb. Praep. Ev. XIII.12.5 & Theosophia Tubingensi 61) - 41 verses
  - Chapter 2: Recensio Iustiniana (ap. Ps.-Iustin. Cohort. ad Graecos 15 & De Monarchia 2) - 21 verses
  - Chapter 3: Hymnus ad Deum Supremum (ap. Clem. Alex. Strom. V.125.1 & Euseb. Praep. Ev. XIII.12) - 10 verses
Outputs:
  - static/docs/PsOrph.xml (Grammateus DTD)
  - static/docs/tei/PsOrph.xml (TEI P5 parallel segmentation)
"""

RECENSION_ARISTOBULUS = [
    ("Φθέγξομαι οἷς θέμις ἐστί· θύρας δ᾽ ἐπίθεσθε βέβηλοι,", "I will speak to those whom it is lawful; shut the doors, you profane,"),
    ("φεύγοντες δικαίων θεσμούς, θείοιο τεθέντος", "fleeing the ordinances of the righteous, when the divine law has been set"),
    ("πᾶσι νόμου. Σὺ δ᾽ ἄκουε, φαεσφόρου ἔκγονε Μήνης,", "before all. But listen thou, son of the light-bearing Moon,"),
    ("Μουσαῖ᾽· ἐξερέω γὰρ ἀληθέα, μηδέ σε τὰ πρὶν", "Musaeus; for I will utter true things; nor let what previously"),
    ("ἐν στήθεσσι φανέντα φίλης αἰῶνος ἀμέρσῃ.", "appeared in thy breast deprive thee of beloved life."),
    ("εἰς δὲ λόγον θεῖον βλέψας τούτῳ προσέδρευε,", "Look unto the divine Word and attend upon it,"),
    ("ἰθύνων κραδίης νοερὸν κύτος· εὖ δ᾽ ἐπίβαινε", "guiding the intellectual vessel of thy heart; walk uprightly"),
    ("ἀτραπιτοῦ, μοῦνον δ᾽ ἐσόρα κόσμοιο τυπωτὴν", "in the path, and look only unto the immortal Framer"),
    ("ἀθάνατον. Παλαιὸς δὲ λόγος περὶ τοῦδε φαείνει·", "of the universe. An ancient saying shines forth concerning Him:"),
    ("εἷς ἔστ᾽, αὐτοτελής, αὐτοῦ δ᾽ ὕπο πάντα τελεῖται,", "He is One, self-complete, and by Him all things are fulfilled,"),
    ("ἐν δ᾽ αὐτοῖς αὐτὸς περινίσσεται, οὐδέ τις αὐτὸν", "and in them He Himself moves around; nor does anyone"),
    ("εἰσοράᾳ ψυχῶν θνητῶν, νῷ δ᾽ εἰσοράαται.", "of mortal souls behold Him, but He is beheld by the mind."),
    ("αὐτὸς δ᾽ ἐξ ἀγαθῶν θνητοῖς κακὸν οὐκ ἐπιτέλλει", "From goods He does not send evil unto mortal men;"),
    ("ἀνθρώποις· αὐτοῖς δὲ κ᾽ Ἔρις καὶ Μῖσος ὀπηδεῖ,", "unto them follow Strife and Hatred,"),
    ("καὶ Πόλεμος καὶ Λοιμὸς ἰδ᾽ Ἄλγεα δακρυόεντα,", "and War, and Pestilence, and tearful Sorrows,"),
    ("οὐδέ τις ἔσθ᾽ ἕτερος· τῷ κεν ῥέα πάντ᾽ ἐσορῆται.", "nor is there any other; unto Him easily all things are visible."),
    ("οὐ κεν ἴδοις αὐτόν, πρὶν δή ποτε δεῦρ᾽ ἐπὶ γαῖαν,", "Thou couldst not see Him, unless once here upon earth,"),
    ("τέκνον ἐμόν, δείξω σοι, ὁπηνίκα δέρκομαι αὐτοῦ", "my child, I show thee, whenever I behold His"),
    ("ἴχνια καὶ χεῖρα στιβαρὴν κρατεροῖο θεοῖο.", "footprints and the mighty hand of the strong God."),
    ("αὐτὸν δ᾽ οὐχ ὁρόω· περὶ γὰρ νέφος ἐστήρικται", "Himself I see not; for a cloud is set about Him,"),
    ("λεπτὸν ἐμοὶ καὶ πᾶσι δεκάπτυχον ἀνθρώποισιν·", "thin to me, but ten-folded to all men;"),
    ("οὐ γάρ κεν τις ἴδοι θνητῶν μερόπων κρείοντα,", "for none of mortal, speech-gifted men could see the Ruler,"),
    ("εἰ μὴ μουνογενής τις ἀπορρώξ, φῦλον ἄνωθεν", "unless a certain only-begotten offshoot, of the race from above,"),
    ("Χαλδαίων· ἴδρις γὰρ ἔην ἄστροιο πορείης,", "of the Chaldaeans [Abraham]; for he was skilled in the path of the stars,"),
    ("καὶ σφαίρης ἥτ᾽ ἀμφὶς ὀχήματι αἰὲν περιτέλλει,", "and the movements of the sphere that turn about,"),
    ("κυκλοτερὴς ἴση τε κατὰ σφέτερον κνώδακα·", "circular and even around their axle;"),
    ("πνεύματά δ᾽ ἡνιοχεῖ περί τ᾽ ἠέρα καὶ περὶ χεῦμα", "and He guides the winds about the air and about the flow"),
    ("νάματος· ἐκφαίνει δὲ πυρὸς σέλας ἰφιγενήτου.", "of water; and reveals the flame of mighty-born fire."),
    ("αὐτὸς δὴ μέγαν αὖθις ἐπ᾽ οὐρανὸν ἐστήρικται", "He Himself is established upon the great heaven"),
    ("χρυσείῳ ἐνὶ θρόνῳ· γαίῃ δ᾽ ὑπὸ ποσσὶ βέβηκε·", "on a golden throne; and the earth is beneath His feet;"),
    ("χεῖρα δὲ δεξιτερὴν ἐπὶ τέρμασιν Ὠκεανοῖο", "and He stretches out His right hand unto the boundaries of Ocean;"),
    ("ἐκτέτακεν· ὀρέων δὲ τρέμει βάσις ἔνδοθι θυμῷ,", "and the base of the mountains trembles within at His wrath,"),
    ("οὐδὲ φέρειν δύναται κρατερὸν μένος. ἔστι δὲ πάντῃ", "nor can it endure His mighty power. And He is wholly"),
    ("αὐτὸς ἐπουράνιος, καὶ ἐπὶ χθονὶ πάντα τελευτᾷ,", "heavenly, and fulfills all things upon earth,"),
    ("ἀρχὴν αὐτὸς ἔχων καὶ μέσσην ἠδὲ τελευτήν,", "having Himself the beginning, the middle, and the end,"),
    ("ὡς λόγος ἀρχαίων, ὡς ὑλογενὴς διέταξεν,", "as the saying of the ancients tells, as the one born from the water [Moses] ordained,"),
    ("ἐκ θεόθεν γνώμαισι λαβὼν κατὰ δίπλακα θεσμόν.", "receiving from God in decrees the two-fold law."),
    ("ἄλλως οὐ θεμιτὸν δὲ λέγειν· τρομέω δέ τε λίην", "Otherwise it is not lawful to speak; and I tremble exceedingly"),
    ("ἐν νοΐ· ἐξ ὑπάτου κραίνει περὶ πάντ᾽ ἐνὶ τάξει.", "in mind; from on high He governs all things in order."),
    ("ὦ τέκνον, σὺ δὲ τοῖσι νόοισι πελάζεο, γλώσσης", "O my child, draw near with these thoughts, holding fast"),
    ("εὖ μάλ᾽ ἐπικρατέων, στέρνοισι δὲ ἔνθεο φήμην.", "thy tongue, and lay up the report within thy breast.")
]

RECENSION_JUSTIN = [
    ("Φθέγξομαι οἷς θέμις ἐστί· θύρας δ᾽ ἐπίθεσθε βέβηλοι", "I will speak to those whom it is lawful; shut the doors, you profane"),
    ("πάντες ὁμῶς. Σὺ δ᾽ ἄκουε, φαεσφόρου ἔκγονε Μήνης,", "all together. But listen thou, son of the light-bearing Moon,"),
    ("Μουσαῖ᾽· ἐξερέω γὰρ ἀληθέα· μηδέ σε τὰ πρὶν", "Musaeus; for I will utter true things; nor let what previously"),
    ("ἐν στήθεσσι φανέντα φίλης αἰῶνος ἀμέρσῃ.", "appeared in thy breast deprive thee of beloved life."),
    ("εἰς δὲ λόγον θεῖον βλέψας τούτῳ προσέδρευε,", "Look unto the divine Word and attend upon it,"),
    ("ἰθύνων κραδίης νοερὸν κύτος· εὖ δ᾽ ἐπίβαινε", "guiding the intellectual vessel of thy heart; walk uprightly"),
    ("ἀτραπιτοῦ, μοῦνον δ᾽ ἐσόρα κόσμοιο ἄνακτα.", "in the path, and look only unto the Ruler of the universe."),
    ("Εἷς ἔστ᾽, αὐτογενής, ἑνὸς ἔκγονα πάντα τέτυκται·", "He is One, self-originated; from this One all things are fashioned;"),
    ("ἐν δ᾽ αὐτοῖς αὐτὸς περιγίγνεται, οὐδέ τις αὐτὸν", "and in them He Himself encompasses, nor does anyone"),
    ("εἰσοράᾳ θνητῶν, αὐτὸς δέ γε πάντας ὁρᾶται.", "of mortals see Him, but He sees all."),
    ("οὗτος δ᾽ ἐξ ἀγαθοῖο κακὸν θνητοῖσι δίδωσι", "He sends evil unto mortals after good,"),
    ("καὶ πόλεμον κρυόεντα καὶ ἄλγεα δακρυόεντα.", "and chilling war, and tearful sorrows."),
    ("οὐδέ τις ἔσθ᾽ ἕτερος χωρὶς μεγάλου βασιλῆος.", "Nor is there any other apart from the Great King."),
    ("αὐτὸν δ᾽ οὐχ ὁρόω· περὶ γὰρ νέφος ἐστήρικται.", "Himself I see not; for a cloud is set about Him."),
    ("πᾶσιν γὰρ θνητοῖς θνηταὶ κόραι εἰσὶν ἐν ὄσσοις,", "For in the eyes of all mortals are mortal pupils,"),
    ("ἀσθενέες δ᾽ ἰδέειν Δία τὸν πάντων μεδέοντα.", "weak to see God the Ruler of all."),
    ("οὗτος γὰρ χάλκειον ἐς οὐρανὸν ἐστήρικται", "For He is established upon the bronze heaven"),
    ("χρυσείῳ ἐνὶ θρόνῳ, γαίης δ᾽ ἐπὶ ποσσὶ βέβηκε,", "on a golden throne, and walks upon the earth with His feet,"),
    ("χεῖρά τε δεξιτερὴν ἐπὶ τέρματος Ὠκεανοῖο", "and stretches forth His right hand unto the end of Ocean"),
    ("πάντοθεν ἐκτέτακεν· περὶ γὰρ τρέμει οὔρεα μακρὰ", "on all sides; for about Him the long mountains tremble,"),
    ("καὶ ποταμοὶ πολιῆς τε βάθος χαροποῖο θαλάσσης.", "and the rivers, and the deep of the grey, fierce sea.")
]

ORPHIC_HYMN = [
    ("Αἰθέρος ἠδ᾽ Ἀΐδου, πόντου γαίης τε τύραννε,", "O Sovereign of Aether and of Hades, of sea and of earth,"),
    ("ὃς βρονταῖς ῥήσσεις βριαρὸν δόμον Οὐλύμποιο·", "who with thunderbolts breakest the mighty house of Olympus;"),
    ("ὅντινα δαίμονες οὐ φρίσσουσι, θεῶν δὲ δέδοικεν ὅμιλος,", "whom spirits dread and the company of the gods fears;"),
    ("ᾧ Μοῖραι πείθονται, ἀμείλικτοι περ ἐοῦσαι·", "whom the Fates obey, unyielding though they be;"),
    ("ἄφθιτε, μητροπάτωρ, οὗ θυμῷ πάντα δονεῖται·", "immortal, mother and father, by whose will all things are moved;"),
    ("ὃς κινεῖς ἀνέμους, νεφέλῃσι δὲ πάντα καλύπτεις,", "who stirrest the winds, and veilest all things in clouds,"),
    ("πρηστῆρα σχίζων πλατὺν αἰθέρα· σὴ μὲν ἐν ἄστροις", "cleaving the broad aether with tempest; Thy station"),
    ("τάξις, ἀναλλοίτοισιν ἐφημοσύναισι τρέχουσα·", "is among the stars, running in unchangeable courses;"),
    ("σῷ δὲ θρόνῳ πυρόεντι παρεστᾶσιν πολύμοχθοι", "and beside Thy fiery throne stand the toiling"),
    ("ἄγγελοι, οἷσι μέμηλε βροτοῖς ὡς πάντα τελεῖται.", "angels, whose care is that all things are accomplished for mortals.")
]

def build_grammateus_xml():
    bib = "Otto Kern, Orphicorum Fragmenta (Berlin: Weidmann, 1922), fr. 245-248; Albert-Marie Denis, Fragmenta Pseudepigraphorum quae supersunt Graeca (PVTG 3; Leiden: Brill, 1970), pp. 163-174. CAVT 183 / CANT 33."
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="PsOrph" title="Testament of Orpheus (Hieroi Logoi)">',
        '  <version author="Kern 1922" language="Greek" title="Greek and English">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Kern" language="Greek" show="yes">',
        '        <name>Kern 1922 (Orphicorum Fragmenta)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Trans" language="English" show="yes">',
        '        <name>English Translation (OCP)</name>',
        f'        <bibliography>{bib}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>'
    ]
    chapters = [
        (1, RECENSION_ARISTOBULUS),
        (2, RECENSION_JUSTIN),
        (3, ORPHIC_HYMN)
    ]
    unit_id = 0
    for c_num, rec in chapters:
        lines.append(f'      <div number="{c_num}">')
        for v_num, (grc, en) in enumerate(rec, 1):
            clean_grc = grc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            clean_en = en.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'        <div number="{v_num}">')
            lines.append(f'          <unit id="{unit_id}">')
            lines.append(f'            <reading option="0" mss="Kern ">{clean_grc}</reading>')
            lines.append(f'            <reading option="1" mss="Trans ">{clean_en}</reading>')
            lines.append('          </unit>')
            lines.append('        </div>')
            unit_id += 1
        lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>\n')
    
    out_path = 'static/docs/PsOrph.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path} ({unit_id} units)')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Testament of Orpheus (Hieroi Logoi / Diathekai)</title>',
        '        <author>Pseudo-Orpheus</author>',
        '        <editor>Otto Kern</editor>',
        '        <respStmt>',
        '          <resp>TEI P5 Parallel Segmentation edition for Online Critical Pseudepigrapha</resp>',
        '          <name>Ken M. Penner</name>',
        '        </respStmt>',
        '      </titleStmt>',
        '      <publicationStmt>',
        '        <publisher>Online Critical Pseudepigrapha</publisher>',
        '        <pubPlace>St. Francis Xavier University, Antigonish, NS</pubPlace>',
        '        <availability>',
        '          <licence target="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</licence>',
        '        </availability>',
        '      </publicationStmt>',
        '      <sourceDesc>',
        '        <biblStruct type="book">',
        '          <monogr>',
        '            <title level="m">Orphicorum Fragmenta</title>',
        '            <editor>Otto Kern</editor>',
        '            <imprint>',
        '              <publisher>Weidmann</publisher>',
        '              <pubPlace>Berolini</pubPlace>',
        '              <date when="1922">1922</date>',
        '              <biblScope unit="page">255-266</biblScope>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>',
        '      <div type="recension" n="1" subtype="Aristobuliana">'
    ]
    for v_num, (grc, en) in enumerate(RECENSION_ARISTOBULUS, 1):
        lines.append(f'        <l n="{v_num}">')
        lines.append(f'          <app>')
        lines.append(f'            <rdg wit="#Kern1922" xml:lang="grc">{grc}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
        lines.append(f'          </app>')
        lines.append(f'        </l>')
    lines.append('      </div>')
    
    lines.append('      <div type="recension" n="2" subtype="Iustiniana">')
    for v_num, (grc, en) in enumerate(RECENSION_JUSTIN, 1):
        lines.append(f'        <l n="{v_num}">')
        lines.append(f'          <app>')
        lines.append(f'            <rdg wit="#Kern1922" xml:lang="grc">{grc}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
        lines.append(f'          </app>')
        lines.append(f'        </l>')
    lines.append('      </div>')

    lines.append('      <div type="hymn" n="3" subtype="HymnusInDeum">')
    for v_num, (grc, en) in enumerate(ORPHIC_HYMN, 1):
        lines.append(f'        <l n="{v_num}">')
        lines.append(f'          <app>')
        lines.append(f'            <rdg wit="#Kern1922" xml:lang="grc">{grc}</rdg>')
        lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
        lines.append(f'          </app>')
        lines.append(f'        </l>')
    lines.append('      </div>')

    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')
    
    out_path = 'static/docs/tei/PsOrph.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
