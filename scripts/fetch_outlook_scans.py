#!/usr/bin/env python3
"""Fetch scanned PDF attachments from StFX Outlook Web via Chrome CDP (:9222).

Extracts scans sent by the NT 5th floor Konica Minolta photocopier,
saves them with dated filenames, and validates magic bytes.
"""

import asyncio
import base64
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
import websockets
from pypdf import PdfReader


async def run_js_in_owa(expr: str):
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json"))
    t = next((t for t in tabs if t["type"] == "page" and "outlook" in t["url"]), None)
    if not t:
        raise RuntimeError("No Outlook Web tab found in Chrome.")

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=64 * 2**20, ping_interval=None) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": expr, "awaitPromise": True, "returnByValue": True, "timeout": 300000}
        }))
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 1:
                break
    res = r["result"]
    if "exceptionDetails" in res:
        raise RuntimeError(f"JS Exception: {res['exceptionDetails']}")
    return res["result"].get("value")


async def get_scan_metadata():
    js = """
    (async () => {
        const B = 'https://outlook.office.com/api/v2.0/me';
        const H = {Authorization: 'Bearer ' + window.__tok, 'Content-Type': 'application/json'};
        
        let allScanMsgs = [];
        let url = B + "/mailfolders/inbox/messages?$top=50&$select=Subject,ReceivedDateTime,From,HasAttachments,Id&$orderby=ReceivedDateTime%20desc";

        for (let page = 0; page < 4; page++) {
          const res = await fetch(url, {headers: H});
          const data = await res.json();
          const msgs = (data.value || []).filter(m => m.Subject && (m.Subject.includes("NT_5th") || m.Subject.toLowerCase().includes("scan")));
          allScanMsgs.push(...msgs);
          if (!data['@odata.nextLink']) break;
          url = data['@odata.nextLink'];
        }

        const results = [];
        for (const m of allScanMsgs) {
          const attRes = await fetch(B + `/messages/${m.Id}/attachments?$select=Name,Size,ContentType,Id`, {headers: H});
          const attData = await attRes.json();
          for (const a of (attData.value || [])) {
            if (a.ContentType === 'application/pdf' || a.Name.endsWith('.pdf')) {
              results.push({
                messageId: m.Id,
                attachmentId: a.Id,
                name: a.Name,
                size: a.Size,
                received: m.ReceivedDateTime
              });
            }
          }
        }
        return results;
    })()
    """
    return await run_js_in_owa(js)


async def fetch_attachment_bytes(msg_id: str, att_id: str) -> bytes:
    js = f"""
    (async () => {{
        const B = 'https://outlook.office.com/api/v2.0/me';
        const H = {{Authorization: 'Bearer ' + window.__tok, 'Content-Type': 'application/json'}};
        const res = await fetch(B + `/messages/{msg_id}/attachments/{att_id}`, {{headers: H}});
        const data = await res.json();
        return data.ContentBytes;
    }})()
    """
    b64_str = await run_js_in_owa(js)
    if not b64_str:
        raise RuntimeError("No ContentBytes returned for attachment.")
    return base64.b64decode(b64_str)


async def main():
    print("-> Querying Outlook Web for scanner attachments...")
    scans = await get_scan_metadata()
    print(f"-> Found {len(scans)} scan attachments in inbox.")

    # Sort chronologically (oldest first)
    scans.sort(key=lambda s: s["received"])

    out_base = Path("raw/editions")
    
    # Group by date
    by_date = {}
    for s in scans:
        date_str = s["received"][:10]  # YYYY-MM-DD
        by_date.setdefault(date_str, []).append(s)

    for date_str, items in by_date.items():
        out_dir = out_base / f"scans_{date_str}"
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== Downloading {len(items)} scans for {date_str} to {out_dir} ===")

        for idx, item in enumerate(items, 1):
            target_filename = f"SNT_5th_{date_str}_{idx:02d}.pdf"
            target_path = out_dir / target_filename
            
            if target_path.exists() and target_path.stat().st_size > 1024:
                print(f"[{idx}/{len(items)}] Already acquired: {target_filename} ({target_path.stat().st_size / 1024 / 1024:.2f} MB)")
                continue

            print(f"[{idx}/{len(items)}] Fetching {target_filename} ({item['size'] / 1024 / 1024:.2f} MB, sent {item['received']})...", end="", flush=True)
            pdf_bytes = await fetch_attachment_bytes(item["messageId"], item["attachmentId"])

            # Verify magic bytes
            if not pdf_bytes.startswith(b"%PDF-"):
                print(" ✗ FAILED: Invalid magic bytes!")
                continue

            target_path.write_bytes(pdf_bytes)
            print(f" ✓ ({len(pdf_bytes) / 1024 / 1024:.2f} MB)")

            # Inspect pages
            try:
                reader = PdfReader(str(target_path))
                print(f"    Pages: {len(reader.pages)}")
            except Exception as e:
                print(f"    Warning reading PDF structure: {e}")


if __name__ == "__main__":
    asyncio.run(main())
