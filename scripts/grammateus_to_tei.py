#!/usr/bin/env python3
"""
grammateus_to_tei.py — Convert OCP Grammateus DTD XML to TEI P5 XML

Transforms Online Critical Pseudepigrapha (OCP) multi-witness documents
into valid TEI P5 (textcrit module, parallel segmentation method)
compliant with tei_all.rng.

Usage:
    python3 scripts/grammateus_to_tei.py static/docs/PssSol.xml -o static/docs/tei/PssSol.xml --validate
    python3 scripts/grammateus_to_tei.py --all --validate
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import OrderedDict
import lxml.etree as ET
from lxml.builder import ElementMaker

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
E = ElementMaker(namespace=TEI_NS, nsmap={None: TEI_NS})

# Language name to ISO 639 code mapping
LANG_MAP = {
    "greek": "grc",
    "aramaic": "arc",
    "syriac": "syr",
    "hebrew": "he",
    "latin": "la",
    "ethiopic": "gez",
    "coptic": "cop",
    "slavonic": "chu",
    "english": "en",
    "french": "fr",
    "german": "de",
    "arabic": "ar"
}

def normalize_lang(lang_str):
    if not lang_str:
        return "und"
    clean = lang_str.strip().lower()
    return LANG_MAP.get(clean, clean[:3] if len(clean) >= 3 else clean)

def clean_xml_id(val, prefix=""):
    """Produce a valid XML NCName."""
    s = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", str(val).strip())
    if not s or not (s[0].isalpha() or s[0] == "_"):
        s = f"{prefix}{s}" if prefix else f"id_{s}"
    return s

def clean_text_content(text):
    if not text:
        return ""
    # Normalize excessive spaces while keeping single spaces
    return " ".join(text.split())

def convert_document(src_path, intros_data=None, schema=None):
    """Convert a single Grammateus XML file to a TEI P5 lxml element."""
    tree = ET.parse(src_path)
    book_elem = tree.getroot()
    if book_elem.tag != "book":
        raise ValueError(f"Root tag is not <book>: {book_elem.tag}")

    filename = book_elem.get("filename") or os.path.splitext(os.path.basename(src_path))[0]
    book_title = book_elem.get("title") or filename
    text_structure = book_elem.get("textStructure") or "criticalApparatus"

    # Match metadata from intros.json if available
    doc_meta = {}
    if intros_data:
        basename = os.path.basename(src_path)
        doc_meta = intros_data.get("documents", {}).get(basename, {})

    # Extract all manuscripts across book and versions
    all_mss = OrderedDict()
    for ms in book_elem.findall(".//ms"):
        abbrev = ms.get("abbrev", "").strip()
        if abbrev and abbrev not in all_mss:
            name_el = ms.find("name")
            name_text = clean_text_content(name_el.text) if name_el is not None else abbrev
            bib_el = ms.find("bibliography")
            bib_text = clean_text_content(bib_el.text) if bib_el is not None else ""
            lang = ms.get("language") or ""
            all_mss[abbrev] = {
                "id": clean_xml_id(abbrev, prefix="wit-"),
                "abbrev": abbrev,
                "name": name_text,
                "bibl": bib_text,
                "lang": normalize_lang(lang)
            }

    # Extract global and version languages
    version_elems = book_elem.findall("version")
    if not version_elems:
        version_elems = [book_elem]

    primary_lang = "grc"
    if version_elems:
        v_lang = version_elems[0].get("language")
        if v_lang:
            primary_lang = normalize_lang(v_lang)

    # 1. <teiHeader>
    # Title statement
    title_el = E.title(doc_meta.get("title") or book_title)
    title_stmt_children = [title_el]

    # Editors from citation or default OCP editors
    citation_text = doc_meta.get("citation", "")
    editors_found = []
    if citation_text:
        # e.g. Evans, Craig A., Ken M. Penner, and Ian W. Scott, eds.
        m = re.search(r"^<p>([^,]+(?:,[^,]+)*?),\s*(?:eds\.|ed\.)", citation_text)
        if m:
            ed_str = m.group(1).replace("and ", "").replace("<em>", "").replace("</em>", "")
            for ed in ed_str.split(";"):
                ed = ed.strip()
                if ed:
                    editors_found.append(ed)

    if editors_found:
        for ed in editors_found:
            title_stmt_children.append(E.editor(ed, role="editor"))
    else:
        title_stmt_children.extend([
            E.editor("Ken M. Penner", role="editor"),
            E.editor("Ian W. Scott", role="editor"),
            E.editor("David M. Miller", role="editor")
        ])

    title_stmt_children.append(
        E.respStmt(
            E.resp("TEI P5 conversion from OCP Grammateus XML"),
            E.name("Online Critical Pseudepigrapha")
        )
    )

    # Publication statement
    pub_stmt = E.publicationStmt(
        E.authority("Online Critical Pseudepigrapha"),
        E.pubPlace("Antigonish, NS"),
        E.date("2026"),
        E.availability(
            E.licence(
                "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                target="https://creativecommons.org/licenses/by/4.0/"
            ),
            status="free"
        )
    )

    # Source description & Witness list (<listWit>)
    witness_elements = []
    for ms_info in all_mss.values():
        wit_children = [
            E.abbr(ms_info["abbrev"], type="siglum"),
            E.name(ms_info["name"])
        ]
        if ms_info["bibl"]:
            wit_children.append(E.bibl(ms_info["bibl"]))
        wit_el = E.witness(*wit_children)
        wit_el.set(f"{{{XML_NS}}}id", ms_info["id"])
        witness_elements.append(wit_el)

    source_desc_children = []
    if witness_elements:
        source_desc_children.append(E.listWit(*witness_elements))
    else:
        source_desc_children.append(E.p("Critical edition based on standard textual witnesses."))

    source_desc = E.sourceDesc(*source_desc_children)

    # Collect refsDecl per version
    refs_decls = []
    seen_vcodes = set()
    version_vcodes = []
    for v_idx, v_elem in enumerate(version_elems):
        v_title = (v_elem.get("title") or "").strip()
        v_lang_name = (v_elem.get("language") or "").strip()
        if not v_title:
            if v_elem.tag == "book":
                v_title = book_title
            elif v_lang_name:
                v_title = v_lang_name
            else:
                v_title = f"Version {v_idx + 1}"
        v_code = f"ver_{clean_xml_id(v_title or f'v{v_idx + 1}')}"
        if v_code in seen_vcodes:
            v_code = f"{v_code}_{v_idx + 1}"
        seen_vcodes.add(v_code)
        version_vcodes.append(v_code)

        div_states = []
        for d in v_elem.findall("divisions/division"):
            lbl = (d.get("label") or "section").strip()
            delim = d.get("delimiter")
            attrs = {"unit": clean_xml_id(lbl.lower())}
            if delim:
                attrs["delim"] = delim
            div_states.append(attrs)

        if div_states:
            refs_attrs = {}
            if len(version_elems) > 1:
                refs_attrs["corresp"] = f"#{v_code}"
            refs_decls.append(
                E.refsDecl(*[E.refState(**attrs) for attrs in div_states], **refs_attrs)
            )

    # Encoding description
    encoding_desc_children = [
        E.projectDesc(
            E.p("The Online Critical Pseudepigrapha (OCP) provides digital critical editions of Jewish and Christian pseudepigrapha with a dynamic, base-text invariant multi-witness apparatus.")
        ),
        E.editorialDecl(
            E.p("Encoded using the TEI P5 textcrit module (Parallel Segmentation method). Variants and witness transcriptions are recorded using <app>, <lem>, and <rdg> elements.")
        )
    ]
    encoding_desc_children.extend(refs_decls)

    header_children = [
        E.fileDesc(
            E.titleStmt(*title_stmt_children),
            pub_stmt,
            source_desc
        ),
        E.encodingDesc(*encoding_desc_children),
        E.profileDesc(
            E.langUsage(
                E.language(primary_lang, ident=primary_lang)
            )
        )
    ]
    tei_header = E.teiHeader(*header_children)

    # 2. <text> and <body>
    body_divisions = []

    for v_idx, v_elem in enumerate(version_elems):
        v_title = (v_elem.get("title") or "").strip()
        v_lang_name = (v_elem.get("language") or "").strip()
        if not v_lang_name:
            first_ms = v_elem.find(".//ms")
            if first_ms is not None and first_ms.get("language"):
                v_lang_name = first_ms.get("language").strip()
        v_lang_code = normalize_lang(v_lang_name)
        if not v_title:
            if v_elem.tag == "book":
                v_title = book_title
            elif v_lang_name:
                v_title = v_lang_name
            else:
                v_title = f"Version {v_idx + 1}"
        v_author = v_elem.get("author") or ""

        # Distinguish primary edition vs translation
        is_trans = ("translation" in v_title.lower() or 
                    "english" in v_title.lower() or 
                    "french" in v_title.lower() or
                    v_lang_code in ("en", "fr"))
        div_type = "translation" if is_trans else "edition"

        # Division hierarchy labels
        div_labels = []
        for d in v_elem.findall("divisions/division"):
            lbl = d.get("label") or "section"
            div_labels.append(lbl.lower())

        text_elem = v_elem.find("text")
        if text_elem is None:
            text_elem = v_elem

        v_code = version_vcodes[v_idx]
        seen_ids = set()

        def make_unique_id(candidate):
            cid = clean_xml_id(candidate)
            if cid not in seen_ids:
                seen_ids.add(cid)
                return cid
            counter = 2
            while f"{cid}_{counter}" in seen_ids:
                counter += 1
            unique_cid = f"{cid}_{counter}"
            seen_ids.add(unique_cid)
            return unique_cid

        # Convert recursive <div> structure
        def convert_div(d_elem, level=0, path=None):
            if path is None:
                path = [v_code]
            d_num = d_elem.get("number", "").strip()
            current_path = path + [d_num] if d_num else path
            label = div_labels[level] if level < len(div_labels) else "section"
            id_str = make_unique_id(".".join([filename] + current_path))
            
            # Check if this div directly contains units or nested divs
            child_divs = [c for c in d_elem if c.tag == "div"]
            child_units = [c for c in d_elem if c.tag == "unit"]

            if child_divs:
                div_children = []
                if d_num and d_num != "0":
                    div_children.append(E.head(f"{label.capitalize()} {d_num}"))
                for c_div in child_divs:
                    div_children.append(convert_div(c_div, level + 1, path=current_path))
                new_div = E.div(*div_children, type=label, n=d_num)
                if d_num:
                    new_div.set(f"{{{XML_NS}}}id", id_str)
                return new_div
            elif child_units:
                # Leaf level containing text units (typically verse or phrase)
                ab_children = []
                for u in child_units:
                    u_id = u.get("id", "").strip()
                    group = u.get("group", "0")
                    parallel = u.get("parallel", "").strip()

                    # Readings
                    rdg_elems = u.findall("reading")
                    app_children = []
                    has_lem = False
                    for r in rdg_elems:
                        opt = r.get("option", "0")
                        mss_str = r.get("mss", "").strip()
                        linebreak = r.get("linebreak", "")
                        indent = r.get("indent", "")
                        r_text = clean_text_content("".join(r.itertext()))

                        # Convert mss sigla to witness pointers: e.g. "149 253" -> "#wit-149 #wit-253"
                        wit_pointers = []
                        if mss_str:
                            for sig in mss_str.split():
                                wit_id = all_mss.get(sig, {}).get("id") or clean_xml_id(sig, prefix="wit-")
                                wit_pointers.append(f"#{wit_id}")
                        wit_attr = " ".join(wit_pointers) if wit_pointers else None

                        is_omission = (len(r_text) == 0)

                        attrs = {}
                        if wit_attr:
                            attrs["wit"] = wit_attr
                        if opt != "0":
                            attrs["n"] = opt
                        if is_omission:
                            attrs["type"] = "omission"

                        # Reading content
                        r_content = []
                        if r_text:
                            r_content.append(r_text)
                        if linebreak == "following" or linebreak == "both":
                            r_content.append(E.lb())

                        # Option 0 is lemma; others are variants. At most one <lem> allowed per <app>.
                        if opt == "0" and not has_lem:
                            app_children.append(E.lem(*r_content, **attrs))
                            has_lem = True
                        else:
                            if opt == "0":
                                attrs["n"] = "0"
                            app_children.append(E.rdg(*r_content, **attrs))

                    app_attrs = {}
                    if u_id:
                        app_attrs[f"{{{XML_NS}}}id"] = make_unique_id(f"u{u_id}_{v_code}")
                    if group and group != "0":
                        app_attrs["subtype"] = f"group-{group}"
                    if parallel:
                        app_attrs["corresp"] = f"#{parallel}"

                    app_el = E.app(*app_children, **app_attrs)
                    ab_children.append(app_el)

                ab_attrs = {"type": label, "n": d_num}
                if d_num:
                    ab_attrs[f"{{{XML_NS}}}id"] = id_str
                return E.ab(*ab_children, **ab_attrs)
            else:
                return E.div(type=label, n=d_num)

        # Process top-level divisions under text
        top_divs = [c for c in text_elem if c.tag == "div"]
        version_div_children = [E.head(v_title)]
        for td in top_divs:
            version_div_children.append(convert_div(td, 0, path=[v_code]))

        v_div = E.div(*version_div_children, type=div_type, n=v_title)
        v_div.set(f"{{{XML_NS}}}lang", v_lang_code)
        v_div.set(f"{{{XML_NS}}}id", v_code)
        body_divisions.append(v_div)

    text_el = E.text(E.body(*body_divisions))
    text_el.set(f"{{{XML_NS}}}lang", primary_lang)

    tei_root = E.TEI(tei_header, text_el)
    tei_root.set(f"{{{XML_NS}}}id", clean_xml_id(filename))

    return tei_root

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_files", nargs="*", help="Specific Grammateus XML files to convert")
    parser.add_argument("--all", action="store_true", help="Convert all XML files in --in-dir")
    parser.add_argument("--in-dir", default="static/docs", help="Source directory containing Grammateus XML")
    parser.add_argument("--out-dir", default="static/docs/tei", help="Output directory for TEI P5 XML files")
    parser.add_argument("-o", "--output", help="Output path when converting a single file")
    parser.add_argument("--intros", default="static/docs/intros.json", help="Path to intros.json metadata")
    parser.add_argument("--validate", action="store_true", help="Validate converted files against TEI RelaxNG schema")
    parser.add_argument("--schema", default="../Revell/schema/tei_all.rng", help="Path to tei_all.rng schema")
    args = parser.parse_args()

    # Load intros.json if present
    intros_data = None
    if os.path.exists(args.intros):
        with open(args.intros, "r", encoding="utf-8") as f:
            intros_data = json.load(f)

    # Load RelaxNG schema if validation requested
    relaxng = None
    if args.validate:
        schema_path = args.schema
        if not os.path.isabs(schema_path):
            schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", schema_path))
        if os.path.exists(schema_path):
            print(f"Loading TEI schema: {schema_path}")
            schema_doc = ET.parse(schema_path)
            relaxng = ET.RelaxNG(schema_doc)
            print("Schema loaded successfully.")
        else:
            print(f"Warning: Schema not found at {schema_path}. Validation will be skipped.")

    # Determine files to process
    if args.all:
        files = sorted(glob.glob(os.path.join(args.in_dir, "*.xml")))
        files = [f for f in files if not f.endswith("_TEI.xml") and not os.path.basename(f).startswith(".")]
    elif args.input_files:
        files = args.input_files
    else:
        parser.error("Specify input files or --all")

    os.makedirs(args.out_dir, exist_ok=True)

    success_count = 0
    fail_count = 0

    for src in files:
        base = os.path.basename(src)
        # Skip zero-byte files
        if os.path.getsize(src) == 0:
            print(f"Skipping empty file: {src}")
            continue

        if args.output and len(files) == 1:
            out_path = args.output
        else:
            out_path = os.path.join(args.out_dir, base)

        try:
            print(f"Converting {base} -> {out_path} ...")
            tei_tree = convert_document(src, intros_data=intros_data)

            # Validate if schema loaded
            if relaxng is not None:
                is_valid = relaxng.validate(tei_tree)
                if not is_valid:
                    print(f"  [VALIDATION WARNING] {base} had validation issues:")
                    for err in list(relaxng.error_log)[:5]:
                        print(f"    - {err}")
                else:
                    print(f"  [VALID] TEI P5 RelaxNG validation passed.")

            # Save XML
            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            xml_bytes = ET.tostring(tei_tree, encoding="utf-8", xml_declaration=True, pretty_print=True)
            with open(out_path, "wb") as f:
                f.write(xml_bytes)

            success_count += 1
        except Exception as e:
            print(f"  [ERROR] Failed to convert {src}: {e}")
            fail_count += 1

    print(f"\nSummary: {success_count} files converted successfully, {fail_count} failed.")

if __name__ == "__main__":
    main()
