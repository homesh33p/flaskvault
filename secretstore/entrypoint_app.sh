#!/bin/bash

if [ -z "$HOST" ]; then
    echo "Error: HOST environment variable is not set."
    exit 1
fi

echo "Waiting for postgres..."

while ! nc -z $HOST 5432; do
    sleep 0.1
done
    echo "PostgreSQL started"

mkdir -p $LOG_PATH
flask db upgrade
flask db stamp head

echo "Starting flask"
flask run --host=0.0.0.0 --debug
echo "Flask started"