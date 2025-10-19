#!/bin/bash
set -e

wait_for_mongodb() {
    MONGO_HOST=${MONGO_HOST:-localhost}
    MONGO_PORT=${MONGO_PORT:-27017}

    echo "Waiting for MongoDB to connect on $MONGO_HOST:$MONGO_PORT..."

    until nc -z "$MONGO_HOST" "$MONGO_PORT"; do
        echo "Waiting for MongoDB..."
        sleep 1
    done

    echo "Connected to MongoDB"
}

wait_for_rabbitmq() {
    RABBITMQ_HOST=${RABBITMQ_HOST:-localhost}
    RABBIT_PORT=${RABBIT_PORT:-5672}

    echo "Waiting for RabbitMQ on $RABBITMQ_HOST:$RABBIT_PORT..."

    until nc -z "$RABBITMQ_HOST" "$RABBIT_PORT"; do
        echo "Waiting for RabbitMQ..."
        sleep 1
    done

    echo "Connected to RabbitMQ"
}

wait_for_mongodb
wait_for_rabbitmq

python3 -m src.app
