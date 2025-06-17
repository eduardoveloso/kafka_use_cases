#!/usr/bin/env bash

MODE=$1
SERVICES=$2
PRODUCERS=1
CONSUMERS=1

shift 2
while [[ $# -gt 0 ]]; do
  case "$1" in
    --producers=*)
      PRODUCERS="${1#*=}"
      shift
      ;;
    --consumers=*)
      CONSUMERS="${1#*=}"
      shift
      ;;
    *)
      echo "Parâmetro desconhecido: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$MODE" ]]; then
  echo "Modo não especificado. Use: infra, dev, test ou all"
  exit 1
fi

if [[ -z "$SERVICES" ]]; then
  echo "Serviços não especificados. Ex: \"base kafka\""
  exit 1
fi

echo "Ajustando permissões de execução para cmd..."
chmod +x infra/cmd/*.sh
echo "Permissões aplicadas."

check_network() {
  echo -e "\nVerificando rede 'kafka-network'..."
  if ! docker network ls | grep -q kafka-network; then
    echo "Rede não encontrada. Criando..."
    docker network create kafka-network
    echo "Rede 'kafka-network' criada com sucesso."
  else
    echo "Rede 'kafka-network' já existe."
  fi
}

start_infra() {
  echo -e "\nIniciando infraestrutura: $SERVICES"
  ./infra/cmd/start_kafka.sh "$SERVICES"
}

start_producers() {
  echo -e "\nIniciando $PRODUCERS produtor(es)..."
  check_network
  ./infra/cmd/start_producer.sh "$PRODUCERS"
}

start_consumers() {
  echo -e "\nIniciando $CONSUMERS consumidor(es)..."
  check_network
  ./infra/cmd/start_consumer.sh "$CONSUMERS"
}

case $MODE in
  infra)
    echo -e "\nModo: INFRA"
    check_network
    start_infra
    ;;
  dev)
    echo -e "\nModo: DEV"
    check_network
    start_infra
    start_producers
    ;;
  test)
    echo -e "\nModo: TEST"
    check_network
    start_infra
    start_consumers
    ;;
  all)
    echo -e "\nModo: ALL"
    check_network
    start_infra
    start_producers
    start_consumers
    ;;
  *)
    echo "Modo inválido. Use: infra, dev, test ou all"
    exit 1
    ;;
esac

echo -e "\n✅ Setup concluído com sucesso para o modo '$MODE'"
