
import os
import sys
import json
import csv

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when

from config.aws_config import s3_client, S3_BUCKET_NAME

# Create directories
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("data/output", exist_ok=True)

# Step 1: Download events from S3
local_file = "data/raw/events.jsonl"

s3_client.download_file(
    S3_BUCKET_NAME,
    "input/events.jsonl",
    local_file
)

print("Events downloaded successfully from S3!")

# Step 2: Create Spark Session
spark = SparkSession.builder \
    .appName("EventProcessingPipeline") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

try:
    print("Spark Version:", spark.version)

    # Step 3: Read JSON events
    df = spark.read.json(local_file)

    print("Original Events:")
    df.show(5, truncate=False)

    # Step 4: Categorize events
    processed_df = df.withColumn(
        "event_category",
        when(
            upper(trim(col("event_type"))) == "PURCHASE",
            "Revenue"
        ).otherwise("Non-Revenue")
    )

    print("Processed Events:")
    processed_df.show(5, truncate=False)

    # Step 5: Calculate total events
    processed_df.createOrReplaceTempView("events")

    print("Total Events:")
    spark.sql("""
        SELECT COUNT(*) AS total_events
        FROM events
    """).show()

    # Step 6: Calculate total revenue
    print("Total Revenue:")
    spark.sql("""
        SELECT SUM(amount) AS total_revenue
        FROM events
        WHERE event_category = 'Revenue'
    """).show()

    # Step 7: Category analytics
    analytics_df = spark.sql("""
        SELECT
            event_category,
            COUNT(*) AS total_events,
            SUM(amount) AS total_amount
        FROM events
        GROUP BY event_category
    """)

    print("Event Category Analytics:")
    analytics_df.show()

    # Step 8: Save processed events using Python
    processed_rows = processed_df.collect()

    with open(
        "data/processed/events.jsonl",
        "w",
        encoding="utf-8"
    ) as file:
        for row in processed_rows:
            file.write(json.dumps(row.asDict()) + "\n")

    print("Processed events saved successfully!")

    # Step 9: Save analytics as CSV
    analytics_rows = analytics_df.collect()

    with open(
        "data/output/event_analytics.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "event_category",
                "total_events",
                "total_amount"
            ]
        )

        writer.writeheader()

        for row in analytics_rows:
            writer.writerow(row.asDict())

    print("Analytics saved successfully!")

finally:
    # Step 10: Stop Spark
    spark.stop()

print("Event processing completed successfully!")
