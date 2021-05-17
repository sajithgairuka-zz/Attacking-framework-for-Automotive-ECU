import socket
import struct
import sys
import os
import time
import argparse
from lib.interface import DEFAULT_INTERFACE
from lib.time import DEFAULT_TIME


def can_moniter():
    sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW) #crating socket
    sock.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_ERR_FILTER, socket.CAN_ERR_MASK)#allow socket to receive error frames
    interface = DEFAULT_INTERFACE

    try:
        sock.bind((interface,))

    except socket.error as e:
        print(str(e))
        print("\n-------------------------------------------------------------------------------")

    can_frame_format = "<LB3x8s"

    with open("can-id.txt", 'a') as outfile:
        while True :
            can_packet = sock.recv(16)
            can_id, can_dlc, can_data = struct.unpack(can_frame_format, can_packet)

            extended_frame = bool(can_id & socket.CAN_EFF_FLAG)
            error_frame = bool(can_id & socket.CAN_ERR_FLAG)
            remote_tx_req_frame = bool(can_id & socket.CAN_RTR_FLAG)

            if error_frame:
                can_id &= socket.CAN_ERR_MASK
                can_id_string = "{:08X} (ERROR)".format(can_id)
            else: #Data Frame
                if extended_frame:
                    can_id &= socket.CAN_EFF_MASK
                    can_id_string = "{:08X}".format(can_id)
                else: #Standard Frame
                    can_id &= socket.CAN_SFF_MASK
                    can_id_string = "{:03X}".format(can_id)

            if remote_tx_req_frame:
                can_id_string = "{:08X} (RTR)".format(can_id)

            hex_data_string = ' '.join(["{:02X}".format(b) for b in can_data[:can_dlc]])
            outfile.write("{}#{}\n".format(can_id_string, can_dlc))
            #outfile.write("{}#{}\n".format(can_id_string, hex_data_string.replace(" ","")))
            return False

def rm_duplic():
    lines_seen = set() # holds lines already seen
    outfile = open("results/outfilename.txt", "w")
    for line in open("results/can-id.txt", "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

def file_sort():
    sortf = open("results/sort.txt", "w")
    with open("results/outfilename.txt", "r") as r:
        for line in sorted(r):
            sortf.write(line)
        sortf.close()

def cap_time():
    if DEFAULT_TIME:
         now=time.time()
         timer = 0
         while timer != DEFAULT_TIME:
             can_moniter()
             end = time.time()
             timer = round(end-now)
             #print(end)
             mins, secs = divmod(timer, 60)
             count = '{:02d}:{:02d}'.format(mins, secs)
             print(count,end="\r")

cap_time()
rm_duplic()
file_sort()
