#!/usr/bin/env python3
"""
Check every feed and site URL in data/blogroll.yaml for broken links.

Usage: python3 scripts/check_blogroll.py [--stale-years N] [--report PATH] [--only-problems] [--json]

Each xmlUrl and htmlUrl is fetched with GET (following redirects, 15s timeout,
one retry on connection errors) and classified as:
  ok          200, and for feeds the body is RSS, Atom or JSON Feed
  redirected  a permanent 301/308 to another URL; update to the final URL
  broken      4xx/5xx, DNS or TLS failure, or a timeout after the retry
  unverified  403/429, usually bot protection such as Cloudflare
  not-a-feed  the xmlUrl returns 200 but isn't a feed (e.g. an HTML page)
Feeds whose newest item is older than --stale-years (default 2) are also
listed as stale. URLs that look like they carry a secret (token=, key=, ...)
are not fetched and are flagged, since they shouldn't be published.

stdout gets a summary plus the problems. --report PATH writes the full Markdown
report, including the OK URLs unless --only-problems is given. --json prints
machine-readable results instead.

Not part of build.sh on purpose: it hits the network. Exits 1 if anything is
broken or not a feed.
"""

import argparse
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import yaml

BLOGROLL = Path(__file__).resolve().parent.parent / 'data' / 'blogroll.yaml'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) '
      'Version/17.0 Safari/605.1.15 (blogroll link check; rickymoorhouse.uk)')
ACCEPT = ('application/rss+xml, application/atom+xml, application/feed+json, application/json, '
          'text/xml, text/html;q=0.8, */*;q=0.5')
SECRET = re.compile(r'[?&](token|key|api_?key|secret|auth|password|access_token|sig)=', re.I)
TIMEOUT = 15
CLASSES = ('broken', 'not-a-feed', 'unverified', 'redirected', 'ok')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


NO_REDIRECT = urllib.request.build_opener(NoRedirect)


def request(url):
    return urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': ACCEPT})


def parse_date(text):
    text = (text or '').strip()
    if not text:
        return None
    try:
        date = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            date = datetime.fromisoformat(text.replace('Z', '+00:00'))
        except ValueError:
            return None
    return date if date.tzinfo else date.replace(tzinfo=timezone.utc)


def newest_item(body):
    """Latest item date in an RSS, Atom or JSON feed, or None."""
    dates = []
    if body.lstrip().startswith(b'{'):
        try:
            for item in json.loads(body).get('items', []):
                dates.append(parse_date(item.get('date_published') or item.get('date_modified')))
        except (ValueError, AttributeError):
            return None
    else:
        try:
            root = ET.fromstring(body)
        except ET.ParseError:
            return None
        for el in root.iter():
            if el.tag.split('}')[-1] in ('pubDate', 'published', 'updated', 'date'):
                dates.append(parse_date(el.text))
    dates = [d for d in dates if d]
    return max(dates) if dates else None


def redirect_codes(url):
    """Status codes of the redirect chain from url, walked without following."""
    codes = []
    for _ in range(10):
        try:
            NO_REDIRECT.open(request(url), timeout=TIMEOUT).close()
            break
        except urllib.error.HTTPError as e:
            location = e.headers.get('location')
            if e.code not in (301, 302, 303, 307, 308) or not location:
                break
            codes.append(e.code)
            url = urllib.parse.urljoin(url, location)
        except Exception:
            break
    return codes


def check(url, is_feed):
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(request(url), timeout=TIMEOUT) as r:
                body = r.read(5_000_000 if is_feed else 4096)
                result = {'status': r.status, 'final': r.geturl()}
            break
        except urllib.error.HTTPError as e:
            kind = 'unverified' if e.code in (403, 429) else 'broken'
            return {'class': kind, 'reason': f'{e.code} {e.reason}'}
        except Exception as e:
            if attempt == 2:
                return {'class': 'broken', 'reason': f'{type(e).__name__}: {getattr(e, "reason", e)}'}
            time.sleep(2)

    if is_feed:
        head = body[:3000].decode('utf-8', 'replace').lstrip('﻿').lstrip()
        if not (re.search(r'<(rss|feed|rdf:RDF)\b', head) or re.search(r'"version"\s*:\s*"https?://jsonfeed', head)):
            return {'class': 'not-a-feed', 'reason': f'200 but body starts {head[:60]!r}'}
        result['newest'] = newest_item(body)

    if result['final'] != url and any(c in (301, 308) for c in redirect_codes(url)):
        result['class'] = 'redirected'
    else:
        result['class'] = 'ok'
    return result


def main():
    parser = argparse.ArgumentParser(description='Check data/blogroll.yaml for broken links.')
    parser.add_argument('--stale-years', type=float, default=2, help='flag feeds with no item newer than this (default 2)')
    parser.add_argument('--report', type=Path, help='write the full Markdown report to this file')
    parser.add_argument('--only-problems', action='store_true', help='leave OK URLs out of the --report file')
    parser.add_argument('--json', action='store_true', help='print results as JSON instead of the summary')
    args = parser.parse_args()

    feeds = (yaml.safe_load(BLOGROLL.read_text(encoding='utf-8')) or {}).get('feeds') or []
    targets, secrets = [], []
    for feed in feeds:
        for field, is_feed in (('xmlUrl', True), ('htmlUrl', False)):
            url = feed.get(field)
            if not url:
                continue
            if SECRET.search(url):
                secrets.append((feed['title'], field))
            else:
                targets.append((feed['title'], field, url, is_feed))

    with cf.ThreadPoolExecutor(10) as pool:
        results = list(pool.map(lambda t: (*t, check(t[2], t[3])), targets))

    cutoff = datetime.now(timezone.utc) - timedelta(days=365.25 * args.stale_years)
    stale = [(title, url, r['newest']) for title, _, url, _, r in results
             if r.get('newest') and r['newest'] < cutoff]

    counts = {c: sum(r['class'] == c for *_, r in results) for c in CLASSES}
    if args.json:
        print(json.dumps({
            'counts': {**counts, 'stale': len(stale)},
            'secrets': [{'title': t, 'field': f} for t, f in secrets],
            'results': [{'title': t, 'field': f, 'url': u, **r} for t, f, u, _, r in results],
        }, indent=2, default=str))
    else:
        print(render(feeds, targets, counts, secrets, results, stale, args.stale_years, include_ok=False))
    if args.report:
        args.report.write_text(render(feeds, targets, counts, secrets, results, stale, args.stale_years,
                                      include_ok=not args.only_problems), encoding='utf-8')
        print(f'Wrote {args.report}', file=sys.stderr)
    sys.exit(1 if counts['broken'] or counts['not-a-feed'] else 0)


def render(feeds, targets, counts, secrets, results, stale, stale_years, include_ok):
    lines = [f'# Blogroll link check, {datetime.now():%d %b %Y}', '',
             f'{len(feeds)} entries, {len(targets)} URLs checked: '
             + ', '.join(f'{n} {c}' for c, n in counts.items()) + f', {len(stale)} stale.', '']
    if secrets:
        lines += ['## Possible secrets (not fetched; these would be published in following.opml)', '']
        lines += [f'- {title}: {field} has a token/key-style parameter' for title, field in secrets] + ['']
    for cls in CLASSES if include_ok else CLASSES[:-1]:
        rows = [(t, f, u, r) for t, f, u, _, r in results if r['class'] == cls]
        if not rows:
            continue
        lines += [f'## {cls.capitalize()}', '']
        for title, field, url, r in rows:
            detail = {'redirected': f' - now {r.get("final")}', 'ok': ''}.get(cls, f' - {r.get("reason")}')
            lines.append(f'- {title} ({field}): {url}{detail}')
        lines.append('')
    if stale:
        lines += [f'## Stale (no item in {stale_years:g} years)', '']
        lines += [f'- {title}: newest item {newest:%d %b %Y} ({url})'
                  for title, url, newest in sorted(stale, key=lambda s: s[2])]
        lines.append('')
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
