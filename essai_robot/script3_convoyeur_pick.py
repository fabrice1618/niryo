# !/usr/bin/env python

from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

# Describe this function...
def go_home():
  n.highlight_block('ppeT_W3gW|]Cigw3IH*v')
  n.highlight_block('9UafcL?2s6;lsHEY6,Q)')
  n.move_pose(*[0.14, 0, 0.203, -0.017, 0.761, -0.001])

# Describe this function...
def prendre_convoyeur():
  n.highlight_block('BTNe%{qsJ9:{MPT:ew!H')
  n.highlight_block('8s%Re,k(a0A=#~RwL_qf')
  n.pick_from_pose(*[(-0.168), 0.182, 0.149, -1.832, 1.483, -0.371])


n.highlight_block('fcBG*O3v=s-q]X3oa@iR')
go_home()
n.highlight_block('B0iTSW6Q!UGL]%TB(:wh')
n.set_conveyor()
n.wait(2)
n.highlight_block('5PdK#x+50p2X-jSR$Hm{')
n.control_conveyor(ConveyorID.ID_1, True, 100, ConveyorDirection.BACKWARD)
n.highlight_block('kn*onixD~e53b2@c%]NF')
while n.digital_read('DI5'):
  n.highlight_block('~N%2mY68?4FUEs|Eu7gO')
  # convoyeur fonctionne
  n.highlight_block('kn*onixD~e53b2@c%]NF')
n.highlight_block('J]l~P].F1r3O!F]vsxur')
n.control_conveyor(ConveyorID.ID_1, False, 0, 1)
n.highlight_block('sOOirvuqHw/[t{YnotAr')
prendre_convoyeur()
 
