import os
import sys

# Configure Python worker
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EventProcessingPipeline") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

print("Spark Version:", spark.version)

data = [
    (101, "Purchase", 55000),
    (102, "Login", 0),
    (103, "Purchase", 2500)
]

columns = ["event_id", "event_type", "amount"]

df = spark.createDataFrame(data, columns)

df.show()

spark.stop()