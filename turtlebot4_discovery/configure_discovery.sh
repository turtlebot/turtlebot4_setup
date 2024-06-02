#!/bin/bash

prompt_YESno() {
  # as the user a Y/n question
  # $1 is the variable into which the answer is saved as either "n" or "y"
  # $2 is the question to ask

  local __resultvar=$1
  local __prompt=$2

  echo -e "\e[39m$__prompt\e[0m"
  echo "Y/n: "

  if [[ $AUTO_YES == 1 ]];
  then
    echo "Automatically answering Yes"
    eval $__resultvar="y"
  else
    read answer
    if [[ $answer =~ ^[n,N].* ]];
    then
      eval $__resultvar="n"
    else
      eval $__resultvar="y"
    fi
  fi
}

read -p "Discovery Server IP [$ip]: " discovery_ip
discovery_ip=${discovery_ip:-$ip}

read -p "Discovery Server ID [0]: " discovery_server_id
discovery_server_id=${discovery_server_id:-0}

read -p "Discovery Server Port [11811]: " discovery_port
discovery_port=${discovery_port:-11811}

read -p "ROS_DOMAIN_ID [0]: " domain_id
domain_id=${domain_id:-0}

discovery_str=""
for i in {0..{$discovery_server_id}}
do
    discovery_str="${discovery_str};"
done
discovery_str="${discovery_str}${discovery_ip}:${discovery_port}"

echo "Configuring:"
echo " ROS_DISCOVERY_SERVER=\"$discovery_str\""
echo " ROS_DOMAIN_ID=$domain_id"

# Make directory to hold configs
sudo mkdir -p /etc/turtlebot4_discovery/

# Create setup.bash file
setup_file_temp="/tmp/turtlebot4_discovery_setup.bash"
echo "source /opt/ros/humble/setup.bash" > $setup_file_temp
echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> $setup_file_temp
echo "[ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False" >> $setup_file_temp

# Add user configured data to setup.bash
echo "export ROS_DISCOVERY_SERVER=\"$discovery_str\"" >> $setup_file_temp
echo "export ROS_DOMAIN_ID=$domain_id" >> $setup_file_temp

# Move setup.bash into final location
setup_file="/etc/turtlebot4_discovery/setup.bash"
sudo mv $setup_file_temp $setup_file

# Source setup.bash in .bashrc
if ! grep -Fq "source $setup_file" ~/.bashrc
then
    echo "source $setup_file" >> ~/.bashrc
fi

if [ -f "/usr/local/sbin/ip_route.sh" ]||[ -f "/etc/systemd/system/ip_route.service" ];
then
    prompt_YESno cleanup "\Would you like to clean up the outdated IP route? This is no longer required as of turtlebot4_robot version 1.0.3.\e[0m"
    if [[ $cleanup == "y" ]];
    then
        # Delete existing route if applicable
        if [ -f "/usr/local/sbin/ip_route.sh" ];
        then
            sudo rm /usr/local/sbin/ip_route.sh
        fi
        if [ -f "/etc/systemd/system/ip_route.service" ];
        then
            # Disable and remove IP route service
            sudo systemctl stop ip_route.service
            sudo systemctl disable ip_route.service
            sudo rm /etc/systemd/system/ip_route.service
        fi
    fi
fi

echo "Source your ~/.bashrc file to apply changes"
