# Turtlesim PID Controllers

### Python Code Overview

The basic structure of both scripts is as follows:

- A class `turtleBotThingieClass` to make the code Object Oriented
- Constructor function to initialise the `Subscriber` and `Publisher` objects and ******create****** the `rosnode`
- A getter function `turtle_pos_updater` to get the live position of the Turtle by ***********subscribing*********** to the `/turtle1/pose` topic
- Error functions to calculate the difference between ******desired****** and *******current******* value
- Finally, a setter function `mover` which *********publishes********* the data onto the `/turtle1/cmd_vel` topic to which the Turtle is subscribed

In general it is a good habit to make this script object oriented by using classes as this allows the user to create multiple nodes if needed

### Normal Steering Mechanism

Basic principle is similar to driving a car, which moves forward/backward along with turning, rather than turn in place before moving forward

The `angle_steer_error` is used to measure the error in angle between the turtle’s current facing direction to the one it is supposed to face, basically aligning it to where its supposed to go

The `position_error` measures the error in the linear distance between the current and final position of the turtle

Using both of them simultaneously gives a smooth ********steering******** curve, the radius and *******smoothness******* of which can be controlled by altering the PID constants

### Turn and Drive Mechanism

It uses the same functions as above, simply the order is changed

First the alignment is done to ****face**** the final direction, without any linear movement; then the linear movement is done, but the PID for angular error is not taken out of the equation due to error large distances
