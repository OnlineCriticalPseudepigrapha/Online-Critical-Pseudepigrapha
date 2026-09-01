#!/usr/bin/env python3
"""
Automated OCP Translation Generator & Injector

Translates OCP XML editions into a target language aligned to the base critical
readings (Option 0) and injects valid <version language="<Target>" ...>
structures conforming to grammateus.dtd.

Usage: python3 scripts/generate_translations.py --language French <xml> [...]
"""

import sys
import os
import json
import time
import subprocess
import xml.etree.ElementTree as ET

OPENROUTER_MODEL = "openrouter/google/gemini-3.7-flash"

DEFAULT_LANGUAGE = "French"


def extract_units(elem):
    """
    Recursively extracts reference path, unit ID, and Option 0 text for each unit in an element.
    Returns list of dicts: [{'path': ['1', '2'], 'ref': '1:2', 'id': '1', 'text': '...'}]
    """
    text_elem = elem.find('text') if elem.find('text') is not None else elem
    units_data = []

    def traverse(child_elem, current_path):
        for child in child_elem:
            tag = child.tag.lower()
            if tag in ['div', 'chapter', 'verse']:
                num = child.attrib.get('number') or child.attrib.get('reference') or child.attrib.get('n') or str(len(current_path) + 1)
                traverse(child, current_path + [num])
            elif tag == 'unit':
                u_id = child.attrib.get('id', '')
                # Find option 0 reading or first reading
                rdg = child.find("reading[@option='0']")
                if rdg is None:
                    rdg = child.find('reading')
                
                txt = "".join(rdg.itertext()) if rdg is not None else ""
                txt_clean = " ".join(txt.split())
                ref_str = ":".join(current_path) if current_path else "1"
                
                units_data.append({
                    'path': list(current_path),
                    'ref': ref_str,
                    'id': u_id,
                    'text': txt_clean
                })

    traverse(text_elem, [])
    return units_data


def translate_units_batch(doc_title, version_title, lang, target_language, units_batch, retries=3):
    """
    Sends a batch of units to LLM to produce a scholarly translation in target_language.
    Returns dict mapping unit 'id' -> translation string.
    """
    if not units_batch:
        return {}

    prompt_items = []
    for u in units_batch:
        prompt_items.append({
            'id': u['id'],
            'ref': u['ref'],
            'original_text': u['text']
        })

    system_prompt = (
        f"You are an expert biblical scholar and classical translator specializing in the Old Testament Pseudepigrapha "
        f"(Greek, Syriac, Latin, Ethiopic, Aramaic). Translate the provided ancient text units into clear, accurate, "
        f"scholarly modern {target_language} suitable for the Online Critical Pseudepigrapha (OCP) digital editions. "
        f"Preserve proper names, titles, and biblical/historical references. "
        f"IMPORTANT: if a unit's original text is an omission marker (e.g. '[...]') or is empty, return the empty "
        f"string \"\" for that unit — do NOT emit '[...]' or any placeholder. "
        f"Return ONLY a JSON object mapping each unit 'id' (as a string) to its corresponding {target_language} "
        f"translation string. Do not include markdown code blocks or additional commentary."
    )

    user_prompt = f"Document: {doc_title}\nVersion/Fragment: {version_title} ({lang})\n\nUnits to translate:\n" + json.dumps(prompt_items, ensure_ascii=False, indent=2)

    for attempt in range(retries):
        try:
            cmd = ["llm", "-m", OPENROUTER_MODEL, "--system", system_prompt, user_prompt]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
            if res.returncode != 0:
                raise RuntimeError(f"llm command failed: {res.stderr}")

            raw_out = res.stdout.strip()
            if raw_out.startswith("```"):
                raw_out = raw_out.split("\n", 1)[1]
                if raw_out.endswith("```"):
                    raw_out = raw_out.rsplit("\n", 1)[0]
            raw_out = raw_out.strip()

            translated_map = json.loads(raw_out)
            return translated_map
        except Exception as e:
            print(f"    [Attempt {attempt+1}/{retries}] Error translating batch: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
            else:
                raise


def build_translation_version_xml(source_elem, translated_map, units_data, ver_title="Translation", ver_author="OCP", target_language="English", lang_code="en"):
    """
    Constructs a new <version language="English" ...> ElementTree reproducing the division structure.
    """
    new_v = ET.Element('version')
    new_v.attrib['title'] = ver_title
    new_v.attrib['author'] = ver_author
    new_v.attrib['language'] = target_language
    if 'fragment' in source_elem.attrib:
        new_v.attrib['fragment'] = source_elem.attrib['fragment']

    # Copy divisions if present
    src_divs = source_elem.find('divisions')
    if src_divs is not None:
        new_v.append(ET.fromstring(ET.tostring(src_divs, encoding='unicode')))
    else:
        divs = ET.SubElement(new_v, 'divisions')
        d1 = ET.SubElement(divs, 'division')
        d1.attrib['label'] = 'Chapter'
        d1.attrib['delimiter'] = ':'
        d2 = ET.SubElement(divs, 'division')
        d2.attrib['label'] = 'Verse'

    # Add manuscripts
    mss = ET.SubElement(new_v, 'manuscripts')
    ms = ET.SubElement(mss, 'ms')
    ms.attrib['abbrev'] = 'OCP-Trans'
    ms.attrib['language'] = target_language
    ms.attrib['show'] = 'yes'
    name_el = ET.SubElement(ms, 'name')
    name_el.text = f'OCP {target_language} Translation'
    bib_el = ET.SubElement(ms, 'bibliography')
    bib_el.text = f'{target_language} translation of {ver_title} based on the OCP critical edition.'

    # Construct text tree
    text_elem = ET.SubElement(new_v, 'text')
    div_cache = {}

    for u in units_data:
        path = u['path']
        u_id = u['id']
        en_text = translated_map.get(str(u_id)) or translated_map.get(u_id) or ""
        # Omissions / untranslated units render as empty strings (zero-length),
        # not '[...]' — per OCP convention.
        if en_text == "[...]":
            en_text = ""

        current_parent = text_elem
        for i in range(len(path)):
            sub_path = tuple(path[:i+1])
            if sub_path not in div_cache:
                new_div = ET.SubElement(current_parent, 'div')
                new_div.attrib['number'] = path[i]
                div_cache[sub_path] = new_div
            current_parent = div_cache[sub_path]

        unit_el = ET.SubElement(current_parent, 'unit')
        unit_el.attrib['id'] = f"{lang_code}_{u_id}"
        unit_el.attrib['group'] = '0'
        unit_el.attrib['parallel'] = ''

        rdg_el = ET.SubElement(unit_el, 'reading')
        rdg_el.attrib['option'] = '0'
        rdg_el.attrib['mss'] = 'OCP-Trans '
        rdg_el.text = en_text

    return new_v


def process_file(xml_path, batch_size=50, target_language=DEFAULT_LANGUAGE):
    """Processes an entire XML file, generating and appending English version(s)."""
    print(f"\nProcessing {xml_path}...")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    doc_title = root.attrib.get('title', os.path.basename(xml_path))

    existing_versions = root.findall('version')

    # Case 1: Direct root structure without <version> tags (e.g. Esdr.xml)
    if not existing_versions:
        units_data = extract_units(root)
        print(f"  Root structure (no <version> tags): {len(units_data)} units to translate.")
        if not units_data:
            return

        # Wrap existing root content into a <version> element
        base_v = ET.Element('version')
        base_v.attrib['title'] = root.attrib.get('title', 'Original')
        base_v.attrib['language'] = root.attrib.get('language', 'Latin')
        base_v.attrib['author'] = 'Anonymous'
        for child in list(root):
            base_v.append(child)
            root.remove(child)
        root.append(base_v)
        existing_versions = [base_v]

    # Check if a translation in the target language already exists
    lang_lower = target_language.lower()
    has_target = any(lang_lower in (v.attrib.get('language') or '').lower() for v in existing_versions)
    if has_target:
        print(f"  Document already contains {target_language} version(s). Skipping.")
        return

    new_versions = []
    lang_code = lang_lower[:2]

    for v_idx, v_elem in enumerate(existing_versions):
        v_title = v_elem.attrib.get('title') or root.attrib.get('title') or f'Version {v_idx+1}'
        v_lang = v_elem.attrib.get('language') or root.attrib.get('language') or 'Greek'
        units_data = extract_units(v_elem)
        print(f"  Version [{v_idx}] '{v_title}' ({v_lang}): {len(units_data)} units to translate.")

        if not units_data:
            continue

        translated_map = {}
        for i in range(0, len(units_data), batch_size):
            chunk = units_data[i:i+batch_size]
            print(f"    Translating units {i+1} to {min(i+batch_size, len(units_data))}...")
            chunk_res = translate_units_batch(doc_title, v_title, v_lang, target_language, chunk)
            translated_map.update(chunk_res)
            time.sleep(0.5)

        if len(existing_versions) == 1:
            tr_title = target_language
        else:
            tr_title = f"{v_title} ({target_language})"

        new_v_elem = build_translation_version_xml(v_elem, translated_map, units_data, ver_title=tr_title, target_language=target_language, lang_code=lang_code)
        new_versions.append(new_v_elem)

    for nv in new_versions:
        root.append(nv)

    xml_str = ET.tostring(root, encoding='utf-8')
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')
    
    lines = [line for line in pretty_xml.splitlines() if line.strip()]
    cleaned_xml = "\n".join(lines) + "\n"

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_xml)

    print(f"  Successfully updated {xml_path} with {len(new_versions)} {target_language} version(s).")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Generate OCP parallel translations in a target language.")
    parser.add_argument("xml_files", nargs="+", help="Path(s) to OCP XML edition files")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help=f"Target language (default: {DEFAULT_LANGUAGE})")
    parser.add_argument("--batch-size", type=int, default=50)
    args = parser.parse_args()

    for p in args.xml_files:
        try:
            process_file(p, batch_size=args.batch_size, target_language=args.language)
        except Exception as e:
            print(f"Error processing {p}: {e}", file=sys.stderr)
