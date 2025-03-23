FROM python:3.10-slim

WORKDIR /app
COPY anomaly_model.pkl /app/
COPY detect_anomalies.py /app/
COPY requirements.txt /app/
COPY metrics.json /app/

RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "-u", "/app/detect_anomalies.py"]
