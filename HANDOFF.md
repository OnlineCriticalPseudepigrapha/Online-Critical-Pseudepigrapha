# HANDOFF — Online Critical Pseudepigrapha

*Current as of 2026-08-27, `master` @ `200885d`, working tree clean and synced with origin.*

## What this repo is

Two coexisting apps share this repository:

1. **Legacy web2py app** (Python 2 — do not run on modern python3). Serves
   pseudepigrapha.org pages like `/docs/intro/<doc>`. All intro-page logic is in
   `controllers/docs.py` (`DISPLAY_FIELDS` at module top is the canonical ordered
   list of body fields). Draft editing uses the `draftdocs` table; publishing
   copies draft rows into `docs`.
2. **Static reader UI** (`reader.html` + `static/js/reader.js` +
   `static/css/reader.css` + `static/js/ocp-tei-parser.js`). No backend; parses
   `static/docs/*.xml` client-side and is deployed by GitHub Pages.

GitHub Pages currently deploys **from `master`** (source was flipped from
`reader-ui`; verified via `gh api repos/.../pages`). Custom domain:
pseudepigrapha.org — it depends on the committed `CNAME` file. Never delete
`CNAME` when resolving merge conflicts between branches that touched it;
always KEEP it.

## Where document introductions live

Only in `databases/storage.sqlite` (`docs` table; drafts in `draftdocs`).
The TEI XML files contain no `<front>`/intro elements.

The db is **gitignored** (`databases/*`) and was purged from git tracking in
early 2018 ("removing cached history of db files"). The newest snapshot in
history is from 2017-10-30 ("Removed private files", commit `d722fb6`). To
recover it:

    git checkout d722fb6 -- databases/
    # then immediately: git restore --staged databases/

Inspect with Python's sqlite3 module (the `sqlite3` CLI is not installed on
this machine). Caveat: the restored snapshot predates later live-site edits,
so the live server's db remains authoritative for anything newer than Oct
2017. There are 32 docs rows / 2 draftdocs rows in that snapshot; most body
fields (introduction, provenance, themes, status, manuscripts, bibliography,
corrections, sigla, copyright) are populated for nearly all documents.

## How intro text reaches the static site

1. `python3 scripts/export_intros.py` reads storage.sqlite → writes
   `static/docs/intros.json` (one entry per doc with title, version, fields).
2. `reader.js` fetches that JSON once per page load; `populateInfoDrawer()`
   renders the fields into the "About Document" drawer.
3. Regenerate `intros.json` after any live-db update — it is a frozen
   snapshot, not live data. Drafts are deliberately excluded (no auth in the
   static site).

## Recent work (Aug 2026)

- PR #33 merged `reader-ui` into `master` (commit `fd71ec0`); Pages now serves master.
- Document introductions surfaced in the reader's info drawer via
  `intros.json` (`2f63a69`).
- Bundled jQuery upgraded 1.11.2 → 3.7.1 after verifying the whole legacy
  stack against it (`2b2aeb8`): web2py.js, calendar.js timeEntry, summernote
  0.8.7 (which requires bootstrap.min.js loaded first for its tooltips), and
  same-origin ajax all pass.
- Omission markers display as U+2E06 (⸆) instead of `[omitted]`
  (`19f1288`) — both the reading pane (`reader.js:402`) and the apparatus
  readings table (`reader.js:456`). TJob.xml is the doc with omission units,
  useful for visual verification.
- Citation boxes show each document's own citation/editors; CSS fix so the
  whole box isn't italicized (`330b371`, `200885d`).

## Open items

### Dependabot alerts #4 and #7 (jQuery) — likely stale, watch and wait

Both should have auto-closed when jquery.js became 3.7.1, but GitHub's alert
records still show `updated_at: 2023-09-05` — i.e. Dependabot hasn't re-crawled
this manifest since before the fix. The file on master is verifiably v3.7.1
(sha256 of official 3.7.1 min build:
`fc9a93dd241f6b045cbff0481cf4e1901becd0e12fb45166a8f17f95823f0b1a`; check version with
`grep -m1 -o 'jQuery v[0-9.]*' static/js/jquery.js`). Expect them to flip to
"fixed" whenever the next crawl runs — could take days to weeks on a quiet
repo. Check with:

    gh api repos/OnlineCriticalPseudepigrapha/Online-Critical-Pseudepigrapha/dependabot/alerts \
      --jq '[.[] | select(.state=="open")]'

If they persist for many weeks despite the remote file being correct, dismiss
them with reason `fix_started` rather than re-upgrading anything.

Three other HIGH alerts (node-static, rollup ×2 from the vendored CodeMirror
copy under `static/js/codemirror/`) were dismissed as `not_used`: those are
upstream devDependencies never installed or executed here.

### Dead code flagged but not removed

- `views/layout.html` (~line 56) loads jQuery UI 1.10.3 from googleapis CDN.
  It is incompatible with jQuery 3 but inert — grep found zero jQuery-UI
  widget calls anywhere. Safe candidate for deletion.
- `static/js/superfish.js` references `$.browser` (removed in jQuery 1.9) and
  would break if ever loaded — but no view or controller references it. Safe
  candidate for deletion.

### Possible editorial follow-ups

- PssSol introduction (154 ch) is a "pre-publication draft — do not use for
  research" notice.
- The TAdam *draft* introduction (3,333 ch) is substantially longer than its
  published one (257 ch) — candidate for the publish-draft flow
  (`controllers/docs.py::draft_intro()` / `update_draft_intro()`).

## Verification recipes

- JS syntax: `node --check static/js/reader.js`
- Reader smoke test: serve the repo root with `python3 -m http.server <port>`
  and load `http://localhost:<port>/reader.html?doc=TJob.xml` (TJob exercises
  variant units and the ⸆ omission marker).
- Legacy-stack check: load any legacy page (e.g. a docs/intro route rendered
  statically won't work without web2py; instead inject jquery.js +
  web2py.js + calendar.js + bootstrap.min.js + summernote in order into a
  same-origin test page — all APIs must exist post-jQuery-3).
- Do NOT try `bin/runtest.py` or `test/` — they are Python 2/web2py-era and
  will not run without a py2 environment.
- Nothing under `databases/` is ever committed (auth/user tables; scrubbed
  from GitHub in 2018).

## Known gotchas

- Merge conflicts between old branches commonly hit `CNAME` (modify/delete) —
  always keep it.
- After pushing to a PR branch, GitHub reports `mergeable_state: unknown` for
  up to ~3 minutes before computing `clean` — poll before concluding conflict.
- The restored sqlite snapshot predates live-site edits; before trusting its
  content for anything date-sensitive, compare against the live server's db
  via the running web2py app.
