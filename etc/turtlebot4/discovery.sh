#!/bin/bash
source /opt/ros/humble/setup.bash
fastdds discovery -i 0 -l 127.0.0.1 -p 11811
