import sys
import os
import socket
import struct
import time
from lib.interface import DEFAULT_INTERFACE

# Open a socket and bind to it from SocketCAN
sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
interface = DEFAULT_INTERFACE

# Bind to the interface
sock.bind((interface,))

# To match this data structure, the following struct format can be used:
can_frame_format = "<LB3x8s"

with open("candump_python.log", 'w') as outfile:
    while True:
        can_packet = sock.recv(16)
        can_id, can_dlc, can_data = struct.unpack(can_frame_format, can_packet)
        extended_frame = bool(can_id & socket.CAN_EFF_FLAG)
        if extended_frame:
            can_id &= socket.CAN_EFF_MASK
            can_id_string = "{:08X}".format(can_id)
        else: #Standard Frame
            can_id &= socket.CAN_SFF_MASK
            can_id_string = "{:03X}".format(can_id)
        hex_data_string = ' '.join(["{:02X}".format(b) for b in can_data[:can_dlc]])
        print("{} {} [{}] {}".format(interface, can_id_string, can_dlc, hex_data_string))
        outfile.write("({:12.6f}) {} {}#{}\n".format(time.time(),interface, can_id_string, hex_data_string.replace(" ","")))
