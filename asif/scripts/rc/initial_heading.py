#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import time
heading=float()
yaw=float()

def callback0(msg):
	global heading
	heading=msg.data
	#print("heading1",heading)

def callback1(msg):
	global yaw,heading
	yaw=msg.data
	print("yaw",yaw)
	print("heading",heading)
	if yaw != 0.0 :
		f= open("initial_heading.txt","w+")
		f.write(str(yaw))
		rospy.sleep(0.1)
		f.close()
		print("data recorded")
		rospy.signal_shutdown("data taken")
def listener():
	rospy.init_node('store_initial_heading')
	rospy.Subscriber('heading', Float32, callback0)
	rospy.Subscriber('yaw', Float32, callback1)
	rospy.spin()
if __name__ == '__main__':
	listener()

