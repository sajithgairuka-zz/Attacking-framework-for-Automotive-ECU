import time
import socket
import struct
import sys
import os
from lib.interface import DEFAULT_INTERFACE

sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW) #crating socket
sock.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_ERR_FILTER, socket.CAN_ERR_MASK)#allow socket to receive error frames

interface = DEFAULT_INTERFACE

try:
    sock.bind((interface,))

except socket.error as e:
    print(str(e))
    print("\n--------------------------------------------------------------------------------")

#The basic CAN frame structure and the sockaddr structure are defined in include/linux/can.h
can_frame_format = "<LB3x8s"

try:
    while True:
        can_pack = sock.recv(16)
        can_id, can_dlc, can_data = struct.unpack(can_frame_format, can_pack)

        can_extended_frame = bool(can_id & socket.CAN_EFF_FLAG)
        can_error_frame = bool(can_id & socket.CAN_ERR_FLAG)
        remote_tx_req_frame = bool(can_id & socket.CAN_RTR_FLAG)

        if can_error_frame:
            can_id &= socket.CAN_ERR_MASK
            can_id_str = "{:08X} (ERROR)".format(can_id)

        else: #Data Frame
            if can_extended_frame:
                can_id &= socket.CAN_EFF_MASK
                can_id_str = "{:08X}".format(can_id)

            else: #Standard Frame
                can_id &= socket.CAN_SFF_MASK
                can_id_str = "{:03X}".format(can_id)

        if remote_tx_req_frame:
            can_id_str = "{:08X} (RTR)".format(can_id)

        can_data_strings = ' '.join(["{:02X}".format(can_byte) for can_byte in can_data])
        print("{:12.6f} {} [{}] {}".format(time.time(), can_id_str, can_dlc, can_data_strings))

except KeyboardInterrupt:
    print("\n packet capture stoped! ")
