from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("SemanticLayer") \
    .getOrCreate()

# Read Gold data
gold_df = spark.read.parquet("/opt/data/gold/sales_summary")

# Semantic layer = business-friendly metrics
business_metrics = gold_df.select(
    col("customer_name").alias("customer"),
    col("total_transactions").alias("number_of_orders"),
    col("total_revenue").alias("lifetime_value")
)

# Write Semantic Layer
business_metrics.write.mode("overwrite").parquet(
    "/opt/data/semantic/business_metrics"
)

print("✅ Semantic Layer Created Successfully")
business_metrics.show(10)

spark.stop()
