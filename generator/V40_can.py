#!/usr/bin/env python3

import socket
import struct
import sys
import time

numbers = {
    '1' : b'\x44',
    '2' : b'\x48',
    '3' : b'\x4C',
    '4' : b'\x50',
    '5' : b'\x54',
    '6' : b'\x58',
    '7' : b'\x5C',
    '8' : b'\x60',
    '9' : b'\x64',
    '*' : b'\x68',
    '0' : b'\x40',
    '#' : b'\x6C',
}

menus = {
    'T' : b'\x90', # telephone
    'M' : b'\x84', # media
    'R' : b'\x82', # radio
    'S' : b'\xA0', # my car (settings)
}

# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

def print_help():
    print("Use numbers, # or *.")
    print("Radio : R\nMedia : M\nSettings : S\nTelephone : T")
    print("OK : O\nExit : E")

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def send_number(number):
    byte = numbers[number]
    s.send(build_can_frame(0x1A0, byte + b'\xF8\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.09)
    s.send(build_can_frame(0x1A0, b'\x7C\xF8\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.18)

def send_menu(menu):
    byte = menus[menu]
    s.send(build_can_frame(0x220, b'\x0A\x36\x67\xC4' + byte + b'\x00\xA8\x00'))
    time.sleep(0.1)
    s.send(build_can_frame(0x220, b'\x0A\x36\x67\xC4\x80\x00\xA7\x00'))
    time.sleep(0.2)

def send_ok():
    s.send(build_can_frame(0x1A0, b'\x3C\x3A\xC0\x00\x16\x16\x00\xA0'))
    time.sleep(0.09)
    s.send(build_can_frame(0x1A0, b'\x3C\x38\xC0\x00\x16\x16\x00\xA0'))
    time.sleep(0.09)
    s.send(build_can_frame(0x1A0, b'\x3C\x3A\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.18)

def send_exit():
    s.send(build_can_frame(0x1A0, b'\x3E\x3C\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.09)
    s.send(build_can_frame(0x1A0, b'\x3E\x38\xC0\x00\x16\x16\x00\x20'))
    time.sleep(0.18)

CAN_IF = 'can0'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Provide commandstring')
        print_help()
        sys.exit(0)
    # create a raw socket and bind it to the given CAN interface
    s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((CAN_IF,))

    for button in sys.argv[1]:
        if button in menus:
            send_menu(button)
        elif button in numbers:
            send_number(button)
        elif button == 'O':
            send_ok()
        elif button == 'E':
            send_exit()

