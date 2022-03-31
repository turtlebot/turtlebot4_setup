#!/usr/bin/env bash

# Flags:
# -h Help

Help()
{
   echo "Create 3 update script for robots running 0.4.0"
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

curl -F fileupload=@$1 http://192.168.186.2/cgi-bin/update.sh
