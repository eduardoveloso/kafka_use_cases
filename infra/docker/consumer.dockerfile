FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/consumer.py .

# ENV KAFKA_BOOTSTRAP_SERVER=kafka:9092
# ENV KAFKA_TOPIC=example_topic
# ENV MESSAGE_INTERVAL=1

CMD ["python", "consumer.py"]