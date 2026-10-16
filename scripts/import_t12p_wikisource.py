"""Import the Greek Testaments of the Twelve Patriarchs from el.wikisource into Grammateus XML.

Source: https://el.wikisource.org/wiki/Διαθήκαι_των_ΙΒ'_Πατριαρχών (public domain; edition not
stated on the page, apparently R. H. Charles's 1908 base text). Collate against Charles before
treating it as an edition of record.
    python3 scripts/import_t12p_wikisource.py   ->  static/docs/T12P.xml
"""
import re, sys, urllib.parse, urllib.request
from xml.sax.saxutils import escape, quoteattr

TITLE = "Διαθήκαι των ΙΒ' Πατριαρχών"
url = "https://el.wikisource.org/w/index.php?action=raw&title=" + urllib.parse.quote(TITLE)
wiki = sys.stdin.read() if not sys.stdin.isatty() else urllib.request.urlopen(url).read().decode()
NAMES = ["Reuben", "Simeon", "Levi", "Judah", "Issachar", "Zebulun", "Dan", "Naphtali", "Gad", "Asher", "Joseph", "Benjamin"]

out, uid, t, ch, open_ch, open_t = [], 0, -1, None, False, False
for line in wiki.splitlines():
    line = line.strip()
    if m := re.match(r"^==([^=].*?)==$", line):
        if open_ch: out.append("        </div>")
        if open_t: out.append("      </div>")
        t += 1; open_t, open_ch = True, False
        out.append(f'      <div number={quoteattr(NAMES[t])}>')
        uid += 1
        out.append(f'        <div number="Title">\n          <unit id="{uid}" group="0" parallel="">\n'
                   f'            <reading option="0" mss="Wikisource " linebreak="doubleFollowing">{escape(m.group(1).strip())}</reading>\n          </unit>\n        </div>')
    elif m := re.match(r"^===\s*ΚΕΦΑΛΑΙΟ\s+(\d+)\s*===$", line):
        if open_ch: out.append("        </div>")
        out.append(f'        <div number="{m.group(1)}">'); open_ch = True
    elif (m := re.match(r"^(\d+)\.\s*(.+)$", line)) and open_ch:
        uid += 1
        text = re.sub(r"'''?|\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", lambda x: x.group(1) or "", m.group(2))
        out.append(f'          <div number="{m.group(1)}">\n            <unit id="{uid}" group="0" parallel="">\n'
                   f'              <reading option="0" mss="Wikisource ">{escape(text)} </reading>\n            </unit>\n          </div>')
    elif line and not line.startswith("{{") and open_ch and "<unit" in out[-1]:
        out[-1] = out[-1].replace(" </reading>", " " + escape(line) + " </reading>")  # continuation of previous verse
    elif line and not line.startswith("{{"):
        print("unparsed:", line[:80], file=sys.stderr)
if open_ch: out.append("        </div>")
if open_t: out.append("      </div>")
assert t == 11, f"expected 12 testaments, got {t + 1}"

xml = f"""<?xml version="1.0" encoding="utf-8"?>
<book filename="T12P" title="Testaments of the Twelve Patriarchs">
  <version title="Greek" author="Anonymous" language="Greek">
    <divisions>
      <division label="Testament" delimiter=" "/>
      <division label="Chapter" delimiter=":"/>
      <division label="Verse"/>
    </divisions>
    <manuscripts>
      <ms abbrev="Wikisource" language="Greek" show="yes">
        <name>Wikisource (Charles base text)</name>
        <bibliography>Text: Greek Wikisource, "{TITLE}" (public domain), apparently the base text of R. H. Charles (ed.), The Greek Versions of the Testaments of the Twelve Patriarchs (Oxford: Clarendon, 1908). Provisional: not yet collated against Charles.</bibliography>
      </ms>
    </manuscripts>
    <text>
{chr(10).join(out)}
    </text>
  </version>
</book>
"""
open("static/docs/T12P.xml", "w", encoding="utf-8").write(xml)
print(f"{uid} units in 12 testaments")
