#!/usr/bin/env python3
"""
Test Integration - Full end-to-end test
Publishes test messages and verifies they are correctly inserted in the database
"""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import pymysql


def test_integration():
    """Test full integration: MQTT → Subscriber → MySQL"""
    print("=" * 60)
    print("Test 4: Integration Test")
    print("=" * 60)
    print("NOTE: subscriber.py must be running before executing this test")
    print()

    # Load configuration
    load_dotenv()

    mqtt_config = {
        'broker': os.getenv('MQTT_BROKER'),
        'port': int(os.getenv('MQTT_PORT', 1883)),
        'user': os.getenv('MQTT_USER'),
        'password': os.getenv('MQTT_PASSWORD'),
        'topic': os.getenv('MQTT_TOPIC')
    }

    mysql_config = {
        'host': os.getenv('MYSQL_HOST'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE')
    }

    # Validate configuration
    if not all(mqtt_config.values()) or not all(mysql_config.values()):
        print("❌ FAILED: Configuration incomplete in .env file")
        return False

    # Generate unique test timestamp
    test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    test_message = {
        "timestamp": test_timestamp,
        "temperature": 22.5,
        "humidite": 60.0,
        "pression": 1015.0
    }

    print(f"Test timestamp: {test_timestamp}")
    print(f"Test message: {json.dumps(test_message, indent=2)}")
    print()

    try:
        # Step 1: Publish test message to MQTT
        print("Step 1: Publishing test message to MQTT...")
        client = mqtt.Client()
        client.username_pw_set(mqtt_config['user'], mqtt_config['password'])
        client.connect(mqtt_config['broker'], mqtt_config['port'], 60)
        client.loop_start()

        result = client.publish(mqtt_config['topic'], json.dumps(test_message))

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"❌ FAILED: MQTT publish error: {result.rc}")
            return False

        print("✓ Message published to MQTT")
        client.loop_stop()
        client.disconnect()

        # Wait for subscriber to process
        print("\nWaiting 3 seconds for subscriber to process...")
        time.sleep(3)

        # Step 2: Verify data in MySQL
        print("\nStep 2: Verifying data in MySQL...")
        connection = pymysql.connect(
            host=mysql_config['host'],
            port=mysql_config['port'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database']
        )

        cursor = connection.cursor()

        # Query for the test measurements
        cursor.execute(
            "SELECT cle, valeur FROM mesures WHERE timestamp = %s ORDER BY cle",
            (test_timestamp,)
        )

        results = cursor.fetchall()

        if len(results) != 3:
            print(f"❌ FAILED: Expected 3 measurements, found {len(results)}")
            cursor.close()
            connection.close()
            return False

        print(f"✓ Found {len(results)} measurements in database")

        # Verify each measurement
        expected = {
            'humidite': 60.0,
            'pression': 1015.0,
            'temperature': 22.5
        }

        all_correct = True
        for cle, valeur in results:
            expected_value = expected.get(cle)
            if expected_value is None:
                print(f"  ❌ Unexpected key: {cle}")
                all_correct = False
            elif abs(valeur - expected_value) < 0.01:
                print(f"  ✓ {cle}: {valeur} (correct)")
            else:
                print(f"  ❌ {cle}: {valeur} (expected {expected_value})")
                all_correct = False

        # Clean up test data
        cursor.execute(
            "DELETE FROM mesures WHERE timestamp = %s",
            (test_timestamp,)
        )
        connection.commit()
        print("\n✓ Test data cleaned up")

        cursor.close()
        connection.close()

        if all_correct:
            print("\n✅ PASSED: Integration test")
            return True
        else:
            print("\n❌ FAILED: Integration test (data mismatch)")
            return False

    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
