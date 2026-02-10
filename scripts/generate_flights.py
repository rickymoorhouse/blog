#!/usr/bin/env python3
import json
import re
import os
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
import yaml

# Load airports
with open('data/airports.json') as f:
    airports = json.load(f)

features = []
flights_dir = Path('content/flights')

# Statistics
total_flights = 0
airport_counter = Counter()
airline_counter = Counter()
airport_coords = {}

# Build coordinate lookup
for code, data in airports.items():
    airport_coords[code] = (data['lat'], data['lng'])

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in miles between two airports"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    miles = 3956 * c  # Earth radius in miles
    return miles

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None

total_distance = 0
total_time = timedelta(0)

for md_file in flights_dir.glob('*.md'):
    with open(md_file) as f:
        content = f.read()
    
    # Extract YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    flights_array = None
    via_airport = None
    
    if yaml_match:
        frontmatter = yaml.safe_load(yaml_match.group(1))
        if frontmatter and 'flights' in frontmatter:
            flights_array = frontmatter['flights']
        if frontmatter and 'via' in frontmatter:
            via_airport = frontmatter['via']
    
    from_match = re.search(r'^from:\s*(\w+)', content, re.MULTILINE)
    to_match = re.search(r'^to:\s*(\w+)', content, re.MULTILINE)
    date_match = re.search(r'^date:\s*([\d-]+)', content, re.MULTILINE)
    
    if from_match and to_match and date_match:
        from_code = from_match.group(1)
        to_code = to_match.group(1)
        
        from_airport = airports.get(from_code)
        to_airport = airports.get(to_code)
        
        if flights_array:
            # Process each flight segment
            prev_code = from_code
            for segment in flights_array:
                if segment.get('airport'):
                    code = segment['airport']
                    airport_counter[code] += 1
                    
                    # Calculate distance from previous airport
                    if prev_code in airport_coords and code in airport_coords:
                        lat1, lon1 = airport_coords[prev_code]
                        lat2, lon2 = airport_coords[code]
                        dist = haversine_distance(lat1, lon1, lat2, lon2)
                        total_distance += dist
                    
                    # Calculate time
                    arrive_str = segment.get('arrive')
                    depart_str = segment.get('depart')
                    if arrive_str and depart_str:
                        arrive = parse_date(arrive_str)
                        depart = parse_date(depart_str)
                        if arrive and depart:
                            if arrive < depart:
                                arrive += timedelta(days=1)
                            total_time += (arrive - depart)
                    
                    prev_code = code
                
                if segment.get('flight'):
                    # This is a flight segment
                    total_flights += 1
                    airline = segment.get('airline', '')
                    if airline:
                        airline_counter[airline] += 1
                    
                    # Add to GeoJSON features for each flight segment
                    if segment.get('airport') and prev_code in airport_coords and segment['airport'] in airport_coords:
                        lat1, lon1 = airport_coords[prev_code]
                        lat2, lon2 = airport_coords[segment['airport']]
                        if from_airport and airports.get(segment['airport']):
                            features.append({
                                "type": "Feature",
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": [
                                        [lon1, lat1],
                                        [lon2, lat2]
                                    ]
                                },
                                "properties": {
                                    "from": prev_code,
                                    "to": segment['airport'],
                                    "from_name": airports.get(prev_code, {}).get('name', prev_code),
                                    "to_name": airports.get(segment['airport'], {}).get('name', segment['airport']),
                                    "date": date_match.group(1),
                                    "year": date_match.group(1)[:4],
                                    "airline": airline,
                                    "flight": segment.get('flight', '')
                                }
                            })
                        prev_code = segment['airport']
            
            # Add final segment to destination
            if prev_code in airport_coords and to_code in airport_coords and prev_code != to_code:
                lat1, lon1 = airport_coords[prev_code]
                lat2, lon2 = airport_coords[to_code]
                dist = haversine_distance(lat1, lon1, lat2, lon2)
                total_distance += dist
                
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
                            "airline": "",
                            "flight": ""
                        }
                    })
        else:
            # Single flight, original logic
            total_flights += 1
            airport_counter[from_code] += 1
            airport_counter[to_code] += 1
            
            airline_match = re.search(r'^airline:\s*(\w+)', content, re.MULTILINE)
            if airline_match:
                airline_counter[airline_match.group(1)] += 1
            
            # Distance calculation
            if from_code in airport_coords and to_code in airport_coords:
                lat1, lon1 = airport_coords[from_code]
                lat2, lon2 = airport_coords[to_code]
                dist = haversine_distance(lat1, lon1, lat2, lon2)
                total_distance += dist
            
            # Time calculation
            depart_match = re.search(r'^depart:\s*([^\n]+)', content, re.MULTILINE)
            arrive_match = re.search(r'^arrive:\s*([^\n]+)', content, re.MULTILINE)
            depart_str = depart_match.group(1).strip() if depart_match else None
            arrive_str = arrive_match.group(1).strip() if arrive_match else None
            if depart_str and arrive_str:
                depart = parse_date(depart_str)
                arrive = parse_date(arrive_str)
                if depart and arrive:
                    if arrive < depart:
                        arrive += timedelta(days=1)
                    total_time += (arrive - depart)
            
            if from_airport and to_airport:
                flight_match = re.search(r'^flight:\s*(\w+)', content, re.MULTILINE)
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

print(f"Generated flights.json with {len(features)} flight segments")

# Generate flight stats
stats = {
    "total_flights": total_flights,
    "total_distance": round(total_distance),
    "total_time_days": total_time.days,
    "total_time_hours": total_time.seconds // 3600,
    "total_time_minutes": (total_time.seconds // 60) % 60,
    "top_airports": [{"code": code, "count": count} for code, count in airport_counter.most_common(10)],
    "top_airlines": [{"code": code, "count": count} for code, count in airline_counter.most_common(10)]
}

with open('data/flights/stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Generated flight stats: {total_flights} flights, {int(total_distance):,} miles, {total_time.days} days {total_time.seconds//3600}h {((total_time.seconds//60)%60)}m")

