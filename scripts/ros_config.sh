#!/usr/bin/env bash

# Flags:
# -h Help

Help()
{
   echo "TurtleBot 4 ROS configuration"
   echo
   echo "usage: sudo bash ros_config.sh [-h]"
   echo "options:"
   echo " -h     Print this help statement"
   echo
}

while getopts "h" flag
do
    case "${flag}" in
        h)
            Help
            exit;;
        \?)
            echo "Error: Invalid flag"
            exit;;
    esac
done

read -p "ROS_DOMAIN_ID (default 0): " ros_domain_id
ros_domain_id=${ros_domain_id:-0}
#read -p "ROS namespace (default empty): " namespace
read -p "RMW Implementation [rmw_cyclonedds_cpp,rmw_fastrtps_cpp] (default rmw_fastrtps_cpp): " rmw
rmw=${rmw:-rmw_fastrtps_cpp}

echo "ROS_DOMAIN_ID: $ros_domain_id";
#echo "Namespace: $namespace";
echo "RMW_IMPLEMENTATION: $rmw";
read -p "Press enter to apply these settings."

ttb4=$( cat /etc/turtlebot4 )

model="standard"

case $ttb4 in
    *"lite"*)
    model="lite";;
esac

# Set Create 3 configuration
curl -d "ros_domain_id=$ros_domain_id&ros_namespace=&rmw_implementation=$rmw" -X POST http://192.168.186.2/ros-config-save-main -o /dev/null

# Reboot Create 3
curl -X POST http://192.168.186.2/api/reboot

# Stop running turtlebot4 service
sudo systemctl stop turtlebot4.service

# Uninstall robot_upstart job
uninstall.py

# Install robot_upstart job with new ROS_DOMAIN_ID
install.py $model --domain $ros_domain_id --rmw $rmw

# Start job
sudo systemctl daemon-reload && sudo systemctl start turtlebot4

# Add settings to .bashrc
if grep -Fq "export RMW_IMPLEMENTATION=" ~/.bashrc
then
    sudo sed -i "s/export RMW_IMPLEMENTATION=.*/export RMW_IMPLEMENTATION=$rmw/g" ~/.bashrc
else
    echo "export RMW_IMPLEMENTATION=$rmw" | sudo tee -a ~/.bashrc
fi

if grep -Fq "export ROS_DOMAIN_ID=" ~/.bashrc
then
    sudo sed -i "s/export ROS_DOMAIN_ID=.*/export ROS_DOMAIN_ID=$ros_domain_id/g" ~/.bashrc
else
    echo "export ROS_DOMAIN_ID=$ros_domain_id" | sudo tee -a ~/.bashrc
fi

echo "Source ~/.bashrc to apply these changes to this terminal."