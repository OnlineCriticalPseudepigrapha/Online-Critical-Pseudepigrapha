#!/usr/bin/env python3
"""Book Scan Processing Utility: Split photocopier spreads & add searchable OCR layer.

Usage:
    raw/.venv/bin/python3 scripts/split_and_ocr_book.py input.pdf [output.pdf] [--lang fra+lat] [--skip-ocr]
"""

import argparse
import copy
import subprocess
import sys
import time
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_spreads(input_pdf: Path, split_pdf: Path) -> int:
    """Split 2-page landscape scans into individual portrait pages down the gutter."""
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    total_in = len(reader.pages)
    spread_count = 0

    for idx, page in enumerate(reader.pages):
        mb = page.mediabox
        w = float(mb.width)
        h = float(mb.height)

        # Detect landscape spread (width > height)
        if w > h:
            spread_count += 1
            mid = w / 2.0

            # Left page
            page_left = copy.copy(page)
            page_left.mediabox.lower_left = (0, 0)
            page_left.mediabox.upper_right = (mid, h)
            writer.add_page(page_left)

            # Right page
            page_right = copy.copy(page)
            page_right.mediabox.lower_left = (mid, 0)
            page_right.mediabox.upper_right = (w, h)
            writer.add_page(page_right)
        else:
            writer.add_page(page)

    with open(split_pdf, "wb") as f:
        writer.write(f)

    print(f"-> Detected {spread_count} spread(s) out of {total_in} sheet(s).")
    print(f"-> Produced {len(writer.pages)} single portrait page(s) in {split_pdf.name}")
    return len(writer.pages)


def run_ocrmypdf(input_pdf: Path, output_pdf: Path, lang: str = "fra+lat+deu", jobs: int = 16) -> None:
    """Run ocrmypdf with multi-core processing to add a searchable PDF/A text layer."""
    cmd = [
        "ocrmypdf",
        "-l", lang,
        "--jobs", str(jobs),
        "--rotate-pages",
        "--deskew",
        "--clean-final",
        str(input_pdf),
        str(output_pdf),
    ]
    print(f"-> Running ocrmypdf (languages: {lang}, jobs: {jobs})...")
    subprocess.run(cmd, check=True)
    print(f"-> Searchable PDF created successfully: {output_pdf}")


def main():
    parser = argparse.ArgumentParser(description="Split photocopier spreads and run OCR.")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("output", type=Path, nargs="?", default=None, help="Output PDF file")
    parser.add_argument("--lang", default="fra+lat", help="OCR languages (default: fra+lat)")
    parser.add_argument("--skip-ocr", action="store_true", help="Only split spreads, skip OCR")
    parser.add_argument("--jobs", type=int, default=16, help="Number of concurrent OCR workers")
    args = parser.parse_args()

    src = args.input.resolve()
    if not src.exists():
        sys.exit(f"Error: input file {src} not found.")

    out = args.output.resolve() if args.output else src.with_name(f"{src.stem}_searchable.pdf")
    temp_split = src.with_name(f"{src.stem}_split_temp.pdf")

    t0 = time.time()
    try:
        split_spreads(src, temp_split)
        if args.skip_ocr:
            temp_split.rename(out)
            print(f"-> Done. Split PDF saved to {out} ({time.time()-t0:.1f}s)")
        else:
            run_ocrmypdf(temp_split, out, lang=args.lang, jobs=args.jobs)
            temp_split.unlink(missing_ok=True)
            print(f"-> All complete in {time.time()-t0:.1f}s: {out}")
    except Exception as e:
        temp_split.unlink(missing_ok=True)
        raise e


if __name__ == "__main__":
    main()
