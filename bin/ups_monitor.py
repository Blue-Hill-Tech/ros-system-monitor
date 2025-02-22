#!/usr/bin/env python3
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

import sys
import rospy
import subprocess

import time

NAME = 'ups_monitor'

def ups_monitor():
    pub = rospy.Publisher("/diagnostics", DiagnosticArray, queue_size = 100)
    rospy.init_node(NAME, anonymous=True)

    while not rospy.is_shutdown():
        try:
            percentage_response = subprocess.check_output(["upower -i $(upower -e | grep 'ups') | grep -E \"percentage\""], shell=True)
            state_response = subprocess.check_output(["upower -i $(upower -e | grep 'ups') | grep -E \"state\""], shell=True)
        except subprocess.CalledProcessError as e:
            print("No UPS info obtained. Exiting...")
            sys.exit(0)
        percentage = float(percentage_response.decode("utf-8").replace('\n','').replace(' ', '').split(":")[1].strip('%'))
        state = state_response.decode("utf-8").replace('\n','').replace(' ', '').split(":")[1]
        bat_stat = DiagnosticStatus()
        bat_stat.name = "UPS Usage"
        bat_stat.values = [KeyValue(key = 'UPS Percentage', value = str(percentage)),
                           KeyValue(key = 'UPS State', value = state)]

        msg = DiagnosticArray()
        msg.header.stamp = rospy.get_rostime()
        msg.status = [bat_stat]
        pub.publish(msg)
        time.sleep(5)

def ups_monitor_main():
    ups_monitor()


if __name__ == "__main__":
    try:
        ups_monitor_main()
    except KeyboardInterrupt: pass
    except SystemExit: pass
    except:
        import traceback
        traceback.print_exc()
