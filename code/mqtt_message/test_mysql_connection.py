#!/usr/bin/env python3
"""
Test MySQL Connection - Verify database connectivity and table structure
Run this on the NUC to verify MySQL configuration
"""

import os
import sys
from dotenv import load_dotenv
import pymysql


def test_mysql_connection():
    """Test MySQL database connection and table structure"""
    print("=" * 60)
    print("Test 2: MySQL Connection")
    print("=" * 60)

    # Load configuration
    load_dotenv()
    host = os.getenv('MYSQL_HOST')
    port = int(os.getenv('MYSQL_PORT', 3306))
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')

    if not all([host, port, user, password, database]):
        print("❌ FAILED: Configuration incomplete in .env file")
        return False

    print(f"Configuration:")
    print(f"  Host: {host}:{port}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    print()

    try:
        # Test connection
        print("Connecting to MySQL database...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("✓ Connection successful")

        # Test table existence
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'mesures'")
        result = cursor.fetchone()

        if not result:
            print("❌ FAILED: Table 'mesures' does not exist")
            connection.close()
            return False

        print("✓ Table 'mesures' exists")

        # Verify table structure
        cursor.execute("DESCRIBE mesures")
        columns = cursor.fetchall()

        expected_columns = {
            'mesure_id': 'int',
            'timestamp': 'datetime',
            'cle': 'varchar',
            'valeur': 'float'
        }

        print("\nTable structure:")
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            print(f"  {col_name}: {col_type}")

            if col_name in expected_columns:
                expected_type = expected_columns[col_name]
                if expected_type in col_type.lower():
                    print(f"    ✓ Type correct")
                else:
                    print(f"    ⚠ Expected type containing '{expected_type}'")

        # Test write permission
        print("\nTesting write permission...")
        try:
            cursor.execute(
                "INSERT INTO mesures (timestamp, cle, valeur) VALUES (%s, %s, %s)",
                ('2025-01-01 00:00:00', 'test', 0.0)
            )
            connection.commit()
            print("✓ Write permission OK")

            # Clean up test data
            cursor.execute(
                "DELETE FROM mesures WHERE timestamp = '2025-01-01 00:00:00' AND cle = 'test'"
            )
            connection.commit()
            print("✓ Test data cleaned up")

        except pymysql.Error as e:
            print(f"❌ Write permission failed: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False

        cursor.close()
        connection.close()

        print("\n✅ PASSED: MySQL connection test")
        return True

    except pymysql.Error as e:
        print(f"❌ FAILED: MySQL error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


if __name__ == "__main__":
    success = test_mysql_connection()
    sys.exit(0 if success else 1)
