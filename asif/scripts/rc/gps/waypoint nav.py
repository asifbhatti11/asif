#!/usr/bin/env python

import rospy
import time
import board
import busio
import adafruit_gps

from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float32
import serial


import xml.etree.ElementTree as ET
from math import *
filePath = r'123.kml'
tree = ET.parse(filePath) 
lineStrings = tree.findall('.//{http://www.opengis.net/kml/2.2}LineString')

earthRadius = 6371000.0
diatance=0
heading=0

for attributes in lineStrings:
	for subAttribute in attributes:
		if subAttribute.tag == '{http://www.opengis.net/kml/2.2}coordinates':
			#print subAttribute.text
			x=subAttribute.text
#print(x)
y = x.split()
for i in range(0,len(y)):
	y[i]=y[i].split(",")
	y[i].remove('0')
	#print(y)
	for j in range(0,2):
		y[i][j]=float(y[i][j])
print(y)
length=len(y)

def Distance(lon1 , lat1, lon2 , lat2): #Returns distance to waypoint in Metres
	lat2, lon2, lat1, lon1 = map(radians, [lat2, lon2, lat1, lon1]) #Convert into Radians to perform math
	a = pow(sin((lat2 - lat1)/2),2) + cos(lat1) * cos(lat2) * pow(sin((lon2 - lon1)/2),2)
	return earthRadius * 2.0 * asin(sqrt(a))  #Return calculated distance to waypoint in Metres

def bearing(lon1 , lat1, lon2 , lat2): #Bearing to waypoint (degrees)
	lat2, lon2, lat1, lon1 = map(radians, [lat2, lon2, lat1, lon1]) #Convert into Radians to perform math
	dLon = lon2 - lon1
	return (atan2(sin(dLon) * cos(lat2), cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dLon)))*180/pi +360)%360

#lon1 , lat1, lon2 , lat2 = -0.32525, 51.59821,-0.33519,51.59573
#distance = distance(lon1 , lat1, lon2 , lat2)
#heading = heading(lon1 , lat1, lon2 , lat2)
#print(distance)
#print(heading)
c=0
def callback(data):
	global length
	msg=data
	msg.latitude = gps.latitude
	msg.longitude = gps.longitude
	lat1 = msg.latitude
	lon1 = msg.longitude
#	lon1 , lat1, lon2 , lat2 = -0.32525, 51.59821,-0.33519,51.59573
	lat2 = y[c][1]
	lon2 = y[c][0]

	distance = distance(lon1 , lat1, lon2 , lat2)
	bearing = bearing(lon1 , lat1, lon2 , lat2)
	print("current position lat:",lat1)
	print("current position lon:",lon1)
	print("target position lat:",lat2)
	print("target position lon:",lon2)

	print("distance:",distance)
	print("bearing:",bearing)

        pub0=rospy.Publisher("distance",Float32,queue_size=10)
        pub1=rospy.Publisher("bearing",Float32,queue_size=10)        
	pub2=rospy.Publisher("lat1",Float32,queue_size=10)
        pub3=rospy.Publisher("lon1",Float32,queue_size=10)
        pub4=rospy.Publisher("lat2",Float32,queue_size=10)
        pub5=rospy.Publisher("lon2",Float32,queue_size=10)


	pub0.publish(distance)
	pub1.publish(bearing)
	pub2.publish(lat1)
	pub3.publish(lon1)
	pub4.publish(lat2)
	pub5.publish(lon2)

	if distance < 3:
		c+=1
	
	if (length-1)==c:
		print("destination reached")
		rospy.signal_shutdown("destination reached")

if __name__ == '__main__':
    try:
	rospy.init_node('gps_navigation', anonymous=True)
	rospy.Subscriber("'NavSatFix", NavSatFix, callback)
	rospy.spin()


    except rospy.ROSInterruptException:
        pass





