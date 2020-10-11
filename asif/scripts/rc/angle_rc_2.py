#!/usr/bin/env python
import rospy
from numpy import interp

from std_msgs.msg import Float32,Int32,String
yaw=0
heading=0
safety=str()
f= open("initial_heading.txt","r+")
x=f.readlines()
initial_heading=float(x[0])
print(initial_heading)
x=0
y=0
z=0
s1_turn=0
s2_turn=0
turn=float(input("enter turnning angle:"))
rospy.init_node('RC_at_angle')

def callback2(msg):
	global safety
	safety=msg.data

def callback0(msg):
	global yaw
	yaw=msg.data
	
def callback1(msg):
	global heading,yaw,turn,initial_heading,safety,x,y,z,s1_turn,s2_turn
	heading=msg.data
	
	pub0 = rospy.Publisher('servo0', Int32, queue_size=10)
	pub1 = rospy.Publisher('servo1', Int32, queue_size=10)
	pub2 = rospy.Publisher('esc', Int32, queue_size=10)

	pub3 = rospy.Publisher('turn', Float32, queue_size=10)
	pub4 = rospy.Publisher('target_heading', Float32, queue_size=10)

	rate = rospy.Rate(10)
	current=yaw
	#d=destination-current
	#print(d)
	target_heading=initial_heading+turn

	#d=headingDegrees
	#print("current heading:-")
	#print(d)

	if target_heading<-180:
		target_heading=target_heading+360
	elif target_heading>180:
		target_heading=target_heading-360

	turn1=target_heading-current

	if turn1<-180:	
		turn1=turn1+360
	elif turn1>180:
		turn1=turn1-360
	print(turn1)
	
	#if abs(turn1)<45:
	#	s1_turn = interp(turn1,[-90,90],[90,0])
		#s2_turn=interp(turn1,[-90,90],[90,0])
	#	s2_turn=45
	#if abs(turn1)<=45:
	#	s1_turn = interp(turn1,[-90,90],[90,0])
	#	s2_turn=interp(turn1/2,[-90,90],[0,90])
	#elif abs(turn1)>90:
	#	s1_turn = interp(turn1,[-90,90],[90,0])
	#	s2_turn=interp(turn1,[-90,90],[0,90])

	s1_turn = interp(turn1,[-90,90],[90,0])
	s2_turn = interp(turn1,[-90,90],[0,90])

#	if abs(turn1)<=45:
#		s1_turn = interp(turn1,[-90,90],[90,0])
#		s2_turn=45
#		s2_turn = interp(turn1,[-45,45],[90,0])
#	elif abs(turn)>45 and abs(turn)<=90:
#		s1_turn = interp(turn1,[-90,90],[90,0])
#		s2_turn = interp(turn1,[-90,90],[90,0])
#	elif abs(turn)>90:
#		s1_turn = interp(turn1,[-90,90],[90,0])
#		s2_turn = interp(turn1,[-90,90],[0,90])
	x=int(s1_turn)
	y=int(s2_turn)
	z=110
	print("s1:",x)
	print("s2:",y)
#	print("esc:",z)
	#x=int(input("enter servo0 angle:"))
	#y=int(input("enter servo1 angle:"))
	#z=int(input("enter esc speed 56-75 ; 93-126:"))	
	#if safety=="not_safe":
#		x=45
#		y=45
#		z=85
#		print("stopping robot")

	if 1==0:
		if turn1<-15:
			x=90
			y=45
		elif turn1>15:
			x=0
			y=45
		else:
			x=45
			y=45
		z=110

#	x=0
#	y=90
#	x=45
#	y=45
#	z=108
	pub0.publish(x)
	pub1.publish(y)
	pub2.publish(z)
	pub3.publish(turn1)
	pub4.publish(target_heading)
#	rospy.sleep(0.1)

if __name__ == '__main__':
    try:
	rospy.Subscriber('safety', String, callback2)
	rospy.Subscriber('yaw', Float32, callback0)
	rospy.Subscriber('heading', Float32, callback1)
	rospy.spin()
    except KeyboardInterrupt:
        pass


