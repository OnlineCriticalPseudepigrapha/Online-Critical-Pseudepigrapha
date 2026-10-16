#!/usr/bin/env python3
"""
Build Pseudo-Hecataeus (De Iudaeis / De Abrahamo, CAVT 84 / CANT 28 / FGrH 264 F 21-24)
Greek text:
  - Flavius Josephus, Contra Apionem I.183-205; II.43
  - Flavius Josephus, Antiquitates Iudaicae I.159; XII.38
  - Clemens Alexandrinus, Stromata V.113.1-2
Critical edition:
  - Felix Jacoby, Die Fragmente der griechischen Historiker (FGrH 264 F 21-24)
  - Albert-Marie Denis, Fragmenta pseudepigraphorum quae supersunt graeca (PVTG 3, 1970), pp. 49-62.
Outputs:
  - static/docs/PsHecat.xml (Grammateus DTD)
  - static/docs/tei/PsHecat.xml (TEI P5 parallel segmentation)
"""

import os
import re

CHAPTERS = [
    {
        "num": 1,
        "title": "De Iudaeis et Aegypto (Contra Apionem I.183-189)",
        "verses": [
            (
                "Ἑκαταῖος δὲ ὁ Ἀβδηρίτης, ἀνὴρ φιλόσοφος ἅμα καὶ περὶ τὰς πράξεις ἱκανώτατος, Ἀλεξάνδρῳ τῷ βασιλεῖ συνακμάσας καὶ Πτολεμαίῳ τῷ Λάγου συγγενόμενος, οὐ παρέργως ἀλλὰ περὶ αὐτῶν Ἰουδαίων συγγέγραφε βιβλίον, ἐξ οὗ βούλομαι κεφαλαιωδῶς ἐπιδραμεῖν ἔνια τῶν εἰρημένων.",
                "Hecataeus of Abdera, both a philosopher and an exceedingly capable man of affairs, who flourished under King Alexander and was associated with Ptolemy son of Lagus, did not write casually, but composed a book specifically about the Jews, from which I wish briefly to summarize some points."
            ),
            (
                "καὶ πρῶτον ἐπιδείξω τὸν χρόνον· μνημονεύει γὰρ τῆς Πτολεμαίου περὶ Γάζαν πρὸς Δημήτριον μάχης· αὕτη δὲ γέγονεν ἑνδεκάτῳ μὲν ἔτει τῆς Ἀλεξάνδρου τελευτῆς, ἐπὶ δὲ ὀλυμπιάδος ἑβδόμης καὶ δεκάτης καὶ ἑκατοστῆς, ὡς ἱστορεῖ Κάστωρ.",
                "And first I will establish the date; for he mentions the battle fought at Gaza by Ptolemy against Demetrius, which took place in the eleventh year after Alexander's death, in the 117th Olympiad, as Castor relates."
            ),
            (
                "προσθεὶς γὰρ ταύτην τὴν ὀλυμπιάδα φησίν· ἐπὶ ταύτης Πτολεμαῖος ὁ Λάγου ἐνίκα κατὰ Γάζαν μάχῃ Δημήτριον τὸν Ἀντιγόνου τὸν ἐπικληθέντα Πολιορκητήν. Ἀλέξανδρον δὲ τεθνάναι πάντες ὁμολογοῦσιν ἐπὶ τῆς ἑκατοστῆς τεσσαρεσκαιδεκάτης ὀλυμπιάδος. δῆλον οὖν, ὅτι καὶ κατʼ ἐκεῖνον καὶ κατὰ Ἀλέξανδρον ἤκμαζεν ἡμῶν τὸ ἔθνος.",
                "For recording this Olympiad he says: 'In this Olympiad Ptolemy son of Lagus defeated in battle at Gaza Demetrius son of Antigonus, surnamed the Besieger.' And all agree that Alexander died in the 114th Olympiad. It is clear, therefore, that both in his time and under Alexander our nation flourished."
            ),
            (
                "λέγει τοίνυν ὁ Ἑκαταῖος πάλιν τάδε, ὅτι μετὰ τὴν ἐν Γάζῃ μάχην ὁ Πτολεμαῖος ἐγένετο τῶν περὶ Συρίαν τόπων ἐγκρατής, καὶ πολλοὶ τῶν ἀνθρώπων πυνθανόμενοι τὴν ἠπιότητα καὶ φιλανθρωπίαν τοῦ Πτολεμαίου συναπαίρειν εἰς Αἴγυπτον ἠβουλήθησαν αὐτῷ καὶ τῶν πραγμάτων κοινωνεῖν.",
                "Hecataeus then says this: that after the battle at Gaza Ptolemy became master of the places about Syria, and many of the inhabitants, learning of the mildness and humanity of Ptolemy, wished to depart with him to Egypt and share in his affairs."
            ),
            (
                "ὧν εἷς ἦν Ἑζεκίας, φησίν, ἀρχιερεὺς τῶν Ἰουδαίων, ἄνθρωπος τὴν μὲν ἡλικίαν ὡς ἑξήκοντα καὶ ἓξ ἐτῶν, τῷ δʼ ἀξιώματι τῷ παρὰ τοῖς ὁμοέθνοις μέγας καὶ τὴν ψυχὴν οὐκ ἀνόητος, ἔτι δὲ καὶ λέγειν δυνατὸς καὶ τοῖς περὶ τῶν πραγμάτων, εἴπερ τις ἄλλος, ἐμπειρότατος.",
                "'Among these,' he says, 'was Hezekiah, a high priest of the Jews, a man about sixty-six years of age, held in great honor by his compatriots, not deficient in intellect, and moreover powerful in speech and thoroughly experienced in affairs, if ever anyone was.'"
            ),
            (
                "καίτοι, φησίν, οἱ πάντες Ἰουδαίων ἱερεῖς οἱ τὴν δεκάτην τῶν γινομένων λαμβάνοντες καὶ τὰ κοινὰ διοικοῦντες ὕστερον περὶ χιλίους καὶ πεντακοσίους μάλιστά εἰσιν.",
                "'Yet,' he says, 'all the priests of the Jews who receive the tithe of the produce and administer public affairs are about fifteen hundred in all.'"
            ),
            (
                "πάλιν δὲ τοῦ προειρημένου μνημονεύων ἀνδρός, οὗτος οὖν, φησίν, ὁ ἄνθρωπος τυχὼν ταύτης τῆς τιμῆς καὶ συνήθης ἡμῖν γενόμενος παραλαβών τινας τῶν μεθʼ ἑαυτοῦ πάντας ἀνέγνω τὴν διαφορὰν αὐτοῖς· εἶχεν γὰρ τὴν κατοίκησιν αὐτῶν καὶ τὴν πολιτείαν γεγραμμένην.",
                "Mentioning again the aforesaid man: 'This man then, having obtained this honor and become familiar with us, gathered together some of his followers and read to them all the charter; for he had their settlement and constitution in writing.'"
            )
        ]
    },
    {
        "num": 2,
        "title": "De pietate et legibus Iudaeorum (Contra Apionem I.190-194)",
        "verses": [
            (
                "εἶτα Ἑκαταῖος δηλοῖ πάλιν, πῶς ἔχομεν πρὸς τοὺς νόμους, ὅτι πάντα πάσχειν ὑπὲρ τοῦ μὴ παραβῆναι τούτους προῃρήμεθα καὶ καλὸν εἶναι νομίζομεν.",
                "Then Hecataeus shows again our attitude toward our laws, that we choose to suffer everything rather than transgress them, and consider this honorable."
            ),
            (
                "τοιγαροῦν, φησί, καὶ κακῶς ἀκούοντες ὑπὸ τῶν ἀστυγειτόνων καὶ προπηλακιζόμενοι πάντες οἵ τε Περσῶν βασιλεῖς καὶ οἱ σατράπαι οὐ δύνανται μεταπεῖσαι τὴν γνώμην, ἀλλὰ γυμνοὶ περὶ τούτων αἰκίας καὶ θανάτους πάντων μάλιστα δεινοτάτους ὑπομένουσι μὴ ἀρνούμενοι τὰ πάτρια.",
                "'Therefore,' he says, 'even though spoken ill of by their neighbors and insulted by all, neither the kings of Persia nor their satraps have been able to change their resolve; but defenseless they endure tortures and the most terrible deaths of all on behalf of these, refusing to renounce the customs of their fathers.'"
            ),
            (
                "παρέχεται δὲ καὶ τεκμήρια τῆς ἰσχυρογνωμοσύνης τῆς περὶ τοὺς νόμους. Ἀλεξάνδρου γάρ, φησίν, ἐν Βαβυλῶνι γενομένου καὶ προελομένου τὸ τοῦ Βήλου συμπεπτωκὸς ἱερὸν ἀνακαθᾶραι, καὶ πάντων αὐτῷ τῶν στρατιωτῶν χοῦν συμφερόντων μόνοι οἱ Ἰουδαῖοι προσέχειν οὐχ ὑπέμειναν, ἀλλὰ καὶ πολλὰς ὑπέστησαν πληγὰς καὶ μεγάλας ἀποτίσεις ἐζημιώθησαν, ἕως αὐτοῖς συγγνώμην ὁ βασιλεὺς ἔδωκεν καὶ καθαιρέσεως ἔτυχον.",
                "He also provides proofs of their steadfastness regarding the laws. 'For when Alexander,' he says, 'was in Babylon and chose to restore the fallen temple of Belus, and all his soldiers were carrying earth, the Jews alone refused to participate, but endured many blows and were fined severe penalties, until the king granted them pardon and they were excused from the demolition.'"
            ),
            (
                "ἔτι γε μὴν ὡς εἰς τὴν χώραν αὐτῶν παραγενομένων τῶν πρότερον νεὼς καὶ βωμοὺς κατασκευασάντων ἅπαντα κατέσκαψαν, καὶ τῶν μὲν ζημίαν ἐξέτεισαν τοῖς σατράπαις, περὶ ὧν δὲ συγγνώμης ἔτυχον.",
                "'Furthermore, when newcomers arrived in their country and built temples and altars, they demolished all of them; and for some they paid fines to the satraps, while for others they obtained pardon.'"
            ),
            (
                "καὶ προστίθησιν, ὅτι δίκαιόν ἐστιν ἐπὶ τούτοις αὐτοὺς θαυμάζειν.",
                "And he adds that it is just to admire them for these things."
            )
        ]
    },
    {
        "num": 3,
        "title": "De terra, Ierosolymis et Templo (Contra Apionem I.195-200)",
        "verses": [
            (
                "ὁ δὲ αὐτὸς οὗτος ἀνὴρ καὶ τὸ μέγεθος τῆς χώρας ἣν κατοικοῦμεν καὶ τὸ κάλλος ἱστόρηκεν· τριακοσίας γὰρ αὐτὴν μυριάδας ἀρουρῶν ἀρίστης καὶ παμφορωτάτης γῆς εἶναί φησιν· τοσαύτη γάρ ἐστιν ἡ Ἰουδαία.",
                "The same author has also described the extent and beauty of the land we inhabit; for he says it comprises three million arourae of the best and most fertile soil; such indeed is the size of Judaea."
            ),
            (
                "ἔτι γε μὴν ὡς αὐτὴν τὴν Ἱεροσολύμων πόλιν, ὅτι καὶ μεγίστην καὶ καλλίστην ἐκ παλαιοτάτου νέμονται, καὶ περὶ πλήθους ἀνθρώπων καὶ περὶ τῆς τοῦ νεὼ κατασκευῆς οὕτως διηγεῖται.",
                "Moreover, concerning the city of Jerusalem itself, that from most ancient times they have inhabited it as a very great and beautiful city, he describes the multitude of people and the structure of the Temple as follows:"
            ),
            (
                "ἔστι γὰρ τῶν Ἰουδαίων τὰ μὲν πολλὰ φρούρια κατὰ τὴν χώραν καὶ κῶμαι, μία δὲ πόλις ὀχυρά, πεντήκοντα μάλιστα σταδίων τὴν περίμετρον, ἣν οἰκοῦσι μὲν ἀνθρώπων περὶ δώδεκα μυριάδες, καλοῦσι δʼ αὐτὴν Ἱεροσόλυμα.",
                "'There are among the Jews many fortresses throughout the country and villages, but one fortified city, about fifty stades in circumference, inhabited by about one hundred and twenty thousand men, and they call it Jerusalem.'"
            ),
            (
                "ἐνταῦθα δʼ ἐστὶ κατὰ μέσον μάλιστα τῆς πόλεως περίβολος λίθινος, μῆκος ὡς πεντάπλεθρος, εὖρος δὲ πηχῶν ἑκατόν, ἔχων διπλᾶς πύλας, ἐν ᾧ βωμός ἐστι τετράγωνος, ἀτμήτων συλλέκτων ἀργῶν λίθων συμπεπηγώς, εἴκοσι μὲν πηχῶν τὸ πλάτος, τὸ δὲ ὕψος ἔχων πηχῶν δέκα, καὶ παρʼ αὐτὸν οἴκημα μέγα, οὗ βωμός ἐστι καὶ λυχνία, χρυσᾶ μὲν ἀμφότερα, σταθμὸν ἔχοντα ταλάντων δύο.",
                "'Here almost in the middle of the city is a stone enclosure, about five plethra in length and one hundred cubits wide, having double gates; within it is a square altar, built of uncut, gathered unhewn stones, twenty cubits in breadth and ten cubits in height; and beside it a great building, in which are an altar and a lampstand, both of gold, weighing two talents.'"
            ),
            (
                "ἐπὶ δὲ τούτων φῶς ἐστιν ἀκοίμητον καὶ τὰς νύκτας καὶ τὰς ἡμέρας. ἄγαλμα δὲ οὐκ ἔστιν οὐδὲ ἀνάθημα τὸ παράπαν οὐδὲ φύτευμα παντελῶς οὐδέν, οἷον ἄλσος ἢ τὸ τοιοῦτον.",
                "'Upon these is an unquenched light both night and day. But image or dedication there is none at all, nor any planting whatsoever, such as a grove or the like.'"
            ),
            (
                "διατρίβουσι δʼ ἐν αὐτῷ καὶ τὰς νύκτας καὶ τὰς ἡμέρας ἱερεῖς ἁγνείας τινὰς ἁγνεύοντες καὶ τὸ παράπαν οἶνον οὐ πίνοντες ἐν τῷ ἱερῷ.",
                "'And priests reside in it both night and day, performing certain purifications and drinking no wine at all in the Temple.'"
            )
        ]
    },
    {
        "num": 4,
        "title": "De Mosollamo et augurio (Contra Apionem I.201-205)",
        "verses": [
            (
                "ἔτι δὲ καὶ ὅτι Ἀλεξάνδρῳ τῷ βασιλεῖ συνεστρατεύσαντο καὶ μετὰ ταῦτα τοῖς διαδόχοις αὐτοῦ, κατόπιν ἱστόρηκεν. οἷς δʼ αὐτὸς παρατυχεῖν φησιν ὑπʼ ἀνδρὸς Ἰουδαίου κατὰ τὴν στρατείαν γενομένοις, τοῦτο παραθήσομαι.",
                "Furthermore, he has recorded below that they served in the army with King Alexander and afterwards with his successors. What he states took place in his presence on campaign through a Jewish man, I will here relate."
            ),
            (
                "λέγει δʼ οὕτως· ἐμοῦ γοῦν ἐπὶ τὴν Ἐρυθρὰν θάλασσαν βαδίζοντος συνηκολούθει τις μετὰ τῶν ἄλλων τῶν παραπεμπόντων ἡμᾶς ἱππέων Ἰουδαίων ὄνομα Μοσόλλαμος, ἀνὴρ ψυχῇ τε ἱκανὸς καὶ τὸ σῶμα κράτιστος καὶ τοξότης ὁμολογουμένως παρά τε τοῖς Ἕλλησι καὶ τοῖς βαρβάροις ἄριστος.",
                "He speaks thus: 'As I was marching toward the Red Sea, there accompanied us among the other Jewish cavalry escorting us one named Mosollamus, a man of stout heart, physically very strong, and confessedly the best archer among both Greeks and barbarians.'"
            ),
            (
                "προϊόντων δὲ πολλῶν κατὰ τὴν ὁδὸν καὶ μάντεώς τινος ὀρνιθευομένου καὶ πάντας ἐπισχεῖν ἀξιοῦντος, ἠρώτησε διὰ τί προσμένουσι.",
                "'As many were advancing along the road and a certain augur was taking auspices from a bird and requiring everyone to halt, he asked why they were waiting.'"
            ),
            (
                "δείξαντος δὲ τοῦ μάντεως αὐτῷ τὸν ὄρνιθα καὶ φήσαντος, ἐὰν μὲν αὐτοῦ μένῃ, προσμένειν συμφέρειν πᾶσιν, ἐὰν δʼ ἀναπτὰς εἰς τοὔμπροσθεν πέτηται, προάγειν, ἐὰν δὲ εἰς τοὐπίσω, πάλιν ἀναχωρεῖν, σιωπήσας καὶ διατείνας τὸ τόξον εἴλκυσε καὶ πατάξας τὸν ὄρνιθα ἀπέκτεινεν.",
                "'When the augur showed him the bird and said that if it stayed there, it was advantageous for all to wait, but if it flew forward, to advance, and if backward, to retreat, he said nothing, but drawing his bow, shot and struck the bird and killed it.'"
            ),
            (
                "ἀγανακτούντων δὲ τοῦ τε μάντεως καί τινων ἄλλων καὶ καταρωμένων αὐτῷ, τί μαίνεσθε, ἔφη, ταλαίπωροι; καὶ λαβὼν τὸν ὄρνιθα εἰς τὰς χεῖρας, πῶς γάρ, ἔφη, περὶ τῆς ἡμετέρας πορείας οὗτος ἂν ὑγιές τι προεδήλωσεν ἡμῖν, ὃς τὴν ἑαυτοῦ σωτηρίαν οὐ προεῖδεν; εἰ γὰρ ἠδύνατο προγινώσκειν τὸ μέλλον, οὐκ ἂν ἦλθεν εἰς τοῦτον τὸν τόπον, φοβούμενος μὴ τοξευθεὶς ὑπὸ Μοσολλάμου τοῦ Ἰουδαίου τελευτήσῃ.",
                "'When the augur and certain others were indignant and cursed him, he said: Why are you raving, miserable men? And taking the bird in his hands, he said: How could this creature give us any sound advice about our march, when it could not foresee its own safety? For if it had been able to foresee the future, it would not have come to this spot, fearing lest it be shot and killed by Mosollamus the Jew.'"
            )
        ]
    },
    {
        "num": 5,
        "title": "Fragmenta minora (Contra Apionem II.43; Antiquitates I.159, XII.38; Stromata V.113.1-2)",
        "verses": [
            (
                "ἐτίμα γὰρ ἡμῶν τὸ ἔθνος [Ἀλέξανδρος], ὡς καί φησιν Ἑκαταῖος περὶ ἡμῶν, ὅτι διὰ τὴν ἐπιείκειαν καὶ πίστιν, ἣν αὐτῷ παρέσχον Ἰουδαῖοι, τὴν Σαμαρεῖτιν χώραν προσέθηκεν ἔχειν αὐτοῖς ἀφορολόγητον. (Contra Apionem II.43)",
                "[Alexander] honored our nation, as Hecataeus also says concerning us, that because of the equity and loyalty which the Jews rendered him, he added the district of Samaria to them to hold free of tribute. (Contra Apionem II.43)"
            ),
            (
                "Ἑκαταῖος δὲ καὶ τοῦ μνησθῆναι πλέον τι πεποίηκε· βιβλίον γὰρ περὶ αὐτοῦ [Ἀβράμου] συνταξάμενος κατέλιπε. (Antiquitates Iudaicae I.159)",
                "Hecataeus did more than merely mention him; for he composed and left behind a book about him [Abraham]. (Antiquitates Iudaicae I.159)"
            ),
            (
                "διὸ καὶ τοὺς ποιητὰς αὐτῆς καὶ τοὺς συγγραφεῖς τῶν ἱστοριῶν οὐκ ἐπιμνησθῆναί φησιν Ἑκαταῖος ὁ Ἀβδηρίτης οὐδὲ τῶν κατʼ αὐτὴν πολιτευσαμένων ἀνδρῶν, ὡς ἁγνῆς οὔσης καὶ μὴ δέον αὐτὴν βεβήλοις στόμασιν διασαφεῖσθαι. (Antiquitates Iudaicae XII.38 / Epist. Aristeae 31)",
                "Wherefore Hecataeus of Abdera says that the poets and historians made no mention of the [divine Law] nor of the men who lived according to it, because it is holy and not to be published through profane mouths. (Antiquitates XII.38 / Ep. Arist. 31)"
            ),
            (
                "Ἑκαταῖος ὁ τὰς Αἰγυπτιακὰς ἱστορίας συνταξάμενος ἐν τῷ κατʼ Ἀβραὰμ βιβλίῳ μέμνηται ὡς ἑνὸς ὄντος τοῦ θεοῦ καὶ πάντων δημιουργοῦ. (Clemens Alex., Stromata V.113.1-2)",
                "Hecataeus, who composed the Egyptian histories, in his book on Abraham mentions that God is One and Creator of all. (Stromata V.113.1-2)"
            )
        ]
    }
]

def build_grammateus_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE document SYSTEM "document.dtd">',
        '<document id="PsHecat">',
        '    <header>',
        '        <title>Fragments of Pseudo-Hecataeus (De Iudaeis / De Abrahamo)</title>',
        '        <author>Pseudo-Hecataeus</author>',
        '        <editor>Felix Jacoby (FGrH 264 F 21-24); Albert-Marie Denis (PVTG 3, 1970)</editor>',
        '        <description>Greek text and English translation of the fragments of Pseudo-Hecataeus preserved in Flavius Josephus (Contra Apionem I.183-205; II.43; Antiquitates I.159; XII.38) and Clement of Alexandria (Stromata V.113.1-2). CAVT 84 / CANT 28.</description>',
        '    </header>',
        '    <body>'
    ]
    for ch in CHAPTERS:
        c_num = ch["num"]
        for v_num, (grc, en) in enumerate(ch["verses"], 1):
            lines.append(f'        <div c="{c_num}" v="{v_num}">')
            lines.append(f'            <line lang="grc">{grc}</line>')
            lines.append(f'            <line lang="en">{en}</line>')
            lines.append('        </div>')
    lines.append('    </body>')
    lines.append('</document>\n')
    
    out_path = 'static/docs/PsHecat.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path}')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Fragments of Pseudo-Hecataeus (De Iudaeis / De Abrahamo)</title>',
        '        <author>Pseudo-Hecataeus</author>',
        '        <editor>Felix Jacoby; Albert-Marie Denis</editor>',
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
        '            <title level="m">Fragmenta pseudepigraphorum quae supersunt graeca</title>',
        '            <editor>Albert-Marie Denis</editor>',
        '            <imprint>',
        '              <publisher>E. J. Brill</publisher>',
        '              <pubPlace>Leiden</pubPlace>',
        '              <date when="1970">1970</date>',
        '              <biblScope unit="page">49-62</biblScope>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>'
    ]
    for ch in CHAPTERS:
        c_num = ch["num"]
        lines.append(f'      <div type="chapter" n="{c_num}">')
        for v_num, (grc, en) in enumerate(ch["verses"], 1):
            lines.append(f'        <p n="{v_num}">')
            lines.append(f'          <app>')
            lines.append(f'            <rdg wit="#Denis1970" xml:lang="grc">{grc}</rdg>')
            lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
            lines.append(f'          </app>')
            lines.append(f'        </p>')
        lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')
    
    out_path = 'static/docs/tei/PsHecat.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
