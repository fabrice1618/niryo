# !/usr/bin/env python

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

# Describe this function...
def signal_begin():
  n.led_ring.flashing([102,255,255,0], period=0.5, iterations=3, wait=False)
  n.sound.play('ready.wav', wait_end=True)

# Describe this function...
def signal_end():
  n.led_ring.flashing([51,255,51,0], period=0.5, iterations=3, wait=False)
  n.sound.play('stop.wav', wait_end=True)


signal_begin()
n.request_new_calibration()
n.calibrate_auto()
signal_end()
 
