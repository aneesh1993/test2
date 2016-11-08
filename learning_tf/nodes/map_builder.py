#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

# *** Minimum Thresholding distance from distance of tag in (x,y) plane from center of camera ***
threshold = 1.5


def find_dists():

    dists = list()
    dists = [1000] * 16

    for i in range(0,16):
        
        tag = "tag_" + str(i)
                
        try:
            (trans,rot) = listener.lookupTransform('/usb_cam2', tag, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        d = math.sqrt(trans[0]**2 + trans[1]**2)
        if d < threshold:
            dists[i] = d

    print dists
    return dists


def publishTf(transRot):

	t = geometry_msgs.msg.TransformStamped()
	t.header.frame_id = baseName
	t.header.stamp = rospy.Time.now()
	t.child_frame_id = tag + "_guess"
	t.transform.translation.x = transRot[0]
	t.transform.translation.y = transRot[1]
	t.transform.translation.z = transRot[2]

	t.transform.rotation.x = transRot[3]
	t.transform.rotation.y = transRot[4]
	t.transform.rotation.z = transRot[5]
	t.transform.rotation.w = transRot[6]

	tfm = tf.msg.tfMessage([t])
	publisher.publish(tfm)        
	rate.sleep()


if __name__ == '__main__':
    rospy.init_node('map_builder')

    listener = tf.TransformListener()

    publisher = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=1)

    rate = rospy.Rate(100)
    '''    
    total = list()
    total = [[0,0,0,0,0,0,0]] * 16    # Initialize list of 16 0's -- stores running sums

    tagCount = list()
    tagCount = [[0,0,0,0,0,0,0]] * 16 # Initialize list of 16 0's -- stores running tagCounts

    Dev = list()
    Dev = [[0,0,0,0,0,0,0]] * 16    # Initialize list of 16 0's -- stores running deviation averages
    '''  
    runningSum = [0,0,0,0,0,0,0]
    average = [0,0,0,0,0,0,0]
    while not rospy.is_shutdown():

        distances = find_dists()
        base = distances.index(min(distances))
        iterations = 0
        for i in distances:
            if i != 1000 and distances.index(i) != base:
                tagNum = str(distances.index(i))
                tag = "/tag_" + tagNum
                baseName = "/tag_" + str(base)

                #print tag
                #print baseName
                
                for avgCount in range(0,iterations):

                    try:
                        (trans,rot) = listener.lookupTransform( baseName, tag, rospy.Time(0))
                    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                        continue
                    transRot = trans + rot
                    runningSum = map(sum, zip(runningSum ,transRot))

                average = [i/iterations for i in runningSum]

            	publishTf(average)
                print "pub"
           		runningSum = [0,0,0,0,0,0,0]










1. find distances (within a certain range)
2. least dist is the base
3. lookup tf from base to all others 100 times
4. get avg and pub