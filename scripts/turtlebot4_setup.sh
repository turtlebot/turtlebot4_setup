#!/usr/bin/env bash

# Copyright 2023 Clearpath Robotics, Inc.
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


Help()
{
   echo "Turtlebot4 Setup script."
   echo
   echo "usage: sudo bash turtlebot4_setup.sh [-h]"
   echo "options:"
   echo " h     Print this help statement"
   echo
}

echo "Setting up Turtlebot4";

sudo apt update && sudo apt upgrade

wget -qO - https://raw.githubusercontent.com/turtlebot/turtlebot4_setup/humble/scripts/humble.sh | bash

sudo apt update && sudo apt upgrade

sudo apt install -y ros-humble-ros-base \
ros-humble-turtlebot4-setup \
ros-humble-turtlebot4-robot \
ros-humble-irobot-create-control \
ros-humble-turtlebot4-navigation \
ros-dev-tools \
socat \
network-manager \
chrony

sudo rm /etc/netplan/50-cloud-init.yaml

git clone https://github.com/turtlebot/turtlebot4_setup.git -b humble && \
sudo mv turtlebot4_setup/boot/firmware/* /boot/firmware && rm turtlebot4_setup/ -rf

echo "export ROBOT_SETUP=/etc/turtlebot4/setup.bash" | sudo tee -a ~/.bashrc
echo "source \$ROBOT_SETUP" | sudo tee -a ~/.bashrc
echo "source /etc/turtlebot4/aliases.bash" | sudo tee -a ~/.bashrc

echo "Installation complete. Reboot then run turtlebot4-setup to configure the robot."
