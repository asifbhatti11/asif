#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import xlsxwriter 

import time, sys
  
rospy.init_node('store_range_data')
time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
worksheet.write(0,0, "pitch")
worksheet.write(0,1, "roll")
worksheet.write(0,2, "yaw")
j=0
pitch=float()
roll=float()
yaw=float()
heading=float()

def callback(msg):
	global pitch
	x=msg.data
	pitch=x
	print("pitch",pitch)

def callback1(msg):
	global roll
	x=msg.data
	roll=x
	print("roll",roll)

def callback3(msg):
	global heading
	x=msg.data
	heading=x
	print("heading",heading)

def callback2(msg):
	global j,pitch,roll,yaw,heading
	x=msg.data
	yaw=x
	print("pitch",pitch)
	print("roll",roll)
	print("yaw",yaw)
	print("heading",heading)
	worksheet.write(j+1,0, pitch)
	worksheet.write(j+1,1, roll)
	worksheet.write(j+1,2, yaw)
	worksheet.write(j+1,3, heading)
	j+=1

if __name__ == '__main__':
    try:
	sub = rospy.Subscriber('pitch', Float32, callback)
	sub1 = rospy.Subscriber('roll', Float32, callback1)
	sub2 = rospy.Subscriber('yaw', Float32, callback2)
	sub3 = rospy.Subscriber('heading', Float32, callback3)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
