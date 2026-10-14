from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col

spark = SparkSession.builder \
    .appName("WeatherTransformation") \
    .getOrCreate()

# 2. Read ALL raw JSON files from your data lake (the raw folder)
# multiLine=True is required because we formatted our JSON with indent=4
df = spark.read.json("raw/*.json", multiLine=True)

cleaned_df = df.select(
    col("latitude"),
    col("longitude"),
    col("current_weather.temperature").alias("temperature"),
    col("current_weather.windspeed").alias("windspeed"),
    col("current_weather.time").alias("reading_time")
).dropDuplicates()

# Add a timestamp column to track when Spark processed this batch
final_df = cleaned_df.withColumn("spark_processed_at", current_timestamp())

print("Here is the cleaned data ready for the Data Warehouse:")
final_df.show()

final_df.write.mode("overwrite").parquet("processed/weather_data")

print("Success! Data transformed by PySpark and saved to the 'processed' folder.")