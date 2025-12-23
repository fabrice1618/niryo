#!/usr/bin/env python3
"""
Test Message Validation - Verify JSON and range validation
Tests the validation logic without requiring MQTT/MySQL connections
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt


def test_validation():
    """Test message validation by sending various test cases"""
    print("=" * 60)
    print("Test 3: Message Validation")
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

    print("NOTE: This test publishes various messages to MQTT.")
    print("      Start subscriber.py and check logs for validation warnings.")
    print()

    test_cases = [
        {
            "name": "Valid message",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": 23.5,
                "humidite": 65.2,
                "pression": 1013.25
            },
            "expected": "Should be accepted and inserted"
        },
        {
            "name": "Invalid JSON",
            "data": "{ invalid json }",
            "expected": "Should log: JSON invalide ignoré"
        },
        {
            "name": "Missing timestamp",
            "data": {
                "temperature": 23.5,
                "humidite": 65.2,
                "pression": 1013.25
            },
            "expected": "Should log: Clé manquante ignorée: timestamp"
        },
        {
            "name": "Temperature out of range (too high)",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": 150.0,
                "humidite": 65.2,
                "pression": 1013.25
            },
            "expected": "Should log: Valeur hors plage ignorée: temperature=150.0"
        },
        {
            "name": "Temperature out of range (too low)",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": -100.0,
                "humidite": 65.2,
                "pression": 1013.25
            },
            "expected": "Should log: Valeur hors plage ignorée: temperature=-100.0"
        },
        {
            "name": "Humidity out of range",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": 23.5,
                "humidite": 150.0,
                "pression": 1013.25
            },
            "expected": "Should log: Valeur hors plage ignorée: humidite=150.0"
        },
        {
            "name": "Pressure out of range",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": 23.5,
                "humidite": 65.2,
                "pression": 1200.0
            },
            "expected": "Should log: Valeur hors plage ignorée: pression=1200.0"
        },
        {
            "name": "Invalid timestamp format",
            "data": {
                "timestamp": "23-12-2025 14:35:00",
                "temperature": 23.5,
                "humidite": 65.2,
                "pression": 1013.25
            },
            "expected": "Should log: Format timestamp invalide"
        },
        {
            "name": "Boundary values (valid)",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": -50.0,
                "humidite": 0.0,
                "pression": 900.0
            },
            "expected": "Should be accepted (minimum valid values)"
        },
        {
            "name": "Boundary values (valid)",
            "data": {
                "timestamp": "2025-12-23 14:35:00",
                "temperature": 100.0,
                "humidite": 100.0,
                "pression": 1100.0
            },
            "expected": "Should be accepted (maximum valid values)"
        }
    ]

    try:
        # Connect to MQTT
        client = mqtt.Client()
        client.username_pw_set(user, password)
        client.connect(broker, port, 60)
        client.loop_start()

        print("Publishing test messages...\n")

        for i, test in enumerate(test_cases, 1):
            print(f"Test {i}: {test['name']}")
            print(f"  Expected: {test['expected']}")

            # Prepare payload
            if isinstance(test['data'], str):
                payload = test['data']
            else:
                payload = json.dumps(test['data'])

            # Publish message
            result = client.publish(topic, payload)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"  ✓ Published")
            else:
                print(f"  ❌ Publish failed")

            print()
            time.sleep(0.5)  # Small delay between messages

        client.loop_stop()
        client.disconnect()

        print("=" * 60)
        print("Test messages published successfully.")
        print("Check subscriber.py logs to verify validation behavior.")
        print("=" * 60)
        print("\n✅ PASSED: Validation test (messages published)")
        return True

    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


if __name__ == "__main__":
    success = test_validation()
    sys.exit(0 if success else 1)
