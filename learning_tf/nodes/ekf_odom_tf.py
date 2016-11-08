#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
from nav_msgs.msg import Odometry

rospy.init_node('ekf_odom_tf_publisher')

publisher = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=0)

rate = rospy.Rate(70)

def callback(msg):
    t = geometry_msgs.msg.TransformStamped()
    t.header.frame_id = "/map"
    t.header.stamp = rospy.Time.now()
    t.child_frame_id = "/ekf_odom_pose"
    t.transform.translation.x = msg.pose.pose.position.x
    t.transform.translation.y = msg.pose.pose.position.y
    t.transform.translation.z = 0.0

    t.transform.rotation.x = 0.0
    t.transform.rotation.y = 0.0
    t.transform.rotation.z = msg.pose.pose.orientation.z
    t.transform.rotation.w = msg.pose.pose.orientation.w

    tfm = tf.msg.tfMessage([t])
    publisher.publish(tfm)

    rate.sleep()

def listener():

    rospy.Subscriber("odometry/ekf_estimate", Odometry, callback)

    rospy.spin()


if __name__ == '__main__':

    listener()

    