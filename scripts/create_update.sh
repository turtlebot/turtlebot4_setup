#!/usr/bin/env bash

# Flags:
# -h Help

Help()
{
   echo "Create 3 update script for robots running G.2.1 or higher"
   echo
   echo "usage: bash create_update.sh /path/to/image.swu [-h]"
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

curl -X POST --data-binary @$1 http://192.168.186.2/api/firmware-update
