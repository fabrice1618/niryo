#!/usr/bin/env python3
"""
Mock du robot Niryo — simule le script7_API_mqtt.py
API Flask + publication MQTT, sans robot physique
"""

import os
import time
import json
import logging
from flask import Flask, jsonify, request
from pathlib import Path
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# --- Logging ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- MQTT Setup ------------------------------------------------------

BROKER_IP = os.getenv('MQTT_BROKER', '192.168.1.3')
BROKER_PORT = int(os.getenv('MQTT_PORT', 1883))
TOPIC = os.getenv('MQTT_TOPIC', 'robot3/events')
MQTT_USER = os.getenv('MQTT_USER', 'nuc')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'nuc')

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.connect(BROKER_IP, BROKER_PORT, 60)
mqtt_client.loop_start()
logger.info(f"MQTT connecté à {BROKER_IP}:{BROKER_PORT} topic={TOPIC}")


def publish_mqtt(event_type, data):
    payload = {
        "event": event_type,
        "timestamp": time.time(),
        "data": data
    }
    mqtt_client.publish(TOPIC, json.dumps(payload))
    logger.info(f"MQTT envoyé: {payload}")

# --- Simulation robot ------------------------------------------------

VALID_COLORS = ["red", "green", "blue"]


def blink_color(color_name):
    """Simule le clignotement LED (~2 secondes)."""
    if color_name not in VALID_COLORS:
        logger.warning(f"Couleur inconnue: {color_name}")
        return False

    logger.info(f"Clignotement {color_name} (simulation 2s)...")
    time.sleep(2)
    return True

# --- Flask API -------------------------------------------------------

app = Flask(__name__)


@app.route('/color', methods=['POST'])
def api_color():
    data = request.json
    if not data or "color" not in data:
        return jsonify({"error": 'Envoyer {"color": "red|green|blue"}'}), 400

    color = data["color"].lower()

    ok = blink_color(color)

    if not ok:
        publish_mqtt("color_error", {"color": color})
        return jsonify({"error": "Couleur inconnue"}), 400

    publish_mqtt("color_done", {"color": color, "status": "success"})
    return jsonify({"status": "ok", "color": color})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint non trouvé"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"status": "error", "message": "Méthode HTTP non autorisée"}), 405


# --- Main ------------------------------------------------------------

if __name__ == '__main__':
    host = os.getenv('MOCK_API_HOST', '0.0.0.0')
    port = int(os.getenv('MOCK_API_PORT', 3000))

    logger.info(f"Mock robot démarré sur {host}:{port}")
    app.run(host=host, port=port, debug=False)
