#!/usr/bin/env python
import rospy
import sys

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()
count =0
path_len = 0
x_prev, y_prev, z_prev = 0,0,0

def pose_cb(data):
    global path
    global count
    global path_len, x_prev, y_prev, z_prev

    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

    dist = ((x-x_prev)**2 + (y-y_prev)**2 + (z-z_prev)**2)**0.5
    
    #Temporary value of 0.5 used for eliminating jumps. CHANGE THIS LATER
    if dist < 0.5:
        path_len = path_len + dist
    else:
        path_len = 0
    
    x_prev, y_prev, z_prev = x,y,z
    #print("Path Length = "+str(path_len))

    path.header = data.header

    path.poses.append(data)
    path_pub.publish(path)

    count = (count+1)%20
    if not count:
        odom = Odometry()
        odom.header = data.header
        odom.pose.pose = data.pose
        odom_pub.publish(odom)
        print("Path Length = "+str(path_len))


if __name__ == '__main__':
    rospy.init_node('pose_to_path')

    pose_sub = rospy.Subscriber('/orbslam3/pose', PoseStamped, pose_cb)

    path_pub = rospy.Publisher('/orbslam3/path', Path, queue_size=10)
    odom_pub = rospy.Publisher('/orbslam3/odom', Odometry, queue_size=10)
    
    rospy.spin()