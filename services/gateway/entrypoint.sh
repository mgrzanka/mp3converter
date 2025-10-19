#!/bin/bash
set -e

wait_for_mongo() {
    MONGO_HOST=${MONGO_HOST:-localhost}
    MONGO_PORT=${MONGO_PORT:-27017}

    echo "Waiting for mongodb to connect on $MONGO_HOST:$MONGO_PORT"
    until nc -z "$MONGO_HOST" "$MONGO_PORT"; do
      echo "Waiting for mongodb..."
      sleep 2
    done
    echo "Connected to mongodb."
}
wait_for_rabbitmq() {
    RABBIT_HOST=${RABBITMQ_HOST:-localhost}
    RABBIT_PORT=${RABBITMQ_PORT:-5672}

    echo "Waiting for RabbitMQ on ${RABBIT_HOST}:${RABBIT_PORT}..."

    until nc -z "$RABBIT_HOST" "$RABBIT_PORT"; do
      echo "Waiting for rabitmq..."
      sleep 2
    done

    echo "Connected to rabbitmq."
}


wait_for_mongo
wait_for_rabbitmq
exec python3 -m src.app
