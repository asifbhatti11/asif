#! /usr/bin/env python
import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
from numpy import interp
import math
from math import degrees
l=50
z=[]
def callback(msg):
	global l,z
	x=msg.ranges
	x=list(x)
	y=[]
	for i in range(0,len(x)):
		if x[i]==0.0:
			x[i]=msg.range_max
#	print(x)
	theta=2*degrees(math.asin(25/l))
#	print(theta)
	n=int(interp(theta,[0,359],[0,718]))
#	print(n)
	if n%2==0:
		n=n+1
	m=int(n/2)
#	print(m)
	p=[]
	for t in range(0,719):
		count=0
		for k in range(t-m,t+m+1):
			if k>=719:
				q=k-719
			else:
				q=k
			if x[q]>(l/100):
				count+=1
		if count==n:
			p.append(t)
	z.append(p)
#	print(z)
	angle=0
	angle=int(interp(angle,[0,359],[0,718]))
	if l==1000:
		l=0
		for f in range(0,len(z)):
			if [] in z:
				z.remove([])
#		print("z:",z)
		c=0
		for d in range(0,len(z)):
			if d==len(z)-1:
				break
			l3=[]
			for e in range(len(z[d])):
				x2=z[d][e]-angle
				if x2>359:
					x2=x2-718
#				print(x2)
				l3.append(x2)
#			print(l3)
			y2=min(l3,key=abs)
			y2=y2+angle
			if y2<0:
				y2=y2+718
#			print(y2)
			new_angle=y2
#			new_angle=min(z[d], key=lambda x:abs(x-angle))
			if new_angle!=angle:
				angle=new_angle
				break
			c=c+1
		z=[]
		a1=int(interp(angle,[0,718],[0,359]))
		a2=int(interp(a,[0,359],[0,-359]))
		if a2<-179:
			a2+=360
		angle=a2
		print("count:",c)
		print("angle:",angle)
		pub0.publish(c)
		pub1.publish(angle)
	l+=50
rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
pub0= rospy.Publisher("count",Int32,queue_size=10)
pub1= rospy.Publisher("angle",Int32,queue_size=10)
rospy.spin()
