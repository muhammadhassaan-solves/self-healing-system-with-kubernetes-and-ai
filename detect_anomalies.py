import time
import json
import joblib
import pandas as pd
from prometheus_client import Gauge, start_http_server

# The Pod name/namespace from the environment:
POD_NAME = os.environ.get("POD_NAME", "unknown-pod")
POD_NAMESPACE = os.environ.get("POD_NAMESPACE", "default")

# Create a gauge with labels
anomaly_gauge = Gauge(
    "anomaly_count",
    "Number of anomalies detected",
    ["pod", "namespace"]
)

# Load model
model = joblib.load("anomaly_model.pkl")

def detect_anomalies():
    # Load data from metrics.json
    with open("metrics.json") as f:
        data = json.load(f)

    # Convert data to DataFrame
    df = pd.DataFrame(data["data"]["result"])
    df["value"] = df["value"].apply(lambda x: float(x[1]))

    # Normalize data
    df["value"] = (df["value"] - df["value"].mean()) / df["value"].std()
