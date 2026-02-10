#!/usr/bin/env python3
import os
import glob
import re
from datetime import datetime, timedelta
from collections import Counter

flights_dir = "content/flights"
flight_files = glob.glob(f"{flights_dir}/*.md")

# Airport coordinates (simplified - need to expand)
airport_coords = {
    'LHR': (51.4700, -0.4543),  # London Heathrow
    'RDU': (35.8801, -78.7880),  # Raleigh-Durham
    'LGW': (51.1537, -0.1820),  # London Gatwick
    'JFK': (40.6413, -73.7781),  # New York JFK
    'LAX': (33.9425, -118.4081),  # Los Angeles
    'SFO': (37.6213, -122.3790),  # San Francisco
    'ORD': (41.9742, -87.9073),  # Chicago O'Hare
    'CDG': (49.0097, 2.5479),  # Paris CDG
    'FRA': (50.0379, 8.5622),  # Frankfurt
    'AMS': (52.3105, 4.7683),  # Amsterdam
    'YVR': (49.1939, -123.1836),  # Vancouver
    'EWR': (40.6895, -74.1745),  # Newark
    'BOS': (42.3656, -71.0096),  # Boston
    'SEA': (47.4502, -122.3088),  # Seattle
    'MIA': (25.7959, -80.2870),  # Miami
    'DFW': (32.8968, -97.0380),  # Dallas
    'IAH': (29.9902, -95.3368),  # Houston
    'ATL': (33.6407, -84.4277),  # Atlanta
    'DEN': (39.8561, -104.6737),  # Denver
    'PHX': (33.4484, -112.0740),  # Phoenix
    'LAS': (36.0840, -115.1537),  # Las Vegas
    'SAN': (32.7338, -117.1933),  # San Diego
    'PDX': (45.5887, -122.5975),  # Portland
    'MSP': (44.8830, -93.2223),  # Minneapolis
    'STL': (38.7495, -90.3701),  # St Louis
    'BWI': (39.1754, -76.6683),  # Baltimore
    'DCA': (38.8512, -77.0377),  # Washington Reagan
    'IAD': (38.9531, -77.4565),  # Washington Dulles
    'YYZ': (43.6777, -79.6248),  # Toronto
    'YUL': (45.4703, -73.7408),  # Montreal
    'MEX': (19.4363, -99.0721),  # Mexico City
    'LIM': (-12.0219, -77.1143),  # Lima
    'SCL': (-33.3930, -70.7858),  # Santiago
    'EZE': (-34.8222, -58.5358),  # Buenos Aires
    'GIG': (-22.8089, -43.2436),  # Rio de Janeiro
    'GRU': (-23.4306, -46.4731),  # Sao Paulo
    'BOG': (4.7016, -74.1469),  # Bogota
    'UIO': (-0.1292, -78.3575),  # Quito
    'CUZ': (-13.5357, -71.9388),  # Cusco
    'LPA': (27.9318, -15.3866),  # Gran Canaria
    'TFS': (28.0445, -16.5735),  # Tenerife South
    'ACE': (28.9454, -13.6052),  # Lanzarote
    'FUE': (28.4527, -13.8676),  # Fuerteventura
    'PMI': (39.5536, 2.6272),  # Palma Mallorca
    'IBZ': (38.8729, 1.4432),  # Ibiza
    'AGP': (36.6749, -4.4991),  # Malaga
    'SVQ': (37.4184, -5.8931),  # Seville
    'BCN': (41.2969, 2.0783),  # Barcelona
    'VLC': (39.4893, -0.4816),  # Valencia
    'OPO': (41.2482, -8.6813),  # Porto
    'LIS': (38.7813, -9.1359),  # Lisbon
    'FAO': (37.0144, -7.9659),  # Faro
    'RVM': (36.8596, -6.3363),  # Jerez
    'NCE': (43.6584, 7.2159),  # Nice
    'MRS': (43.4356, 5.2136),  # Marseille
    'TLS': (43.6296, 1.3638),  # Toulouse
    'LYS': (45.7256, 5.0908),  # Lyon
    'NTE': (47.1569, -1.6071),  # Nantes
    'BOD': (44.8283, -0.7156),  # Bordeaux
    'FNI': (43.9117, 4.4024),  # Nimes
    'BIO': (43.3010, -2.9095),  # Bilbao
    'MAD': (40.4983, -3.5676),  # Madrid
    'GVA': (46.2280, 6.1090),  # Geneva
    'ZRH': (47.4647, 8.5492),  # Zurich
    'VIE': (48.1103, 16.5697),  # Vienna
    'PRG': (50.1008, 14.2555),  # Prague
    'BUD': (47.4393, 19.2616),  # Budapest
    'KBP': (50.3450, 30.8947),  # Kiev
    'WAW': (52.1657, 20.9678),  # Warsaw
    'KRK': (50.0777, 19.7848),  # Krakow
    'DBV': (42.5614, 18.2636),  # Dubrovnik
    'SPU': (43.5390, 16.2980),  # Split
    'ZAD': (44.1078, 15.3485),  # Zadar
    'PUY': (44.8935, 13.9222),  # Pula
    'RJK': (45.2126, 14.5703),  # Rijeka
    'OSI': (45.4669, 13.5146),  # Osijek
    'ZAG': (45.7429, 16.0689),  # Zagreb
    'SLU': (14.0203, -60.9936),  # St Lucia
    'ANU': (17.1367, -61.7928),  # Antigua
    'PUJ': (18.5717, -68.4200),  # Punta Cana
    'SDQ': (18.4294, -69.6689),  # Santo Domingo
    'POS': (10.5953, -61.3372),  # Trinidad
    'BGI': (13.0746, -59.4925),  # Barbados
    'UVF': (13.7332, -60.9533),  # St Lucia Hewanorra
    'SXM': (17.4986, -63.1116),  # St Maarten
    'HAV': (22.9892, -82.4091),  # Havana
    'VRA': (23.1619, -81.2532),  # Varadero
    'MBJ': (18.5033, -77.8993),  # Montego Bay
    'KIN': (17.9357, -76.7875),  # Kingston
    'PAP': (18.5801, -72.2926),  # Port au Prince
    'CUR': (12.1889, -68.8838),  # Curacao
    'BON': (12.1310, -68.2680),  # Bonaire
    'AUA': (12.5014, -70.0131),  # Aruba
    'SAL': (13.4409, -89.0518),  # El Salvador
    'GUA': (14.5833, -90.5275),  # Guatemala
    'SAP': (15.4526, -87.9237),  # San Pedro Sula
    'BZE': (17.5391, -88.3080),  # Belize
}

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in miles between two airports"""
    from math import radians, cos, sin, asin, sqrt
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

total_flights = 0
total_distance = 0
total_time = timedelta(0)
airport_counter = Counter()
airline_counter = Counter()

for f in flight_files:
    with open(f) as file:
        content = file.read()
    
    # Extract frontmatter
    from_re = re.search(r'from:\s*(\w+)', content)
    to_re = re.search(r'to:\s*(\w+)', content)
    depart_re = re.search(r'depart:\s*([^\n]+)', content)
    arrive_re = re.search(r'arrive:\s*([^\n]+)', content)
    airline_re = re.search(r'airline:\s*(\w+)', content)
    
    from_airport = from_re.group(1) if from_re else None
    to_airport = to_re.group(1) if to_re else None
    depart_str = depart_re.group(1).strip() if depart_re else None
    arrive_str = arrive_re.group(1).strip() if arrive_re else None
    airline = airline_re.group(1) if airline_re else None
    
    if from_airport and to_airport:
        total_flights += 1
        airport_counter[from_airport] += 1
        airport_counter[to_airport] += 1
        
        # Calculate distance
        if from_airport in airport_coords and to_airport in airport_coords:
            lat1, lon1 = airport_coords[from_airport]
            lat2, lon2 = airport_coords[to_airport]
            dist = haversine_distance(lat1, lon1, lat2, lon2)
            total_distance += dist
        
        # Calculate time
        if depart_str and arrive_str:
            depart = parse_date(depart_str)
            arrive = parse_date(arrive_str)
            if depart and arrive:
                # Handle overnight flights
                if arrive < depart:
                    arrive += timedelta(days=1)
                total_time += (arrive - depart)
    
    if airline:
        airline_counter[airline] += 1

print(f"Total Flights: {total_flights}")
print(f"Total Distance: {int(total_distance):,} miles")
print(f"Total Time: {total_time.days} days, {total_time.seconds//3600} hours, {(total_time.seconds//60)%60} minutes")
print(f"\nTop 5 Airports:")
for airport, count in airport_counter.most_common(5):
    print(f"  {airport}: {count}")
print(f"\nTop Airlines:")
for airline, count in airline_counter.most_common(10):
    print(f"  {airline}: {count}")
