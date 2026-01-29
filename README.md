# 🚀 DE Project 360 – End-to-End Spark Data Platform

## 📌 Overview

**DE Project 360** is a production-style **Data Engineering platform** built using **Apache Spark, Docker, and Jupyter**, following the **Medallion Architecture (Bronze–Silver–Gold)** pattern. The project demonstrates how raw data is ingested, cleaned, validated, enriched, aggregated, monitored, and analyzed with **ML-based anomaly detection** and **interactive dashboards**.

This repository is designed to mirror **real-world data engineering systems**, not just scripts.

---

## 🧱 Architecture

```
Raw CSV Data
     ↓
Bronze Layer  (Raw → Parquet)
     ↓
Silver Layer  (Clean + Validate + Quarantine)
     ↓
Gold Layer    (Business Aggregations)
     ↓
Semantic Layer (Business Metrics)
     ↓
Analytics / ML / Dashboards
```

---

## 🛠 Tech Stack

* **Apache Spark 3.5** (PySpark)
* **Docker & Docker Compose**
* **JupyterLab** (Spark UI enabled)
* **Plotly** (Dashboards)
* **Spark MLlib** (Anomaly Detection)
* **Git & GitHub**

---

## 📂 Project Structure

```
DE PROJECT 360/
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── data/
│   └── raw/
│       └── client_sales_raw.csv
├── jobs/
│   ├── bronze/
│   │   └── bronze_layer.py
│   ├── silver/
│   │   └── silver_layer.py
│   ├── gold/
│   │   └── gold_layer.py
│   ├── observability/
│   │   └── observability.py
│   ├── semantic/
│   │   └── semantic_layer.py
│   └── ai/
│       └── anomaly_detection.py
├── notebooks/
│   ├── dashboards/
│   │   └── sales_kpis_plotly.ipynb
│   └── ml/
│       └── anomaly_detection.ipynb
└── README.md
```

---

## 🥉 Bronze Layer – Raw Ingestion

Reads raw CSV data and stores it as immutable Parquet files.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BronzeLayer").getOrCreate()

df = spark.read.option("header", True) \
    .csv("/opt/data/data/raw/client_sales_raw.csv")

df.write.mode("overwrite") \
    .parquet("/opt/data/bronze/sales_transactions")

spark.stop()
```

---

## 🥈 Silver Layer – Data Cleaning & Validation

* Casts data types
* Filters invalid records
* Quarantines bad data

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("SilverLayer").getOrCreate()

df = spark.read.parquet("/opt/data/bronze/sales_transactions")

clean_df = df \
    .withColumn("amount", col("amount").cast("double")) \
    .filter(col("amount") > 0)

clean_df.write.mode("overwrite") \
    .parquet("/opt/data/silver/sales_clean")

(df.subtract(clean_df)) \
    .write.mode("overwrite") \
    .parquet("/opt/data/silver/sales_quarantine")

spark.stop()
```

---

## 🥇 Gold Layer – Business Aggregations

Creates KPI-ready datasets.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark = SparkSession.builder.appName("GoldLayer").getOrCreate()

df = spark.read.parquet("/opt/data/silver/sales_clean")

gold_df = df.groupBy("status") \
    .agg(sum("amount").alias("total_sales"))

gold_df.write.mode("overwrite") \
    .parquet("/opt/data/gold/sales_summary")

spark.stop()
```

---

## 🧠 Semantic Layer

Provides business-friendly metrics.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SemanticLayer").getOrCreate()

df = spark.read.parquet("/opt/data/gold/sales_summary")

df.write.mode("overwrite") \
    .parquet("/opt/data/semantic/business_metrics")

spark.stop()
```

---

## 🔎 Observability Layer

Tracks pipeline health and row counts.

```python
from pyspark.sql import SparkSession
from datetime import datetime

spark = SparkSession.builder.appName("Observability").getOrCreate()

metrics = [(1000, True, datetime.now())]

df = spark.createDataFrame(metrics, ["row_count", "success", "timestamp"])

df.write.mode("append") \
    .parquet("/opt/data/observability/pipeline_metrics")

spark.stop()
```

---

## 🤖 AI / ML – Anomaly Detection

Uses Spark MLlib to detect unusual sales behavior.

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql.functions import col

assembler = VectorAssembler(inputCols=["amount"], outputCol="features")
data = assembler.transform(df)

kmeans = KMeans(k=2, seed=42)
model = kmeans.fit(data)

predictions = model.transform(data)
```

---

## 📊 Dashboards

Interactive dashboards built using **Plotly + Jupyter**:

* Total sales over time
* Clean vs quarantined records
* Customer-level sales

Notebook: `notebooks/dashboards/sales_kpis_plotly.ipynb`

---

## ▶️ How to Run

```bash
docker-compose up --build
```

Open:

* JupyterLab → [http://localhost:8888](http://localhost:8888)
* Spark UI → [http://localhost:4040](http://localhost:4040) (when a job runs)

---

## 🎯 What This Project Demonstrates

* Real-world Spark pipeline design
* Medallion Architecture
* Data quality & observability
* ML integration in data platforms
* Analytics-ready outputs

---
### 🧪 Data Quality – Clean vs Quarantined Records

![Clean vs Quarantined Records](Images/clean_vs_quarantined_raw.png)

This visualization shows the comparison between valid (clean) records and quarantined records that failed business or data quality rules.

### 🔎 Pipeline Data Quality & Observability

![Pipeline Data Quality](Images/Pipeline_data_quality.png)

Tracks row counts, pipeline success status, and overall data health across Bronze, Silver, and Gold layers.

### 🤖 ML-Based Sales Clustering

![Sales Clustering](Images/Sales_clustering.png)

KMeans clustering applied on sales amounts to identify anomalies and unusual transaction patterns.

### 👥 Total Sales by Customer

![Total Sales by Customer](Images/Total_sales_by_customers.png)

Highlights high-value customers and customer-level revenue contribution.

### 📈 Total Sales by Transaction Status

![Total Sales by Status](Images/Total_sales_by_status.png)

Summarizes business performance based on transaction status (e.g., completed, pending, failed).


## 👤 Author

**Muhammed Fathah**
Data Engineer | Apache Spark | Docker | Big Data

---

⭐ If you find this project useful, give it a star!
