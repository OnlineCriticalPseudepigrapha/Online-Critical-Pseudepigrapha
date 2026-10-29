#!/usr/bin/env python3
"""
Generate static/data/catalog.json from data/master_crosswalk.csv,
static/docs/*.xml, static/docs/intros.json, and bibliography/*.md dossiers.
Converts any markdown syntax in summaries, dossiers, and notes into clean semantic HTML.
"""
import csv
import json
import os
import re
import xml.etree.ElementTree as ET

def inline_format(text):
    if not text:
        return ""
    # Bold italic ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *text* or _text_
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', text)
    # Links [label](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text

def markdown_to_html(md_text):
    if not md_text:
        return ""
    # If already fully structured HTML with tags
    if ('<p>' in md_text or '<div>' in md_text or '<table>' in md_text) and not md_text.startswith('*'):
        # Check if there are stray unrendered markdown bold/italics inside html
        return inline_format(md_text)

    lines = md_text.strip().split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue

        # Subheadings within section ### or ####
        if stripped.startswith('#### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h5 style="margin:10px 0 4px; color:var(--text-primary);">{inline_format(stripped[5:].strip())}</h5>')
            continue
        elif stripped.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h4 style="margin:12px 0 6px; color:var(--accent-gold-dark); font-size:1rem;">{inline_format(stripped[4:].strip())}</h4>')
            continue

        # Bullet lists * or -
        if stripped.startswith('* ') or stripped.startswith('- '):
            if not in_list:
                html_lines.append('<ul style="margin:8px 0 12px 18px; padding-left:8px;">')
                in_list = True
            item_content = stripped[2:].strip()
            html_lines.append(f'<li>{inline_format(item_content)}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p style="margin-bottom:8px; line-height:1.6;">{inline_format(stripped)}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)

def parse_dossier_sections(md_content):
    sections = {}
    current_sec = None
    sec_content = []
    for line in md_content.split('\n'):
        m = re.match(r'^##\s+(\d+)\.\s+(.*)', line)
        if m:
            if current_sec:
                sections[current_sec] = '\n'.join(sec_content).strip()
            current_sec = m.group(2).strip()
            sec_content = []
        elif current_sec:
            if line.startswith('---'):
                continue
            sec_content.append(line)
    if current_sec:
        sections[current_sec] = '\n'.join(sec_content).strip()
    return sections

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
                    sections = parse_dossier_sections(content)
                    dossier_data[md_file] = {
                        'sections': sections,
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

        intro_text = ""
        provenance_text = ""
        mss_text = ""
        biblio_text = ""

        # Priority 1: Check intros.json for existing XML
        intro_obj = intros_json.get(xml_file, {})
        fields = intro_obj.get('fields', {})

        if fields:
            intro_text = markdown_to_html(fields.get('introduction', ''))
            provenance_text = markdown_to_html(fields.get('provenance', ''))
            mss_text = markdown_to_html(fields.get('manuscripts', ''))
            biblio_text = markdown_to_html(fields.get('bibliography', ''))
        
        # Priority 2: Enrich from dossier if present
        if dossier_file in dossier_data:
            sec_dict = dossier_data[dossier_file]['sections']
            
            # Map common section names from dossiers
            # Section 1: Usually Overview / Textual Witnesses
            if not intro_text:
                for sec_title, sec_body in sec_dict.items():
                    if any(k in sec_title.lower() for k in ['compositional', 'overview', 'witness', 'structure', 'tradition']):
                        intro_text = markdown_to_html(sec_body)
                        break
            
            # Witnesses / Manuscripts
            if not mss_text:
                for sec_title, sec_body in sec_dict.items():
                    if any(k in sec_title.lower() for k in ['witnesses', 'manuscript tradition', 'witness']):
                        mss_text = markdown_to_html(sec_body)
                        break

            # Bibliography / Critical Editions
            if not biblio_text:
                for sec_title, sec_body in sec_dict.items():
                    if any(k in sec_title.lower() for k in ['critical editions', 'editions', 'translations', 'studies', 'bibliography']):
                        biblio_text = markdown_to_html(sec_body)
                        break

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

    print(f"Successfully generated {output_path} with {len(catalog)} entries and rendered HTML.")

if __name__ == '__main__':
    main()
