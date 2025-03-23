import json
import pandas as pd

# Load the metrics data
with open('metrics.json') as f:
    data = json.load(f)

# Convert data to DataFrame
df = pd.DataFrame(data['data']['result'])
df['value'] = df['value'].apply(lambda x: float(x[1]))

# Normalize data
df['value'] = (df['value'] - df['value'].mean()) / df['value'].std()
df.to_csv("processed_data.csv", index=False)

print("Data preprocessed and saved!")
