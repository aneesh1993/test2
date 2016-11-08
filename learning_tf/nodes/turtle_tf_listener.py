#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('velocity_planner')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('RosAria/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/target', '/ekf_odom_pose', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angular = 0.4 * math.atan2(trans[1], trans[0]) * (1/math.pi)
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular

	if abs(linear) < 0.005:
		cmd.linear.x = 0
	if abs(angular) < 0.05:
		cmd.angular.z = 0	

        turtle_vel.publish(cmd)

        rate.sleep()

