#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('base_stabilized_publisher')

    listener = tf.TransformListener()

    publisher = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=1)

    rate = rospy.Rate(70)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/map', '/usb_cam2', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        t = geometry_msgs.msg.TransformStamped()
        t.header.frame_id = "/map"
        t.header.stamp = rospy.Time.now()
        t.child_frame_id = "/base_stabilized"
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

        rate.sleep()