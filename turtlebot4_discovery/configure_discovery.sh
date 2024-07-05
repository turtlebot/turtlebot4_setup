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

# Read in the ROS domain ID from user input
while [ 1 ]
do
  read -p "ROS_DOMAIN_ID [0]: " domain_id
  domain_id=${domain_id:-0}
  if [[ $domain_id =~ ^[0-9]{1,3}$ ]];
  then
    if ((domain_id > 232));
    then
      echo "Invalid domain ID, cannot exceed 232"
      continue
    fi
    break
  else
    echo "Invalid domain ID, must be an integer (0-232)"
  fi
done

# Collect input data for each discovery server that the user wants to connect to
server_ip_list=()
server_id_list=()
server_port_list=()
server_count=0
complete=0

echo "Enter the information for the first discovery server"

while ((! $complete))
do

  # Read in the Server ID
  while [ 1 ]
  do
    read -p "Discovery Server ID [0]: " discovery_server_id
    discovery_server_id=${discovery_server_id:-0}
    if [[ $discovery_server_id =~ ^[0-9]{1,3}$ ]];
    then
      if ((discovery_server_id > 255));
      then
        echo "Invalid server ID, cannot exceed 255"
        continue
      fi
      duplicate=0
      for ((i=0; i < server_count; i+=1))
      do
        if ((server_id_list[i] == discovery_server_id));
        then
          duplicate=1
          break
        fi
      done
      if ((duplicate));
      then
        echo "Invalid server ID, must be unique and cannot be repeated"
        continue
      fi
      break
    else
      echo "Invalid server ID, must be an integer (0-255)"
    fi
  done

  # Read in the Server IP Address
  while [ 1 ]
  do
    read -p "Discovery Server IP: " discovery_ip
    if [[ $discovery_ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]];
    then
      break
    else
      echo "Invalid IP address"
    fi
  done

  # Read in the Server Port
  while [ 1 ]
  do
    read -p "Discovery Server Port [11811]: " discovery_port
    discovery_port=${discovery_port:-11811}
    if [[ $discovery_port =~ ^[0-9]{5}$ ]];
    then
      break
    else
      echo "Invalid port, must be an integer (10000-65535)"
    fi
  done

  # Prompt the user to offer the ability to correct the last server info or add additional servers
  while [ 1 ]
  do
    read -p "Re-enter the last server (r), add another server (a), or done (d): " option
    if [[ $option =~ ^[r,R].* ]];
    then
      echo "Removing last server entry, re-enter the correct server information"
      break
    elif [[ $option =~ ^[a,A,d,D].* ]];
    then
      # add to list to track all that have been added
      server_ip_list+=($discovery_ip)
      server_id_list+=($discovery_server_id)
      server_port_list+=($discovery_port)
      ((server_count+=1))
      if [[ $option =~ ^[d,D].* ]];
      then
        complete=1
      else
        echo "Enter the information for the next discovery server"
      fi
      break
    else
      echo "Invalid option"
    fi
  done
done

# Build the ROS Discovery Server environment variable string from the input data
discovery_str=""
complete=0
count=0
for ((id=0; count != server_count && id < 256; id+=1))
do
  found=0
  for ((i=0; i < server_count; i+=1))
  do
    if ((server_id_list[i] == id));
    then
      discovery_str="${discovery_str}${server_ip_list[i]}:${server_port_list[i]};"
      ((count+=1))
      found=1
      break
    fi
  done
  if ((! found));
  then
    discovery_str="${discovery_str};"
  fi
done

echo "Configuring:"
echo " ROS_DOMAIN_ID=$domain_id"
echo " ROS_DISCOVERY_SERVER=\"$discovery_str\""

# Make directory to hold configs
sudo mkdir -p /etc/turtlebot4_discovery/

# Create setup.bash file
setup_file_temp="/tmp/turtlebot4_discovery_setup.bash"
echo "source /opt/ros/jazzy/setup.bash" > $setup_file_temp
echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> $setup_file_temp
echo "[ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False" >> $setup_file_temp

# Add user configured data to setup.bash
echo "export ROS_DOMAIN_ID=$domain_id" >> $setup_file_temp
echo "export ROS_DISCOVERY_SERVER=\"$discovery_str\"" >> $setup_file_temp

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
