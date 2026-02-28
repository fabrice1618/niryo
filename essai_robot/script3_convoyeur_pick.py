# !/usr/bin/env python

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

# Describe this function...
def go_home():
  n.move_pose(*[0.14, 0, 0.203, -0.017, 0.761, -0.001])

# Describe this function...
def prendre_convoyeur():
  n.pick_from_pose(*[(-0.168), 0.182, 0.149, -1.832, 1.483, -0.371])


go_home()
n.set_conveyor()
n.wait(2)
n.control_conveyor(ConveyorID.ID_1, True, 100, ConveyorDirection.BACKWARD)
while n.digital_read('DI5'):
  n.highlight_block('~N%2mY68?4FUEs|Eu7gO')
  # convoyeur fonctionne
  n.highlight_block('kn*onixD~e53b2@c%]NF')
n.control_conveyor(ConveyorID.ID_1, False, 0, 1)
prendre_convoyeur()
 
