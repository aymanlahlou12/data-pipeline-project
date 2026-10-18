from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col

spark = SparkSession.builder \
    .appName("WeatherTransformation") \
    .getOrCreate()


df = spark.read.json("/opt/airflow/raw/*.json", multiLine=True)

cleaned_df = df.select(
    col("latitude"),
    col("longitude"),
    col("current_weather.temperature").alias("temperature"),
    col("current_weather.windspeed").alias("windspeed"),
    col("current_weather.time").alias("reading_time")
).dropDuplicates()

final_df = cleaned_df.withColumn("spark_processed_at", current_timestamp())

print("Here is the cleaned data ready for the Data Warehouse:")
final_df.show()

final_df.write.mode("overwrite").parquet("/opt/airflow/processed/weather_data")

print("Success! Data transformed by PySpark and saved to the 'processed' folder.")