#!/usr/bin/env python3
"""
Generate static/data/catalog.json from data/master_crosswalk.csv,
static/docs/*.xml, static/docs/intros.json, and bibliography/*.md dossiers.
"""
import csv
import json
import os
import re
import xml.etree.ElementTree as ET

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return ' '.join(cleantext.split())

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    crosswalk_path = os.path.join(base_dir, 'data', 'master_crosswalk.csv')
    intros_path = os.path.join(base_dir, 'static', 'docs', 'intros.json')
    docs_dir = os.path.join(base_dir, 'static', 'docs')
    dossiers_dir = os.path.join(base_dir, 'bibliography')
    output_path = os.path.join(base_dir, 'static', 'data', 'catalog.json')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(crosswalk_path, 'r', encoding='utf-8') as f:
        crosswalk = list(csv.DictReader(f))

    intros_json = {}
    if os.path.exists(intros_path):
        with open(intros_path, 'r', encoding='utf-8') as f:
            intros_json = json.load(f).get('documents', {})

    # Extract dossier summaries & overviews
    dossier_data = {}
    if os.path.exists(dossiers_dir):
        for md_file in os.listdir(dossiers_dir):
            if not md_file.endswith('.md'):
                continue
            path = os.path.join(dossiers_dir, md_file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # extract summary paragraph
                    summary = ""
                    m = re.search(r'## 1\.[^\n]*\n+([^#\n][^\n]+(?:\n[^#\n][^\n]+)*)', content)
                    if m:
                        summary = m.group(1).strip()
                    dossier_data[md_file] = {
                        'summary': summary,
                        'full_md': content
                    }
            except Exception:
                pass

    # Inspect XML files
    xml_metadata = {}
    for f in os.listdir(docs_dir):
        if not f.endswith('.xml'):
            continue
        p = os.path.join(docs_dir, f)
        size_kb = round(os.path.getsize(p) / 1024.0, 1)
        mss_count = 1
        mss_langs = []
        try:
            tree = ET.parse(p)
            root = tree.getroot()
            witnesses = root.findall('.//{http://www.tei-c.org/ns/1.0}witness') or root.findall('.//witness') or root.findall('.//msDesc')
            if witnesses:
                mss_count = len(witnesses)
            langs = root.findall('.//{http://www.tei-c.org/ns/1.0}language') or root.findall('.//language')
            for l in langs:
                name = l.text or l.get('ident') or ''
                if name and name.strip() not in mss_langs:
                    mss_langs.append(name.strip())
        except Exception:
            pass
        xml_metadata[f] = {
            'size_kb': size_kb,
            'mss_count': mss_count,
            'mss_langs': mss_langs
        }

    catalog = []
    
    for row in crosswalk:
        ocp_id = row['ocp_canon_id']
        cavt_no = row['cavt_no']
        cant_no = row['cant_no']
        title = row['standard_title']
        section = row['section']
        lang = row['primary_language']
        xml_file = row['ocp_xml']
        dossier_file = row['dossier']
        status_raw = row['status']

        has_xml = bool(xml_file and os.path.exists(os.path.join(docs_dir, xml_file)))
        xml_info = xml_metadata.get(xml_file, {}) if has_xml else {}

        if has_xml:
            status = 'live'
        elif status_raw == 'In Progress / Staged':
            status = 'staged'
        else:
            status = 'gap'

        # Get intro info if XML has one
        intro_obj = intros_json.get(xml_file, {})
        fields = intro_obj.get('fields', {})

        intro_text = ""
        provenance_text = ""
        mss_text = ""
        biblio_text = ""

        if fields:
            intro_text = fields.get('introduction', '')
            provenance_text = fields.get('provenance', '')
            mss_text = fields.get('manuscripts', '')
            biblio_text = fields.get('bibliography', '')
        elif dossier_file in dossier_data:
            intro_text = dossier_data[dossier_file]['summary']

        item = {
            'id': ocp_id,
            'cavt': cavt_no,
            'cant': cant_no,
            'title': title,
            'section': section,
            'lang': lang,
            'status': status,
            'filename': xml_file if has_xml else '',
            'size_kb': xml_info.get('size_kb', 0.0),
            'mss_count': xml_info.get('mss_count', 0),
            'mss_langs': xml_info.get('mss_langs', []),
            'dossier': dossier_file,
            'concordance': {
                'denis': row['denis_ref'],
                'ditommaso': row['ditommaso_ref'],
                'otp': row['otp_ref'],
                'apot': row['apot_ref'],
                'aot': row['sparks_ref']
            },
            'details': {
                'intro': intro_text,
                'provenance': provenance_text,
                'manuscripts': mss_text,
                'bibliography': biblio_text
            }
        }
        catalog.append(item)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {output_path} with {len(catalog)} entries.")
    live_cnt = sum(1 for c in catalog if c['status'] == 'live')
    staged_cnt = sum(1 for c in catalog if c['status'] == 'staged')
    gap_cnt = sum(1 for c in catalog if c['status'] == 'gap')
    print(f"Breakdown: {live_cnt} live, {staged_cnt} staged, {gap_cnt} clavis gaps.")

if __name__ == '__main__':
    main()
