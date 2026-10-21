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

## 5. Logos Bible Software Library & Pseudepigrapha Extraction
- **Non-Biblical Milestones:** Never attempt to pass human pseudepigraphal titles into `logos read <ref>` (which relies on biblical versification parsers). Always retrieve the `indexedOffset` from the Table of Contents (`getTableOfContentsEntries`) or search results (`getBasicSearchResults`) and read via `getResourceArticle({ resourceId, offset })`.
- **Search Result Structure:** In `appClient.getBasicSearchResults`, matches are stored in `val.results` (not `val.items`). Preview highlights are extracted from `previewTextRanges[].richTextXml` `<Run Text="..."/>` spans.
- **Resource Selection:** Always draw on Ken Penner's *Old Testament Greek Pseudepigrapha* (`LLS:8.20.7`), Charlesworth OTP 1–2 (`LLS:OTPSEUD01`, `LLS:OTPSEUD02`), Eerdmans Dictionary (`LLS:EERDDICTEARJUD`), and Anchor Yale Bible Dictionary (`LLS:14.0.4`) before falling back to web or unverified secondary sources.
