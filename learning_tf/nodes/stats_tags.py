#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('tag_relative')

    listener = tf.TransformListener()

    publisher = rospy.Publisher("/tf", tf.msg.tfMessage, queue_size=1)

    rate = rospy.Rate(100)
    
    total = list()
    total = [[0,0,0]] * 16    # Initialize list of 16 0's -- stores running sums

    tagCount = list()
    tagCount = [[0,0,0]] * 16 # Initialize list of 16 0's -- stores running tagCounts

    Dev = list()
    Dev = [[0,0,0]] * 16    # Initialize list of 16 0's -- stores running deviation averages
    
    while not rospy.is_shutdown():

        for i in range(4,5):
            if i != 5:
                tag = "tag_" + str(i)
                    
                try:
                    (trans,rot) = listener.lookupTransform('/tag_5', tag, rospy.Time(0))
                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    continue


                print "Transform from tag_5 to " + tag 

                #print "current X = " + str(trans[0]) 
                
                for k in range(0,3):
                    print "--------------"+str(k)+"-------------------------"
                    total[i][k] += trans[k]

                    tagCount[i][k] += 1

                    runningAvg = total[i][k]/tagCount[i][k]

                    Dev[i][k] += abs(runningAvg - trans[k])
                    aveDev = Dev[i][k]/tagCount[i][k]
                    print "Running Average = " + str(runningAvg)
                    
                    print "Deviation = " + str(abs(runningAvg - trans[k]))
                    print "Average Deviation ="  + str(aveDev)

                print""

            
                rate.sleep()

            