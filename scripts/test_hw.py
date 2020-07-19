#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String, Bool
from custom_msgs.msg import ActuatorControl

import threading
import Queue
import time
import readchar

def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')    
    while (True):
        input_char = readchar.readchar()
        inputQueue.put(input_char)
        if(input_char == "q"):
            break
        
def talker():
    cmd_pub = rospy.Publisher('/hw/manual_cmd', ActuatorControl, queue_size=10)
    cmd_type_pub = rospy.Publisher('/autonomous_driver', Bool, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    
    inputQueue = Queue.Queue()
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,))
    inputThread.start()
    
    rate = rospy.Rate(20) # 10hz
    ctrl = ActuatorControl()
    ctrl.dc = 0
    ctrl.delta = 0
    
    while not rospy.is_shutdown():
        cmd_type_pub.publish(False)
        
        if (inputQueue.qsize() > 0):
            input_ch = inputQueue.get()
            if(input_ch == "w"):
				ctrl.dc += 0.02
            if(input_ch == "s"):
				ctrl.dc -= 0.02
            if(input_ch == "a"):
				ctrl.delta += 0.1
            if(input_ch == "d"):
				ctrl.delta -= 0.1
            if(input_ch == " "):
                ctrl.dc = 0
                ctrl.delta = 0
            if(input_ch == "q"):
				break
        print("\r {:4f} {:4f}".format(ctrl.dc, ctrl.delta))
        ctrl.stamp = rospy.Time.now()       
        cmd_pub.publish(ctrl)
        rate.sleep()
    inputThread.join()
    print("End.")

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
