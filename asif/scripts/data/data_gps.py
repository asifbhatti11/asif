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
distance=float()
bearing=float()
lat1=float()
lon1=float()
lat2=float()
lon2=float()

def callback0(msg):
	global distance
	distance=msg.data
	print("distance",distance)

def callback1(msg):
	global bearing
	bearing=msg.data
	print("bearing",bearing)

def callback2(msg):
	global lat1
	lat1=msg.data
	print("lat1",lat1)
def callback3(msg):
	global lon1
	lon1=msg.data
	print("lon1",lon1)
def callback4(msg):
	global lat2
	lat2=msg.data
	print("lat2",lat2)

def callback5(msg):
	global j,distance,bearing,lat1,lon1,lat2,lon2
	lon2=msg.data

	print("pitch",pitch)
	print("roll",roll)
	print("yaw",yaw)
	print("heading",heading)
	worksheet.write(j+1,0, distance)
	worksheet.write(j+1,1, bearing)
	worksheet.write(j+1,2, lat1)
	worksheet.write(j+1,3, lon1)
	worksheet.write(j+1,4, lat2)
	worksheet.write(j+1,5, lon2)
	j+=1

if __name__ == '__main__':
    try:
	sub = rospy.Subscriber('distance', Float32, callback0)
	sub1 = rospy.Subscriber('bearing', Float32, callback1)
	sub2 = rospy.Subscriber('lat1', Float32, callback2)
	sub3 = rospy.Subscriber('lon1', Float32, callback3)
	sub3 = rospy.Subscriber('lat2', Float32, callback4)
	sub3 = rospy.Subscriber('lon2', Float32, callback5)
	
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
