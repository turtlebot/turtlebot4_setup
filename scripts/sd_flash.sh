#!/usr/bin/env bash

# Flags:
# -h Help

Help()
{
   echo "RPI4 SD card flash script. Supports flashing multiple cards simultaneously."
   echo
   echo "usage: sudo bash sd_flash.sh /path/to/image.img [-h]"
   echo "options:"
   echo " -h     Print this help statement"
   echo
}

while getopts "h" flag
do
    case "${flag}" in
        h)
            Help
            exit;;
        \?)
            echo "Error: Invalid flag"
            exit;;
    esac
done

echo "Image path: $1";

read -p "Enter each SD card device name separated with a space (i.e. sda sdb sdc): " device_names

read -p "The SD card(s) will be unmounted and flashed. Press enter to continue."

for device in $device_names
do
    of="$of of=/dev/$device"
    sudo umount /dev/$device*
done

sudo dcfldd if=$1 sizeprobe=if bs=1M$of

for device in $device_names
do
    sudo growpart /dev/$device 2
    sudo resize2fs /dev/${device}p2
done