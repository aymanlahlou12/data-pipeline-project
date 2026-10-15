USE weather_etl;

CREATE TABLE IF NOT EXISTS dim_location(
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    UNIQUE(latitude, longitude)
);

CREATE TABLE IF NOT EXISTS dim_time(
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    reading_time VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS fact_weather (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT,
    time_id INT,
    temperature FLOAT,
    windspeed FLOAT,
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);


INSERT IGNORE INTO dim_location (latitude, longitude)
SELECT DISTINCT latitude, longitude FROM staging_weather;

INSERT IGNORE INTO dim_time (reading_time)
SELECT DISTINCT reading_time FROM staging_weather;

INSERT INTO fact_weather (location_id, time_id, temperature, windspeed)
SELECT 
    l.location_id,
    t.time_id,
    s.temperature,
    s.windspeed
FROM staging_weather s
JOIN dim_location l ON s.latitude = l.latitude AND s.longitude = l.longitude
JOIN dim_time t ON s.reading_time = t.reading_time;