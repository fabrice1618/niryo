#!/usr/bin/env python3
"""Outil de diagnostic MQTT — TP Niryo"""

import os
import sys
import signal
from pathlib import Path
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Charger .env racine
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Lire config
BROKER = os.getenv("MQTT_BROKER", "192.168.1.3")
PORT = int(os.getenv("MQTT_PORT", 1883))
USER = os.getenv("MQTT_USER", "nuc")
PASSWORD = os.getenv("MQTT_PASSWORD", "nuc")
DEFAULT_TOPIC = os.getenv("MQTT_TOPIC", "robot3/events")


def afficher_config():
    print("=" * 40)
    print("  Diagnostic MQTT — TP Niryo")
    print("=" * 40)
    print(f"  Broker   : {BROKER}")
    print(f"  Port     : {PORT}")
    print(f"  User     : {USER}")
    print(f"  Password : {PASSWORD}")
    print("=" * 40)


def publish(topic, message):
    client = mqtt.Client()
    client.username_pw_set(USER, PASSWORD)
    try:
        client.connect(BROKER, PORT)
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        sys.exit(1)
    result = client.publish(topic, message)
    result.wait_for_publish()
    client.disconnect()
    print(f"Message publié sur '{topic}' : {message}")


def subscribe(topic):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connecté au broker. Écoute sur '{topic}' (Ctrl+C pour arrêter)")
            client.subscribe(topic)
        else:
            print(f"Erreur de connexion, code retour : {rc}")
            sys.exit(1)

    def on_message(client, userdata, msg):
        print(f"[{msg.topic}] {msg.payload.decode()}")

    client = mqtt.Client()
    client.username_pw_set(USER, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    def handler(sig, frame):
        print("\nDéconnexion...")
        client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    try:
        client.connect(BROKER, PORT)
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        sys.exit(1)
    client.loop_forever()


def main():
    afficher_config()

    # Choix du mode
    print("\nMode :")
    print("  1. Subscribe (écouter)")
    print("  2. Publish (envoyer)")
    choix = input("Choix [1/2] : ").strip()

    if choix not in ("1", "2"):
        print("Choix invalide.")
        sys.exit(1)

    # Topic
    topic = input(f"Topic [{DEFAULT_TOPIC}] : ").strip()
    if not topic:
        topic = DEFAULT_TOPIC

    if choix == "2":
        message = input("Message : ").strip()
        if not message:
            print("Message vide, abandon.")
            sys.exit(1)
        publish(topic, message)
    else:
        subscribe(topic)


if __name__ == "__main__":
    main()
