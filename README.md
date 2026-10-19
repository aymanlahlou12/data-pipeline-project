# Automated Weather ETL Pipeline

## Project Overview
An end-to-end data engineering pipeline that automatically extracts daily weather data, processes it using Apache Spark, and loads it into a local data warehouse for Business Intelligence reporting.

## Architecture
1. **Extraction:** Python scripts pull raw JSON data from a Weather API.
2. **Orchestration:** Apache Airflow (running in Docker) schedules and monitors the daily workflow.
3. **Transformation:** PySpark cleans the data, drops duplicates, and saves it in optimized Parquet format.
4. **Loading:** Processed data is ingested into a local MySQL Star Schema using SQLAlchemy.
5. **Visualization:** Power BI connects directly to the MySQL database to visualize daily trends.

## Tech Stack
* **Languages:** Python, SQL
* **Infrastructure & Tools:** Docker, Apache Airflow, PySpark, MySQL, Power BI, Git

## How to Run Locally
1. Clone this repository.
2. Start the infrastructure using Docker:
   `docker compose up -d --build`
3. Access the Airflow UI at `http://localhost:8080` to trigger the `weather_automated_pipeline` DAG.
4. Connect Power BI to the local MySQL instance on port 3306.