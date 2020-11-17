import numpy as np
import time

import rospy
from sensor_msgs.msg import Imu

pub_topic = "/imu/imu"
sub_topic = "/imu/imu0"

np.random.seed(42)

rospy.init_node("imu_noise_node", anonymous=True)


imu_pub = rospy.Publisher(pub_topic, Imu, queue_size=20)

def add_noise(msg):

	#t0 = time.time()
	global imu_pub

	msg2 = Imu()

	std_lin = 0.07
	std_rot = 0.01

	noise_lin = np.random.randn(3)*std_lin
	noise_rot = np.random.randn(3)*std_rot

	msg2.header = msg.header

	msg2.linear_acceleration.x = msg.linear_acceleration.x + noise_lin[0]
	msg2.linear_acceleration.y = msg.linear_acceleration.y + noise_lin[1]
	msg2.linear_acceleration.z = msg.linear_acceleration.z + noise_lin[2]

	msg2.angular_velocity.x = msg.angular_velocity.x + noise_rot[0]
	msg2.angular_velocity.y = msg.angular_velocity.y + noise_rot[1]
	msg2.angular_velocity.z = msg.angular_velocity.z + noise_rot[2]

	imu_pub.publish(msg2)

	#print(time.time()-t0)

imu_sub = rospy.Subscriber(sub_topic, Imu, add_noise)

def main():
	rospy.spin()

if __name__ == "__main__":
	main()