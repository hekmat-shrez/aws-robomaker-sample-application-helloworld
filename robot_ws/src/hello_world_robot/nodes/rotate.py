#!/usr/bin/env python
# source: https://get-help.robotigniteacademy.com/t/how-to-stop-your-robot-when-ros-is-shutting-down/225

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import rospy
from geometry_msgs.msg import Twist
import time

class MoveRobotStopOnShutdown(object):
    

    def __init__(self):
        

        # create publisher and message as instance variables
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.msg = Twist()

        # do some cleanup on shutdown
        rospy.on_shutdown(self.clean_shutdown)

        # start by moving robot
        rospy.init_node('move_and_stop_robot')
        self.move_robot()
        rospy.spin()

    def publish(self, msg_type="move"):
        

        while self.publisher.get_num_connections() < 1:
            # wait for a connection to publisher
            rospy.loginfo("Waiting for connection to publisher...")
            time.sleep(1)

        rospy.loginfo("Connected to publisher.")

        rospy.loginfo("Publishing %s message..." % msg_type)
        self.publisher.publish(self.msg)

    def move_robot(self):
       

        self.msg.linear.x = 0.2
        self.publish()

        time.sleep(55) # sleep and then stop

        rospy.signal_shutdown("We are done here!")

    def clean_shutdown(self):
        

        rospy.loginfo("System is shutting down. Stopping robot...")
        self.msg.linear.x = 0
        self.publish("stop")

if __name__ == '__main__':
    MoveRobotStopOnShutdown()
 