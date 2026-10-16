#!/usr/bin/env python3
"""
Comprehensive test suite for OCP editions, TEI files, intros.json, and reader.js.
"""

import os
import json
import xml.etree.ElementTree as ET
import glob
import re
import sys

def test_grammateus_xml():
    print("=== Testing Grammateus XML files in static/docs/ ===")
    xml_files = sorted(glob.glob('static/docs/*.xml'))
    errors = []
    total_units = 0
    validated_files = 0
    
    for f in xml_files:
        # Skip standalone TEI files placed directly in static/docs/ (like ApDan_TEI.xml)
        if f.endswith('_TEI.xml'):
            continue
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            if root.tag != 'book':
                errors.append(f"{f}: root tag is '{root.tag}', expected 'book'")
                continue
            
            # Attributes
            title = root.attrib.get('title') or root.attrib.get('name')
            filename = root.attrib.get('filename')
            if not title:
                errors.append(f"{f}: missing 'title' or 'name' attribute on <book>")
            if not filename:
                errors.append(f"{f}: missing 'filename' attribute on <book>")
                
            # Versions
            versions = root.findall('version')
            if not versions:
                # Direct structure without <version> (e.g. Esdr.xml)
                versions = [root]
                
            file_units = 0
            for v in versions:
                text_elem = v.find('text')
                if text_elem is None:
                    errors.append(f"{f}: version '{v.attrib.get('title', '')}' missing <text>")
                    continue
                units = text_elem.findall('.//unit')
                file_units += len(units)
                for u in units:
                    readings = u.findall('reading')
                    if not readings:
                        errors.append(f"{f}: unit id={u.attrib.get('id')} has no <reading> elements")
                        break
                        
            if file_units == 0:
                errors.append(f"{f}: contains 0 text <unit> elements")
            total_units += file_units
            validated_files += 1
        except Exception as e:
            errors.append(f"{f}: XML Parse Error: {e}")
            
    print(f"Validated {validated_files} Grammateus XML documents ({total_units} total verse/text units).")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors[:10]:
            print("  -", err)
        return False
    else:
        print("ALL Grammateus XML files PASSED validation.")
        return True

def test_tei_p5_xml():
    print("\n=== Testing TEI P5 files in static/docs/tei/ ===")
    tei_files = sorted(glob.glob('static/docs/tei/*.xml'))
    errors = []
    total_elements = 0
    
    for f in tei_files:
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            tag = root.tag
            # TEI namespace
            if not tag.endswith('TEI'):
                errors.append(f"{f}: root tag is '{tag}', expected TEI")
            
            # check teiHeader
            header = root.find('{http://www.tei-c.org/ns/1.0}teiHeader')
            if header is None:
                header = root.find('teiHeader')
            if header is None:
                errors.append(f"{f}: missing <teiHeader>")
                
            # check text / body
            text = root.find('{http://www.tei-c.org/ns/1.0}text')
            if text is None:
                text = root.find('text')
            if text is None:
                errors.append(f"{f}: missing <text>")
            else:
                body = text.find('{http://www.tei-c.org/ns/1.0}body')
                if body is None:
                    body = text.find('body')
                if body is None:
                    errors.append(f"{f}: missing <body>")
                else:
                    children = list(body)
                    if not children:
                        errors.append(f"{f}: <body> is empty")
                    total_elements += len(children)
        except Exception as e:
            errors.append(f"{f}: TEI XML Parse Error: {e}")
            
    print(f"Validated {len(tei_files)} TEI P5 documents.")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors[:10]:
            print("  -", err)
        return False
    else:
        print("ALL TEI P5 XML files PASSED validation.")
        return True

def test_intros_json():
    print("\n=== Testing static/docs/intros.json ===")
    try:
        with open('static/docs/intros.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        docs = data.get('documents', {})
        print(f"Loaded intros.json successfully: {len(docs)} document introductions found.")
        missing_fields = []
        for doc_id, info in docs.items():
            if not info.get('title'):
                missing_fields.append(f"{doc_id}: missing 'title'")
            # Accept either 'description' or 'fields' / 'sections' / 'content'
            has_desc = bool(info.get('description') or info.get('fields') or info.get('sections') or info.get('content'))
            if not has_desc:
                missing_fields.append(f"{doc_id}: missing descriptive content")
        if missing_fields:
            print("Intros warnings:", missing_fields[:5])
            return False
        else:
            print("ALL intros have complete title and introductory metadata.")
            return True
    except Exception as e:
        print(f"FAILED intros.json test: {e}")
        return False

def test_reader_js_sync():
    print("\n=== Testing static/js/reader.js OCP_DOCUMENTS sync ===")
    with open('static/js/reader.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'OCP_DOCUMENTS\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not m:
        print("FAILED: Could not find OCP_DOCUMENTS in reader.js")
        return False
    
    doc_entries = re.findall(r"filename:\s*'([^']+)'", m.group(1))
    print(f"Found {len(doc_entries)} registered documents in reader.js.")
    
    missing_on_disk = []
    for fn in doc_entries:
        path = os.path.join('static/docs', fn)
        if not os.path.exists(path):
            missing_on_disk.append(fn)
            
    if missing_on_disk:
        print(f"FAILED: Documents in reader.js missing on disk: {missing_on_disk}")
        return False
    else:
        print("ALL registered reader.js documents exist on disk in static/docs/.")
        return True

if __name__ == '__main__':
    t1 = test_grammateus_xml()
    t2 = test_tei_p5_xml()
    t3 = test_intros_json()
    t4 = test_reader_js_sync()
    if all([t1, t2, t3, t4]):
        print("\n=========================================")
        print("SUCCESS: ALL TEST SUITES PASSED (100% OK)")
        print("=========================================")
        sys.exit(0)
    else:
        print("\nFAILURE: One or more test suites failed.")
        sys.exit(1)
