# Apache Kafka Zero → Hero

Projeto hands-on para dominar Apache Kafka do zero, com foco em fundamentos, boas práticas e integração real com Python.
Este repositório segue um plano semanal progressivo, com desafios práticos e automação via Docker.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Setup Inicial](#setup-inicial)
- [Execução dos Serviços](#execução-dos-serviços)
- [Fluxos Principais](#fluxos-principais)

---

## Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.11+](https://www.python.org/)
- (Opcional) [Make](https://www.gnu.org/software/make/) para automação de comandos

---

## Estrutura do Projeto

```
├── infra/                # Infraestrutura Docker e scripts de automação
│   ├── cmd/              # Scripts shell para subir serviços/produtores/consumidores
│   └── docker/           # Arquivos docker-compose e Dockerfiles
├── scripts/              # Código Python dos produtores e consumidores Kafka
├── docs/                 # Documentação e plano de estudos
├── setup.sh              # Script principal de setup e orquestração
├── requirements.txt      # Dependências Python
└── .gitignore
```

---

## Setup Inicial

1. **Clone o repositório:**

   ```sh
   git clone <url-do-repo>
   cd kafka_from_zero
   ```

2. **Crie a rede Docker (caso não exista):**

   O script `setup.sh` já verifica/cria a rede automaticamente, mas se quiser criar manualmente:

   ```sh
   docker network create kafka-network
   ```

3. **Ajuste permissões dos scripts:**

   O próprio `setup.sh` faz isso, mas pode ser feito manualmente:

   ```sh
   chmod +x infra/cmd/*.sh
   ```

---

## Execução dos Serviços

O script [`setup.sh`](setup.sh) orquestra toda a infraestrutura e aplicações.
**Sintaxe:**

```sh
./setup.sh <modo> <serviços> [--producers=N] [--consumers=N]
```

- `<modo>`: `infra`, `dev`, `test` ou `all`
- `<serviços>`: Quais serviços subir (ex: `"base kafka"`)
- `--producers=N`: Quantidade de produtores (default: 1)
- `--consumers=N`: Quantidade de consumidores (default: 1)

### Exemplos

#### 1. Subir apenas a infraestrutura base (Kafka, Zookeeper, UI)

```sh
./setup.sh infra "base"
```

#### 2. Subir infraestrutura + produtores

```sh
./setup.sh dev "base kafka" --producers=2
```

#### 3. Subir infraestrutura + consumidores

```sh
./setup.sh test "base kafka" --consumers=3
```

#### 4. Subir tudo (infraestrutura, produtores e consumidores)

```sh
./setup.sh all "base kafka" --producers=2 --consumers=2
```

---

## Fluxos Principais

### 1. Produção de Mensagens

- O [`scripts/producer.py`](scripts/producer.py) gera mensagens aleatórias simulando compras.
- Configurações de broker e tópico são passadas via variáveis de ambiente (ver Dockerfiles e YAMLs).
- O producer tenta se conectar ao Kafka com retry/backoff e envia lotes de mensagens a cada 30s.

### 2. Consumo de Mensagens

- O [`scripts/consumer.py`](scripts/consumer.py) consome mensagens do tópico configurado.
- Cada container/instância tem um `client.id` único (hostname).
- O consumer faz commit manual dos offsets (`enable.auto.commit=False`).

### 3. Observação via UI

- Acesse [http://localhost:8080](http://localhost:8080) para visualizar tópicos, mensagens e offsets via Kafka UI.

---
