import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when

# Step 1: Create Spark Session
spark = SparkSession.builder \
    .appName("EventAnalytics") \
    .master("local[*]") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

# Step 2: Create sample event data
data = [
    (101, "Purchase", 55000),
    (102, "Login", 0),
    (103, "Purchase", 2500),
    (104, "Signup", 0),
    (105, "Purchase", 12000)
]

columns = ["event_id", "event_type", "amount"]

# Step 3: Create DataFrame
df = spark.createDataFrame(data, columns)

# Step 4: Categorize events
processed_df = df.withColumn(
    "event_category",
    when(
        upper(trim(col("event_type"))) == "PURCHASE",
        "Revenue"
    ).otherwise("Non-Revenue")
)

# Step 5: Create SQL temporary view
processed_df.createOrReplaceTempView("events")

# Step 6: Calculate total events
print("Total Events:")

spark.sql("""
SELECT COUNT(*) AS total_events
FROM events
""").show()

# Step 7: Calculate total revenue
print("Total Revenue:")

spark.sql("""
SELECT SUM(amount) AS total_revenue
FROM events
WHERE event_category = 'Revenue'
""").show()

# Step 8: Event category analytics
print("Event Category Analytics:")

analytics_df = spark.sql("""
SELECT
    event_category,
    COUNT(*) AS total_events,
    SUM(amount) AS total_amount
FROM events
GROUP BY event_category
""")

analytics_df.show()

# Step 9: Save analytics to CSV
os.makedirs("data/output", exist_ok=True)

pandas_df = analytics_df.toPandas()

pandas_df.to_csv(
    "data/output/event_analytics.csv",
    index=False
)

print("Analytics CSV file saved successfully!")

# Step 10: Stop Spark
spark.stop()


