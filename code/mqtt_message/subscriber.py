#!/usr/bin/env python3
"""
MQTT Subscriber - Receives sensor data and stores in MySQL
Subscribes to MQTT topic and inserts validated measurements into database
"""

import os
import sys
import json
import signal
import logging
from datetime import datetime
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import pymysql

# Global variables for clean shutdown
mqtt_client = None
db_connection = None
running = True


def setup_logging():
    """Configure logging with custom format"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def validate_message(payload, logger):
    """
    Validate JSON structure and required keys
    Returns: dict with validated data or None if invalid
    """
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON invalide ignoré: {e}")
        return None

    # Check required keys
    required_keys = ['timestamp', 'temperature', 'humidite', 'pression']
    for key in required_keys:
        if key not in data:
            logger.warning(f"Clé manquante ignorée: {key}")
            return None

    # Validate timestamp format
    try:
        datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        logger.warning(f"Format timestamp invalide: {data['timestamp']}")
        return None

    # Validate numeric types
    try:
        data['temperature'] = float(data['temperature'])
        data['humidite'] = float(data['humidite'])
        data['pression'] = float(data['pression'])
    except (ValueError, TypeError):
        logger.warning("Valeurs numériques invalides")
        return None

    return data


def validate_ranges(data, logger):
    """
    Validate measurement ranges
    Returns: dict with valid measurements only (may be partial)
    """
    valid_data = {'timestamp': data['timestamp']}

    # Temperature: -50.0 to 100.0°C
    if -50.0 <= data['temperature'] <= 100.0:
        valid_data['temperature'] = data['temperature']
    else:
        logger.warning(f"Valeur hors plage ignorée: temperature={data['temperature']}")

    # Humidity: 0.0 to 100.0%
    if 0.0 <= data['humidite'] <= 100.0:
        valid_data['humidite'] = data['humidite']
    else:
        logger.warning(f"Valeur hors plage ignorée: humidite={data['humidite']}")

    # Pressure: 900.0 to 1100.0 hPa
    if 900.0 <= data['pression'] <= 1100.0:
        valid_data['pression'] = data['pression']
    else:
        logger.warning(f"Valeur hors plage ignorée: pression={data['pression']}")

    return valid_data


def insert_measurements(cursor, data, logger):
    """
    Insert measurements into database (3 rows per message)
    Returns: number of inserted measurements
    """
    timestamp = data['timestamp']
    inserted_count = 0

    measurements = [
        ('temperature', data.get('temperature')),
        ('humidite', data.get('humidite')),
        ('pression', data.get('pression'))
    ]

    for key, value in measurements:
        if value is not None:
            try:
                cursor.execute(
                    "INSERT INTO mesures (timestamp, cle, valeur) VALUES (%s, %s, %s)",
                    (timestamp, key, value)
                )
                inserted_count += 1
            except pymysql.Error as e:
                logger.error(f"Erreur insertion SQL pour {key}: {e}")

    return inserted_count


def on_connect(client, userdata, flags, rc):
    """MQTT connection callback"""
    logger = userdata['logger']
    config = userdata['config']

    if rc == 0:
        logger.info(f"Connexion MQTT établie sur {config['MQTT_BROKER']}:{config['MQTT_PORT']}")
        client.subscribe(config['MQTT_TOPIC'])
        logger.info(f"Souscription au topic: {config['MQTT_TOPIC']}")
    else:
        logger.error(f"Erreur de connexion MQTT: code {rc}")
        sys.exit(1)


def on_message(client, userdata, msg):
    """MQTT message callback"""
    logger = userdata['logger']
    db_conn = userdata['db_connection']

    # Validate message structure
    data = validate_message(msg.payload.decode(), logger)
    if data is None:
        return

    # Validate value ranges
    valid_data = validate_ranges(data, logger)

    # Insert valid measurements
    if len(valid_data) > 1:  # More than just timestamp
        try:
            cursor = db_conn.cursor()
            inserted = insert_measurements(cursor, valid_data, logger)
            db_conn.commit()
            cursor.close()

            if inserted > 0:
                logger.info(f"Message reçu et traité: {inserted} mesures insérées")
        except pymysql.Error as e:
            logger.error(f"Erreur lors de l'insertion: {e}")
            db_conn.rollback()


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    global running
    running = False


def main():
    global mqtt_client, db_connection

    # Setup logging
    logger = setup_logging()

    # Load environment variables
    load_dotenv()

    config = {
        'MQTT_BROKER': os.getenv('MQTT_BROKER'),
        'MQTT_PORT': int(os.getenv('MQTT_PORT', 1883)),
        'MQTT_USER': os.getenv('MQTT_USER'),
        'MQTT_PASSWORD': os.getenv('MQTT_PASSWORD'),
        'MQTT_TOPIC': os.getenv('MQTT_TOPIC'),
        'MYSQL_HOST': os.getenv('MYSQL_HOST'),
        'MYSQL_PORT': int(os.getenv('MYSQL_PORT', 3306)),
        'MYSQL_USER': os.getenv('MYSQL_USER'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'MYSQL_DATABASE': os.getenv('MYSQL_DATABASE')
    }

    # Validate configuration
    for key, value in config.items():
        if value is None:
            logger.error(f"Configuration manquante: {key}")
            sys.exit(1)

    # Setup signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Connect to MySQL
        db_connection = pymysql.connect(
            host=config['MYSQL_HOST'],
            port=config['MYSQL_PORT'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE'],
            autocommit=False
        )
        logger.info(f"Connexion MySQL établie sur {config['MYSQL_DATABASE']}")

    except pymysql.Error as e:
        logger.error(f"Erreur de connexion MySQL: {e}")
        sys.exit(1)

    try:
        # Setup MQTT client
        mqtt_client = mqtt.Client(userdata={
            'logger': logger,
            'db_connection': db_connection,
            'config': config
        })

        mqtt_client.username_pw_set(config['MQTT_USER'], config['MQTT_PASSWORD'])
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        # Connect to MQTT broker
        mqtt_client.connect(config['MQTT_BROKER'], config['MQTT_PORT'], 60)

        # Start MQTT loop
        mqtt_client.loop_start()

        # Keep running until signal received
        logger.info("En attente de messages MQTT (Ctrl+C pour arrêter)...")
        while running:
            signal.pause()

    except Exception as e:
        logger.error(f"Erreur de connexion MQTT: {e}")
        sys.exit(1)

    finally:
        # Clean shutdown
        logger.info("Arrêt en cours...")

        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
            logger.info("Connexion MQTT fermée")

        if db_connection:
            db_connection.close()
            logger.info("Connexion MySQL fermée")

        logger.info("Arrêt terminé")
        sys.exit(0)


if __name__ == "__main__":
    main()
