import pandas as pd 
import json 
import os 
from sqlalchemy import create_engine

raw_files = [f for f in os.listdir('/opt/airflow/raw') if f.endswith('.json')]
latest_file = f"/opt/airflow/raw/{sorted(raw_files)[-1]}"
with open(latest_file,'r') as file:
    data = json.load(file)

current = data['current_weather']
df = pd.DataFrame([{
    'latitude': data['latitude'],
    'longitude': data['longitude'],
    'temperature': current['temperature'],
    'windspeed': current['windspeed'],
    'reading_time': current['time']
}])
print("Data transformed successfully :"),print(df)

engine = create_engine('mysql+pymysql://root:zikovitch123@host.docker.internal:3306/weather_etl')
df.to_sql('staging_weather',con=engine, if_exists='append', index=False)
print("Data loaded to staging successfully.")