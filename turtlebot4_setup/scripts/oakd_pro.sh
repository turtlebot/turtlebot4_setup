#!/usr/bin/env bash
sudo apt install libopencv-dev
cd src
mkdir luxonis
cd luxonis
git clone https://github.com/luxonis/depthai-ros.git -b main
git clone https://github.com/luxonis/depthai-ros-examples.git -b main
