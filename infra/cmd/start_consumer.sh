#!/usr/bin/env bash

# docker compose -p kafka_from_zero -f infra/docker/consumer.yaml up --build -d

N_CONSUMERS=${1:-1}

echo "Subindo $N_CONSUMERS consumer(s)..."
docker compose -p kafka_from_zero -f infra/docker/consumer.yaml up --build -d --scale kafka-consumer=$N_CONSUMERS
