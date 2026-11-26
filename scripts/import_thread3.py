#!/usr/bin/env python3
"""Import a THREAD3 TEI XML edition into OCP and rebuild the site catalog.

Usage:
  python3 scripts/import_thread3.py <edition.xml> <CAVT-NNN> [TargetName.xml]
"""
import csv
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CROSSWALK = ROOT / "data" / "master_crosswalk.csv"


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser().resolve()
    cavt_id = sys.argv[2].strip().upper()
    if not cavt_id.startswith("CAVT-"):
        cavt_id = f"CAVT-{cavt_id.zfill(3)}"
    target_name = sys.argv[3] if len(sys.argv) > 3 else f"{cavt_id}.xml"
    if not target_name.endswith(".xml"):
        target_name += ".xml"

    if not src.is_file():
        print(f"Error: {src} not found")
        sys.exit(1)

    for dest_dir in (ROOT / "static" / "docs", ROOT / "static" / "docs" / "tei"):
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / target_name)

    rows = []
    updated = False
    with CROSSWALK.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("ocp_canon_id", "").upper() == cavt_id:
                row["ocp_xml"] = target_name
                row["status"] = "Live Edition"
                updated = True
            rows.append(row)

    if not updated:
        print(f"Warning: {cavt_id} not found in {CROSSWALK}")
    else:
        with CROSSWALK.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_site_catalog.py")], check=True, cwd=ROOT)
    print(f"Imported {src.name} as {target_name} for {cavt_id}. Ready to commit & push.")


if __name__ == "__main__":
    main()
