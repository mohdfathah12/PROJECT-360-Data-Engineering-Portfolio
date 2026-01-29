import subprocess
from email_alerts import send_alert

jobs = [
    {"name": "Bronze Layer", "file": "bronze_laye.py"},
    {"name": "Silver Layer", "file": "silver_layer.py"},
    {"name": "Gold Layer", "file": "gold_layer.py"},
    {"name": "Semantic Layer", "file": "semantic_layer.py"},
    {"name": "AI Layer", "file": "ai_layer.py"}
]

for job in jobs:
    try:
        print(f"🚀 Running {job['name']} ...")
        subprocess.check_call(f"/opt/spark/bin/spark-submit {job['file']}", shell=True)
        print(f"✅ {job['name']} completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ {job['name']} failed with error: {e}")
        send_alert(
            f"{job['name']} Failure",
            f"{job['name']} failed during execution.\nError: {e}",
            ["client@example.com"]
        )
        break  # Stop pipeline if one stage fails
