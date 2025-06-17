#!/usr/bin/env bash

# docker compose -p kafka_from_zero -f infra/docker/producer.yaml up --build -d


N_PRODUCERS=${1:-1}

echo "Subindo $N_PRODUCERS producer(s)..."
docker compose -p kafka_from_zero -f infra/docker/producer.yaml up --build -d --scale kafka-producer=$N_PRODUCERS
