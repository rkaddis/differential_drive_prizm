#!/usr/bin/env python3

import rospy
import cv2 as cv
from geometry_msgs.msg import Point
from sensor_msgs.msg import Joy, Image
from cv_bridge import CvBridge, CvBridgeError

drive = (0.0, 0.0)
bridge = CvBridge()

def joy_cb(msg):
    global drive
    drive = (msg.axes[1], msg.axes[3])
    vel_msg = Point(-30 *drive[0], -30*drive[1], 0)
    vel_pub.publish(vel_msg)

def image_cb(msg):
    global drive, bridge
    try: #convert ros image to cv image
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")   
    except CvBridgeError:
        return
    
    (rows, cols, channels) = cv_image.shape
    
    cv_image = cv.circle(cv_image, (30,  int((rows * (1-drive[0]))/2)), 20, (200, 200, 200), -1)
    cv_image = cv.circle(cv_image, (cols - 30, int((rows * (1-drive[1]))/2)), 20, (200, 200, 200), -1)

    cv.imshow("Drive Window", cv_image)
    cv.waitKey(3)


if __name__ == '__main__':
    rospy.init_node("differential_drive", anonymous=True)
    rospy.Subscriber("/joy", Joy, joy_cb, queue_size=1)
    rospy.Subscriber("/cam_pub/image_raw", Image, image_cb, queue_size=1)
    vel_pub = rospy.Publisher("/prizm/motor_cmd", Point, queue_size=1)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
