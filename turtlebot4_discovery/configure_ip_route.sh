#!/bin/bash

read -p "RPi4 IP address: " ip

echo "Configuring IP route for $ip";

# Make directory to hold configs
sudo mkdir -p /etc/turtlebot4_discovery/

# Clone turtlebot4_setup and install files
git clone -b humble https://github.com/turtlebot/turtlebot4_setup.git /tmp/turtlebot4_setup/
sudo mv /tmp/turtlebot4_setup/turtlebot4_discovery/ip_route.sh /usr/local/sbin/
sudo mv /tmp/turtlebot4_setup/turtlebot4_discovery/ip_route.service /etc/systemd/system/
sudo mv /tmp/turtlebot4_setup/turtlebot4_discovery/fastdds_discovery_super_client.xml /etc/turtlebot4_discovery/
sudo mv /tmp/turtlebot4_setup/turtlebot4_discovery/setup.bash /etc/turtlebot4_discovery/
rm /tmp/turtlebot4_setup/ -rf

# Modify IP address
sudo sed -i "s/10.42.0.1/$ip/g" /usr/local/sbin/ip_route.sh
sudo sed -i "s/10.42.0.1/$ip/g" /etc/turtlebot4_discovery/fastdds_discovery_super_client.xml
sudo sed -i "s/10.42.0.1/$ip/g" /etc/turtlebot4_discovery/setup.bash

# Source setup.bash in .bashrc
echo 'source /etc/turtlebot4_discovery/setup.bash' >> ~/.bashrc

# Enable and start IP route service
sudo systemctl enable ip_route.service
sudo systemctl start ip_route.service