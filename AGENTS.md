# OCP Project Guidelines & Operational Rules

## 1. Digital Resource Acquisition & PDF Integrity
- **Magic Bytes Verification:** NEVER assume a downloaded resource is a valid PDF based on the HTTP 200 status or `.pdf` extension. Always verify that the file starts with the `%PDF-` signature (or inspect with `file <path>`) before claiming an item is acquired or saving it to `raw/editions/`.
- **HTML Paywall Trap:** Academic platforms (JSTOR, SBL, Brepols, SAGE, etc.) frequently return HTTP 200 OK with an HTML page when an institution lacks access to a specific collection (e.g. SBL Press eBooks on JSTOR returning an unentitled message). Inspect response content-type and body; never save an HTML error or login page under a `.pdf` filename.
- **Minimum Size & 0-Byte Detection:** Any 0-byte or <1 KB PDF indicates a failed or incomplete acquisition. Diagnose the root cause (unaccepted terms of service, session token expiration, Cloudflare interception, or backend rendering delays).

## 2. ProQuest Ebook Central Automation
- **User Terms Consent:** ProQuest Ebook Central patron accounts require active terms consent before chapter or book downloads are permitted. If downloads fail or return 0 bytes, check for `#consentModal` and trigger `/auth/lib/stfx/userConsentAction.json?action=accept`.
- **In-Browser CDP Fetch:** Do not use external Python HTTP clients (`urllib`, `requests`) to download generated chapter PDFs; ProQuest validates origin headers, session cookies, Cloudflare tokens, and download tokens. Always trigger the chapter download modal in the DOM (`tool_chapterdownload_{docId}_{st}_{chaptId}`), await the ready state, and fetch the PDF bytes directly inside the Chrome execution context via CDP (`fetch(url)` evaluated in page), decoding the resulting buffer.

## 3. Library Proxy & Institutional Access
- **StFX Proxy URLs:** Use `https://libproxy.stfx.ca/login?auth=shib&url=<TARGET>` or LibKey Nomad resolver links (`https://libkey.io/libraries/3054/articles/<ID>/full-text-file`) in Chrome to obtain full text from licensed publishers (SAGE, De Gruyter, JSTOR).
- **Sub-Collection Scoping:** Always verify on the publisher landing page whether the institution actually holds the specific volume/journal issue before attempting bulk chapter downloads.

## 4. Beta maṣāḥǝft Access Architecture
- **Web Frontend Firewall:** `https://betamasaheft.eu/` is protected by an IP-level Nginx firewall maintained by the University of Hamburg / Hiob Ludolf Centre (returning static 403 pages to external IPs). It does not have an external login portal, nor is it configured in StFX EZproxy.
- **Direct GitHub Data Extraction:** Do not attempt to bypass or scrape the web domain. All manuscript records, work authorities (Clavis Aethiopica), and place/person files are open source and version-controlled on GitHub:
  - Manuscripts: `https://github.com/BetaMasaheft/Manuscripts` (subdivided by collection, e.g. `ParisBNF/abb`, `EMML/1001-2000`, `TelAviv`)
  - Works: `https://github.com/BetaMasaheft/Works`
  Download raw TEI XML files directly via `https://raw.githubusercontent.com/BetaMasaheft/...`.

## 5. Book Scans, OCR & Polyglot VLM Architecture
- **Photocopier Spreads Bisecting:** Copier scans (e.g. NT 5th floor Konica Minolta) produce 2-page landscape sheets. Never feed raw spreads directly to OCR or layout parsers; columns and footnotes will interleave across the gutter. Always bisect spreads into single portrait pages first using `scripts/split_and_ocr_book.py`.
- **Searchable PDF vs. Edition Text Extraction:**
  - For searchable PDF reading layers, use `ocrmypdf` with modern European languages (`fra+lat+deu` or `eng+lat`). Do not use `--clean-final` unless `unpaper` is present.
  - For transcribing critical editions with polytonic Greek, Semitic scripts, or apparatus sigla, NEVER use Tesseract or Docling (which cause cross-alphabet pollution and drops). Always use a Vision-Language Model directly via `scripts/vlm_transcribe.py` or `scripts/batch_vlm_extract.py`.
- **Copier Scan Ingestion (Outlook Web over CDP):**
  - NT 5th floor Konica Minolta photocopier sends PDF scans to `kpenner@stfx.ca` with subject `Message from NT_5th` and generic attachment names (`SNT_5th...pdf`).
  - Use `scripts/fetch_outlook_scans.py` to ingest directly via OWA REST API v2.0 (`/messages/<id>/attachments/<att_id>` base64 `ContentBytes`), sort chronologically, group by scan date (`raw/editions/scans_YYYY-MM-DD/SNT_5th_YYYY-MM-DD_NN.pdf`), and validate `%PDF-` magic bytes.
- **Digital Cover & Spine Restoration (Sticker/Barcode Removal):**
  - Library copies often carry barcodes on the front cover and call numbers on the spine.
  - VLM Prompt Safety Refusal Trap: Prompting a VLM to "find library security features or barcodes" triggers false-positive safety refusals. Use CV color segmentation / thresholding for bounding box detection, and query VLMs with neutral visual questions ("Describe text or markings in this crop").
  - Seamless Restoration: For flat book boards, use `cv2.seamlessClone` sampled from adjacent clean cloth. For curved spines, sample clean buckram from the upper spine, match local illumination gradients, and alpha-feather boundaries to avoid rectangular patch outlines or erasing embossed gold lettering.
- **OpenCode Go VLM Architecture & Model Selection:**
  - Endpoint: `https://opencode.ai/inference/go/openai/v1/chat/completions` ($0 net cost covered by Go subscription allowance).
  - Contributor Vision Model: `muse-spark-1.2-contributor` is the recommended default for book scan extraction (~36 pages/min batch throughput, flawless polytonic Greek, $0 net cost with contributor data-training opt-in enabled).
  - Alternative High-Accuracy Models: `minimax-m3.1-flash`, `qwen3.8-flash`, and `claude-haiku-5-5`. Note: `beam-free` and `iceman-contributor-free` are text-only (reject vision with HTTP 400).
  - Always send headers: `User-Agent: Mozilla/5.0` (avoids Cloudflare 1010) and `x-opencode-session: <id>` (avoids 400 MissingSessionID).
  - Set `"reasoning_effort": "low"` and `"max_tokens": 4000` for reasoning models (`minimax-m3.1-flash`, `muse-spark-1.3-contributor`) to prevent reasoning tokens from exhausting the completion window.
  - Multi-page batches must checkpoint per page (`page_NNN.md`) to permit seamless resumption.

## 6. Canonical Crosswalk & Catalog Pipeline
- **6-Way Concordance Framework:** The OCP Canon ([`CANON.md`](CANON.md)) synthesizes Haelewyck (CAVT), Denis (1970/2000), DiTommaso (2001), Charlesworth (OTP), Charles (APOT), and Sparks (AOT). CAVT numbers 1–277 are preserved verbatim; supplemental numbers `CAVT-JH-01` through `CAVT-JH-22` accommodate non-apocryphal Hellenistic/sapiential, sectarian (Damascus Document), and segregated visionary texts.
- **Site Catalog Generation:** Always update the web presentation using `scripts/generate_site_catalog.py` and `scripts/update_index_catalog.py` to synchronize [`static/data/catalog.json`](static/data/catalog.json) and [`index.html`](index.html).
- **Markdown-to-HTML Sanitation:** When ingesting descriptions, witnesses, or bibliographies from Markdown dossiers into the web catalog/modal DOM, never insert raw Markdown (`*`, `**`, `###`, bullet lists) directly into HTML containers. Run through the semantic HTML parser (`scripts/generate_site_catalog.py:markdown_to_html`) to ensure clean paragraph, list (`<ul><li>`), bold, and italic rendering.

