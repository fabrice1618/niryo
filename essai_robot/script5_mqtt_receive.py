#!/usr/bin/env python3

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy
import time
import paho.mqtt.client as mqtt

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

# Describe this function...
def signal_begin():
    n.led_ring.flashing([102, 255, 255, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('ready.wav', wait_end=True)

# Describe this function...
def signal_end():
    n.led_ring.flashing([51, 255, 51, 0], period=0.5, iterations=3, wait=False)
    n.sound.play('stop.wav', wait_end=True)


# --- ACTION EN FONCTION DU MESSAGE MQTT ------------------------

def blink_color(color_name):
    """Fait clignoter le ring 2 secondes dans la couleur demandée."""
    
    colors = {
        "red":   [255,   0,   0, 0],
        "green": [  0, 255,   0, 0],
        "blue":  [  0,   0, 255, 0],
    }

    if color_name not in colors:
        print("Couleur inconnue :", color_name)
        return

    color = colors[color_name]
    n.led_ring.flashing(color, period=0.2, iterations=10, wait=False)  
    # 10 clignotements × 0.2s ≈ 2 secondes


# --- MQTT CALLBACKS -------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("MQTT connecté avec code :", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Message reçu :", message)
    blink_color(message)


# --- MQTT SETUP ------------------------------------------------

BROKER_IP = "192.168.0.92"
BROKER_PORT = 1883
TOPIC = "hello"
USERNAME = "mqtt"
PASSWORD = "mqtt"

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()


# --- ROBOT READY ----------------------------------------------

signal_begin()
n.request_new_calibration()
n.calibrate_auto()
signal_end()

# --- BOUCLE PRINCIPALE (ne fait rien, juste attendre MQTT) ----

try:
    while not rospy.is_shutdown():
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
