#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
"""
if __name__ == '__main__':
	rospy.init_node('tf_turtle')

	listener = tf.TransformListener()

	#rospy.wait_for_service('spawn')
	#spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
	#spawner(4, 2, 0, 'turtle2')

	#turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

	rate = rospy.Rate(10.0)
	while not rospy.is_shutdown():
		try:
			(trans,rot) = listener.lookupTransform('/turtle2', '/turtle1', rospy.Time(0))
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue

		angular = 4 * math.atan2(trans[1], trans[0])
		linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
		cmd = geometry_msgs.msg.Twist()
		cmd.linear.x = linear
		cmd.angular.z = angular
		turtle_vel.publish(cmd)

		rate.sleep()
"""
n = 16

class DynamicTFBroadcaster:

	def __init__(self):
		self.pub_tf = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=1)

		change = 0.0

		listener = tf.TransformListener()

		rate = rospy.Rate(500)

		while not rospy.is_shutdown():
			# Run this loop at about 10Hz
			#rospy.sleep(0.1)

				#name = '/tag_' + str(i), '/usb_cam1'
			try:
				(trans,rot) = listener.lookupTransform('/tag_1', '/usb_cam2', rospy.Time(0))
			except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
				continue
				#print trans
				#print rot
			
			"""
			angular = 4 * math.atan2(trans[1], trans[0])
			linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
			cmd = geometry_msgs.msg.Twist()
			cmd.linear.x = linear
			cmd.angular.z = angular
			turtle_vel.publish(cmd)
			"""

			t = geometry_msgs.msg.TransformStamped()
			t.header.frame_id = "tag_1_ideal"
			t.header.stamp = rospy.Time.now()
			t.child_frame_id = "tag_1_guess"

			t.transform.translation.x = trans[0]
			t.transform.translation.y = trans[1]
			t.transform.translation.z = trans[2]

			t.transform.rotation.x = rot[0]
			t.transform.rotation.y = rot[1]
			t.transform.rotation.z = rot[2]
			t.transform.rotation.w = rot[3]
			tfm = tf.msg.tfMessage([t])
			self.pub_tf.publish(tfm)

			#print t

			rate.sleep()


if __name__ == '__main__':
	rospy.init_node('tag_1_guess')
	tfb = DynamicTFBroadcaster()
	rospy.spin()