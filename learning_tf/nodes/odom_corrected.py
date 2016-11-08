#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
import os

if __name__ == '__main__':
    rospy.init_node('odom_corrected_publisher')

    muerto = False

    listener = tf.TransformListener()

    publisher = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=0)

    rate = rospy.Rate(70)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        t = geometry_msgs.msg.TransformStamped()
        t.header.frame_id = "/odom0"
        t.header.stamp = rospy.Time.now()
        t.child_frame_id = "/odom_corrected"
        t.transform.translation.x = trans[0]
        t.transform.translation.y = trans[1]
        t.transform.translation.z = 0.0
        """
        t.transform.rotation.x = rot[0]
        t.transform.rotation.y = rot[1]
        t.transform.rotation.z = rot[2]
        t.transform.rotation.w = rot[3]
        """
        t.transform.rotation.x = 0
        t.transform.rotation.y = 0
        t.transform.rotation.z = rot[2]
        t.transform.rotation.w = rot[3]

        tfm = tf.msg.tfMessage([t])
        publisher.publish(tfm)
        
        """

        if not muerto:
            os.system("source ~/catkin_ws/devel/setup.bash")
            os.system("rosnode kill /camera_to_base_link_publisher")
            muerto = True

        t1 = geometry_msgs.msg.TransformStamped()
        t1.header.frame_id = "/odom_corrected"
        t1.header.stamp = rospy.Time.now()
        t1.child_frame_id = "/base_link_dummy"
        t1.transform.translation.x = 0.0
        t1.transform.translation.y = 0.0
        t1.transform.translation.z = 0.0

        t1.transform.rotation.x = rot[0]
        t1.transform.rotation.y = rot[1]
        t1.transform.rotation.z = rot[2]
        t1.transform.rotation.w = rot[3]

        t1.transform.rotation.x = 0.0
        t1.transform.rotation.y = 0.0
        t1.transform.rotation.z = 0.0
        t1.transform.rotation.w = 0.0

        tfm1 = tf.msg.tfMessage([t1])
        publisher.publish(tfm1)
        """

        rate.sleep()