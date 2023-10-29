"""
This module converts a CSV file to a JSON file.
"""

import csv
import json
from datetime import datetime

# Initialize a list to store the JSON objects
projects = []

# Define a function to convert the date string to the desired format
def convert_date(date_str):
    """
    Convert a date string in the format 'MM/YYYY' to a dictionary.
    
    Args:
        date_str (str): A date string in the format 'MM/YYYY'.
    
    Returns:
        dict: A dictionary with keys 'quarter', 'month', and 'year'.
            'quarter' is an integer between 1 and 4.
            'month' is an integer between 1 and 12.
            'year' is an integer representing the year.
    """
    date_obj = datetime.strptime(date_str, "%m/%Y")
    return {
        "quarter": (date_obj.month - 1) // 3 + 1,
        "month": date_obj.month,
        "year": date_obj.year
    }

# Read the CSV data and create JSON objects
with open('../projects/coinbase.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row //TODO read attribute mapping from header row
    PROJECT_ID = 1
    for row in reader:
        project = {
            "index": PROJECT_ID,
            "date": convert_date(row[3]),
            "description": row[0] + " - " + row[2] + " - " + row[1],
            "id": "CB" + "-" + str(PROJECT_ID),
            "images": [{"url": ""}],  # // FIXME
            "link": "https://app.url/",  # // FIXME
            "name": row[0],
            "organization": "Coinbase",
            "pillar": row[6],
            "team": row[5],
            "type": row[2],
            "value": row[4] +  " - " + row[5],
            "startDate": row[3],  # // FIXME
            "endDate": row[3]  # // FIXME
        }
        projects.append(project)
        PROJECT_ID += 1

# Create a JSON object with the "projects" key
result = {
    "projects": projects
}

# Write the JSON string to a file
with open('../projects/coinbase.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=4)
