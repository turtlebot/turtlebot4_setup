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

while getopts "m:c:h" flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        h)
            Help
            exit;;
        \?)
            echo "Error: Invalid flag"
            exit;;
    esac
done

# Check that the model is valid
if [ -z $model ]
then
    model="standard";
else
    if [ $model != "standard" ] && [ $model != "lite" ]
    then
        echo "Invalid model";
        exit 1
    fi
fi

echo "Setting up Turtlebot4 $model";

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SETUP_DIR=${SCRIPT_DIR%/*}

# Install ROS2 Galactic
bash $SCRIPT_DIR/galactic.sh
source /opt/ros/galactic/setup.bash

# Install packages
sudo apt install -y \
network-manager \
daemontools \
chrony \
socat \
ros-galactic-robot-upstart \
ros-galactic-turtlebot4-robot \
ros-galactic-irobot-create-control \
ros-galactic-rmw-fastrtps-cpp

# Copy udev rules
sudo cp $SETUP_DIR/udev/turtlebot4.rules /etc/udev/rules.d/

# Copy chrony config
sudo cp $SETUP_DIR/conf/chrony.conf /etc/chrony/

# Restart chrony
sudo service chrony restart

# Copy webserver service
sudo cp $SETUP_DIR/conf/webserver.service /etc/systemd/system/

# Enable webserver service to run from boot
sudo systemctl enable webserver.service

# Enable usb0
echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/usercfg.txt
sudo sed -i '${s/$/ modules-load=dwc2,g_ether/}' /boot/firmware/cmdline.txt

# Enable i2c-3
echo "dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/firmware/usercfg.txt 

# Source galactic setup in bashrc
echo "source /opt/ros/galactic/setup.bash" | sudo tee -a ~/.bashrc

# Configure cyclonedds
sudo cp $SETUP_DIR/conf/cyclonedds_rpi.xml /etc/
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" | sudo tee -a ~/.bashrc
echo "export CYCLONEDDS_URI=/etc/cyclonedds_rpi.xml" | sudo tee -a ~/.bashrc

# Copy discovery server files
sudo cp $SETUP_DIR/conf/discovery.conf /etc/
sudo cp $SETUP_DIR/scripts/discovery.sh /etc/

# Set ROS_DOMAIN_ID
echo "export ROS_DOMAIN_ID=0" | sudo tee -a ~/.bashrc

# Robot upstart
$SCRIPT_DIR/install.py $model

sudo systemctl daemon-reload

# Copy scripts to local bin
sudo cp $SCRIPT_DIR/wifi.sh \
        $SCRIPT_DIR/create_update_0.4.0.sh \
        $SCRIPT_DIR/create_update.sh \
        $SCRIPT_DIR/ros_config.sh \
        $SCRIPT_DIR/swap_on.sh \
        $SCRIPT_DIR/swap_off.sh \
        $SCRIPT_DIR/bluetooth.sh \
        $SCRIPT_DIR/install.py \
        $SCRIPT_DIR/uninstall.py /usr/local/bin

# Set image information
sudo touch /etc/turtlebot4
echo "TurtleBot 4 $model v0.1.4" | sudo tee /etc/turtlebot4

echo "Installation complete, press enter to reboot in AP mode."

sudo $SETUP_DIR/scripts/wifi.sh -a && sudo reboot
