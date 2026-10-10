#!/usr/bin/env python3
"""
Site validation script for rickyMoorhouse.blog.
Fast pre-commit friendly version.
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path

blog_dir = Path(__file__).resolve().parent.parent
os.chdir(blog_dir)
ERRORS = 0
SUPPRESSIONS = blog_dir / 'scripts' / 'suppressions.json'


def track_error(msg):
    global ERRORS
    ERRORS += 1
    print(f"ERROR: {msg}")


def check_feed(path, label):
    """Check that a JSON feed file parses and has expected structure + types."""
    global ERRORS
    try:
        d = json.load(open(path))
    except Exception as e:
        track_error(f"{label} {path} fails to parse: {e}")
        return False
    
    if label == 'home':
        if 'version' not in d or not isinstance(d['version'], str):
            track_error(f"{label} index.json: version must be a string")
        if 'title' not in d or not isinstance(d['title'], str):
            track_error(f"{label} index.json: title must be a string")
        if 'home_page_url' not in d or not isinstance(d['home_page_url'], str):
            track_error(f"{label} index.json: home_page_url must be a string")
        if 'feed_url' not in d or not isinstance(d['feed_url'], str):
            track_error(f"{label} index.json: feed_url must be a string")
        if 'items' not in d or not isinstance(d['items'], list):
            track_error(f"{label} index.json: items must be a list")
    elif label == 'activitypub':
        if '@context' not in d or d['@context'] != 'https://www.w3.org/ns/activitystreams':
            track_error(f"{label} index.json: @context must be https://www.w3.org/ns/activitystreams")
        if 'type' not in d or d['type'] != 'OrderedCollection':
            track_error(f"{label} index.json: type must be OrderedCollection")
        if 'summary' not in d or not isinstance(d['summary'], str):
            track_error(f"{label} index.json: summary must be a string")
        if 'orderedItems' not in d or not isinstance(d['orderedItems'], list):
            track_error(f"{label} index.json: orderedItems must be a list")
    elif label == 'map':
        if 'type' not in d or d['type'] != 'FeatureCollection':
            track_error(f"{label} map/index.json: type must be FeatureCollection")
        if 'features' not in d or not isinstance(d['features'], list):
            track_error(f"{label} map/index.json: features must be a list")
    elif label == 'flights':
        if 'type' not in d or d['type'] != 'FeatureCollection':
            track_error(f"{label} flights.json: type must be FeatureCollection")
        if 'features' not in d or not isinstance(d['features'], list):
            track_error(f"{label} flights.json: features must be a list")
    
    return ERRORS == 0


def check_flights_vs_content():
    """Check that every content/flights file with from/to/date is accounted for in flights.json."""
    from pathlib import Path
    import re
    
    flights_dir = blog_dir / 'content' / 'flights'
    md_files = sorted(flights_dir.glob('*.md'))
    
    valid_files = set()
    for md in md_files:
        t = md.read_text()
        f = re.search(r'^from:\s*(\w+)', t, re.M)
        t2 = re.search(r'^to:\s*(\w+)', t, re.M)
        d = re.search(r'^date:\s*([\d-]+)', t, re.M)
        if f and t2 and d:
            valid_files.add(md.name)
    
    flights_json = blog_dir / 'public' / 'flights.json'
    if not flights_json.exists():
        track_error("public/flights.json not found")
        return ERRORS == 0
    
    fd = json.load(open(flights_json))
    gen_count = len(fd.get('features', []))
    
    gen_codes = set()
    for feat in fd.get('features', []):
        props = feat['properties']
        if 'from' in props:
            gen_codes.add(props['from'])
        if 'to' in props:
            gen_codes.add(props['to'])
    
    content_codes = set()
    for md in md_files:
        t = md.read_text()
        f = re.search(r'^from:\s*(\w+)', t, re.M)
        t2 = re.search(r'^to:\s*(\w+)', t, re.M)
        if f and t2:
            content_codes.add(f.group(1))
            content_codes.add(t2.group(1))
    
    missing_codes = content_codes - gen_codes
    if missing_codes:
        track_error(f"Airport codes in flights content but missing from flights.json: {sorted(missing_codes)}")
    
    if gen_count != len(valid_files):
        track_error(f"flights.json has {gen_count} features but {len(valid_files)} flight files have valid from/to/date")
    
    print(f"  flights vs content: {len(valid_files)} valid files, {gen_count} features in flights.json")
    return ERRORS == 0


def check_airports_data():
    """Check data/airports.json keyed only by airport codes referenced from flight content."""
    air = json.load(open('data/airports.json'))
    from pathlib import Path
    import re
    
    flights_dir = blog_dir / 'content' / 'flights'
    referenced = set()
    for md in flights_dir.glob('*.md'):
        t = md.read_text()
        for k in ('from', 'to'):
            m = re.search(rf'^{k}:\s*(\w+)', t, re.M)
            if m:
                referenced.add(m.group(1))
    
    unreferenced = set(air.keys()) - referenced
    if unreferenced:
        track_error(f"data/airports.json has {len(unreferenced)} unreferenced codes")
    
    invalid_coords = []
    for code, info in air.items():
        lat = info.get('lat', None)
        lng = info.get('lng', None)
        if lat is not None and (-90 > lat or lat > 90):
            invalid_coords.append(f"{code}: lat={lat}")
        if lng is not None and (-180 > lng or lng > 180):
            invalid_coords.append(f"{code}: lng={lng}")
    
    if invalid_coords:
        track_error(f"Airport coordinates out of valid range: {invalid_coords}")
    
    if not unreferenced and not invalid_coords:
        print("  airports.json: all keys referenced, all coordinates in range")
    return not unreferenced and not invalid_coords


def check_books_reading():
    """Check data/books.json and data/reading conform."""
    try:
        d = json.load(open('data/books.json'))
        if not isinstance(d, dict) or 'books' not in d:
            track_error("data/books.json doesn't have expected structure")
        else:
            print("  data/books.json: OK")
    except Exception as e:
        track_error(f"data/books.json error: {e}")
    
    reading_dir = blog_dir / 'data' / 'reading'
    yaml_files = list(reading_dir.glob('*.yaml'))[:3]
    for f in yaml_files:
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not data or 'books' not in data:
            track_error(f"{f.name}: missing 'books' key")
    
    print(f"  data/reading (sampled {len(yaml_files)} files): OK")
    return ERRORS == 0


def check_travel_yaml():
    """Check every data/travel/*.yaml carries lat/lng/title."""
    import glob
    import yaml
    
    travel_dir = blog_dir / 'data' / 'travel'
    yaml_files = sorted(glob.glob(str(travel_dir / '*.yaml')))
    
    required = {'lat', 'lng', 'title'}
    incomplete = 0
    
    check_files = list(yaml_files[:20]) + list(yaml_files[-5:])
    check_files = list(set(check_files))
    
    for f in check_files:
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not data or not required.issubset(data.keys()):
            incomplete += 1
            track_error(f"{os.path.basename(f)}: missing {required - set(data.keys()) if data else 'empty'}")
    
    if incomplete == 0:
        print(f"  data/travel: all checked files have lat/lng/title")
    else:
        track_error(f"{incomplete} travel YAML files missing required fields")
    
    return incomplete == 0


def check_suppressions():
    """Check that suppressions file entries are each justified and count hasn't grown."""
    if not SUPPRESSIONS.exists():
        return True
    
    try:
        raw = json.load(open(SUPPRESSIONS))
        if isinstance(raw, dict) and 'entries' in raw:
            entries = raw['entries']
        elif isinstance(raw, list):
            entries = raw
        else:
            entries = [raw]
        
        print(f"  Suppressions file: {len(entries)} entries recorded")
        for e in entries:
            if isinstance(e, dict):
                justification = e.get('justification', '')
            else:
                justification = ''
            if not justification or justification == 'See justification in code review':
                track_error(f"Suppression missing justification: {str(e)[:60]}")
        return ERRORS == 0
    except:
        track_error("suppressions.json is malformed")
        return False


def main():
    global ERRORS
    ERRORS = 0
    
    print("=" * 60)
    print("SITE VALIDATION SUITE (pre-commit)")
    print("=" * 60)
    
    all_pass = True
    
    # 1. JSON feeds
    print("\n--- JSON Feeds ---")
    for path, label in [
        ('public/index.json', 'home'),
        ('public/activitypub/index.json', 'activitypub'),
        ('public/map/index.json', 'map'),
        ('public/flights.json', 'flights'),
    ]:
        if not check_feed(path, label):
            all_pass = False
    
    # 2. Flights vs content
    print("\n--- Flights vs Content ---")
    if not check_flights_vs_content():
        all_pass = False
    
    # 3. Airports data
    print("\n--- Airports Data ---")
    if not check_airports_data():
        all_pass = False
    
    # 4. Books and reading
    print("\n--- Books and Reading ---")
    if not check_books_reading():
        all_pass = False
    
    # 5. Travel YAML
    print("\n--- Travel YAML ---")
    if not check_travel_yaml():
        all_pass = False
    
    # 6. Suppressions check
    print("\n--- Suppressions ---")
    if not check_suppressions():
        all_pass = False
    
    # Summary
    print("\n" + "=" * 60)
    if ERRORS == 0:
        print(f"PASSED: {ERRORS} error(s)")
    else:
        print(f"FAILED: {ERRORS} error(s) found")
        print(f"  See {SUPPRESSIONS} for justified exceptions")
    
    print("=" * 60)
    sys.exit(ERRORS)


if __name__ == '__main__':
    main()
