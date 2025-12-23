#!/usr/bin/env python3
"""
MQTT Sender - Generates and sends test sensor data
Publishes 1440 messages (24 hours at 1 message/minute) with realistic variations
"""

import os
import sys
import json
import math
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import paho.mqtt.client as mqtt


def setup_logging():
    """Configure logging with custom format"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def generate_temperature(hour):
    """
    Generate realistic temperature with daily oscillation
    Range: 15°C (night) to 25°C (afternoon)
    Formula: 20 + 5 * sin(2π * hour/24) + random(-1, 1)
    """
    base = 20
    amplitude = 5
    oscillation = amplitude * math.sin(2 * math.pi * hour / 24)
    noise = random.uniform(-1, 1)
    return round(base + oscillation + noise, 1)


def generate_humidity(hour):
    """
    Generate realistic humidity with inverse correlation to temperature
    Range: 40% (hot) to 80% (cool)
    Formula: 60 - 20 * sin(2π * hour/24) + random(-3, 3)
    """
    base = 60
    amplitude = 20
    oscillation = amplitude * math.sin(2 * math.pi * hour / 24)
    noise = random.uniform(-3, 3)
    return round(base - oscillation + noise, 1)


def generate_pressure(hour):
    """
    Generate realistic atmospheric pressure with slow variation
    Range: 1010 to 1020 hPa
    Formula: 1015 + 5 * sin(2π * hour/48) + random(-0.5, 0.5)
    """
    base = 1015
    amplitude = 5
    oscillation = amplitude * math.sin(2 * math.pi * hour / 48)
    noise = random.uniform(-0.5, 0.5)
    return round(base + oscillation + noise, 1)


def generate_message(timestamp):
    """
    Generate a complete sensor message for a given timestamp
    Returns: JSON string
    """
    # Calculate hour for oscillation formulas
    hour = timestamp.hour + timestamp.minute / 60.0

    data = {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'temperature': generate_temperature(hour),
        'humidite': generate_humidity(hour),
        'pression': generate_pressure(hour)
    }

    return json.dumps(data)


def on_connect(client, userdata, flags, rc):
    """MQTT connection callback"""
    logger = userdata['logger']
    config = userdata['config']

    if rc == 0:
        logger.info(f"Connexion MQTT établie sur {config['MQTT_BROKER']}:{config['MQTT_PORT']}")
    else:
        logger.error(f"Erreur de connexion MQTT: code {rc}")
        sys.exit(1)


def on_publish(client, userdata, mid):
    """MQTT publish callback (optional, for debugging)"""
    pass


def main():
    # Setup logging
    logger = setup_logging()

    # Load environment variables
    load_dotenv()

    config = {
        'MQTT_BROKER': os.getenv('MQTT_BROKER'),
        'MQTT_PORT': int(os.getenv('MQTT_PORT', 1883)),
        'MQTT_USER': os.getenv('MQTT_USER'),
        'MQTT_PASSWORD': os.getenv('MQTT_PASSWORD'),
        'MQTT_TOPIC': os.getenv('MQTT_TOPIC')
    }

    # Validate configuration
    for key, value in config.items():
        if value is None:
            logger.error(f"Configuration manquante: {key}")
            sys.exit(1)

    try:
        # Setup MQTT client
        mqtt_client = mqtt.Client(userdata={
            'logger': logger,
            'config': config
        })

        mqtt_client.username_pw_set(config['MQTT_USER'], config['MQTT_PASSWORD'])
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish

        # Connect to MQTT broker
        mqtt_client.connect(config['MQTT_BROKER'], config['MQTT_PORT'], 60)
        mqtt_client.loop_start()

        # Wait for connection
        import time
        time.sleep(1)

        # Generate and send 1440 messages (24 hours, 1 per minute)
        total_messages = 1440
        logger.info(f"Génération de {total_messages} messages sur 24 heures")

        # Starting timestamp: current time - 24 hours
        start_time = datetime.now() - timedelta(hours=24)

        for i in range(total_messages):
            # Calculate timestamp for this message
            current_timestamp = start_time + timedelta(minutes=i)

            # Generate message
            message = generate_message(current_timestamp)

            # Publish to MQTT
            result = mqtt_client.publish(config['MQTT_TOPIC'], message)

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"Erreur de publication MQTT: {result.rc}")
                sys.exit(1)

            # Log progress every 100 messages
            if (i + 1) % 100 == 0 or i == 0:
                logger.info(f"Publication du message {i + 1}/{total_messages}")

        # Wait for all messages to be sent
        mqtt_client.loop_stop()

        logger.info("Tous les messages ont été publiés avec succès")
        logger.info("Fermeture de la connexion MQTT")
        mqtt_client.disconnect()

    except Exception as e:
        logger.error(f"Erreur lors de la publication: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
