#!/usr/bin/env python3

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy
import time
import threading
from flask import Flask, request, jsonify

# -------------------------------------------------------------------
# INIT ROS + ROBOT
# -------------------------------------------------------------------

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

def signal_begin():
    n.led_ring.flashing([102, 255, 255, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('ready.wav', wait_end=True)

def signal_end():
    n.led_ring.flashing([51, 255, 51, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('stop.wav', wait_end=True)

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
    n.led_ring.flashing(color, period=0.2, iterations=10, wait=False)
    return True

# -------------------------------------------------------------------
# FLASK API
# -------------------------------------------------------------------

app = Flask(__name__)

@app.route('/color', methods=['POST'])
def api_color():
    data = request.json
    if not data or "color" not in data:
        return jsonify({"error": "Vous devez envoyer {\"color\": \"red|green|blue\"}"}), 400

    color = data["color"].lower()
    ok = blink_color(color)

    if not ok:
        return jsonify({"error": "Couleur inconnue"}), 400

    return jsonify({"status": "ok", "color": color})

def run_flask():
    app.run(host="0.0.0.0", port=3000, debug=False)

# Lance Flask dans un thread
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

# Boucle principale ROS (le robot attend juste des requêtes HTTP)
try:
    while not rospy.is_shutdown():
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
