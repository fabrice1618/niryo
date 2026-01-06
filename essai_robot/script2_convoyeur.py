# !/usr/bin/env python

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

n.set_conveyor()
n.wait(2)
n.control_conveyor(ConveyorID.ID_1, True, 100, ConveyorDirection.BACKWARD)
while n.digital_read('DI5'):
  # convoyeur fonctionne
  ...
n.control_conveyor(ConveyorID.ID_1, False, 0, 1)
 
