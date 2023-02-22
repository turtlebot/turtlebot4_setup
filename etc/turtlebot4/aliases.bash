# Run turtlebot4_setup
alias turtlebot4-setup='ros2 run turtlebot4_setup turtlebot4_setup'

# Source ROBOT_SETUP
alias turtlebot4-source='source $ROBOT_SETUP'

# Restart ROS2 daemon
alias turtlebot4-daemon-restart='ros2 daemon stop; ros2 daemon start'

# Restart ntpd on Create 3
alias turtlebot4-ntpd-sync='curl -X POST http://192.168.186.2/api/restart-ntpd'

# Update all packages
alias turtlebot4-update='sudo apt update && sudo apt upgrade'

# Help command
alias turtlebot4-help='echo -e "\
TurtleBot 4 User Manual: https://turtlebot.github.io/turtlebot4-user-manual \n\
TurtleBot 4 Github: https://github.com/turtlebot/turtlebot4"'
