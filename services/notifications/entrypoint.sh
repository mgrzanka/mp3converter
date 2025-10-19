#!/bin/bash
set -e

wait_for_rabbitmq() {
    local host="${RABBITMQ_HOST:-rabbitmq}"
    local port="${RABBITMQ_PORT:-5672}"

    echo "Waiting to connect with RabbitMQ on $host:$port..."

    until nc -z "$host" "$port"; do
        echo "Waiting for rabbitmq..."
        sleep 1
    done

    echo "Connected with RabbitMQ."
}

wait_for_rabbitmq

python3 -m src.app
