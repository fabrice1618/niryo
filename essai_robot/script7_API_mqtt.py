#!/usr/bin/env python3

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import rospy
import time
import threading
import json
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

# -------------------------------------------------------------------
# INIT ROS + ROBOT
# -------------------------------------------------------------------

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()
n.calibrate_auto()

# -------------------------------------------------------------------
# SIGNALS
# -------------------------------------------------------------------

def signal_begin():
    n.led_ring.flashing([102, 255, 255, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('ready.wav', wait_end=True)

def signal_end():
    n.led_ring.flashing([51, 255, 51, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('stop.wav', wait_end=True)

# -------------------------------------------------------------------
# MQTT SETUP
# -------------------------------------------------------------------

BROKER_IP = "192.168.1.3"
BROKER_PORT = 1883
TOPIC = "robot3/events"
USERNAME = "nuc"
PASSWORD = "nuc"

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()

def publish_mqtt(event_type, data):
    payload = {
        "event": event_type,
        "timestamp": time.time(),
        "data": data
    }
    client.publish(TOPIC, json.dumps(payload))
    print("MQTT envoyé :", payload)

# -------------------------------------------------------------------
# FONCTION CLIGNOTEMENT
# -------------------------------------------------------------------

def blink_color(color_name):
    colors = {
        "red":   [255,   0,   0, 0],
        "green": [  0, 255,   0, 0],
        "blue":  [  0,   0, 255, 0],
    }

    if color_name not in colors:
        print("Couleur inconnue :", color_name)
        return False

    color = colors[color_name]

    # wait=True pour être sûr que l'action est terminée
    n.led_ring.flashing(color, period=0.2, iterations=10, wait=True)

    return True

# -------------------------------------------------------------------
# FLASK API
# -------------------------------------------------------------------

app = Flask(__name__)

@app.route('/color', methods=['POST'])
def api_color():

    data = request.json
    if not data or "color" not in data:
        return jsonify({"error": "Envoyer {\"color\": \"red|green|blue\"}"}), 400

    color = data["color"].lower()

    ok = blink_color(color)

    if not ok:
        publish_mqtt("color_error", {"color": color})
        return jsonify({"error": "Couleur inconnue"}), 400

    # ✅ Envoi MQTT une fois l’action terminée
    publish_mqtt("color_done", {
        "color": color,
        "status": "success"
    })

    return jsonify({"status": "ok", "color": color})

# -------------------------------------------------------------------
# THREAD FLASK
# -------------------------------------------------------------------

def run_flask():
    app.run(host="0.0.0.0", port=3000, debug=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# -------------------------------------------------------------------
# ROBOT READY
# -------------------------------------------------------------------

signal_begin()
n.request_new_calibration()
n.calibrate_auto()
signal_end()

# -------------------------------------------------------------------
# LOOP PRINCIPALE
# -------------------------------------------------------------------

try:
    while not rospy.is_shutdown():
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
