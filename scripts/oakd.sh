#!/usr/bin/env bash
sudo wget -qO- https://raw.githubusercontent.com/luxonis/depthai-ros/main/install_dependencies.sh | sudo bash
sudo apt install libopencv-dev
cd src
mkdir luxonis
cd luxonis
git clone https://github.com/luxonis/depthai-ros.git -b main
git clone https://github.com/luxonis/depthai-ros-examples.git -b devel
