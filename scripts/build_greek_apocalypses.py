#!/usr/bin/env python3
"""Build Greek Apocalypse of Ezra (CAVT 184.i) and Apocalypse of Sedrach (CAVT 184.ii)
Grammateus DTD XML and TEI P5 XML.
"""
import os, sys, re, subprocess
from xml.sax.saxutils import escape

def build_sedrach():
    print("Building Apocalypse of Sedrach...")
    # Load and clean James 1893 text
    with open('raw/editions/Sedrach_archive_djvu.txt', 'r', encoding='utf-8') as f:
        raw = f.read()

    # Pre-clean lines
    cleaned_lines = []
    for line in raw.splitlines():
        l = line.strip()
        if not l: continue
        if 'APOCALYPSIS SEDRACH' in l: continue
        if re.search(r'^\d+\s+APOCALYPSIS', l): continue
        if 'The remainder of the Homily is omitted' in l: continue
        # Strip marginal line numbers
        l = re.sub(r'\s+\b(5|10|15|20|25|30|35)\b\s*$', '', l)
        cleaned_lines.append(l)

    text = ' '.join(cleaned_lines)
    # Normalize Greek uppercase header
    title_incipit = "ΤΟΥ͂ ἁγίου καὶ μακαρίου Σεδρὰχ λόγος περὶ ἀγάπης καὶ περὶ μετανοίας καὶ ὀρθοδόξων Χριστιανῶν καὶ περὶ δευτέρας παρουσίας τοῦ κυρίου ἡμῶν Ἰησοῦ Χριστοῦ. Δέσποτα εὐλόγησον."

    # Split into 16 chapters based on Roman numerals
    # Roman numerals in James 1893:
    # I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII, XIII, XIV, XV, XVI
    ch_patterns = [
        (1, r'(?:I\s*a\.|I\.|1\.)[\s\S]{1,30}(?:[᾿\']?Αγαπητοὶ|Ἀγαπητοὶ|[;:]\s*γαπητοὶ)'),
        (2, r'(?:II\.|ΙΙ\.|Il\.|2\.)\s+(?:Καὶ|Kat)\s+φωνὴν\s+ἀοράτως'),
        (3, r'(?:III\.|ΙΙΙ\.)\s+Καὶ λέγει αὐτὸν ὁ κύριος'),
        (4, r'(?:IV\.|ΙV\.)\s+Λέγει αὐτῷ Σεδράχ'),
        (5, r'(?:V\.|V\.)\s+Λέγει αὐτῷ Σεδράχ'),
        (6, r'(?:VI\.|VΙ\.)\s+Λέγει αὐτὸν ὁ θεός'),
        (7, r'(?:VII\.|VΙΙ\.)\s+Λέγει αὐτῷ Σεδράχ'),
        (8, r'(?:VIII\.|VΙΙΙ\.)\s+Λέγει αὐτῷ ὁ θεός'),
        (9, r'(?:IX\.|ΙX\.)\s+Καὶ εἶπεν ὁ θεὸς τὸν υἱὸν'),
        (10, r'(?:X\.|Χ\.)\s+Καὶ εἶπεν Σεδρὰχ τὸν θεόν'),
        (11, r'(?:XI\.|ΧΙ\.)\s+Καὶ ἤρξατο κλαίων'),
        (12, r'(?:XII\.|ΧΙΙ\.|ΧΙ\]\.)\s*Λέγει αὐτὸν ὁ Χριστός'),
        (13, r'(?:XIII\.|ΧΙΙΙ\.)\s+Λέγει αὐτῷ Σεδράχ'),
        (14, r'(?:XIV\.|ΧΙV\.)\s+Καὶ λέγει Σεδρὰχ πρὸς τὸν ἀρχάγγελον'),
        (15, r'(?:XV\.|ΧV\.)\s+Λέγει Σεδρὰχ πρὸς τὸν θεόν'),
        (16, r'(?:XVI\.|ΧVΙ\.)\s+Λέγει κύριος τὸν Σεδράχ')
    ]

    # Find positions
    positions = []
    for ch_num, pat in ch_patterns:
        m = re.search(pat, text)
        if m:
            positions.append((ch_num, m.start()))
        else:
            print(f"Warning: pattern for Ch {ch_num} not found directly with {pat}")

    # Sort by start pos
    positions.sort(key=lambda x: x[1])
    
    chapters = {}
    for i, (ch_num, pos) in enumerate(positions):
        next_pos = positions[i+1][1] if i+1 < len(positions) else len(text)
        ch_raw = text[pos:next_pos].strip()
        # strip chapter numeral prefix
        ch_raw = re.sub(r'^(?:[IΙVΧX1-9\.]+\s+)+', '', ch_raw).strip()
        # Clean stray OCR marks
        ch_raw = re.sub(r'\[f\.\s*\d+[a-z]?\]', '', ch_raw)
        ch_raw = re.sub(r'\s+', ' ', ch_raw).strip()
        
        # Split chapter into verses at punctuation (. or ; or :)
        v_tokens = re.split(r'(?<=[.·;:])\s+', ch_raw)
        # Combine very short tokens if any
        verses = []
        buf = ""
        for tok in v_tokens:
            tok = tok.strip()
            if not tok: continue
            if buf:
                buf += " " + tok
            else:
                buf = tok
            if len(buf.split()) >= 4 or tok.endswith(('.', ';', '·')):
                verses.append(buf)
                buf = ""
        if buf:
            if verses:
                verses[-1] += " " + buf
            else:
                verses.append(buf)
                
        chapters[ch_num] = verses

    # XML generation
    bib = ("Montague Rhodes James, Apocrypha Anecdota: A Collection of Thirteen Apocryphal Books and Fragments "
           "(Texts and Studies 2.3; Cambridge: Cambridge University Press, 1893), pp. 127-137. "
           "Critical Greek text from Oxford Bodleian MS Misc. Gr. 56 (Auct. T. 2. 26).")
    
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="Sedrach" title="Apocalypse of Sedrach">',
        '  <version author="James 1893" language="Greek" title="Greek">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="James" language="Greek" show="yes">',
        '        <name>James 1893 (Texts &amp; Studies 2.3)</name>',
        f'        <bibliography>{escape(bib)}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>'
    ]

    unit_id = 0
    for ch_num in sorted(chapters.keys()):
        lines.append(f'      <div number="{ch_num}">')
        for v_num, v_text in enumerate(chapters[ch_num], 1):
            lines.append(f'        <div number="{v_num}">')
            lines.append(f'          <unit id="{unit_id}">')
            lines.append(f'            <reading option="0" mss="James ">{escape(v_text)}</reading>')
            lines.append('          </unit>')
            lines.append('        </div>')
            unit_id += 1
        lines.append('      </div>')

    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>')

    xml_content = '\n'.join(lines) + '\n'
    out_path = 'static/docs/Sedrach.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote {out_path} with {len(chapters)} chapters and {unit_id} verses.")


def build_apoc_ezra():
    print("Building Greek Apocalypse of Ezra...")
    # Read the clean text
    with open('raw/editions/Apoc_Esdrae_pure.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Normalize Greek characters and fix common OCR substitutions
    text = text.replace('Δόγος', 'Λόγος')
    text = text.replace('χαὶ', 'καὶ')
    text = text.replace('χόλασιν', 'κόλασιν')
    text = text.replace('χρίσεως', 'κρίσεως')
    text = text.replace('χρίσεις', 'κρίσεις')
    text = text.replace('χρίσιν', 'κρίσιν')
    text = text.replace('χρίνον', 'κρῖνον')
    text = text.replace('δύκαιον', 'δίκαιον')
    text = text.replace('δύκαιοι', 'δίκαιοι')
    text = text.replace('᾿Εσδρῦὺμ', 'Ἐσδράμ')
    text = text.replace('᾿Εσδρὰμ', 'Ἐσδράμ')
    text = text.replace('᾿Εσδοάμ', 'Ἐσδράμ')
    text = text.replace('ὄἜγζετο', 'Ἐγένετο')
    text = text.replace('Χοιστιανῶν', 'Χριστιανῶν')
    text = text.replace('Π. ἈΡΟΟΛΙΥ͂ΡΘΙ9 ΕΒΡΒΛΕ,', '')
    
    # Remove Latin apparatus leftovers that crept in
    text = re.sub(r'ἀναπαύσωμαι:[^ἐ]+(?=ἐποίησα)', '', text)
    text = re.sub(r'Ω ΕΝ [^ἄ]+(?=ἄμμον)', '', text)
    text = re.sub(r'ν᾿\s*,\s*᾿\s*,\s*“\s*,\s*\.\s*,\s*2\s*', '', text)
    text = re.sub(r'\s+[0-9]{1,2}\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 7 Chapters division based on standard boundaries (Wahl 1977 / Stone 1983):
    ch_starts = [
        (1, r'Λόγος καὶ ἀποκάλυψις'),
        (2, r'ὡς ἐποίησα νύκτα καὶ ἡμέραν'),
        (3, r'ἐξαρίθμησον τοὺς ἀστέρας'),
        (4, r'μέρη τοῦ ταρτάρου'),
        (5, r'στόμα αὐτοῦ πῆχυς μία'),
        (6, r'Οὐριήλ|Γαβριήλ'),
        (7, r'χλαύσατέ με|κλαύσατέ με|παρέδωκεν τὴν τιμίαν')
    ]

    positions = []
    for ch_num, pat in ch_starts:
        m = re.search(pat, text)
        if m:
            positions.append((ch_num, m.start()))
        else:
            print(f"Warning: Ch {ch_num} start not found with {pat}")

    positions.sort(key=lambda x: x[1])

    chapters = {}
    for i, (ch_num, pos) in enumerate(positions):
        next_pos = positions[i+1][1] if i+1 < len(positions) else len(text)
        ch_raw = text[pos:next_pos].strip()
        ch_raw = re.sub(r'\s+', ' ', ch_raw).strip()
        
        v_tokens = re.split(r'(?<=[.·;:])\s+', ch_raw)
        verses = []
        buf = ""
        for tok in v_tokens:
            tok = tok.strip()
            if not tok: continue
            if buf:
                buf += " " + tok
            else:
                buf = tok
            if len(buf.split()) >= 5 or tok.endswith(('.', ';', '·')):
                verses.append(buf)
                buf = ""
        if buf:
            if verses:
                verses[-1] += " " + buf
            else:
                verses.append(buf)
        chapters[ch_num] = verses

    bib = ("Constantin von Tischendorf, Apocalypses Apocryphae Mosis, Esdrae, Pauli, Iohannis, item Mariae Dormitio "
           "(Leipzig: Hermann Mendelssohn, 1866), pp. 24-33. "
           "Editio princeps based on Paris, Bibliothèque nationale de France, MS grec 929.")

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE book SYSTEM "grammateus.dtd">',
        '<book filename="ApEzra" title="Greek Apocalypse of Ezra">',
        '  <version author="Tischendorf 1866" language="Greek" title="Greek">',
        '    <divisions>',
        '      <division delimiter="." label="Chapter"/>',
        '      <division label="Verse"/>',
        '    </divisions>',
        '    <manuscripts>',
        '      <ms abbrev="Tisch" language="Greek" show="yes">',
        '        <name>Tischendorf 1866 (Apocalypses Apocryphae)</name>',
        f'        <bibliography>{escape(bib)}</bibliography>',
        '      </ms>',
        '    </manuscripts>',
        '    <text>'
    ]

    unit_id = 0
    for ch_num in sorted(chapters.keys()):
        lines.append(f'      <div number="{ch_num}">')
        for v_num, v_text in enumerate(chapters[ch_num], 1):
            lines.append(f'        <div number="{v_num}">')
            lines.append(f'          <unit id="{unit_id}">')
            lines.append(f'            <reading option="0" mss="Tisch ">{escape(v_text)}</reading>')
            lines.append('          </unit>')
            lines.append('        </div>')
            unit_id += 1
        lines.append('      </div>')

    lines.append('    </text>')
    lines.append('  </version>')
    lines.append('</book>')

    xml_content = '\n'.join(lines) + '\n'
    out_path = 'static/docs/ApEzra.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Wrote {out_path} with {len(chapters)} chapters and {unit_id} verses.")

if __name__ == '__main__':
    build_sedrach()
    build_apoc_ezra()
