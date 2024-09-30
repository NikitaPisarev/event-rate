#!/bin/bash

# Waiting for Postgres and Kafka
sleep 10

poetry run python3 manage.py makemigrations
poetry run python3 manage.py migrate

poetry run python3 -m uvicorn config.asgi:application --host 0.0.0.0 --port 8001