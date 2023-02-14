#!/usr/bin/env bash

# Copyright 2022 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

# Flags:
# -m Turtlebot4 Model (lite, standard)

Help()
{
   echo "Turtlebot4 Setup script. To be called from the workspace directory."
   echo
   echo "usage: sudo bash turtlebot4_setup.sh [-m] [value] [-h]"
   echo "options:"
   echo " m     Turtlebot4 Model (lite, standard). Defaults to standard"
   echo " h     Print this help statement"
   echo
}


echo "Setting up Turtlebot4 $model";

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SETUP_DIR=${SCRIPT_DIR%/*}

sudo apt update && sudo apt upgrade
sudo apt install software-properties-common curl
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2-testing/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update && sudo apt upgrade
sudo apt install -y ros-humble-ros-base ros-dev-tools socat network-manager chrony
#sudo apt install -y ros-humble-turtlebot4-setup ros-humble-turtlebot4-robot
sudo rm /etc/netplan/50-cloud-init.yaml
git clone https://github.com/turtlebot/turtlebot4_setup.git -b humble && \
sudo mv turtlebot4_setup/boot/firmware/* /boot/firmware && rm turtlebot4_setup/ -rf
sudo sed -i "s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g" /etc/sysctl.conf

echo "source /etc/turtlebot4/setup.bash" | sudo tee -a ~/.bashrc
echo "source /etc/turtlebot4/aliases.bash" | sudo tee -a ~/.bashrc

echo "Installation complete, press enter to reboot in AP mode."

