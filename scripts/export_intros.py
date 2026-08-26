#!/usr/bin/env python3
"""
Export document introduction/body fields from the web2py SQLite database
(databases/storage.sqlite) to a static JSON file consumed by the standalone
reader UI (static/js/reader.js).

The reader is deployed as a fully static site (GitHub Pages), so it cannot
query the web2py database directly. This script bridges the gap: run it after
the database is updated, commit the resulting static/docs/intros.json, and
the reader's "About Document" drawer will show the introduction and related
body fields for each document.

Usage (from the repository root):

    python3 scripts/export_intros.py [--db databases/storage.sqlite] \
        [--out static/docs/intros.json]

Only the public display fields from the `docs` table are exported. Draft rows
(`draftdocs`) are intentionally excluded because the static site has no
authentication layer.
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys

# Same fields, in the same display order, as controllers/docs.py DISPLAY_FIELDS
DISPLAY_FIELDS = [
    ('introduction', 'Introduction'),
    ('provenance', 'Provenance and Cultural Setting'),
    ('themes', 'Major Themes'),
    ('status', 'Current State of the OCP Text'),
    ('manuscripts', 'Manuscripts'),
    ('bibliography', 'Bibliography'),
    ('corrections', 'Corrections'),
    ('sigla', 'Sigla Used in the Text'),
    ('copyright', 'Copyright Information'),
]

DEFAULT_DB = 'databases/storage.sqlite'
DEFAULT_OUT = 'static/docs/intros.json'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=DEFAULT_DB, help='Path to storage.sqlite')
    parser.add_argument('--out', default=DEFAULT_OUT, help='Path for output JSON')
    args = parser.parse_args(argv)

    if not os.path.exists(args.db):
        sys.exit(f'Database not found: {args.db}\n'
                 f'Restore it from git history if needed, e.g.:\n'
                 f'  git checkout d722fb6 -- databases/')

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    columns = {row[1] for row in conn.execute('PRAGMA table_info(docs)')}
    export_fields = [(k, label) for k, label in DISPLAY_FIELDS if k in columns]

    docs = {}
    empty = 0
    for row in conn.execute('SELECT * FROM docs'):
        filename = row['filename']
        if not filename:
            continue
        entry = {
            'title': row['name'],
            'version': row['version'],
            'fields': OrderedDict_safe(export_fields, row),
        }
        if not any(entry['fields'].values()):
            empty += 1
        docs[f'{filename}.xml'] = entry
    conn.close()

    payload = {
        '_meta': {
            'exported': datetime.date.today().isoformat(),
            'source': 'web2py databases/storage.sqlite (docs table)',
            'note': 'Regenerate with scripts/export_intros.py after database updates.',
        },
        'documents': docs,
    }

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write('\n')

    populated = len(docs) - empty
    print(f'Exported {len(docs)} documents ({populated} with intro/body text) '
          f'to {args.out}')


def OrderedDict_safe(fields, row):
    return {key: row[key] for key, _label in fields
            if row[key] is not None and str(row[key]).strip()}


if __name__ == '__main__':
    main()
