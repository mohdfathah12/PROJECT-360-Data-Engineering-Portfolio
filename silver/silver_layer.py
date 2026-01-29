from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("SilverLayer").getOrCreate()

df = spark.read.parquet("/opt/data/bronze/sales_transactions")

clean_df = df.withColumn("amount", col("amount").cast("double")) \
             .filter(col("amount").isNotNull() & (col("amount") > 0))

clean_df.write.mode("overwrite").parquet("/opt/data/silver/sales_clean")

df.subtract(clean_df) \
  .write.mode("overwrite") \
  .parquet("/opt/data/silver/sales_quarantine")

print("Silver layer completed")

spark.stop()
