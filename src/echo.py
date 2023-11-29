#!/usr/bin/python3 -u
import time
import numpy as np
import json
import socket
import sys

from ws_client import *
from task import *

def test_telemetry_udp(address: str, subscriber_addr: str, subscriber_port: int, echo_time):
    print("Testing Telemtry_UDP module...")
    print("subscribe to Telemetry_UDP with finger_width and joint position ...")
    result_1 = call_method(address, 12000, "subscribe_telemetry",
                           {"ip": subscriber_addr, "port": subscriber_port, "subscribe": ["q", "finger_width"]},silent=False, timeout=7)
    if result_1["result"]["result"]:
        print("successfull subscribed.")
    else:
        print("Error while subscribing: ", result_1)
    print("receiving subscribed telemetry packages for next " + str(echo_time) +  " seconds...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((subscriber_addr, subscriber_port))
    cnt = 0
    received_pkgs = []
    start_time = time.time()
    try:
        print("\n    --Interrupt with ctrl+c--\n")
        while True:
            data, adrr = s.recvfrom(8192)
            received_pkgs.append(json.loads(data.decode("utf-8")))
            cnt += 1
            print(data)
            if time.time() - start_time > echo_time:
                break
    except KeyboardInterrupt:
        pass
    end_time = time.time()
    print("received ", cnt, " packages over last", end_time - start_time, " seconds")
    pkg_validation_cnt = 0
    for pkg in received_pkgs:
        if pkg.get("tau_ext", False) != False and pkg.get("q", False) != False:
            pkg_validation_cnt += 1
    print(cnt - pkg_validation_cnt, " package(s) are corrupted.")
    print("unsubscribe...")
    result_2 = call_method(address, 12000, "unsubscribe_telemetry", {"ip": subscriber_addr})
    if result_2["result"]["result"]:
        print("successfull unsibscribed.")
    if cnt < 1:
        print("Received no package. Test failed!")
    elif result_1["result"]["result"] and cnt - pkg_validation_cnt == 0 and result_2["result"]["result"]:
        print("\nEverything works fine :)")
    else:
        print("\nTest failed!")


def main() -> int:
    """Echo the input arguments to standard output"""
    sender = "localhost"
    receiver = "localhost" # IP address of your PC
    echo_time = 10
    test_telemetry_udp(sender, receiver, 8888, echo_time)
    return 0

# if __name__ == '__main__':
#     sys.exit(main())

def send_start():
    result_1 = call_method("localhost", 12000, "subscribe_telemetry",
                           {"ip": "localhost", "port": 8888, "subscribe": ["K_F_ext_K"]},silent=False, timeout=7)
    
def send_off():
    result_2 = call_method("localhost", 12000, "unsubscribe_telemetry", {"ip": "localhost"})
    
def null_skill(x):
    context = {
        "skill":{
            "t_max":x
        },
        "control":{
            "control_mode":1
        }
    }
    t = Task("localhost")
    t.add_skill("Hold", "HoldPose", context)
    t.start()