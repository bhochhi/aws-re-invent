import json
import csv

all_sessions_file = 'all_sessions.json'

# Load all sessions data
try:
    with open(all_sessions_file, 'r') as f:
        all_sessions_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {all_sessions_file} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {all_sessions_file} contains invalid JSON.")
    exit(1)

# Extract and flatten session data
flattened_sessions = []
for session in all_sessions_data["items"]:
    times = session.get('times', [{}])[0]
    #do not append if room is not available for the session
    if times.get('room', 'N/A') == 'N/A':
        continue
    flattened_sessions.append({
        "sessionID": session.get('sessionID', 'N/A'),
        "title": session.get('title', 'N/A'),
        "abstract": session.get('abstract', 'N/A'),
        "date": times.get('date', 'N/A'),
        "startTime": times.get('startTime', 'N/A'),
        "endTime": times.get('endTime', 'N/A'),
        "room": times.get('room', 'N/A'),
        "seatsRemaining": times.get('seatsRemaining', 'N/A'),
        "venue": times.get('roomId', 'Unknown')
    })

# Create the flattened JSON file
flattened_json_file = 'all_sessions_flattened.json'
with open(flattened_json_file, 'w') as f:
    json.dump(flattened_sessions, f, indent=4)

# Create the CSV file
csv_file = 'all_sessions_flattened.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["sessionID", "title", "abstract", "date", "startTime", "endTime", "room", "seatsRemaining", "venue"])
    writer.writeheader()
    for session in flattened_sessions:
        writer.writerow(session)

print(f"Flattened JSON file '{flattened_json_file}' and CSV file '{csv_file}' created successfully.")
