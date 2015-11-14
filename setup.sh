#!/bin/bash

if [ $# -ne 0 ]
then
    BITRATE=$1
else
    BITRATE=500000
fi

# set the bitrate 
sudo ip link set can0 type can bitrate $BITRATE

# automatically recover from bus-off state
sudo ip link set can0 type can restart-ms 100

# set the interface up
sudo ip link set can0 up
