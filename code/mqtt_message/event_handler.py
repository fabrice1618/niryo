#!/usr/bin/env python3
"""
Handler MQTT → MySQL pour les événements robot
Souscrit au topic robot3/events et insère les événements dans la table events
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

running = True


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger = userdata['logger']
    topic = userdata['config']['MQTT_TOPIC']

    if rc == 0:
        logger.info(f"Connecté au broker MQTT")
        client.subscribe(topic)
        logger.info(f"Souscription au topic: {topic}")
    else:
        logger.error(f"Erreur connexion MQTT: code {rc}")
        sys.exit(1)


def on_message(client, userdata, msg):
    logger = userdata['logger']
    db_conn = userdata['db_connection']

    raw = msg.payload.decode()
    logger.info(f"Message reçu: {raw}")

    # Décodage JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON invalide: {e}")
        return

    # Extraction des champs
    event_type = data.get("event")
    ts_epoch = data.get("timestamp")
    event_data = data.get("data", {})

    if not event_type or ts_epoch is None:
        logger.warning("Champs 'event' ou 'timestamp' manquants")
        return

    # Conversion timestamp epoch → datetime
    try:
        ts = datetime.fromtimestamp(float(ts_epoch))
    except (ValueError, TypeError, OSError):
        logger.warning(f"Timestamp invalide: {ts_epoch}")
        return

    color = event_data.get("color")
    status = event_data.get("status")

    # Insertion en base
    try:
        cursor = db_conn.cursor()
        cursor.execute(
            "INSERT INTO events (timestamp, event_type, color, status, raw_json) "
            "VALUES (%s, %s, %s, %s, %s)",
            (ts, event_type, color, status, raw)
        )
        db_conn.commit()
        cursor.close()
        logger.info(f"Événement inséré: {event_type} color={color} status={status}")
    except pymysql.Error as e:
        logger.error(f"Erreur insertion SQL: {e}")
        db_conn.rollback()


def signal_handler(signum, frame):
    global running
    running = False


def main():
    logger = setup_logging()
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

    for key, value in config.items():
        if value is None:
            logger.error(f"Configuration manquante: {key}")
            sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        db_connection = pymysql.connect(
            host=config['MYSQL_HOST'],
            port=config['MYSQL_PORT'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE'],
            autocommit=False
        )
        logger.info(f"Connexion MySQL établie ({config['MYSQL_DATABASE']})")
    except pymysql.Error as e:
        logger.error(f"Erreur connexion MySQL: {e}")
        sys.exit(1)

    try:
        mqtt_client = mqtt.Client(userdata={
            'logger': logger,
            'db_connection': db_connection,
            'config': config
        })
        mqtt_client.username_pw_set(config['MQTT_USER'], config['MQTT_PASSWORD'])
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect(config['MQTT_BROKER'], config['MQTT_PORT'], 60)
        mqtt_client.loop_start()

        logger.info("En attente d'événements MQTT (Ctrl+C pour arrêter)...")
        while running:
            signal.pause()

    except Exception as e:
        logger.error(f"Erreur: {e}")
        sys.exit(1)

    finally:
        logger.info("Arrêt en cours...")
        if 'mqtt_client' in locals():
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        if db_connection:
            db_connection.close()
        logger.info("Arrêt terminé")


if __name__ == "__main__":
    main()
