# Propriétaire : E1 — Image du conteneur « producer » (Python + client Kafka)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY prepare_data.py producer.py entrypoint.sh ./
RUN sed -i '1s/^\xEF\xBB\xBF//; s/\r$//' entrypoint.sh && chmod +x entrypoint.sh
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
