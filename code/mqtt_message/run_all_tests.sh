#!/bin/bash
#
# Run all tests for MQTT message handler
# Execute this script on the NUC after configuration
#

echo "============================================================"
echo "MQTT Message Handler - Test Suite"
echo "============================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found"
    echo "   Please create .env file from .env.example"
    exit 1
fi

# Make test scripts executable
chmod +x test_*.py

# Track test results
PASSED=0
FAILED=0

# Test 1: MQTT Connection
echo ""
python3 test_mqtt_connection.py
if [ $? -eq 0 ]; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 2: MySQL Connection
echo ""
python3 test_mysql_connection.py
if [ $? -eq 0 ]; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 3: Validation (requires subscriber to be running)
echo ""
echo "============================================================"
echo "Test 3: Message Validation"
echo "============================================================"
echo ""
echo "⚠ WARNING: This test requires subscriber.py to be running"
echo "          in another terminal."
echo ""
read -p "Is subscriber.py running? (y/n): " answer
if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    python3 test_validation.py
    if [ $? -eq 0 ]; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
else
    echo "⊘ SKIPPED: Validation test"
fi

# Test 4: Integration (requires subscriber to be running)
echo ""
echo "============================================================"
echo "Test 4: Integration Test"
echo "============================================================"
echo ""
echo "⚠ WARNING: This test requires subscriber.py to be running"
echo "          in another terminal."
echo ""
read -p "Is subscriber.py running? (y/n): " answer
if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    python3 test_integration.py
    if [ $? -eq 0 ]; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
else
    echo "⊘ SKIPPED: Integration test"
fi

# Summary
echo ""
echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
