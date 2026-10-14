#!/usr/bin/env python3
"""
Merge feeds from one or more OPML exports into data/blogroll.yaml.

Usage: python3 scripts/import_opml.py [--dry-run] FILE.opml [FILE2.opml ...]

- Existing entries are never removed or reordered, and their fields are never
  overwritten. A missing htmlUrl or description is filled in from the import.
- Feeds are de-duplicated on a normalised xmlUrl (http/https, "www.", host case,
  trailing slash, fragment and tracking parameters ignored), against the blogroll
  and across all the input files.
- A new feed whose htmlUrl matches an existing site is still added, but reported
  as a possible duplicate, since one site can have several feeds.
- The innermost OPML folder becomes the category.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml

BLOGROLL = Path(__file__).resolve().parent.parent / 'data' / 'blogroll.yaml'
FIELDS = ('title', 'xmlUrl', 'htmlUrl', 'description', 'category')
FILLABLE = ('htmlUrl', 'description')
TRACKING = {'fbclid', 'gclid', 'mc_cid', 'mc_eid', 'ref', 'source'}


def strip_tracking(query):
    return urlencode([(k, v) for k, v in parse_qsl(query, keep_blank_values=True)
                      if not k.lower().startswith('utm_') and k.lower() not in TRACKING])


def clean(url):
    """The URL as stored: tracking parameters and fragment removed, otherwise as given."""
    parts = urlsplit(url.strip())
    return urlunsplit(parts._replace(query=strip_tracking(parts.query), fragment=''))


def normalise(url):
    """Comparable form of an absolute URL, or None if it isn't one."""
    parts = urlsplit((url or '').strip())
    if parts.scheme.lower() not in ('http', 'https') or not parts.netloc:
        return None
    host = parts.netloc.lower().removeprefix('www.')
    path = parts.path.rstrip('/')
    query = strip_tracking(parts.query)
    return host + path + (f'?{query}' if query else '')


def outlines(node, folder=None):
    """Yield (outline, innermost folder name) for every outline carrying a feed."""
    for child in node.findall('outline'):
        if child.get('xmlUrl') is not None:
            yield child, folder
        else:
            name = (child.get('title') or child.get('text') or '').strip()
            yield from outlines(child, name or folder)


def load_blogroll():
    text = BLOGROLL.read_text(encoding='utf-8')
    # The documentation comments above `feeds:` are kept as-is on rewrite.
    lines = text.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if line.startswith('feeds:')), len(lines))
    feeds = (yaml.safe_load(text) or {}).get('feeds') or []
    return ''.join(lines[:start]), feeds


def dump_feeds(feeds):
    """Readable, stable YAML: one block per feed, fields in a fixed order, values quoted."""
    if not feeds:
        return 'feeds: []\n'
    out = ['feeds:\n']
    for feed in feeds:
        keys = [k for k in FIELDS if feed.get(k)] + [k for k in feed if k not in FIELDS]
        for i, key in enumerate(keys):
            value = yaml.safe_dump(feed[key], default_style='"', allow_unicode=True, width=10000).strip()
            value = value.removesuffix('\n...').strip()
            out.append(f'{"  - " if i == 0 else "    "}{key}: {value}\n')
    return ''.join(out)


def main():
    parser = argparse.ArgumentParser(description='Merge OPML exports into data/blogroll.yaml.')
    parser.add_argument('files', nargs='+', type=Path, help='OPML files to import')
    parser.add_argument('--dry-run', action='store_true', help='report what would change without writing')
    args = parser.parse_args()

    header, feeds = load_blogroll()
    by_feed = {normalise(f.get('xmlUrl')): f for f in feeds if normalise(f.get('xmlUrl'))}
    by_site = {normalise(f.get('htmlUrl')): f for f in feeds if normalise(f.get('htmlUrl'))}

    added = filled = duplicates = invalid = failed = 0
    for path in args.files:
        try:
            body = ET.parse(path).getroot().find('body')
            if body is None:
                raise ValueError('no <body> element')
        except (OSError, ET.ParseError, ValueError) as e:
            print(f'ERROR {path}: {e} (file skipped)', file=sys.stderr)
            failed += 1
            continue

        print(f'{path}:')
        for outline, folder in outlines(body):
            xml_url = (outline.get('xmlUrl') or '').strip()
            html_url = (outline.get('htmlUrl') or '').strip()
            key = normalise(xml_url)
            if not key:
                print(f'  skip   invalid or relative feed URL: {xml_url!r}')
                invalid += 1
                continue
            xml_url = clean(xml_url)
            html_url = clean(html_url) if normalise(html_url) else ''

            candidate = {
                'title': (outline.get('title') or outline.get('text') or '').strip()
                         or urlsplit(xml_url).netloc.removeprefix('www.'),
                'xmlUrl': xml_url,
                'htmlUrl': html_url,
                'description': (outline.get('description') or '').strip(),
                'category': folder,
            }

            existing = by_feed.get(key)
            if existing:
                missing = [k for k in FILLABLE if candidate[k] and not existing.get(k)]
                for k in missing:
                    existing[k] = candidate[k]
                if missing:
                    print(f'  fill   {existing["title"]}: {", ".join(missing)}')
                    filled += 1
                else:
                    print(f'  skip   duplicate of {existing["title"]!r}: {xml_url}')
                    duplicates += 1
                continue

            entry = {k: candidate[k] for k in FIELDS if candidate[k]}
            site = normalise(html_url)
            if site and site in by_site:
                print(f'  add    {entry["title"]} <{xml_url}>  (possible duplicate: same site as {by_site[site]["title"]!r})')
            else:
                print(f'  add    {entry["title"]} <{xml_url}>')
            feeds.append(entry)
            by_feed[key] = entry
            if site:
                by_site.setdefault(site, entry)
            added += 1

    print(f'\n{added} added, {filled} filled in, {duplicates} duplicate(s), '
          f'{invalid} invalid, {failed} file(s) failed, {len(feeds)} total'
          + (' (dry run, nothing written)' if args.dry_run else ''))
    if not args.dry_run and (added or filled):
        BLOGROLL.write_text(header + dump_feeds(feeds), encoding='utf-8')
        print(f'Wrote {BLOGROLL}')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
