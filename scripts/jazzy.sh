#!/usr/bin/env bash
sudo apt update && sudo apt install curl gnupg lsb-release -y

# Add ROS sources
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install the packages
sudo apt update
sudo apt install -y \
ros-jazzy-ros-base \
build-essential \
cmake \
git \
wget \
ros-dev-tools \
socat \
network-manager \
chrony
