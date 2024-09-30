#!/bin/bash

# Waiting for Kafka
sleep 10

poetry run python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000