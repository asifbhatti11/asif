#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu

import xlsxwriter 

import time, sys
  
rospy.init_node('store_imu_data')
time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
worksheet.write(0,0, "acc_x")
worksheet.write(0,1, "acc_y")
worksheet.write(0,2, "acc_z")
worksheet.write(0,3, "gyro_x")
worksheet.write(0,4, "gyro_y")
worksheet.write(0,5, "gyro_z")

j=0

def callback(data):
	global j
        msg=data
        acc_x=msg.linear_acceleration.x
        acc_y=msg.linear_acceleration.y
        acc_z=msg.linear_acceleration.z
        gyro_x=msg.angular_velocity.x
        gyro_y=msg.angular_velocity.y
        gyro_z=msg.angular_velocity.z

	#print("acc_x",acc_x)
	#print("acc_y",acc_y)
	#print("acc_z",acc_z)
	#print("gyro_x",gyro_x)
	#print("gyro_y",gyro_y)
	#print("gyro_z",gyro_z)

	worksheet.write(j+1,0, acc_x)
	worksheet.write(j+1,1, acc_y)
	worksheet.write(j+1,2, acc_z)
	worksheet.write(j+1,3, gyro_x)
	worksheet.write(j+1,4, gyro_y)
	worksheet.write(j+1,5, gyro_z)
	j+=1

if __name__ == '__main__':
    try:
	rospy.Subscriber("imu", Imu, callback)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
