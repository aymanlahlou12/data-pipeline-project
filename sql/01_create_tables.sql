CREATE DATABASE IF NOT EXISTS weather_etl;
USE weather_etl;

CREATE TABLE IF NOT EXISTS staging_weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    windspeed FLOAT,
    reading_time VARCHAR(50),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);









SELECT * FROM weather_etl.staging_weather;