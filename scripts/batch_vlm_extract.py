#!/usr/bin/env python3
"""Batch VLM extractor: Transcribes book pages via OpenCode Go MiniMax M3.1 Flash.

Features:
- Checkpoints per-page in a dedicated folder (e.g. denis1970_vlm_pages/page_001.md)
- Skips already-completed pages (fully resumable)
- Exponential backoff on rate limits (429) or transient network errors
- Concatenates all pages into a final master Markdown file

Usage:
    raw/.venv/bin/python3 scripts/batch_vlm_extract.py [options]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from pypdf import PdfReader


def get_api_key() -> str:
    key = os.environ.get("OPENCODE_GO_API_KEY")
    if key:
        return key

    hermes_env = Path.home() / ".hermes/.env"
    if hermes_env.exists():
        with open(hermes_env) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENCODE_GO_API_KEY="):
                    return line.split("=", 1)[1].strip()

    sys.exit("Error: OPENCODE_GO_API_KEY not found in environment or ~/.hermes/.env")


def render_page(pdf_path: Path, page_num: int, out_png: Path) -> None:
    """Render 1-based page of PDF to PNG via pdftoppm."""
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = Path(tmpdir) / "p"
        cmd = [
            "pdftoppm",
            "-png",
            "-r", "150",
            "-f", str(page_num),
            "-l", str(page_num),
            str(pdf_path),
            str(prefix),
        ]
        subprocess.run(cmd, check=True)
        rendered = list(Path(tmpdir).glob("p-*.png"))
        if not rendered:
            raise RuntimeError(f"Could not render page {page_num}")
        rendered[0].rename(out_png)


def transcribe_page_with_retry(image_path: Path, api_key: str, prompt: str, page_num: int, model: str = "muse-spark-1.2-contributor", max_retries: int = 5) -> str:
    """Transcribe single image via OpenCode Go VLM with exponential backoff."""
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_img}",
                        },
                    },
                ],
            }
        ],
        "reasoning_effort": "low",
        "max_tokens": 4000,
    }

    url = "https://opencode.ai/inference/go/openai/v1/chat/completions"
    data = json.dumps(payload).encode("utf-8")

    backoff = 5
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "x-opencode-session": f"ocp-denis-p{page_num}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=75) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                msg = res["choices"][0]["message"]
                content = msg.get("content")
                if not content and msg.get("reasoning_content"):
                    content = msg["reasoning_content"]
                if content and content.strip():
                    return content.strip()
                raise ValueError("Empty response received from model.")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"[Page {page_num}] HTTP {e.code} on attempt {attempt}: {err_body[:120]}")
            if e.code == 429:
                sleep_time = backoff * attempt * 2
                print(f"[Page {page_num}] Rate limit hit; waiting {sleep_time}s...")
                time.sleep(sleep_time)
            elif attempt == max_retries:
                raise
            else:
                time.sleep(backoff)
        except Exception as e:
            print(f"[Page {page_num}] Error on attempt {attempt}: {e}")
            if attempt == max_retries:
                raise
            time.sleep(backoff)

    raise RuntimeError(f"Failed to transcribe page {page_num} after {max_retries} attempts.")


def process_single_page(pdf_path: Path, page_num: int, page_file: Path, api_key: str, prompt: str, model: str = "muse-spark-1.2-contributor") -> bool:
    """Process and write one page if not already completed."""
    if page_file.exists() and page_file.stat().st_size > 50:
        return True  # already done

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_png = Path(tmp.name)

    try:
        render_page(pdf_path, page_num, tmp_png)
        text = transcribe_page_with_retry(tmp_png, api_key, prompt, page_num, model=model)
        page_file.write_text(f"<!-- Page {page_num} -->\n\n{text}\n\n", encoding="utf-8")
        print(f"✓ Completed page {page_num}")
        return True
    finally:
        tmp_png.unlink(missing_ok=True)


def merge_pages(pages_dir: Path, total_pages: int, merged_file: Path, title: str = "Scholarly Edition", model_name: str = "OpenCode Go VLM") -> int:
    """Assemble individual page markdown files in order into master markdown."""
    count = 0
    with open(merged_file, "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        out.write(f"*Transcribed via {model_name}*\n\n---\n\n")
        for p in range(1, total_pages + 1):
            pf = pages_dir / f"page_{p:03d}.md"
            if pf.exists() and pf.stat().st_size > 0:
                out.write(pf.read_text(encoding="utf-8"))
                out.write("\n\n---\n\n")
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="Batch transcribe PDF book pages via OpenCode Go VLM.")
    parser.add_argument("--input", type=Path, default=Path("raw/editions/Denis1970_Introduction_pseudepigraphes_grecs_SVTP1_searchable.pdf"))
    parser.add_argument("--pages-dir", type=Path, default=Path("raw/editions/denis1970_vlm_pages"))
    parser.add_argument("--output", type=Path, default=Path("raw/editions/Denis1970_Introduction_pseudepigraphes_grecs_SVTP1.md"))
    parser.add_argument("--title", type=str, default="Albert-Marie Denis, Introduction aux pseudépigraphes grecs d'Ancien Testament (SVTP 1; 1970)")
    parser.add_argument("--model", type=str, default="muse-spark-1.2-contributor", help="Model name (e.g. muse-spark-1.2-contributor, minimax-m3.1-flash, qwen3.8-flash, claude-haiku-5-5)")
    parser.add_argument("--workers", type=int, default=2, help="Concurrent worker threads (default: 2)")
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--end-page", type=int, default=None)
    args = parser.parse_args()

    api_key = get_api_key()
    pdf_path = args.input.resolve()
    if not pdf_path.exists():
        sys.exit(f"Input PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    end_p = min(args.end_page or total_pages, total_pages)
    start_p = max(1, args.start_page)

    pages_dir = args.pages_dir.resolve()
    pages_dir.mkdir(parents=True, exist_ok=True)

    prompt = (
        "Transcribe this scholarly book page accurately into clean Markdown. "
        "Preserve polytonic Greek, Latin, Hebrew, German, and French verbatim with exact accents and diacritics. "
        "Preserve footnote numbers and format footnotes clearly at the bottom of the page. "
        "Do not summarize or skip content. Output only the transcription."
    )

    print(f"Batch transcription started for {pdf_path.name}")
    print(f"Pages: {start_p} to {end_p} (total: {end_p - start_p + 1})")
    print(f"Workers: {args.workers} | Output dir: {pages_dir}")

    t0 = time.time()
    completed = 0
    skipped = 0

    to_process = []
    for p in range(start_p, end_p + 1):
        pf = pages_dir / f"page_{p:03d}.md"
        if pf.exists() and pf.stat().st_size > 50:
            skipped += 1
        else:
            to_process.append(p)

    print(f"Found {skipped} already completed page(s); {len(to_process)} remaining.")

    if to_process:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_page = {
                executor.submit(
                    process_single_page,
                    pdf_path,
                    p,
                    pages_dir / f"page_{p:03d}.md",
                    api_key,
                    prompt,
                    model=args.model
                ): p
                for p in to_process
            }

            for future in as_completed(future_to_page):
                p = future_to_page[future]
                try:
                    res = future.result()
                    if res:
                        completed += 1
                        time.sleep(1.0)  # Gentle delay between completed requests
                except Exception as e:
                    print(f"✗ Failed page {p}: {e}")

    merged_count = merge_pages(pages_dir, total_pages, args.output.resolve(), title=args.title, model_name=args.model)
    elapsed = time.time() - t0
    print(f"\nFinished batch in {elapsed:.1f}s ({elapsed/60:.1f} min).")
    print(f"Consolidated {merged_count}/{total_pages} pages into {args.output}")


if __name__ == "__main__":
    main()
