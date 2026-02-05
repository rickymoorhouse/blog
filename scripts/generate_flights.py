#!/usr/bin/env python3
import json
import re
import os
from pathlib import Path

# Load airports
with open('data/airports.json') as f:
    airports = json.load(f)

features = []
flights_dir = Path('content/flights')

for md_file in flights_dir.glob('*.md'):
    with open(md_file) as f:
        content = f.read()
    
    from_match = re.search(r'^from:\s*(\w+)', content, re.MULTILINE)
    to_match = re.search(r'^to:\s*(\w+)', content, re.MULTILINE)
    date_match = re.search(r'^date:\s*([\d-]+)', content, re.MULTILINE)
    airline_match = re.search(r'^airline:\s*(\w+)', content, re.MULTILINE)
    flight_match = re.search(r'^flight:\s*(\w+)', content, re.MULTILINE)
    
    if from_match and to_match and date_match:
        from_code = from_match.group(1)
        to_code = to_match.group(1)
        
        from_airport = airports.get(from_code)
        to_airport = airports.get(to_code)
        
        if from_airport and to_airport:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [from_airport['lng'], from_airport['lat']],
                        [to_airport['lng'], to_airport['lat']]
                    ]
                },
                "properties": {
                    "from": from_code,
                    "to": to_code,
                    "from_name": from_airport['name'],
                    "to_name": to_airport['name'],
                    "date": date_match.group(1),
                    "year": date_match.group(1)[:4],
                    "airline": airline_match.group(1) if airline_match else "",
                    "flight": flight_match.group(1) if flight_match else ""
                }
            })

output = {
    "type": "FeatureCollection",
    "features": features
}

with open('public/flights.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Generated flights.json with {len(features)} flights")
