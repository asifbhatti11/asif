#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from std_msgs.msg import Float32
from math import *

time_old=0
rospy.init_node('listener', anonymous=True)
time_old=rospy.get_time()

mag_x=float()
mag_y=float()
mag_z=float()
pitch=0
roll=0
yaw=0
def callback0(data):
        global mag_x,mag_y,mag_z
        msg=data
        mag_x=msg.magnetic_field.x
        mag_y=msg.magnetic_field.y
        mag_z=msg.magnetic_field.z

def callback1(data):
	global time_old,mag_x,mag_y,mag_z,pitch,roll,yaw

	msg=data
	acc_x=msg.linear_acceleration.x
	acc_y=msg.linear_acceleration.y
	acc_z=msg.linear_acceleration.z
	gyro_x=msg.angular_velocity.x
	gyro_y=msg.angular_velocity.y
	gyro_z=msg.angular_velocity.z

	pitch_acc=atan(-acc_x/sqrt(acc_y*acc_y + acc_z*acc_z))
	roll_acc=atan(acc_y/sqrt(acc_x*acc_x + acc_z*acc_z))

	current_time=rospy.get_time()
	dt=current_time-time_old
	time_old=current_time

	pitch=(pitch+gyro_x*dt)*0.5+pitch_acc*0.5
	roll=(roll+gyro_y*dt)*0.5+roll_acc*0.5
	yaw_comp =  atan2((mag_y * cos(roll)) - (mag_z * sin(roll)), (mag_x * cos(pitch))+(mag_y * sin(roll)*sin(pitch)) + (mag_z * cos(roll) * sin(pitch)))
#	yaw=(yaw+gyro_z*dt)*0.3+yaw_comp*0.7
	yaw=yaw_comp
	heading=degrees(yaw)-0.116667
	if heading<0:
		heading+=360
	print("heading:",heading)
	pub0=rospy.Publisher("pitch",Float32,queue_size=10)
	pub1=rospy.Publisher("roll",Float32,queue_size=10)
	pub2=rospy.Publisher("yaw",Float32,queue_size=10)
	rate = rospy.Rate(10)

	pub0.publish(degrees(pitch))
	pub1.publish(degrees(roll))
	pub2.publish(heading)
#	rate.sleep()
	time_old=rospy.get_time()

def listener():
	rospy.Subscriber("MagneticField", MagneticField, callback0)
	rospy.Subscriber("imu", Imu, callback1)
	rospy.spin()

if __name__ == '__main__':
    listener()
