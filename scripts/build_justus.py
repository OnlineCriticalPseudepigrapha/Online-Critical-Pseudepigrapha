#!/usr/bin/env python3
"""
Build Justus of Tiberias (FGrH 734 / FHJA 1.371-389 / Denis Introduction 267)
Testimonia and Fragments:
  - Frag. 1: Photius, Bibliotheca Codex 33 (Review of Justus's Chronicle of the Jewish Kings)
  - Frag. 2: Diogenes Laertius, Vitae Philosophorum 2.41 (The Trial of Socrates / Plato on the Bema)
  - Frag. 3: Flavius Josephus, Vita 340 (Direct apostrophe on the cause of the war in Galilee)
  - Frag. 4: Flavius Josephus, Vita 357-360 (Critique of Justus's historical reliability and absence from battles)

Outputs:
  - static/docs/Justus.xml (Grammateus DTD)
  - static/docs/tei/Justus.xml (TEI P5 parallel segmentation)
"""

import os

FRAGMENTS = [
    {
        "num": 1,
        "title": "Fragmentum 1: De Iudaeorum regibus in stemmatibus (apud Photium, Bibliotheca cod. 33)",
        "verses": [
            (
                "Ἀνεγνώσθη Ἰούστου Τιβεριέως χρονικόν, οὗ ἡ ἐπιγραφὴ «Ἰούστου Τιβεριέως Ἰουδαίων βασιλέων τῶν ἐν τοῖς στέμμασιν». Οὗτος ἀπὸ πόλεως τῆς ἐν Γαλιλαίᾳ Τιβεριάδος ὡρμᾶτο.",
                "There was read the chronicle of Justus of Tiberias, entitled 'A Chronicle of the Kings of the Jews in the Form of a Genealogy, by Justus of Tiberias.' He came from the city of Tiberias in Galilee."
            ),
            (
                "Ἄρχεται δὲ τῆς ἱστορίας ἀπὸ Μωϋσέως, καταλήγει δὲ ἕως τελευτῆς Ἀγρίππα τοῦ ἑβδόμου μὲν τῶν ἀπὸ τῆς οἰκίας Ἡρῴδου, ὑστάτου δὲ ἐν τοῖς Ἰουδαίας βασιλεῦσιν, ὃς παρέλαβε μὲν τὴν ἀρχὴν ἐπὶ Κλαυδίου, ηὐξήθη δὲ ἐπὶ Νέρωνος καὶ ἔτι μᾶλλον ὑπὸ Οὐεσπασιανοῦ, τελευτᾷ δὲ ἔτει τρίτῳ Τραϊανοῦ, οὗ καὶ ἡ ἱστορία κατέληξεν.",
                "He begins his history with Moses and concludes with the death of Agrippa, the seventh of the house of Herod and the last of the kings of Judaea, who received his realm under Claudius, was augmented under Nero and still more by Vespasian, and died in the third year of Trajan, where the history also ended."
            ),
            (
                "Ἔστι δὲ τὴν φράσιν συντομώτατός τε καὶ τὰ πλεῖστα τῶν ἀναγκαιοτάτων παρατρέχων· καὶ τῷ κοινῷ νοσήματι τῆς τῶν Ἰουδαίων προλήψεως, ὧν καὶ αὐτὸς τῷ γένει ὑπῆρχε, περιπεσών, οὐδὲ τῆς παρουσίας τοῦ Χριστοῦ ἢ τῶν κατ’ αὐτὸν συμβάντων ἢ τῶν ὑπ’ αὐτοῦ ἐπιτελεσθέντων θαυμάτων τὴν παραμικρὰν μνήμην ἐποιήσατο.",
                "In his phrasing he is extremely concise, and bypasses most of the essential events; and having fallen victim to the common affliction of Jewish prejudice (since he was himself of that race), he made not the slightest mention of the appearance of Christ, of the events concerning him, or of the miracles performed by him."
            )
        ]
    },
    {
        "num": 2,
        "title": "Fragmentum 2: De Platone in iudicio Socratis (apud Diogenem Laertium, Vitae Philosophorum 2.41)",
        "verses": [
            (
                "Κρινομένου δ’ αὐτοῦ φησιν Ἰοῦστος ὁ Τιβεριεὺς ἐν τῷ Στέμματι Πλάτωνα ἀναβῆναι ἐπὶ τὸ βῆμα καὶ εἰπεῖν· «Νεώτατος ὤν, ὦ ἄνδρες Ἀθηναῖοι, τῶν ἐπὶ τὸ βῆμα ἀναβάντων»· τοὺς δὲ δικαστὰς ἐκβοῆσαι· «Κατάβα, κατάβα» [τουτέστι κατάβηθι].",
                "When Socrates was on trial, Justus of Tiberias in his book entitled The Wreath says that Plato mounted the speaker's platform and said: 'Though I am the youngest, men of Athens, of all who ever rose to address you'—whereupon the judges shouted out: 'Get down! Get down!' [that is, descend from the platform]."
            )
        ]
    },
    {
        "num": 3,
        "title": "Fragmentum 3: De origine seditionis Galilaeorum (apud Flavium Josephum, Vita 340)",
        "verses": [
            (
                "Πῶς οὖν, ἵνα φῶ πρὸς αὐτὸν ὡς παρόντα, Ἰοῦστε δεινότατε συγγραφέων, τοῦτο γὰρ αὐχεῖς περὶ σεαυτοῦ, αἴτιοι γεγόναμεν ἐγώ τε καὶ Γαλιλαῖοι τῇ πατρίδι σου τῆς πρὸς Ῥωμαίους καὶ πρὸς τὸν βασιλέα στάσεως;",
                "How then, that I may speak to him as if he were present, O Justus, most clever of writers (for this you boast concerning yourself), did I and the Galileans become the cause of your native city's rebellion against the Romans and against the king?"
            )
        ]
    },
    {
        "num": 4,
        "title": "Fragmentum 4: De absentia et fide historica Justi (apud Flavium Josephum, Vita 357-360)",
        "verses": [
            (
                "Οὔτε γὰρ κατὰ τὴν Γαλιλαίαν ἦσθα, ὅτε συνέβαινεν τὰ δεινά, οὔτε Ἰωταπάτων τινὸς πολιορκίας ἀνέσχου, οὔτε περὶ τὴν Ἱεροσολύμων ἦσθα μάχην ἢ πόνον.",
                "For you were not in Galilee when these dreadful things were happening, nor did you endure any part of the siege of Jotapata, nor were you present at the battle or hardships in Jerusalem."
            ),
            (
                "Πῶς οὖν θαρρήσας ἔλεγες ὡς ἀκριβέστερον πάντων συγγεγραφὼς τὰ πραχθέντα, μηδὲ τοῖς γενομένοις παρατυχὼν μήτε τοὺς ἄλλους τοὺς εἰδότας ἐξετάσας;",
                "How then did you dare to say that you have written what took place more accurately than anyone else, when you neither witnessed what occurred nor questioned others who were eyewitnesses?"
            )
        ]
    }
]

def make_grammateus_xml():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Justus.xml" title="Justus of Tiberias">',
        '  <version id="Greek" title="Greek Text (FGrH 734 / Holladay FHJA 1)" lang="grc">',
        '    <divisions>',
        '      <division id="1" title="Fragments" type="fragment"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <manuscript id="Phot" name="Photius Bibliotheca Cod. 33"/>',
        '      <manuscript id="Diog" name="Diogenes Laertius"/>',
        '      <manuscript id="Jos" name="Flavius Josephus Vita"/>',
        '    </manuscripts>',
        '    <text>'
    ]
    
    for frag in FRAGMENTS:
        fnum = frag["num"]
        lines.append(f'      <div number="{fnum}">')
        for vidx, (grk, _) in enumerate(frag["verses"], 1):
            uid = f"{fnum}.{vidx}"
            escaped_grk = grk.replace('&', '&amp;')
            lines.append(f'        <unit id="{uid}">')
            lines.append(f'          <reading option="base" mss="Phot">{escaped_grk}</reading>')
            lines.append('        </unit>')
        lines.append('      </div>')
        
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('  <version id="English" title="English Translation" lang="eng">')
    lines.append('    <divisions>')
    lines.append('      <division id="1" title="Fragments" type="fragment"/>')
    lines.append('    </divisions>')
    lines.append('    <manuscripts>')
    lines.append('      <manuscript id="Eng" name="English Translation"/>')
    lines.append('    </manuscripts>')
    lines.append('    <text>')
    
    for frag in FRAGMENTS:
        fnum = frag["num"]
        lines.append(f'      <div number="{fnum}">')
        for vidx, (_, eng) in enumerate(frag["verses"], 1):
            uid = f"{fnum}.{vidx}"
            escaped_eng = eng.replace('&', '&amp;')
            lines.append(f'        <unit id="{uid}">')
            lines.append(f'          <reading option="base" mss="Eng">{escaped_eng}</reading>')
            lines.append('        </unit>')
        lines.append('      </div>')
        
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>')
    
    return '\n'.join(lines) + '\n'

def main():
    xml_content = make_grammateus_xml()
    out_xml = 'static/docs/Justus.xml'
    with open(out_xml, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote Grammateus XML: {out_xml} (4 fragments, {sum(len(f['verses']) for f in FRAGMENTS)} units)")
    
    out_tei = 'static/docs/tei/Justus.xml'
    ret = os.system(f"python3 scripts/grammateus_to_tei.py {out_xml} -o {out_tei}")
    if ret == 0:
        print(f"Wrote TEI P5 XML: {out_tei}")
    else:
        print(f"Error converting to TEI P5: {ret}")

if __name__ == '__main__':
    main()
