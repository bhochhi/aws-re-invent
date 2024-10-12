import requests
import csv

# Constants
url = 'https://catalog.awsevents.com/api/search'
headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'rfauthtoken':'556fae35eeea46cda5bf17f019e55cae',
    'rfapiprofileid': '3ol5ZxLLv8O462NxA19WthWuAzT7Ud9o'
}
params_template = 'showMyInterest=true&type=session&browserTimezone=America%2FChicago&catalogDisplay=list&from={}'

# Function to fetch data
def fetch_data(from_value):
    params = params_template.format(from_value)
    response = requests.post(url, headers=headers, data=params)
    response.raise_for_status()
    data = response.json()
    if from_value == 0:
        print(f'from value {from_value}==>Total items: {data.get("sectionList", [{}])[0].get("total",0)} - Items per page: {data.get("sectionList", [{}])[0].get("numItems",0)}')
        return data.get("sectionList", [{}])[0].get("items", [{}])
    print(f'from value {from_value}==>Total items: {data.get("total",0)} - Items per page: {data.get("numItems",0)}')
    return data.get("items",[{}])

# Collect data
all_items = []
for i in range(50):
    from_value = i * 50
    print(f"Fetching data from {from_value}...")
    items = fetch_data(from_value)
    if not items:
        break
    for item in items:
        times = item.get('times', [{}])[0]
        all_items.append({
            "type": item.get('type', 'N/A'),
            "title": item.get('title', 'N/A'),
            "abstract": item.get('abstract', 'N/A'),
            "date": times.get('date', 'N/A'),
            "startTime": times.get('startTime', 'N/A'),
            "endTime": times.get('endTime', 'N/A'),
            "room": times.get('room', 'N/A'),
        })

# Create the CSV file
csv_file = 'fav_sessions_filtered.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["type","title", "abstract", "date", "startTime", "endTime", "room"])
    writer.writeheader()
    for session in all_items:
        writer.writerow(session)

print(f"CSV file '{csv_file}' created successfully.")
