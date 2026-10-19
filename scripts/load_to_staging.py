import json
from pathlib import Path

from sqlalchemy import text

from db_config import create_mysql_engine


raw_files = sorted(Path("/opt/airflow/raw").glob("*.json"))
if not raw_files:
    raise FileNotFoundError("No JSON files were found in /opt/airflow/raw.")

with raw_files[-1].open("r", encoding="utf-8") as file:
    data = json.load(file)

current = data['current_weather']
reading = {
    "latitude": float(data["latitude"]),
    "longitude": float(data["longitude"]),
    "temperature": float(current["temperature"]),
    "windspeed": float(current["windspeed"]),
    "reading_time": str(current["time"]),
}

engine = create_mysql_engine()
with engine.begin() as connection:
    connection.execute(
        text(
            """
            INSERT INTO staging_weather
                (latitude, longitude, temperature, windspeed, reading_time)
            VALUES
                (:latitude, :longitude, :temperature, :windspeed, :reading_time)
            ON DUPLICATE KEY UPDATE
                temperature = VALUES(temperature),
                windspeed = VALUES(windspeed),
                extracted_at = CURRENT_TIMESTAMP
            """
        ),
        reading,
    )
print("Weather reading loaded or updated in staging successfully.")
