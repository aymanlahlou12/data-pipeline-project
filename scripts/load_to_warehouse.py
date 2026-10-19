import pandas as pd
from sqlalchemy import text

from db_config import create_mysql_engine


PROCESSED_PATH = "/opt/airflow/processed/weather_data"
REQUIRED_COLUMNS = [
    "latitude",
    "longitude",
    "reading_time",
    "temperature",
    "windspeed",
]

df = pd.read_parquet(PROCESSED_PATH)
missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
if missing_columns:
    raise ValueError(f"Processed data is missing required columns: {missing_columns}")

weather_rows = (
    df[REQUIRED_COLUMNS]
    .dropna(subset=REQUIRED_COLUMNS)
    .drop_duplicates(subset=["latitude", "longitude", "reading_time"])
)
if weather_rows.empty:
    raise ValueError("No complete weather records were found in the processed data.")

engine = create_mysql_engine()
with engine.begin() as connection:
    for row in weather_rows.itertuples(index=False):
        location_result = connection.execute(
            text(
                """
                INSERT INTO dim_location (latitude, longitude)
                VALUES (:latitude, :longitude)
                ON DUPLICATE KEY UPDATE location_id = LAST_INSERT_ID(location_id)
                """
            ),
            {"latitude": float(row.latitude), "longitude": float(row.longitude)},
        )
        location_id = location_result.lastrowid

        time_result = connection.execute(
            text(
                """
                INSERT INTO dim_time (reading_time)
                VALUES (:reading_time)
                ON DUPLICATE KEY UPDATE time_id = LAST_INSERT_ID(time_id)
                """
            ),
            {"reading_time": str(row.reading_time)},
        )
        time_id = time_result.lastrowid

        connection.execute(
            text(
                """
                INSERT INTO fact_weather (location_id, time_id, temperature, windspeed)
                VALUES (:location_id, :time_id, :temperature, :windspeed)
                ON DUPLICATE KEY UPDATE
                    temperature = VALUES(temperature),
                    windspeed = VALUES(windspeed)
                """
            ),
            {
                "location_id": location_id,
                "time_id": time_id,
                "temperature": float(row.temperature),
                "windspeed": float(row.windspeed),
            },
        )

print(f"Successfully loaded or updated {len(weather_rows)} weather records.")
