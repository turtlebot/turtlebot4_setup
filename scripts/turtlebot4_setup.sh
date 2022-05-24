#!/usr/bin/env bash

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
ros-galactic-robot-upstart \
chrony \
ros-galactic-turtlebot4-robot \
ros-galactic-irobot-create-control

# Copy udev rules
sudo cp $SETUP_DIR/udev/turtlebot4.rules /etc/udev/rules.d/

# Copy chrony config
sudo cp $SETUP_DIR/conf/chrony.conf /etc/chrony/

# Restart chrony
sudo service chrony restart

# Enable usb0
echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/usercfg.txt
sudo sed -i '${s/$/ modules-load=dwc2,g_ether/}' /boot/firmware/cmdline.txt

# Enable i2c-3
echo "dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/firmware/usercfg.txt 

# Configure cyclonedds
sudo cp $SETUP_DIR/conf/cyclonedds_rpi.xml /etc/
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" | sudo tee -a ~/.bashrc
echo "export CYCLONEDDS_URI=/etc/cyclonedds_rpi.xml" | sudo tee -a ~/.bashrc

# Source galactic setup in bashrc
echo "source /opt/ros/galactic/setup.bash" | sudo tee -a ~/.bashrc

# Robot upstart

ros2 run robot_upstart install turtlebot4_bringup/launch/$model.launch.py --job turtlebot4 \
                                                                          --rmw rmw_cyclonedds_cpp \
                                                                          --rmw_config /etc/cyclonedds_rpi.xml \
                                                                          --setup /opt/ros/galactic/setup.bash

sudo systemctl daemon-reload

# Copy scripts to local bin
sudo cp $SETUP_DIR/scripts/wifi.sh \
        $SETUP_DIR/scripts/create_update_0.4.0.sh \
        $SETUP_DIR/scripts/create_update.sh \
        $SETUP_DIR/scripts/swap_on.sh \
        $SETUP_DIR/scripts/swap_off.sh \
        $SETUP_DIR/scripts/bluetooth.sh /usr/local/bin

echo "Installation complete, press enter to reboot in AP mode."

sudo $SETUP_DIR/scripts/wifi.sh -a && sudo reboot
