#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32,Int32
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField

import xlsxwriter 

import time, sys
pitch=0
roll=0
yaw=0
heading=0
acc_x=0
acc_y=0
acc_z=0
gyro_x=0
gyro_y=0
gyro_z=0
mag_x=0
mag_y=0
mag_z=0


rospy.init_node('store_data')

time_old=rospy.get_time()

time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
worksheet.write(0,0, "pitch")
worksheet.write(0,1, "roll")
worksheet.write(0,2, "yaw")
worksheet.write(0,3, "heading")

worksheet.write(0,4, "acc_x")
worksheet.write(0,5, "acc_y")
worksheet.write(0,6, "acc_z")
worksheet.write(0,7, "gyro_x")
worksheet.write(0,8, "gyro_y")
worksheet.write(0,9, "gyro_z")

worksheet.write(0,10, "mag_x")
worksheet.write(0,11, "mag_y")
worksheet.write(0,12, "mag_z")

worksheet.write(0,13, "time")
j=0

def callback0(msg):
	global pitch
	pitch=msg.data
def callback1(msg):
	global roll
	roll=msg.data
def callback2(msg):
	global yaw
	yaw=msg.data
def callback3(msg):
	global heading
	heading=msg.data
def callback4(data):
	global acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z
        msg=data
        acc_x=msg.linear_acceleration.x
        acc_y=msg.linear_acceleration.y
        acc_z=msg.linear_acceleration.z
        gyro_x=msg.angular_velocity.x
        gyro_y=msg.angular_velocity.y
        gyro_z=msg.angular_velocity.z

def callback5(msg):
	global j,pitch,roll,yaw,heading,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,mag_x,mag_y,mag_z,time_old
        mag_x=msg.magnetic_field.x
        mag_y=msg.magnetic_field.y
        mag_z=msg.magnetic_field.z

	print("pitch",pitch)
	print("roll",roll)
	print("yaw",yaw)
	print("heading",heading)
	print("acc_x",acc_x)
	print("acc_y",acc_y)
	print("acc_z",acc_z)
	print("gyro_x",gyro_x)
	print("gyro_y",gyro_y)
	print("gyro_z",gyro_z)
	print("mag_x",mag_x)
	print("mag_y",mag_y)
	print("mag_z",mag_z)

	time_c=rospy.get_time()
	t=time_c-time_old

	worksheet.write(j+1,0, pitch)
	worksheet.write(j+1,1, roll)
	worksheet.write(j+1,2, yaw)
	worksheet.write(j+1,3, heading)
	worksheet.write(j+1,4, acc_x)
	worksheet.write(j+1,5, acc_y)
	worksheet.write(j+1,6, acc_z)
	worksheet.write(j+1,7, gyro_x)
	worksheet.write(j+1,8, gyro_y)
	worksheet.write(j+1,9, gyro_z)
	worksheet.write(j+1,10, mag_x)
	worksheet.write(j+1,11, mag_y)
	worksheet.write(j+1,12, mag_z)
	worksheet.write(j+1,13, t)

	j+=1

if __name__ == '__main__':
    try:
	rospy.Subscriber('pitch', Float32, callback0)
	rospy.Subscriber('roll', Float32, callback1)
	rospy.Subscriber('yaw', Float32, callback2)
	rospy.Subscriber('heading', Float32, callback3)
	rospy.Subscriber("imu", Imu, callback4)
	rospy.Subscriber("MagneticField", MagneticField, callback5)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
