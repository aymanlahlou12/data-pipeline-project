import pandas as pd
from sqlalchemy import create_engine

db_url = "mysql+pymysql://root:zikovitch123@host.docker.internal:3306/weather_etl"
engine = create_engine(db_url)

processed_path = "/opt/airflow/processed/weather_data"
df = pd.read_parquet(processed_path)

df.to_sql("fact_weather", con=engine, if_exists="append", index=False)

print(f"Successfully loaded {len(df)} rows into the Data Warehouse!")