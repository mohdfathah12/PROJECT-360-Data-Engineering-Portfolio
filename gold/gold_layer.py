from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark = SparkSession.builder.appName("GoldLayer").getOrCreate()

df = spark.read.parquet("/opt/data/silver/sales_clean")

gold_df = df.groupBy("status") \
            .agg(sum("amount").alias("total_sales"))

gold_df.write.mode("overwrite").parquet("/opt/data/gold/sales_summary")

print("Gold layer completed")

spark.stop()
