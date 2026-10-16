#!/usr/bin/env python3
"""
Build Demetrius the Chronographer (FGrH 722 / FHJA 1.51-91 / Denis FPG 175-179)
De Iudaeis / De Regibus Iudaeae:
  - Frag. 1: PE 9.19.4 (Sacrifice of Isaac / Aqedah)
  - Frag. 2: PE 9.21.1-19 (Chronology of Jacob, Patriarchs, and Levi to Moses)
  - Frag. 3: PE 9.29.1-3 (Genealogy of Moses and Zipporah)
  - Frag. 4: PE 9.29.15 (The Waters of Marah and Elim)
  - Frag. 5: PE 9.29.16 (Israelite Weapons at the Red Sea)
  - Frag. 6: Clement of Alexandria, Stromateis 1.21.141.1-2 (Chronology to Ptolemy IV)

Outputs:
  - static/docs/Demetr.xml (Grammateus DTD)
  - static/docs/tei/Demetr.xml (TEI P5 parallel segmentation)
"""

import os
import re

FRAGMENTS = [
    {
        "num": 1,
        "title": "Fragmentum 1: De immolatione Isaac (apud Eusebium, Praep. Evang. 9.19.4)",
        "verses": [
            (
                "Μετ’ οὐ πολὺν δὲ χρόνον τὸν θεὸν τῷ Ἀβραὰμ προστάξαι Ἰσαὰκ τὸν υἱὸν ὁλοκαρπῶσαι αὐτῷ. τὸν δὲ ἀναγαγόντα τὸν παῖδα ἐπὶ τὸ ὄρος πυρὰν νῆσαι καὶ ἐπιθεῖναι τὸν Ἰσαάκ· σφάζειν δὲ μέλλοντα κωλυθῆναι ὑπὸ ἀγγέλου, κριὸν αὐτῷ πρὸς τὴν κάρπωσιν παραστήσαντος· τὸν δὲ Ἀβραὰμ τὸν μὲν παῖδα καθελεῖν ἀπὸ τῆς πυρᾶς, τὸν δὲ κριὸν καρπῶσαι.",
                "Not long afterward, God commanded Abraham to offer his son Isaac as a whole burnt offering to him. And he, having led the lad up onto the mountain, built a pyre and placed Isaac upon it; but when he was about to slay him, he was restrained by an angel, who provided a ram for him to sacrifice. And Abraham took down the lad from the pyre, and offered the ram as a sacrifice."
            )
        ]
    },
    {
        "num": 2,
        "title": "Fragmentum 2: De chronologia et progenie Iacob (apud Eusebium, Praep. Evang. 9.21.1-19)",
        "verses": [
            (
                "Δημήτριός φησι τὸν Ἰακὼβ γενόμενον ἐτῶν ἑβδομήκοντα πέντε φυγεῖν εἰς Χαρρὰν τῆς Μεσοποταμίας, ἀποσταλέντα ὑπὸ τῶν γονέων διὰ τὴν πρὸς τὸν ἀδελφὸν Ἠσαῦ κρυφίαν ἔχθραν, διὰ τὸ εὐλογῆσαι αὐτὸν τὸν πατέρα δοκοῦντα εἶναι τὸν Ἠσαῦ, καὶ ὅπως λάβῃ ἐκεῖθεν γυναῖκα.",
                "Demetrius says that Jacob, when he was seventy-five years old, fled to Haran in Mesopotamia, sent away by his parents on account of the secret hatred of his brother Esau, because their father had blessed him supposing him to be Esau, and so that he might take a wife from there."
            ),
            (
                "ἀφορμῆσαι οὖν τὸν Ἰακὼβ εἰς Χαρρὰν τῆς Μεσοποταμίας, τὸν μὲν πατέρα καταλιπόντα Ἰσαὰκ ἐτῶν ἑκατὸν τριάκοντα ἑπτά, αὐτὸν δὲ ὄντα ἐτῶν ἑβδομήκοντα ἑπτά.",
                "Jacob therefore set out for Haran in Mesopotamia, having left his father Isaac when Isaac was a hundred and thirty-seven years old, while he himself was seventy-seven years old."
            ),
            (
                "διατρίψαντα οὖν αὐτὸν ἐκεῖ ἑπτὰ ἔτη λαβεῖν τοῦ μητρῴου δύο θυγατέρας γῆμαι, Λείαν καὶ Ῥαχήλ, ὄντα ἐτῶν ὀγδοήκοντα τεσσάρων· καὶ γενέσθαι ἐν ἑπτὰ ἔτεσιν ἄλλοις αὐτῷ παιδία ιβʹ· ὀγδόῳ μὲν ἔτει μηνὶ δεκάτῳ Ῥουβήν· καὶ τῷ ἔτει δὲ τῷ ἐνάτῳ μηνὶ ὀγδόῳ Συμεών· καὶ τῷ ἔτει δὲ τῷ δεκάτῳ μηνὶ ἕκτῳ Λευίν· τῷ δὲ ἑνδεκάτῳ ἔτει μηνὶ τετάρτῳ Ἰούδαν. Ῥαχήλ τε μὴ τίκτουσαν ζηλῶσαι τὴν ἀδελφήν, καὶ παρακοιμίσαι τῷ Ἰακὼβ τὴν ἑαυτῆς παιδίσκην Βάλλαν, τῷ αὐτῷ χρόνῳ ᾧ καὶ Λείαν συλλαβεῖν τὸν Νεφθαλείμ, τῷ ἑνδεκάτῳ ἔτει μηνὶ πέμπτῳ, καὶ τεκεῖν τῷ δωδεκάτῳ ἔτει μηνὶ δευτέρῳ υἱόν, ὃν ὑπὸ Ῥαχὴλ Δὰν ὀνομασθῆναι· καὶ ἐκ τῆς αὐτῆς τοῦ αὐτοῦ ἔτους καὶ μηνὸς δωδεκάτου ἕτερον τεκεῖν, ὃν καὶ αὐτὸν προσαγορευθῆναι ὑπὸ Ῥαχὴλ Νεφθαλείμ.",
                "Having spent seven years there, he married two daughters of his mother's brother, Leah and Rachel, being eighty-four years old; and in seven more years twelve children were born to him: in the eighth year, in the tenth month, Reuben; and in the ninth year, in the eighth month, Simeon; and in the tenth year, in the sixth month, Levi; and in the eleventh year, in the fourth month, Judah. And since Rachel did not bear children, she was jealous of her sister, and gave her maidservant Bilhah to lie with Jacob, at the same time that Leah conceived, in the eleventh year, in the fifth month, and bore a son in the twelfth year, in the second month, who was named Dan by Rachel; and from the same maidservant in the same year and the twelfth month she bore another son, whom Rachel named Naphtali."
            ),
            (
                "καὶ Λείαν πάλιν ἀντὶ τῶν μήλων τοῦ μανδραγόρου, ἃ Ῥουβὴν εἰσενεγκεῖν παρὰ Ῥαχήλ, συλλαβεῖν ἐν γαστρί, καὶ τῷ αὐτῷ χρόνῳ τὴν παιδίσκην αὐτῆς Ζελφάν, τῷ δωδεκάτῳ ἔτει μηνὶ τρίτῳ, καὶ τεκεῖν τοῦ αὐτοῦ ἔτους μηνὸς δωδεκάτου υἱόν, καὶ ὄνομα αὐτῷ θέσθαι Ἰσσαχάρ.",
                "And Leah again, in return for the mandrake apples which Reuben brought in to Rachel, conceived in her womb, and at the same time her maidservant Zilpah, in the twelfth year, in the third month, and bore a son in the twelfth month of the same year, and gave him the name Issachar."
            ),
            (
                "καὶ πάλιν Λείαν τῷ τρισκαιδεκάτῳ ἔτει μηνὶ δεκάτῳ υἱὸν ἄλλον τεκεῖν, ᾧ ὄνομα Ζαβουλών, καὶ τὴν αὐτὴν τῷ τεσσαρεσκαιδεκάτῳ ἔτει μηνὶ ὀγδόῳ θυγατέρα Δεῖναν τεκεῖν. Ῥαχὴλ δὲ συλλαβοῦσαν γεννῆσαι Ἰωσὴφ τῷ τεσσαρεσκαιδεκάτῳ ἔτει καὶ αὐτὴν μηνὶ ὀγδόῳ, ὥστε γενέσθαι ἐν τοῖς ἑπτὰ ἔτεσι τοῖς παρὰ Λάβαν παιδία ιβʹ.",
                "And Leah again in the thirteenth year, in the tenth month, bore another son, whose name was Zebulun, and the same Leah in the fourteenth year, in the eighth month, bore a daughter Dinah. And Rachel, having conceived, herself also bore Joseph in the fourteenth year, in the eighth month, so that in the seven years with Laban twelve children were born."
            ),
            (
                "θέλοντα δὲ τὸν Ἰακὼβ πρὸς τὸν πατέρα εἰς Χαναὰν ἀπιέναι, ἀξιωθέντα ὑπὸ Λάβαν ἄλλα ἔτη ἓξ μεῖναι, ὥστε τὰ πάντα αὐτὸν μεῖναι ἔτη εἴκοσι.",
                "And when Jacob wished to depart to his father in Canaan, he was requested by Laban to remain another six years, so that in all he remained twenty years."
            ),
            (
                "πορευομένῳ δὲ αὐτῷ εἰς Χαναὰν ἄγγελον τοῦ θεοῦ παλαῖσαι, καὶ ἅψασθαι τοῦ πλάτους τοῦ μηροῦ τοῦ Ἰακώβ, τὸν δὲ ναρκήσαντα χωλεῦσαι· ὅθεν τὸν μὲν ἄγγελον εἰπεῖν αὐτῷ μὴ καλεῖσθαι αὐτὸν ἔτι Ἰακώβ, ἀλλʼ Ἰσραήλ.",
                "And as he was traveling to Canaan, an angel of God wrestled with him, and touched the hollow of Jacob's thigh, and he, growing numb, became lame; wherefore the angel told him that he should no longer be called Jacob, but Israel."
            ),
            (
                "καὶ ἐλθεῖν αὐτὸν τῆς Χαναὰν γῆς εἰς ἑτέραν πόλιν Σικίμων, ἔχοντα παιδία Ῥουβὴν ἐτῶν ιβʹ μηνῶν δυοῖν, Συμεῶνα ἐτῶν ιαʹ μηνῶν τεσσάρων, Λευὶν ἐτῶν ιʹ μηνῶν ἕξ, Ἰούδαν ἐτῶν θʹ μηνῶν ὀκτώ, Νεφθαλείμ ἐτῶν ηʹ μηνῶν ὀκτώ, Γὰδ ἐτῶν ηʹ μηνῶν ιʹ, Ἀσὴρ ἐτῶν ηʹ, Ἰσσαχὰρ ἐτῶν ζʹ, Ζαβουλὼν ἐτῶν ϛʹ μηνῶν ἕξ, Δεῖναν ἐτῶν ϛʹ μηνῶν ἕξ, Ἰωσὴφ ἐτῶν ϛʹ μηνῶν ἕξ.",
                "And he came into the land of Canaan to another city of Shechem, having children: Reuben twelve years and two months old, Simeon eleven years and four months, Levi ten years and six months, Judah nine years and eight months, Naphtali eight years and eight months, Gad eight years and ten months, Asher eight years, Issachar seven years, Zebulun six years and six months, Dinah six years and six months, Joseph six years and six months."
            ),
            (
                "παροικῆσαι δὲ Ἰσραὴλ παρὰ Ἑμμὼρ ἔτη δέκα, καὶ φθαρῆναι τὴν Ἰσραὴλ θυγατέρα Δεῖναν ὑπὸ Συχὲμ τοῦ Ἑμμὼρ υἱοῦ, ἐτῶν οὖσαν δεκαὲξ μηνῶν τεσσάρων. ἐξαλλομένους δὲ τοὺς Ἰσραὴλ υἱούς, Συμεῶνα μὲν ὄντα ἐτῶν εἴκοσι ἑνὸς μηνῶν τεσσάρων, Λευὶν δὲ ἐτῶν εἴκοσι μηνῶν ἕξ, ἀποκτεῖναι τόν τε Ἑμμὼρ καὶ Συχὲμ τὸν υἱὸν αὐτοῦ καὶ πάντας τοὺς ἄρσενας διὰ τὴν Δεῖνας φθοράν· Ἰακὼβ δὲ τότε εἶναι ἐτῶν ἑκατὸν ἑπτά.",
                "And Israel dwelt as an alien near Hamor for ten years, and Israel's daughter Dinah was violated by Shechem the son of Hamor, when she was sixteen years and four months old. And the sons of Israel leaping upon them, Simeon being twenty-one years and four months old, and Levi twenty years and six months, slew both Hamor and Shechem his son and all the males on account of the violation of Dinah; and Jacob was then one hundred and seven years old."
            ),
            (
                "ἐλθόντα δ’ οὖν αὐτὸν εἰς Λουζὰ τῆς Βαιθήλ, φάναι τὸν θεὸν μηκέτι Ἰακώβ, ἀλλ’ Ἰσραὴλ ὀνομάζεσθαι. ἐκεῖθεν δὲ ἐλθεῖν εἰς Χαφραθά, ἔνθεν παραγενέσθαι εἰς Ἐφραθά, ἣν εἶναι Βηθλεέμ, καὶ γεννῆσαι αὐτὸν ἐκεῖ Βενιαμίν, καὶ τελευτῆσαι Ῥαχήλ, τεκοῦσαν τὸν Βενιαμίν, συμβιῶσαι δ’ αὐτῇ τὸν Ἰακὼβ ἔτη εἴκοσι τρία.",
                "Having then come to Luz of Bethel, God told him that he was no longer to be called Jacob, but Israel. And from there he came to Kaphrah, and thence arrived at Ephrathah, which is Bethlehem, and there he begat Benjamin, and Rachel died having given birth to Benjamin, Jacob having lived with her twenty-three years."
            ),
            (
                "αὐτόθεν δὲ ἐλθεῖν τὸν Ἰακὼβ εἰς Μαμβρὶ τῆς Χεβρὼν πρὸς Ἰσαὰκ τὸν πατέρα. εἶναι δὲ τότε Ἰωσὴφ ἐτῶν δεκαεπτά, καὶ πραθῆναι αὐτὸν εἰς Αἴγυπτον, καὶ ἐν τῷ δεσμωτηρίῳ μεῖναι ἔτη δεκατρία, ὥστ’ εἶναι αὐτὸν ἐτῶν τριάκοντα, Ἰακὼβ δὲ ἐτῶν ἑκατὸν δέκα, ἐν ᾧ καὶ τελευτῆσαι τὸν Ἰσαὰκ ἔτει ἑνὶ ἔμπροσθεν, ἐτῶν ὄντα ἑκατὸν ὀγδοήκοντα.",
                "And from there Jacob came to Mamre of Hebron to his father Isaac. Joseph was then seventeen years old, and he was sold into Egypt, and remained in prison thirteen years, so that he was thirty years old, and Jacob was one hundred and ten years old, in which time Isaac also died one year before, being one hundred and eighty years old."
            ),
            (
                "κρίναντα δὲ τῷ βασιλεῖ τὸν Ἰωσὴφ τὰ ἐνύπνια ἄρξαι Αἰγύπτου ἔτη ἑπτά, ἐν οἷς καὶ συνοικῆσαι Ἀσενέθ, Πεντεφρῆ τοῦ Ἡλιουπόλεως ἱερέως θυγατρί, καὶ γεννῆσαι Μανασσῆν καὶ Ἐφραΐμ· καὶ τοῦ λιμοῦ ἐπιγενέσθαι ἔτη βʹ.",
                "And Joseph, having interpreted the dreams for the king, ruled Egypt seven years, in which he also married Aseneth, daughter of Potiphera the priest of Heliopolis, and begat Manasseh and Ephraim; and two years of the famine ensued."
            ),
            (
                "τὸν δὲ Ἰωσὴφ ἔτη ἐννέα εὐτυχήσαντα πρὸς τὸν πατέρα μὴ πέμψαι, διὰ τὸ ποιμένα αὐτόν τε καὶ τοὺς ἀδελφοὺς εἶναι· ἐπονείδιστον δὲ Αἰγυπτίοις εἶναι τὸ ποιμαίνειν· ὅτι δὲ διὰ τοῦτο οὐκ ἔπεμψεν αὐτὸν δεδηλωκέναι. ἐλθόντων γὰρ αὐτοῦ τῶν συγγενῶν φάναι αὐτοῖς, ἐὰν κληθῶσιν ὑπὸ τοῦ βασιλέως καὶ ἐρωτῶνται τί διαπράσσονται, λέγειν κτηνοτρόφους αὐτοὺς εἶναι.",
                "And Joseph, though enjoying prosperity for nine years, did not send for his father, because both he and his brothers were shepherds; and to the Egyptians being a shepherd was an abomination; and that he made it clear that on this account he did not send. For when his relatives came, he told them, if they should be called by the king and asked what they did, to say that they were keepers of cattle."
            ),
            (
                "διαπορεῖσθαι δὲ διὰ τί ποτε ὁ Ἰωσὴφ Βενιαμὶν ἐπὶ τοῦ ἀρίστου πενταπλασίονα μερίδα ἔδωκε, μὴ δυναμένου αὐτοῦ τοσαῦτα καταναλῶσαι κρέα. τοῦτο οὖν αὐτὸν πεποιηκέναι διὰ τὸ ἐκ τῆς Λείας τῷ πατρὶ αὐτοῦ γεγονέναι υἱοὺς ἑπτά, ἐκ Ῥαχὴλ δὲ τῆς μητρὸς αὐτοῦ δύο· διὰ τοῦτο τῷ Βενιαμὶν πέντε μερίδας παραθεῖναι, καὶ αὐτὸν λαβεῖν δύο· γενέσθαι οὖν ἑπτά, ὅσας καὶ τοὺς ἐκ τῆς Λείας υἱοὺς λαβεῖν.",
                "And the problem is raised why ever Joseph at the dinner gave Benjamin a fivefold portion, when he could not consume so much meat. He did this, therefore, because by Leah his father had seven sons, but by Rachel his mother two; therefore he set five portions before Benjamin, and took two himself; so they became seven, as many as the sons of Leah received."
            ),
            (
                "ὡσαύτως δὲ καὶ ἐπὶ τοῦ τὰς στολὰς δοῦναι ἑκάστῳ διπλᾶς, τῷ δὲ Βενιαμὶν πέντε καὶ τριακοσίους χρυσοῦς καὶ τῷ πατρὶ δὲ ἀποστεῖλαι κατὰ ταὐτά, ὥστε τὸν οἶκον αὐτοῦ τῆς μητρὸς εἶναι ἴσον.",
                "Likewise also with respect to giving each a double change of clothing, but to Benjamin five changes and three hundred pieces of gold, and sending to his father in the same way, so that his mother's house might be equal."
            ),
            (
                "οἰκῆσαι δὲ αὐτοὺς ἐν γῇ Χαναάν, ἀφ’ οὗ ἐκλεγῆναι Ἀβραὰμ ἐκ τῶν ἐθνῶν καὶ μετελθεῖν εἰς Χαναάν, Ἀβραὰμ ἐτῶν εἴκοσι πέντε, Ἰσαὰκ ἐτῶν ἑξήκοντα, Ἰακὼβ ἐτῶν ἑκατὸν τριάκοντα, γίνεσθαι τὰ πάντα ἔτη ἐν γῇ Χαναὰν σιεʹ.",
                "And they dwelt in the land of Canaan, from the time Abraham was chosen from the nations and moved to Canaan: Abraham twenty-five years, Isaac sixty years, Jacob one hundred and thirty years, making in all two hundred and fifteen years in the land of Canaan."
            ),
            (
                "καὶ τῷ τρίτῳ ἔτει λιμοῦ οὔσης ἐν Αἰγύπτῳ ἐλθεῖν εἰς Αἴγυπτον τὸν Ἰακώβ, ὄντα ἐτῶν ἑκατὸν τριάκοντα, Ῥουβὴν ἐτῶν μεʹ, Συμεῶνα ἐτῶν μδʹ, Λευὶν ἐτῶν μγʹ, Ἰούδαν ἐτῶν μβʹ μηνῶν τριῶν, Ἀσὴρ ἐτῶν μʹ μηνῶν ὀκτώ, Νεφθαλείμ ἐτῶν μαʹ μηνῶν ϛʹ, Γὰδ ἐτῶν μαʹ μηνῶν γʹ, Ζαβουλὼν ἐτῶν μʹ, Δεῖναν ἐτῶν λθʹ, Βενιαμὶν ἐτῶν κηʹ.",
                "And in the third year of the famine in Egypt Jacob came into Egypt, being one hundred and thirty years old: Reuben forty-five years old, Simeon forty-four, Levi forty-three, Judah forty-two years and three months, Asher forty years and eight months, Naphtali forty-one years and six months, Gad forty-one years and three months, Zebulun forty, Dinah thirty-nine, Benjamin twenty-eight."
            ),
            (
                "τὸν δὲ Ἰωσήφ φησι γενέσθαι ἐν Αἰγύπτῳ ἔτη λθʹ. εἶναι δὲ ἀπὸ τοῦ Ἀδὰμ ἕως τοῦ εἰσελθεῖν εἰς Αἴγυπτον τοὺς τοῦ Ἰωσὴφ συγγενεῖς ἔτη γχκδʹ. ἀπὸ δὲ τοῦ κατακλυσμοῦ ἕως τῆς Ἰακὼβ παρουσίας εἰς Αἴγυπτον ἔτη ασλεʹ· ἀφ’ οὗ δὲ ἐκλεγῆναι Ἀβραὰμ ἐκ τῶν ἐθνῶν καὶ ἐλθεῖν ἐκ Χαρρὰν εἰς Χαναὰν ἕως εἰς Αἴγυπτον τοὺς περὶ Ἰακὼβ ἐλθεῖν ἔτη σιεʹ.",
                "And he says that Joseph was in Egypt thirty-nine years. And from Adam until the relatives of Joseph entered into Egypt there were 3,624 years; and from the flood until the arrival of Jacob in Egypt 1,365 years; and from the time Abraham was chosen from the nations and came from Haran into Canaan until Jacob and his family entered into Egypt, 215 years."
            ),
            (
                "Ἰακὼβ δὲ ἐκ Χαρρὰν πρὸς Λάβαν ἐλθεῖν, ἐτῶν ὄντα πʹ, καὶ γεννῆσαι Λευίν· Λευὶν δὲ ἐν Αἰγύπτῳ ἐπιγενέσθαι ἔτη ιζʹ, ἀφ’ οὗ ἐκ Χαναὰν αὐτὸν ἐλθεῖν εἰς Αἴγυπτον, ὥστε εἶναι αὐτὸν ἐτῶν ξʹ, καὶ γεννῆσαι Κλάθ· τῷ αὐτῷ δὲ ἔτει ᾧ γενέσθαι Κλάθ, τελευτῆσαι Ἰακὼβ ἐν Αἰγύπτῳ, εὐλογήσαντα τοὺς Ἰωσὴφ υἱούς, ὄντα ἐτῶν ρμζʹ, καταλιπόντα Ἰωσὴφ ἐτῶν νϛʹ. Λευὶν δὲ γενόμενον ἐτῶν ρλζʹ τελευτῆσαι, Κλὰθ δὲ ὄντα ἐτῶν μʹ γεννῆσαι Ἀμράμ, ὃν ἐτῶν εἶναι ιδʹ ἐν ᾧ τελευτῆσαι Ἰωσὴφ ἐν Αἰγύπτῳ ὄντα ριʹ ἐτῶν· Κλὰθ δὲ γενόμενον ἐτῶν ἑκατὸν λγʹ τελευτῆσαι. Ἀμρὰμ λαβεῖν γυναῖκα τὴν τοῦ θείου θυγατέρα Ἰωχαβέδ, καὶ ὄντα ἐνιαυτῶν οεʹ γεννῆσαι Ἀαρὼν καὶ Μωσῆν· γεννῆσαι δὲ Μωσῆν τὸν Ἀμρὰμ ὄντα ἐτῶν οηʹ, καὶ γενόμενον Ἀμρὰμ ἐτῶν ρλϛʹ τελευτῆσαι.",
                "Jacob came from Haran to Laban being eighty years old, and begat Levi; and Levi lived in Egypt seventeen years from the time he came from Canaan into Egypt, so that he was sixty years old, and begat Kohath; and in the same year that Kohath was born, Jacob died in Egypt, having blessed the sons of Joseph, being one hundred and forty-seven years old, leaving Joseph fifty-six years old. And Levi, having reached the age of one hundred and thirty-seven years, died; and Kohath, being forty years old, begat Amram, who was fourteen years old when Joseph died in Egypt, being one hundred and ten years old; and Kohath, having reached the age of one hundred and thirty-three years, died. Amram took as wife Jochebed his uncle's daughter, and when he was seventy-five years old begat Aaron and Moses; and Amram begat Moses when he was seventy-eight years old, and Amram, having reached the age of one hundred and thirty-six years, died."
            )
        ]
    },
    {
        "num": 3,
        "title": "Fragmentum 3: De genealogia Moysis et Sepphorae (apud Eusebium, Praep. Evang. 9.29.1-3)",
        "verses": [
            (
                "Δημήτριος δὲ περὶ τῆς ἀναιρέσεως τοῦ Αἰγυπτίου καὶ τῆς διαφορᾶς τῆς πρὸς τὸν μηνύσαντα τὸν τελευτήσαντα ὁμοίως τῷ τὴν ἱερὰν βίβλον γράψαντι ἱστόρησε· φυγεῖν μέντοι γε τὸν Μωσῆν εἰς Μαδιάμ, καὶ συνοικῆσαι ἐκεῖ τῇ Ἰοθὸρ θυγατρὶ Σεπφώρᾳ, ἣν εἶναι, ὅσα στοχάζεσθαι ἀπὸ τῶν ὀνομάτων, τῶν γενομένων ἐκ Χεττούρας, τοῦ Ἀβραὰμ γένους, ἐκ τοῦ Ἰεξὰν τοῦ γενομένου Ἀβραὰμ ἐκ Χεττούρας· ἐκ δὲ τοῦ Ἰεξὰν γενέσθαι Δαδάν, ἐκ δὲ Δαδὰν Ῥαγουήλ, ἐκ δὲ Ῥαγουὴλ Ἰοθὸρ καὶ Ὀβάβ, ἐκ δὲ τοῦ Ἰοθὸρ Σεπφώραν, ἣν γῆμαι Μωσῆν.",
                "Demetrius related the circumstances of the slaying of the Egyptian and the quarrel with the man who disclosed the dead man similarly to the writer of the sacred book; however, he says that Moses fled to Midian, and there married Zipporah the daughter of Jothor, who was, as far as can be inferred from names, of the descendants of Keturah, of Abraham's stock, from Jokshan who was born to Abraham from Keturah; and from Jokshan was born Dedan, and from Dedan Raguel, and from Raguel Jothor and Hobab, and from Jothor Zipporah, whom Moses married."
            ),
            (
                "καὶ τὰς γενεὰς δὲ συμφωνεῖν· τὸν γὰρ Μωσῆν εἶναι ἀπὸ Ἀβραὰμ ἕβδομον, τὴν δὲ Σεπφώραν ἕκτην. συνοικοῦντος γὰρ ἤδη τοῦ Ἰσαάκ, ἀφ’ οὗ Μωσῆν εἶναι, γῆμαι Ἀβραὰμ τὴν Χεττούραν ὄντα ἐτῶν ρμʹ, καὶ γεννῆσαι Ἰεξὰν ἐξ αὐτῆς δεύτερον· τὸν δὲ Ἰσαὰκ ὄντα ἐτῶν ἑκατὸν γεννῆσαι· ὥστε μβʹ ἐτῶν ὕστερον γεγονέναι τὸν Ἰεξάν, ἀφ’ οὗ τὴν Σεπφώραν γεγενεαλογῆσθαι.",
                "And he says that the generations agree; for Moses is seventh from Abraham, while Zipporah is sixth. For when Isaac (from whom Moses was descended) was already married, Abraham married Keturah, being one hundred and forty years old, and begat Jokshan from her second; and Isaac begat when he was one hundred years old; so that Jokshan, from whom Zipporah is genealogically traced, was born forty-two years later."
            ),
            (
                "οὐδὲν οὖν ἀντιπίπτει τὸν Μωσῆν καὶ τὴν Σεπφώραν κατὰ τοὺς αὐτοὺς γεγονέναι χρόνους. κατοικεῖν δ’ αὐτοὺς Μαδιὰμ πόλιν, ἣν ἀπὸ ἑνὸς τῶν Ἀβραὰμ παίδων ὀνομασθῆναι. φησὶ γὰρ τὸν Ἀβραὰμ τοὺς παῖδας πρὸς ἀνατολὰς ἐπὶ κατοικίαν πέμψαι· διὰ τοῦτο δὲ καὶ Ἀαρὼν καὶ Μαριὰμ εἰπεῖν ἐν Ἀσηρὼθ Μωσῆν Αἰθιοπίδα γῆμαι γυναῖκα.",
                "Nothing therefore conflicts with Moses and Zipporah having lived at the same time. And they dwelt in the city of Midian, which was named after one of the sons of Abraham. For he says that Abraham sent his sons toward the east to dwell; and on this account Aaron and Miriam said at Hazeroth that Moses had married an Ethiopian woman."
            )
        ]
    },
    {
        "num": 4,
        "title": "Fragmentum 4: De aquis Marath et Elim (apud Eusebium, Praep. Evang. 9.29.15)",
        "verses": [
            (
                "Ἐκεῖθεν ἦλθον ἡμέρας τρεῖς, ὡς αὐτός τε ὁ Δημήτριος λέγει καὶ συμφώνως τούτῳ ἡ ἱερὰ βίβλος· μὴ ἔχοντα δὲ ὕδωρ ἐκεῖ γλυκύ, ἀλλὰ πικρόν, τοῦ θεοῦ εἰπόντος ξύλον τι ἐμβαλεῖν εἰς τὴν πηγήν, καὶ γενέσθαι γλυκὺ τὸ ὕδωρ. ἐκεῖθεν δὲ εἰς Ἐλεὶμ ἐλθεῖν, καὶ εὑρεῖν ἐκεῖ δώδεκα μὲν πηγὰς ὑδάτων, ἑβδομήκοντα δὲ στελέχη φοινίκων.",
                "'From there they journeyed three days,' as Demetrius himself says and in agreement with him the sacred book; 'and having no sweet water there, but bitter, when God told him to cast a piece of wood into the spring, the water became sweet. And from there they came to Elim, and found there twelve springs of water, and seventy date-palm trunks.'"
            )
        ]
    },
    {
        "num": 5,
        "title": "Fragmentum 5: De armis Israelitarum (apud Eusebium, Praep. Evang. 9.29.16)",
        "verses": [
            (
                "Ἐπιζητεῖν δέ τινα πῶς οἱ Ἰσραηλῖται ὅπλα ἔσχον ἄνοπλοι ἐξελθόντες. ἔφασαν γὰρ τριῶν ἡμερῶν ὁδὸν ἐξελθόντας καὶ θυσιάσαντας πάλιν ἀνακάμψειν. φαίνεται οὖν τοὺς μὴ κατακλυσθέντας τοῖς ἐκείνων ὅπλοις χρήσασθαι.",
                "Someone inquires how the Israelites obtained weapons, having gone out unarmed. For they said that having gone out a three days' journey and sacrificed, they would return again. It appears therefore that those who were not drowned used the weapons of those [Egyptians who drowned]."
            )
        ]
    },
    {
        "num": 6,
        "title": "Fragmentum 6: De captivitate et chronologia ad Ptolemaeum IV (apud Clementem Alex., Strom. 1.21.141.1-2)",
        "verses": [
            (
                "Δημήτριος δέ φησιν ἐν τῷ Περὶ τῶν ἐν τῇ Ἰουδαίᾳ βασιλέων τὴν Ἰούδα φυλὴν καὶ Βενιαμὶν καὶ Λευὶ μὴ αἰχμαλωτισθῆναι ὑπὸ τοῦ Σεναχηρείμ, ἀλλ’ εἶναι ἀπὸ τῆς αἰχμαλωσίας ταύτης εἰς τὴν ἐσχάτην, ἣν ἐποιήσατο Ναβουχοδονόσορ ἐξ Ἱεροσολύμων, ἔτη ἑκατὸν εἴκοσι ὀκτὼ μῆνας ἕξ.",
                "Demetrius says in his work On the Kings in Judaea that the tribe of Judah and Benjamin and Levi were not taken captive by Sennacherib, but that from this captivity to the final one which Nebuchadnezzar made from Jerusalem, there were 128 years and 6 months."
            ),
            (
                "ἀφ’ οὗ δὲ αἱ φυλαὶ αἱ δέκα ἐκ Σαμαρείας αἰχμάλωτοι γεγόνασιν ἕως Πτολεμαίου τετάρτου ἔτη πεντακόσια ἑβδομήκοντα τρία μῆνας ἐννέα, ἀφ’ οὗ δὲ ἐξ Ἱεροσολύμων ἔτη τριακόσια τριάκοντα ὀκτὼ μῆνας τρεῖς.",
                "And from the time when the ten tribes were taken captive from Samaria until Ptolemy IV, there were 573 years and 9 months, and from the time of the captivity from Jerusalem, 338 years and 3 months."
            )
        ]
    }
]

def make_grammateus_xml():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Demetr.xml" title="Demetrius the Chronographer">',
        '  <version id="Greek" title="Greek Text (FGrH 722 / Denis 1970)" lang="grc">',
        '    <divisions>',
        '      <division id="1" title="Fragments" type="fragment"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <manuscript id="PE" name="Eusebius Praeparatio Evangelica"/>',
        '      <manuscript id="Strom" name="Clemens Alexandrinus Stromateis"/>',
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
            lines.append(f'          <reading option="base" mss="PE">{escaped_grk}</reading>')
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
    out_xml = 'static/docs/Demetr.xml'
    with open(out_xml, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote Grammateus XML: {out_xml} (6 fragments, {sum(len(f['verses']) for f in FRAGMENTS)} units)")
    
    # Convert to TEI P5
    out_tei = 'static/docs/tei/Demetr.xml'
    ret = os.system(f"python3 scripts/grammateus_to_tei.py {out_xml} -o {out_tei}")
    if ret == 0:
        print(f"Wrote TEI P5 XML: {out_tei}")
    else:
        print(f"Error converting to TEI P5: {ret}")

if __name__ == '__main__':
    main()
