#!/usr/bin/env python3

import socket
import struct
import sys
import time

buttons = {
    '1':b'\x44',
    '2':b'\x48',
    '3':b'\x4C',
    '4':b'\x50',
    '5':b'\x54',
    '6':b'\x58',
    '7':b'\x5C',
    '8':b'\x60',
    '9':b'\x64',
    '*':b'\x68',
    '0':b'\x40',
    '#':b'\x6C',
}

# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def send_button(button):
    byte = buttons[button]
    s.send(build_can_frame(0x1A0, byte + b'\xF8\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.4)
    s.send(build_can_frame(0x1A0, b'\x7C\xF8\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.01)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Provide CAN device name (can0, slcan0 etc.)')
        sys.exit(0)
    # create a raw socket and bind it to the given CAN interface
    s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((sys.argv[1],))

    for i in range(9,1,-1):
        send_button(str(i))

