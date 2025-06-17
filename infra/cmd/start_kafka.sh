#!/usr/bin/env bash
compose_file=$1

for file in $compose_file; do
    files="$files -f infra/docker/${file}.yaml"
done

docker compose -p kafka_from_zero $files up -d