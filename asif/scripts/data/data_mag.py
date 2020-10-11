#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import MagneticField

import xlsxwriter 

import time, sys
  
rospy.init_node('store_mag_data')
time_now=str(rospy.get_time())
title=time_now+".xlsx"
print(title)
workbook = xlsxwriter.Workbook(title) 

worksheet = workbook.add_worksheet("My sheet")
worksheet.write(0,0, "mag_x")
worksheet.write(0,1, "mag_y")
worksheet.write(0,2, "mag_z")
j=0

def callback(msg):
	global j
        mag_x=msg.magnetic_field.x
        mag_y=msg.magnetic_field.y
        mag_z=msg.magnetic_field.z

	#print("mag_x",mag_x)
	#print("mag_y",mag_y)
	#print("mag_z",mag_z)

	worksheet.write(j+1,0, mag_x)
	worksheet.write(j+1,1, mag_y)
	worksheet.write(j+1,2, mag_z)
	j+=1

if __name__ == '__main__':
    try:
	rospy.Subscriber("MagneticField", MagneticField, callback)
	rospy.spin()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing data file")
	workbook.close()
