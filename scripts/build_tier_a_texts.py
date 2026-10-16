#!/usr/bin/env python3
"""Build Tier A texts:
1. Prayer of Manasseh (CAVT 178) - Greek & Latin parallel
2. Vision of Elijah (CAVT 169) - Latin
"""
import re, xml.sax.saxutils as saxutils
from xml.sax.saxutils import escape

def build_prayer_of_manasseh():
    print("Building Prayer of Manasseh (CAVT 178)...")
    greek_verses = [
        "Κύριε παντοκράτωρ, ὁ θεὸς τῶν πατέρων ἡμῶν, τοῦ Ἀβραὰμ καὶ Ἰσαὰκ καὶ Ἰακὼβ καὶ τοῦ σπέρματος αὐτῶν τοῦ δικαίου,",
        "ὁ ποιήσας τὸν οὐρανὸν καὶ τὴν γῆν σὺν παντὶ τῷ κόσμῳ αὐτῶν,",
        "ὁ πεδήσας τὴν θάλασσαν τῷ λόγῳ τοῦ προστάγματός σου, ὁ κλείσας τὴν ἄβυσσον καὶ σφραγισάμενος τῷ φοβερῷ καὶ ἐνδόξῳ ὀνόματί σου,",
        "ὃν πάντα φρίσσει καὶ τρέμει ἀπὸ προσώπου τῆς δυνάμεώς σου, ὅτι ἄστεκτος ἡ μεγαλοπρέπεια τῆς δόξης σου,",
        "καὶ ἀνυπόστατος ἡ ὀργὴ τῆς ἀπειλῆς σου ἐπὶ ἁμαρτωλούς,",
        "ἀμέτρητόν τε καὶ ἀνεξιχνίαστον τὸ ἔλεος τῆς ἐπαγγελίας σου,",
        "ὅτι σὺ εἶ κύριος ὕψιστος, εὔσπλαγχνος, μακρόθυμος καὶ πολυέλεος καὶ μετανοῶν ἐπὶ κακίαις ἀνθρώπων. σὺ οὖν, κύριε, κατὰ τὸ πλῆθος τῆς χρηστότητός σου ἐπηγγείλω μετάνοιαν καὶ ἄφεσιν τοῖς ἡμαρτηκόσιν σοι, καὶ τῷ πλήθει τῶν οἰκτιρμῶν σου ὥρισας μετάνοιαν ἁμαρτωλοῖς εἰς σωτηρίαν.",
        "σὺ οὖν, κύριε, ὁ θεὸς τῶν δικαίων, οὐκ ἔθου μετάνοιαν δικαίοις, τῷ Ἀβραὰμ καὶ Ἰσαὰκ καὶ Ἰακώβ, τοῖς οὐχ ἡμαρτηκόσιν σοι, ἀλλ᾽ ἔθου μετάνοιαν ἐμοὶ τῷ ἁμαρτωλῷ.",
        "διότι ἥμαρτον ὑπὲρ ἀριθμὸν ψάμμου θαλάσσης· ἐπληθύνθησαν αἱ ἀνομίαι μου, κύριε, ἐπληθύνθησαν, καὶ οὐκ εἰμὶ ἄξιος ἀναβλέψαι καὶ ἰδεῖν τὸ ὕψος τοῦ οὐρανοῦ ἀπὸ τοῦ πλήθους τῶν ἀδικιῶν μου.",
        "κατακαμπτόμενος πολλῷ δεσμῷ σιδήρου εἰς τὸ μὴ ἀνανεῦσαί με, καὶ οὐκ ἔστιν μοι ἄνεσις, διότι παρώργισα τὸν θυμόν σου καὶ τὸ πονηρὸν ἐνώπιόν σου ἐποίησα, στήσας βδελύγματα καὶ πληθύνας προσοχθίσματα.",
        "καὶ νῦν κλίνω γόνυ καρδίας δεόμενος τῆς παρὰ σοῦ χρηστότητος.",
        "ἡμάρτηκα, κύριε, ἡμάρτηκα, καὶ τὰς ἀνομίας μου ἐγὼ γινώσκω.",
        "αἰτοῦμαι δεόμενός σου· ἄνες μοι, κύριε, ἄνες μοι, καὶ μὴ συναπολέσῃς με ταῖς ἀνομίαις μου, μηδὲ εἰς τὸν αἰῶνα μηνίσας τηρήσῃς τὰ κακά μοι, μηδὲ καταδικάσῃς με ἐν τοῖς κατωτάτοις τῆς γῆς.",
        "ὅτι σὺ εἶ, κύριε, ὁ θεὸς τῶν μετανοούντων, καὶ ἐν ἐμοὶ δείξεις τὴν ἀγαθωσύνην σου, ὅτι ἀνάξιον ὄντα σώσεις με κατὰ τὸ πολὺ ἔλεός σου.",
        "καὶ αἰνέσω σε διαπαντὸς ἐν ταῖς ἡμέραις τῆς ζωῆς μου, ὅτι σὲ ὑμνεῖ πᾶσα ἡ δύναμις τῶν οὐρανῶν, καὶ σοῦ ἐστιν ἡ δόξα εἰς τοὺς αἰῶνας. ἀμήν."
    ]

    latin_verses = [
        "Domine omnipotens, Deus patrum nostrorum, Abraham, et Isaac, et Jacob, et seminis eorum justi,",
        "qui fecisti cælum, et terram cum omni ornatu eorum,",
        "qui ligasti mare verbo præcepti tui, qui conclusisti abyssum, et signasti eam terribili et laudabili nomine tuo:",
        "quem omnia pavent, et tremunt a vultu virtutis tuæ, quia importabilis est magnificentia gloriæ tuæ,",
        "et insustentabilis ira comminationis tuæ super peccatores:",
        "immensa vero et investigabilis misericordia promissionis tuæ:",
        "quoniam tu es Dominus, altissimus, benignus, longanimis, et multum misericors, et pœnitens super malitias hominum. Tu Domine, secundum multitudinem bonitatis tuæ promisisti pœnitentiam, et remissionem iis, qui peccaverunt tibi, et multitudinem miserationum tuarum decrevisti pœnitentiam peccatoribus, in salutem.",
        "Tu igitur Domine Deus justorum, non posuisti pœnitentiam justis, Abraham, et Isaac, et Jacob, iis qui tibi non peccaverunt: sed posuisti pœnitentiam propter me peccatorem:",
        "quoniam peccavi super numerum arenæ maris: multiplicatæ sunt iniquitates meæ Domine, multiplicatæ sunt iniquitates meæ, et non sum dignus intueri et aspicere altitudinem cæli, præ multitudine iniquitatum mearum.",
        "Incurvatus sum multo vinculo ferreo, ut non possim attollere caput meum, et non est respiratio mihi: quia excitavi iracundiam tuam, et malum coram te feci: non feci voluntatem tuam, et mandata tua non custodivi: statui abominationes, et multiplicavi offensiones.",
        "Et nunc flecto genu cordis mei, precans a te bonitatem.",
        "Peccavi Domine, peccavi, et iniquitates meas agnosco.",
        "Quare peto rogans te, remitte mihi Domine, remitte mihi, et ne simul perdas me cum iniquitatibus meis, neque in æternum, iratus, reserves mala mihi, neque damnes me in infima terræ loca:",
        "quia tu es Deus, Deus, inquam pœnitentium: et in me ostendes omnem bonitatem tuam, quia indignum salvabis me secundum magnam misericordiam tuam,",
        "et laudabo te semper omnibus diebus vitæ meæ: quoniam te laudat omnis virtus cælorum, et tibi est gloria in sæcula sæculorum. Amen."
    ]

    bib_gr = "H. B. Swete, The Old Testament in Greek according to the Septuagint, Vol. III (Cambridge: Cambridge University Press, 1896), Odes 12 (Ode of Manasses)."
    bib_la = "Biblia Sacra Vulgata (Clementina), Appendix: Oratio Manassae regis Juda cum captus teneretur in Babylone."

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="OrMan" title="Prayer of Manasseh">',
        '  <version author="Septuagint and Vulgate" language="Greek" title="Greek and Latin">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="LXX" language="Greek" show="yes">',
        '        <name>Septuagint (Odes 12)</name>',
        f'        <bibliography>{escape(bib_gr)}</bibliography>',
        '      </ms>',
        '      <ms abbrev="Vulg" language="Latin" show="yes">',
        '        <name>Clementine Vulgate Appendix</name>',
        f'        <bibliography>{escape(bib_la)}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ]

    for v in range(1, 16):
        lines.append(f'        <div number="{v}">')
        lines.append(f'          <unit id="{v-1}">')
        lines.append(f'            <reading option="0" mss="LXX ">{escape(greek_verses[v-1])}</reading>')
        lines.append(f'            <reading option="1" mss="Vulg ">{escape(latin_verses[v-1])}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')

    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>')

    xml_content = '\n'.join(lines) + '\n'
    out_path = 'static/docs/OrMan.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote {out_path} with 15 parallel Greek/Latin verses.")


def build_visio_eliae():
    print("Building Vision of Elijah (CAVT 169)...")
    latin_units = [
        "Denique testatur propheta Helias vidisse:",
        "Ostendit, inquit, mihi angelus Domini convallem altam quae vocatur Gehenna, ardensque sulphure et bitumine.",
        "Et in illo loco sunt multae animae peccatorum et taliter ibi cruciantur diversis tormentis:",
        "patiuntur aliqui pendentes naturale, alii autem linguis, quidam vero oculis, alii inversi pendentes,",
        "et feminae mammillis suis cruciabuntur, et iuvenes manibus pendentes, quaedam in craticula virgines uruntur et quaedam figuntur animae perpetuae poenae.",
        "Per ipsa vero varia supplicia ostenditur uniuscuiusque actus:",
        "naturalium dolor utique adulteri sunt et pederasti;",
        "qui autem linguis suspenduntur blasphemi sunt, falsi etiam testes;",
        "qui oculis vero cremantur hi sunt qui in videndo scandalizati sunt respicientes in concupiscentia reatu gesta;",
        "qui vero inversi pendebant hi sunt odientes iustitiam Dei, pravi consilii, nec quisquam fratri consentit, merito ergo poenis sententiae uruntur;",
        "nam quod feminae mammillis torqueri iubentur istae sunt quae in ludibrio corpus suum tradiderunt masculis, ideoque et ipsi iuxta erunt in tormentis manibus pendentes propter hanc rem."
    ]

    bib = "Donatien De Bruyne, 'Epistula Titi discipuli Pauli de dispositione sanctimonii', Revue Bénédictine 37 (1925), pp. 47-72 (Visio Eliae at p. 58, ll. 400-417)."

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="VisEl" title="Vision of Elijah">',
        '  <version author="De Bruyne 1925" language="Latin" title="Latin">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="DeBruyne" language="Latin" show="yes">',
        '        <name>De Bruyne 1925 (Revue Bénédictine 37)</name>',
        f'        <bibliography>{escape(bib)}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>',
        '      <div number="1">'
    ]

    for v, text in enumerate(latin_units, 1):
        lines.append(f'        <div number="{v}">')
        lines.append(f'          <unit id="{v-1}">')
        lines.append(f'            <reading option="0" mss="DeBruyne ">{escape(text)}</reading>')
        lines.append('          </unit>')
        lines.append('        </div>')

    lines.append('      </div>')
    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>')

    xml_content = '\n'.join(lines) + '\n'
    out_path = 'static/docs/VisEl.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote {out_path} with 11 verses.")

if __name__ == '__main__':
    build_prayer_of_manasseh()
    build_visio_eliae()
