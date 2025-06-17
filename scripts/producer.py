import json
import logging
import os
import time
from random import choice, random, randint

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient
from confluent_kafka.error import KafkaError, KafkaException

# Config
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
TOPIC = os.getenv("KAFKA_TOPIC")

# Retry/backoff
WAITING_TIME = 10
MAX_ATTEMPTS = 5
INITIAL_DELAY = 3

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s",
)


def connect_with_retry():
    delay = INITIAL_DELAY
    for attempt in range(1, MAX_ATTEMPTS + 1):
        logging.info(
            f"Tentativa {attempt}/{MAX_ATTEMPTS} de conexao ao broker Kafka em {KAFKA_BROKER}..."
        )
        try:
            admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
            metadata = admin_client.list_topics(timeout=10)
            topics = metadata.topics
            logging.info(f"Broker Kafka está acessível, lista de tópicos: {topics}...")
        except:
            logging.info(
                f"Aguardando {WAITING_TIME} segundos para nova tentativa de conexão..."
            )
            time.sleep(WAITING_TIME)

        try:

            config = {
                "bootstrap.servers": KAFKA_BROKER,
                "client.id": "kafka_producer",
                "acks": 1,
                "retries": 2,
                "linger.ms": 5,
                "compression.type": "lz4",
            }

            producer = Producer(**config)
            logging.info("Conexão com o Kafka estabelecida com sucesso.")
            return producer
        except KafkaException as e:
            error: KafkaError = e.args[0]
            logging.error(f"KafkaException: {error}")
            logging.warning(
                f"Broker indisponível. Aguardando {int(delay)} segundos antes de tentar novamente..."
            )
            time.sleep(delay)
            delay *= 1.2

    logging.error("Não foi possível conectar ao Kafka após múltiplas tentativas.")
    exit(1)


def main():
    producer = connect_with_retry()

    user_ids = ["eabara", "jsmith", "sgarcia", "jbernard", "htanaka", "awalther"]
    products = ["book", "alarm clock", "t-shirts", "gift card", "batteries"]

    count = 0
    qty = randint(1, 15)

    logging.info(f"Produzindo {qty} mensagens para o tópico '{TOPIC}'...")

    for _ in range(qty):
        user_id = choice(user_ids)
        product = choice(products)

        message = {
            "user_id": user_id,
            "product": product,
            "price": round(randint(10,50)*random(),2),
            "quantity": randint(1,3),
            "timestamp": int(time.time()),
        }

        logging.info(f"Enfileirando mensagens {_} no buffer")

        producer.produce(TOPIC, key=user_id, value=json.dumps(message).encode("utf-8"))
        count += 1


    try:
        # producer.produce(TOPIC, key=user_id, value=json.dumps(message).encode("utf-8"))
        logging.info(f"Processando buffer e enviando mensagem para o tópico '{TOPIC}'...")

        producer.poll(10000)
        producer.flush()

        logging.info("Mensagem enviada com sucesso.")
    except Exception as e:
        logging.error("Falha ao enviar mensagem para o Kafka:")
        logging.error(str(e))


if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)
