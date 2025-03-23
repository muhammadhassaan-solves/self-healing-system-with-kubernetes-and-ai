import json
import numpy as np
import pandas as pd
import joblib
from prometheus_client import Gauge, start_http_server
import time

# Load the pre-trained anomaly detection model
MODEL_PATH = "anomaly_model.pkl"
model = joblib.load(MODEL_PATH)

# Define Prometheus metric
anomaly_gauge = Gauge("anomaly_count", "Number of anomalies detected")

# Function to detect anomalies
def detect_anomalies():
    # Load data from the static JSON file
    with open("metrics.json") as f:
        data = json.load(f)

    # Convert data to DataFrame
    df = pd.DataFrame(data["data"]["result"])
    df["value"] = df["value"].apply(lambda x: float(x[1]))

    # Normalize data
    df["value"] = (df["value"] - df["value"].mean()) / df["value"].std()

    # Make predictions
    df["anomaly"] = model.predict(df[["value"]])

    # Count anomalies
    anomaly_count = (df["anomaly"] == -1).sum()
    anomaly_gauge.set(anomaly_count)  # Update Prometheus metric

    # Print results
    print(f"Anomalies detected: {anomaly_count}")
    print(df[df["anomaly"] == -1])

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000, addr="0.0.0.0")

    while True:
        detect_anomalies()
        time.sleep(30)  # Run detection every 30 seconds
