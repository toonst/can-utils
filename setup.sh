#!/bin/bash

function get_iface {
    ifconfig $1 | sed 's/[ \t].*//;/^$/d' | grep can
}

if [ $# -ne 0 ]; then
    BITRATE=$1
else
    BITRATE=500000
fi

# check if can kernel module is loaded
if ! lsmod | grep '^can ' > /dev/null 2>&1; then
    echo "Loading can kernel module..."
    modprobe can
fi

# check if ISO-TP kernel module is loaded
if ! lsmod | grep '^can_isotp ' > /dev/null 2>&1; then
    echo "Loading iso-tp kernel module..."
    insmod can-isotp.ko
fi

# check if interface exists
if ! IFACE=$(get_iface -a); then
    echo "No can interface found. Is the USB interface plugged in?"
    exit 1
else
    echo "Found interface $iface"
fi

# check if iface is already up
if get_iface > /dev/null 2>&1; then
    echo "Already up"
    exit 0
else
    echo "Seting up..."
fi

# configure restart
sudo ip link set $IFACE type can restart-ms 100

# configure baudrate
sudo ip link set $IFACE up type can bitrate $BITRATE

echo "Finished"

