#!/usr/bin/env python3

import rospy
import math
from geometry_msgs.msg import Twist # for the publisher
from turtlesim.msg import Pose # for the subscriber

class turtleBotThingieClass:
    def __init__(self):
        # only 1 node, will subscribe to the /turtle1/pose topic
        # and publish to the /turtle1/cmd_vel topic
        rospy.init_node("turtle_controller")
        rospy.loginfo("Starting turtlesim_PID_controller node as turtle_controller.")

        # defining the publisher and subscriber objects
        self.turtle_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        self.turtle_sub = rospy.Subscriber("/turtle1/pose", Pose, self.turtle_pos_updater)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    # callback function for the subscriber, updates the current position of the turtle
    def turtle_pos_updater(self, position_data):
        self.pose = position_data

    # linear error value
    def position_error(self, destination):
        return math.sqrt((destination.x - self.pose.x)**2 + (destination.y - self.pose.y)**2)

    # angular error value
    def angle_steer_error(self, destination):
        angle = math.atan2((destination.y - self.pose.y),(destination.x - self.pose.x)) - self.pose.theta
        if angle > math.pi:
            angle -= 2*math.pi
        elif angle < -math.pi:
            angle += 2*math.pi
        return angle
    
    # angular error but for the final positioning of the bot
    def angle_target_error(self, destination):
        angle = destination.theta - self.pose.theta
        while angle > math.pi:
            angle -= 2*math.pi
        while angle < -math.pi:
            angle += 2*math.pi
        return angle
    
    # only P controller, no need of D, since direct mapping of X and Theta to X' and Theta'

    def mover(self):
        # making position and velocity objects to send over the topics
        final_destination = Pose()
        pid_output = Twist()

        # initialising some pid_output values which will remain constant
        pid_output.linear.y = 0
        pid_output.linear.z = 0
        pid_output.angular.x = 0
        pid_output.angular.y = 0

        # getting the inputs from the user
        final_destination.x = float(input("Enter the value of the x position: "))
        final_destination.y = float(input("Enter the value of the y position: "))
        final_destination.theta = math.pi/180*float(input("Enter the value of the final angle (in degrees): "))

        error_tolerance = 0.01 # can take as user input, but i don't want to
        control_constants = [1, 7.0] # pid kp constants

        # loop for getting to the final destination point
        while self.position_error(final_destination) >= error_tolerance and not rospy.is_shutdown():
            # PID feedback loop
            pid_output.linear.x = control_constants[0]*self.position_error(final_destination)
            pid_output.angular.z = control_constants[1]*self.angle_steer_error(final_destination)

            # publishing the value on the /turtle1/cmd_vel topic
            self.turtle_pub.publish(pid_output)
            self.rate.sleep()

        # stopping the bot after out of the loop
        pid_output.linear.x = 0
        self.turtle_pub.publish(pid_output)

        # loop for positioning the turtle at the given angle
        while abs(self.angle_target_error(final_destination)) >= error_tolerance and not rospy.is_shutdown():
            pid_output.angular.z = control_constants[1]*self.angle_target_error(final_destination)

            self.turtle_pub.publish(pid_output)
            self.rate.sleep()

        pid_output.angular.z = 0
        self.turtle_pub.publish(pid_output)

        rospy.spin()

if __name__ == "__main__":
    try:
        ros_node = turtleBotThingieClass()
        ros_node.mover()
    except rospy.ROSInterruptException:
        pass