#!/usr/bin/env python3
"""Transcribe scholarly book scans and manuscript pages using OpenCode Go's MiniMax M3.1 Flash vision model.

Usage:
    raw/.venv/bin/python3 scripts/vlm_transcribe.py image_or_page.png [output.md] [--prompt "custom prompt"]
    raw/.venv/bin/python3 scripts/vlm_transcribe.py book.pdf --page 144
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


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


def extract_pdf_page_as_png(pdf_path: Path, page_num: int, out_png: Path) -> None:
    """Render a single PDF page to PNG using pdftoppm at 150 DPI."""
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = Path(tmpdir) / "page"
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
        rendered = list(Path(tmpdir).glob("page-*.png"))
        if not rendered:
            sys.exit(f"Failed to render page {page_num} of {pdf_path}")
        rendered[0].rename(out_png)


def transcribe_image(image_path: Path, prompt: str, api_key: str, model: str = "minimax-m3.1-flash") -> str:
    """Send image to OpenCode Go MiniMax M3.1 Flash for transcription."""
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    suffix = image_path.suffix.lstrip(".").lower()
    mime = "image/png" if suffix == "png" else "image/jpeg"

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
                            "url": f"data:{mime};base64,{b64_img}",
                        },
                    },
                ],
            }
        ],
        "reasoning_effort": "low",
        "max_tokens": 4000,
    }

    url = "https://opencode.ai/inference/go/openai/v1/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "x-opencode-session": "ocp-vlm-transcribe",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            msg = data["choices"][0]["message"]
            content = msg.get("content")
            if not content and msg.get("reasoning_content"):
                content = msg["reasoning_content"]
            return content.strip() if content else ""
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        sys.exit(f"OpenCode Go API Error {e.code}: {err_msg}")


def main():
    default_prompt = (
        "Transcribe this scholarly page accurately into Markdown. "
        "Preserve polytonic Greek, Latin, Hebrew, footnotes, and critical apparatus sigla verbatim. "
        "Format footnotes in Markdown format at the bottom."
    )

    parser = argparse.ArgumentParser(description="Transcribe book scans via MiniMax M3.1 Flash VLM.")
    parser.add_argument("input", type=Path, help="Input image (PNG/JPG) or PDF file")
    parser.add_argument("output", type=Path, nargs="?", default=None, help="Output Markdown file")
    parser.add_argument("--page", type=int, default=1, help="Page number if input is a PDF (1-based)")
    parser.add_argument("--prompt", default=default_prompt, help="Transcription instruction")
    parser.add_argument("--model", default="minimax-m3.1-flash", help="Model name (default: minimax-m3.1-flash)")
    args = parser.parse_args()

    api_key = get_api_key()
    inp = args.input.resolve()
    if not inp.exists():
        sys.exit(f"Input file not found: {inp}")

    if inp.suffix.lower() == ".pdf":
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_png = Path(tmp.name)
        try:
            print(f"-> Rendering page {args.page} of {inp.name}...")
            extract_pdf_page_as_png(inp, args.page, tmp_png)
            print(f"-> Transcribing with {args.model} via OpenCode Go...")
            text = transcribe_image(tmp_png, args.prompt, api_key, model=args.model)
        finally:
            tmp_png.unlink(missing_ok=True)
    else:
        print(f"-> Transcribing {inp.name} with {args.model} via OpenCode Go...")
        text = transcribe_image(inp, args.prompt, api_key, model=args.model)

    if args.output:
        args.output.resolve().write_text(text, encoding="utf-8")
        print(f"-> Saved transcription to {args.output}")
    else:
        print("\n=== TRANSCRIPTION ===\n")
        print(text)


if __name__ == "__main__":
    main()
