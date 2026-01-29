from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("AI_Semantic_Layer") \
    .enableHiveSupport() \
    .getOrCreate()

# Load semantic layer
spark.sql("USE analytics")
semantic_df = spark.table("business_metrics")
semantic_df.createOrReplaceTempView("semantic_metrics")

def ai_query_router(question: str):
    q = question.lower()

    if "total revenue" in q:
        return """
            SELECT SUM(total_revenue) AS total_revenue
            FROM semantic_metrics
        """

    if "top" in q and "products" in q:
        return """
            SELECT product_id, total_revenue
            FROM semantic_metrics
            ORDER BY total_revenue DESC
            LIMIT 5
        """

    if "average order value" in q:
        return """
            SELECT AVG(avg_order_value) AS avg_order_value
            FROM semantic_metrics
        """

    return None


def ask_ai(question: str):
    sql_query = ai_query_router(question)

    if not sql_query:
        return "❌ Sorry, I don't understand this business question yet."

    result = spark.sql(sql_query)
    result.show()
    return "✅ Query executed successfully"


# Demo questions
if __name__ == "__main__":
    ask_ai("What is total revenue?")
