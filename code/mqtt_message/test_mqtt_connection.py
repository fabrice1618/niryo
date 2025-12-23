#!/usr/bin/env python3
"""
Test MQTT Connection - Verify broker connectivity and authentication
Run this on the NUC to verify MQTT configuration
"""

import os
import sys
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt


def test_mqtt_connection():
    """Test MQTT broker connection with authentication"""
    print("=" * 60)
    print("Test 1: MQTT Connection")
    print("=" * 60)

    # Load configuration
    load_dotenv()
    broker = os.getenv('MQTT_BROKER')
    port = int(os.getenv('MQTT_PORT', 1883))
    user = os.getenv('MQTT_USER')
    password = os.getenv('MQTT_PASSWORD')
    topic = os.getenv('MQTT_TOPIC')

    if not all([broker, port, user, password, topic]):
        print("❌ FAILED: Configuration incomplete in .env file")
        return False

    print(f"Configuration:")
    print(f"  Broker: {broker}:{port}")
    print(f"  User: {user}")
    print(f"  Topic: {topic}")
    print()

    # Test connection
    connection_success = False
    subscription_success = False

    def on_connect(client, userdata, flags, rc):
        nonlocal connection_success, subscription_success
        if rc == 0:
            connection_success = True
            print("✓ Connection successful")
            client.subscribe(topic)
        else:
            print(f"❌ Connection failed with code: {rc}")

    def on_subscribe(client, userdata, mid, granted_qos):
        nonlocal subscription_success
        subscription_success = True
        print(f"✓ Subscription successful to topic: {topic}")

    try:
        client = mqtt.Client()
        client.username_pw_set(user, password)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe

        print("Connecting to MQTT broker...")
        client.connect(broker, port, 60)
        client.loop_start()

        # Wait for callbacks
        time.sleep(2)

        client.loop_stop()
        client.disconnect()

        if connection_success and subscription_success:
            print("\n✅ PASSED: MQTT connection test")
            return True
        else:
            print("\n❌ FAILED: MQTT connection test")
            return False

    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


if __name__ == "__main__":
    success = test_mqtt_connection()
    sys.exit(0 if success else 1)
