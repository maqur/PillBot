#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import http.client



def callback(data):
    print( data.data)

    conn = http.client.HTTPSConnection("box-6748659.us-east-1.bonsaisearch.net")

    payload = "{\"dispensename\":\"" + data.data +  "\"}"

    headers = {
        'authorization': "Basic NTh5NWNrNmU6djdvY3c3NWY3MjlxYXp3NQ==",
        'cache-control': "no-cache",
        'postman-token': "fe0ea64d-4096-c09b-579c-c8299a44caf9"
        }

    conn.request("POST", "/try/try/dispensename", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("name", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
