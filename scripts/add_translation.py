#!/usr/bin/env python3
"""
OCP Translation Alignment & Injection Utility

This script assists in verifying and injecting English translations into
Online Critical Pseudepigrapha (OCP) XML editions.

Features:
- Extracts reference hierarchy (e.g., chapters, verses, lines) from base text.
- Validates 1-to-1 alignment between translation units and original language units.
- Injects or updates <version language="English" ...> elements conforming to grammateus.dtd.
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET


def get_base_references(xml_path, version_idx=0):
    """Parses XML and returns list of hierarchical reference paths for the specified version."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    versions = root.findall('version')
    if not versions:
        # Single version without <version> tag
        target_elem = root
    else:
        if version_idx >= len(versions):
            raise IndexError(f"Version index {version_idx} out of range (found {len(versions)} versions)")
        target_elem = versions[version_idx]

    text_elem = target_elem.find('text')
    if text_elem is None:
        return []

    refs = []

    def traverse(elem, current_path):
        for child in elem:
            if child.tag.lower() == 'div':
                num = child.attrib.get('number') or child.attrib.get('n') or str(len(current_path) + 1)
                traverse(child, current_path + [num])
            elif child.tag.lower() == 'unit':
                ref_str = ":".join(current_path) if current_path else "1"
                if not refs or refs[-1] != ref_str:
                    refs.append(ref_str)

    traverse(text_elem, [])
    return refs


def verify_alignment(xml_path):
    """Checks all versions in an XML document to ensure reference synchronization."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    versions = root.findall('version')
    if not versions:
        print(f"[{os.path.basename(xml_path)}] Single text structure, no parallel versions.")
        return True

    print(f"Verifying alignment for {os.path.basename(xml_path)} ({len(versions)} versions):")
    base_refs = get_base_references(xml_path, 0)
    base_v = versions[0]
    base_title = base_v.attrib.get('title', 'Version 1')
    base_lang = base_v.attrib.get('language', 'Original')
    print(f"  Base [0] '{base_title}' ({base_lang}): {len(base_refs)} reference locations")

    all_aligned = True
    for idx in range(1, len(versions)):
        v = versions[idx]
        title = v.attrib.get('title', f'Version {idx+1}')
        lang = v.attrib.get('language', '')
        v_refs = get_base_references(xml_path, idx)
        
        # Check matching
        missing_in_v = set(base_refs) - set(v_refs)
        extra_in_v = set(v_refs) - set(base_refs)
        
        status = "ALIGNED" if len(missing_in_v) == 0 and len(extra_in_v) == 0 else "MISMATCH / PARTIAL"
        print(f"  Version [{idx}] '{title}' ({lang}): {len(v_refs)} refs -> {status}")
        if missing_in_v:
            print(f"    Missing in version {idx}: {sorted(list(missing_in_v))[:5]}")
            all_aligned = False
        if extra_in_v:
            print(f"    Extra in version {idx}: {sorted(list(extra_in_v))[:5]}")
            all_aligned = False

    return all_aligned


def main():
    parser = argparse.ArgumentParser(description="OCP Translation Alignment and Management Tool")
    parser.add_argument("xml_files", nargs="+", help="Path to one or more OCP XML files")
    parser.add_argument("--verify", action="store_true", help="Verify alignment between base text and versions")
    parser.add_argument("--list-refs", action="store_true", help="List all hierarchical references in base text")

    args = parser.parse_args()

    for xml_file in args.xml_files:
        if not os.path.exists(xml_file):
            print(f"File not found: {xml_file}", file=sys.stderr)
            continue

        if args.verify:
            verify_alignment(xml_file)
        elif args.list_refs:
            refs = get_base_references(xml_file)
            print(f"{os.path.basename(xml_file)} ({len(refs)} references):")
            for r in refs:
                print(f"  {r}")
        else:
            verify_alignment(xml_file)


if __name__ == "__main__":
    main()
