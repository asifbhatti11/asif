#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan
import xlsxwriter 

import time, sys
  
rospy.init_node('store_range_data')
time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
for i in range(0,719):
	worksheet.write(0, i+1, i) 
j=0
def callback(msg):
	global j
	x=msg.ranges
	print(x)
	worksheet.write(j+1,0, j)
	for k in range(0,719):
		worksheet.write(j+1,k+1,x[k])
	j+=1

if __name__ == '__main__':
    try:
	sub = rospy.Subscriber('scan', LaserScan, callback)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
