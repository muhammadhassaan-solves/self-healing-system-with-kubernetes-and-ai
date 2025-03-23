import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load preprocessed data
df = pd.read_csv('processed_data.csv')

# Train the Isolation Forest model
model = IsolationForest(contamination=0.01)
df['anomaly'] = model.fit_predict(df[['value']])

# Save the trained model
joblib.dump(model, "anomaly_model.pkl")

# Print detected anomalies
anomalies = df[df['anomaly'] == -1]
print(f"Number of anomalies detected: {len(anomalies)}")
