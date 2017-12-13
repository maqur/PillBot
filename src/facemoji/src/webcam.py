#!/usr/bin/env python
"""
This module is the main module in this package. It loads emotion recognition model from a file,
shows a webcam image, recognizes face and it's emotion and draw emotion on the image.
"""
from cv2 import WINDOW_NORMAL

import cv2
from face_detect import find_faces
from image_commons import nparray_as_image, draw_with_alpha
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge,CvBridgeError


def callback(face_stream):
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', face_stream.data)
    return face_stream.data


def _load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    :param emotions: Array of emotions names.
    :return: Array of emotions graphics.
    """

    return [nparray_as_image(cv2.imread('/home/human/PillBot/src/facemoji/src/graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]

def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    :param model: Learnt emotion detection model.
    :param emoticons: List of emotions images.
    :param window_size: Size of webcam image window.
    :param window_name: Name of webcam image window.
    :param update_time: Image update time interval.
    """
    # Need to subscribe to the topic face_stream, receive the images in the ROS format, and convert them to openCV format
    pub = rospy.Publisher('mood', String, queue_size=10)
    rospy.init_node('webcam', anonymous=True)
    bg = CvBridge()
    sub = rospy.Subscriber('face_stream', sensor_msgs.msg.Image, callback)
    rate = rospy.Rate(10)

    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()
    else:
        print("webcam not found")
        return
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    while read_value and not rospy.is_shutdown():
        #for normalized_face, (x, y, w, h) in find_faces(webcam_image):
        for normalized_face, (x, y, w, h) in find_faces(sub):
            prediction = model.predict(normalized_face)  # do prediction
            if cv2.__version__ != '3.1.0':
                prediction = prediction[0]

            image_to_draw = emoticons[prediction]
            print(emotions[prediction])
            rospy.loginfo(emotions[prediction])
            pub.publish(emotions[prediction])
            rate.sleep()
            #draw_with_alpha(webcam_image, image_to_draw, (x, y, w, h))

        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)

        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow(window_name)


if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = _load_emoticons(emotions)

    # load model
    if cv2.__version__ == '3.1.0':
        fisher_face = cv2.face.createFisherFaceRecognizer()
    else:
        fisher_face = cv2.face.createFisherFaceRecognizer()

    fisher_face.load('/home/human/PillBot/src/facemoji/src/models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'WEBCAM (press ESC to exit)'
    try:
        show_webcam_and_run(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
    except rospy.ROSInterruptException:
        pass
