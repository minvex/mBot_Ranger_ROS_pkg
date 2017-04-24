#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy
from meauriga import *
from mBot_Ranger_ROS_pkg.srv import *

bot = None
useTankSteering = True;
online = False;


# Defining functions
# -------------------------

# Callback for readings from ultrasonic sensor 
def onUltrasonicSensorRead(v):
    #print("and here!")
    rospy.loginfo('Distance' + v)
    pub.publish(v)


# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into Twist commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed
def joyCallback(data):
    #twist = Twist()
    #twist.linear.x = 4*data.axes[1]
    #twist.angular.z = 4*data.axes[0]
    #pub.publish(twist)
    #if(useTankSteering)
    m1 = numpy.interp(data.axes[1],[-1,1],[-255,255])
    m2 = numpy.interp(data.axes[4],[-1,1],[-255,255])
    bot_control_motors(m1, m2)
    rospy.loginfo(m1)
    rospy.loginfo(m2)
    #rospy.loginfo(data)


# Service method add velocity to motors 
def handle_makeblock_motors(req):
    rospy.loginfo(req)
    bot_control_motors(req.s1, req.s2)
    return 1


def bot_control_motors(m1, m2):
    global bot
    global online
    if online:
        bot.motorRun(M1, req.s1)
        bot.motorRun(M2, req.s2)


# Defining variables
# ----------------------
pub = rospy.Publisher('mBot_Ranger_controller_ultrasensor', Float32, queue_size=1)
s = rospy.Service('mBot_Ranger_controller_move_motors', MakeBlockMover,
                  handle_makeblock_motors)


def main():
    global bot
    global online
    if online:
        bot = MeAuriga()
        bot.start("/dev/ttyUSB0")

    # Subscribe for teleoperations
    rospy.Subscriber("joy", Joy, joyCallback)

    rospy.init_node('mBot_Ranger_controller', anonymous=False)

    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        sleep(0.1)
        #print("been here!")
	if online:
            bot.ultrasonicSensorRead(3, onUltrasonicSensorRead)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
