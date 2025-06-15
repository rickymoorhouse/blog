# Open CSV File
import csv
import os
import sys
import re
import json
import datetime

# Get the current working directory
current_directory = os.getcwd()
# Get the path to the CSV file
csv_file_path = os.path.join(current_directory, 'flights.csv')
# Check if the file exists
if not os.path.isfile(csv_file_path):
    print(f"File {csv_file_path} does not exist.")
    sys.exit(1)
# Read the CSV file
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Create a list to store the flight data
    flight_data = []
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Convert the row to a dictionary and append it to the list
        flight_data.append(row)
        print(row)
        # Convert the data to Markdown format
        output = f"""---
layout: flight
from: {row['From']}
to: {row['To']}
date: {row['Date']}
airline: {row['Airline']}
flight: {row['Flight']}
""" 
        # if departure is not empty, add it to the output
        if row['Gate Departure (Actual)']:
            output += f"depart: {row['Gate Departure (Actual)']}:00\n"
            output += f"date: {row['Gate Departure (Actual)']}:00\n"
        else:
            output += f"date: {row['Date']}\n"
        # if arrival is not empty, add it to the output
        if row['Gate Arrival (Actual)']:
            output += f"arrive: {row['Gate Arrival (Actual)']}:00\n"
        # if tail not empty, add it to the output
        if row['Tail Number']:
            output += f"tail: {row['Tail Number']}\n"
        # if aircraft not empty, add it to the output
        if row['Aircraft Type Name']:
            output += f"aircraft: {row['Aircraft Type Name']}\n"
        output += "\n---"
        # Write the output to a file
        output_file_path = os.path.join(current_directory, 'flights', f"{row['Date']}-{row['Airline']}{row['Flight']}.md")
        # Ensure the flights directory exists
        flights_directory = os.path.join(current_directory, 'flights')
        if not os.path.exists(flights_directory):
            os.makedirs(flights_directory)  
        # Check if the file already exists
        if os.path.isfile(output_file_path):
            print(f"File {output_file_path} already exists. Skipping.")
            continue
        # Write the output to the file
        with open(output_file_path, mode='w', encoding='utf-8') as output_file:
            output_file.write(output)
        # Print the output to the console
        print(f"Output written to {output_file_path}")
