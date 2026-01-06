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

# --- MQTT SETUP ---------------------------------------------------

BROKER_IP = "192.168.0.92"
BROKER_PORT = 1883
TOPIC = "hello"
USERNAME = "mqtt"
PASSWORD = "mqtt"

client = mqtt.Client()

# Authentification
client.username_pw_set(USERNAME, PASSWORD)

# Connexion
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()    # Permet de gérer le réseau MQTT en arrière-plan

# ---------------------------------------------------------------

signal_begin()
n.request_new_calibration()
n.calibrate_auto()
signal_end()

# --- ENVOI D’UN MESSAGE MQTT CHAQUE SECONDE --------------------

try:
    while not rospy.is_shutdown():
        client.publish(TOPIC, "hello world")
        time.sleep(1)

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
