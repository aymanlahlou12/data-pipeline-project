USE weather_etl;

CREATE TABLE IF NOT EXISTS dim_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    UNIQUE KEY uq_dim_location_coordinates (latitude, longitude)
);

CREATE TABLE IF NOT EXISTS dim_time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    reading_time VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS fact_weather (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    time_id INT NOT NULL,
    temperature FLOAT,
    windspeed FLOAT,
    UNIQUE KEY uq_fact_weather_location_time (location_id, time_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);
