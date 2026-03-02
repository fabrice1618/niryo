#!/usr/bin/env bash
# Démarre le handler MQTT → MySQL (event_handler)
set -e

cd "$(dirname "$0")"

source venv/bin/activate

exec python code/mqtt_message/event_handler.py
