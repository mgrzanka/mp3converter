#!/bin/bash
set -e

wait_for_db() {
    echo "Waiting for database to connect on ${DB_HOST}:${DB_PORT}"
    until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}"; do
        echo "Database is not running, waiting..."
        sleep 2
    done
    echo "Database is ready!"
}

wait_for_db

flask --app src.app db upgrade --directory migrations

exec python3 -m src.app
