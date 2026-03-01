#!/usr/bin/env bash
# Démarre le mock du robot Niryo (API Flask + MQTT)
set -e

cd "$(dirname "$0")"

source venv/bin/activate

exec python code/mock_robot/app.py
