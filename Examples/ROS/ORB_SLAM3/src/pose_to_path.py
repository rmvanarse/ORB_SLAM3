#!/usr/bin/env python
import rospy
import sys

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()
count =0

def pose_cb(data):
    global path
    global count
    path.header = data.header

    path.poses.append(data)
    path_pub.publish(path)

    count = (count+1)%20
    if not count:
        odom = Odometry()
        odom.header = data.header
        odom.pose.pose = data.pose
        odom_pub.publish(odom)


if __name__ == '__main__':
    rospy.init_node('pose_to_path')

    pose_sub = rospy.Subscriber('/orbslam3/pose', PoseStamped, pose_cb)

    path_pub = rospy.Publisher('/orbslam3/path', Path, queue_size=10)
    odom_pub = rospy.Publisher('/orbslam3/odom', Odometry, queue_size=10)
    
    rospy.spin()