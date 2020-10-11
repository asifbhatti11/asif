#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

import xlsxwriter 

import time, sys
  
rospy.init_node('store_turnning_data')
time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
worksheet.write(0,0, "count")
worksheet.write(0,1, "angle")

count=0
angle=0
j=0

def callback0(msg):
	global count
	count=int(msg.data)

def callback1(msg):
	global angle,count,j
	angle=int(msg.data)
	print(count)
	print(angle)
	worksheet.write(j+1,0, count)
	worksheet.write(j+1,1, angle)
	j+=1

if __name__ == '__main__':
    try:
	sub = rospy.Subscriber('count', Int32, callback0)
	sub1 = rospy.Subscriber('angle', Int32, callback1)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()




