#!/usr/bin/env python
import rospy
from sensor_msgs.msg import MagneticField
from std_msgs.msg import Float32
from math import *

def callback(data):
	msg=data
	mag_x=msg.magnetic_field.x
	mag_y=msg.magnetic_field.y
	mag_z=msg.magnetic_field.z
	psi=atan2(mag_y,mag_x)
	psi=(degrees(psi))-0.116667
	if psi<0:
		psi+=360
	print("heading",psi)
	pub = rospy.Publisher("heading",Float32,queue_size=10)
	pub.publish(psi)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("MagneticField", MagneticField, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
