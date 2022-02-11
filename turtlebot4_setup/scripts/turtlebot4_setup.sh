#!/usr/bin/env bash

# Flags:
# -m Turtlebot4 Model (lite, standard)
# -c OAK-D Camera Model (lite, pro)

Help()
{
   echo "Turtlebot4 Setup script. To be called from the workspace directory."
   echo
   echo "usage: sudo bash turtlebot4_setup.sh [-m] [value] [-c] [value] [-h]"
   echo "options:"
   echo " m     Turtlebot4 Model (lite, standard). Defaults to standard"
   echo " c     OAK-D Camera Model (lite, pro). Defaults to the models default camera."
   echo " h     Print this help statement"
   echo
}

while getopts "m:c:h" flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        c) camera=${OPTARG};;
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

# Check that the camera is valid
if [ -z $camera ]
then
    if [ $model = "standard" ]
    then 
        camera="pro";
    else
        camera="lite";
    fi
else
    if [ $camera != "pro" ] && [ $camera != "lite" ]
    then
        echo "Invalid camera";
        exit 1
    fi
fi

echo "Setting up Turtlebot4 $model with OAK-D $camera";

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SETUP_DIR=${SCRIPT_DIR%/*}

# Install ROS2 Galactic
bash $SCRIPT_DIR/galactic.sh
source /opt/ros/galactic/setup.bash

# Install source packages
vcs import src < $SETUP_DIR/turtlebot4_packages.repos

# Install additional packages
sudo apt install -y \
libgpiod-dev \
network-manager \
daemontools 

# Install bluetooth packages
if [ $model = "standard"]
then
    bash $SCRIPT_DIR/bluetooth.sh
fi

# Install the correct camera
if [ $camera = "pro" ]
then
    sudo bash $SCRIPT_DIR/oakd_pro_dependencies.sh
    bash $SCRIPT_DIR/oakd_pro.sh
else
    bash $SCRIPT_DIR/oakd_lite.sh
fi

sudo rosdep init
rosdep update
rosdep install -r --from-paths src -i -y --rosdistro galactic
colcon build
source install/setup.bash

# Copy udev rules
sudo cp $SETUP_DIR/udev/turtlebot4.rules /etc/udev/rules.d/

# Enable usb0
echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/usercfg.txt
sudo sed -i '${s/$/ modules-load=dwc2,g_ether/}' /boot/firmware/cmdline.txt

# Enable i2c-3
echo "dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/firmware/usercfg.txt 

# Configure cyclonedds
echo "export CYCLONEDDS_URI='<CycloneDDS><Domain><General><NetworkInterfaceAddress>wlan0,usb0</></></></>'" | sudo tee -a ~/.bashrc

# Robot upstart

ros2 run robot_upstart install turtlebot4_bringup/launch/$model.launch.py --job turtlebot4

sudo systemctl daemon-reload

echo "Installation complete, restart required";