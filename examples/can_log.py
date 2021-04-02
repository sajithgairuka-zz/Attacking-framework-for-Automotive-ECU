import sys
import os
import socket
import time
import struct

sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
interface = "vcan0"

try:
    sock.bind((interface,))
    can_frame = "<LB3x8s"

    with open("can_dump_python.log", 'w') as outfile:
        while True:
            can_pack = sock.recv(16)
            can_id, can_dlc, can_data = struct.unpack(can_frame, can_pack)
            can_extended_frame = bool(can_id & socket.CAN_EFF_FLAG)
            if can_extended_frame:
                can_id &= socket.CAN_EFF_MASK
                can_id_str = "{:08X}".format(can_id)
            else:
                can_id &= socket.CAN_SFF_MASK
                can_id_str = "{:03X}".format(can_id)
            can_data_strings = ' '.join(["{:02X}".format(b) for b in can_data[:can_dlc]])
            print("{} {} [{}] {}".format(interface, can_id_str, can_dlc, can_data_strings))
            outfile.write("({:12.6f}) {} {}#{}\n".format(time.time(),interface, can_id_str, can_data_strings.replace(" ","")))

except KeyboardInterrupt:
    print("\n log save as:can_dump_python.log ")
