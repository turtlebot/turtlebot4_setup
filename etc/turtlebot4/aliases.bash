# Restart ROS2 daemon
alias turtlebot4-daemon-restart='ros2 daemon stop; ros2 daemon start'

# Help command
alias turtlebot4-help='echo -e "\
TurtleBot 4 User Manual: https://turtlebot.github.io/turtlebot4-user-manual \n\
TurtleBot 4 Github: https://github.com/turtlebot/turtlebot4"'

# Restart ntpd on Create 3
alias turtlebot4-ntpd-sync='curl -X POST http://192.168.186.2/api/restart-ntpd'

# Restart turtlebot4 service
alias turtlebot4-service-restart='sudo systemctl restart turtlebot4.service'

# Run turtlebot4_setup
alias turtlebot4-setup='ros2 run turtlebot4_setup turtlebot4_setup'

# Source ROBOT_SETUP
alias turtlebot4-source='source $ROBOT_SETUP'

# Update all packages
alias turtlebot4-update='sudo apt update && sudo apt upgrade'

# Re-connect a previously-paired game controller
alias turtlebot4-connect-controller='bluetoothctl connect $(bt-device -l|grep "Wireless Controller" | grep -o "..:..:..:..:..:..")'
