from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BronzeLayer").getOrCreate()

df = spark.read.option("header", True).csv("/opt/data/data/raw/client_sales_raw.csv")

df.write.mode("overwrite").parquet("/opt/data/bronze/sales_transactions")

print("Bronze layer completed")

spark.stop()
