#!/usr/bin/env bash

# Flags:
# -m Turtlebot4 Model (lite, standard)
# -c OAK-D Camera Model (lite, pro)

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

# Install source packages
cd src
git clone https://github.com/turtlebot/turtlebot4.git
git clone https://github.com/turtlebot/turtlebot4_robot.git
cd ..
vcs import src < $SETUP_DIR/turtlebot4_packages.repos

# Install additional packages
sudo apt install -y \
libgpiod-dev \
network-manager \
daemontools 

# Install bluetooth packages
bash $SCRIPT_DIR/bluetooth.sh
# Install OAK-D drivers
bash $SCRIPT_DIR/oakd.sh

# Run rosdep
sudo rosdep init
rosdep update
rosdep install -r --from-paths src -i -y --rosdistro galactic

# Add swap memory and build packages
sudo bash $SCRIPT_DIR/swap_on.sh
colcon build --symlink-install
source install/setup.bash
sudo bash $SCRIPT_DIR/swap_off.sh

# Copy udev rules
sudo cp $SETUP_DIR/udev/turtlebot4.rules /etc/udev/rules.d/

# Enable usb0
echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/usercfg.txt
sudo sed -i '${s/$/ modules-load=dwc2,g_ether/}' /boot/firmware/cmdline.txt

# Enable i2c-3
echo "dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/firmware/usercfg.txt 

# Configure cyclonedds
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" | sudo tee -a ~/.bashrc
echo "export CYCLONEDDS_URI='<CycloneDDS><Domain><General><NetworkInterfaceAddress>wlan0,usb0</></></></>'" | sudo tee -a ~/.bashrc

# Robot upstart

ros2 run robot_upstart install turtlebot4_bringup/launch/$model.launch.py --job turtlebot4

sudo systemctl daemon-reload

# Copy Wifi and Create 3 Update scripts to local bin
chmod +x $SETUP_DIR/scripts/wifi.sh
sudo cp $SETUP_DIR/scripts/wifi.sh /usr/local/bin

chmod +x $SETUP_DIR/scripts/create_update.sh
sudo cp $SETUP_DIR/scripts/create_update.sh /usr/local/bin

read -p "Installation complete, press enter to reboot."

sudo reboot
