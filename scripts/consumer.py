from confluent_kafka import Consumer, KafkaError
import os
import logging
import socket

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s",
)

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
TOPIC_SUBSCRIBED = os.getenv("KAFKA_TOPIC")

client_id = socket.gethostname()  # cada container terá um hostname único

def main():
    config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": f"kafka_consumer_{client_id}",
        "client.id": client_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }

    consumer = Consumer(config)

    consumer.subscribe([TOPIC_SUBSCRIBED])
    logging.info(f"{client_id} subscribed to topic: {TOPIC_SUBSCRIBED}")

    try:
        while True:
            msg = consumer.poll(10)
            if msg is None:
                logging.warning("No message received within the timeout period.")
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(
                        f"End of partition reached for topic {msg.topic()} at offset {msg.offset()}"
                    )
                    continue
                else:
                    logging.error(f"Error occurred: {msg.error()}")
                    break
            else:
                logging.info(
                    "Consumed event from topic [{topic}] partition [{partition}] at offset [{offset}] >> key = {key:12}".format(
                        topic=msg.topic(),
                        partition=msg.partition(),
                        offset=msg.offset(),
                        key=msg.key().decode("utf-8") if msg.key() else "None",
                        # value=msg.value().decode("utf-8"),
                    )
                )
    # except KeyboardInterrupt:
    #     logging.info("Consumer interrupted.")
    finally:
        consumer.close()
        logging.info("Consumer closed.")


if __name__ == "__main__":
    main()
