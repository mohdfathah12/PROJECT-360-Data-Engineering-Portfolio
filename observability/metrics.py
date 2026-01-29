from pyspark.sql import SparkSession
from datetime import datetime

spark = SparkSession.builder.appName("Observability").getOrCreate()

metrics = [(datetime.now(), "SUCCESS")]

df = spark.createDataFrame(metrics, ["run_time", "status"])

df.write.mode("append").parquet("/opt/data/observability/pipeline_metrics")

print("Metrics recorded")

spark.stop()
