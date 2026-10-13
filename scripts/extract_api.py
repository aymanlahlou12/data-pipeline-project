import requests
import json
from datetime import datetime

url = "https://api.open-meteo.com/v1/forecast?latitude=32.30&longitude=-9.23&current_weather=true"

response = requests.get(url)
raw_data = response.json()

today = datetime.now().strftime("%Y_%m_%d")
filename = f"raw/weather_{today}.json"

with open (filename, "w") as file:
    json.dump(raw_data, file, indent = 4)

print(f"Success! Weather data saved to {filename}")