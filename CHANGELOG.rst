^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package turtlebot4_setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.0.3 (2023-11-08)
------------------
* Cleanup <https://github.com/turtlebot/turtlebot4_setup/issues/7>
* Remove scripts that should not be used in Humble
* Update create_update.sh to reference Humble minimum version
* Updated README
* Updated turtlebot4_setup.sh script
* Fixed setting robot model
* Contributors: Hilary Luo, Roni Kreinin

1.0.2 (2023-03-01)
------------------
* Fixed Discovery Server IP
* Updated default configs
* Contributors: Roni Kreinin

1.0.1 (2023-02-28)
------------------
* Fixed script install path
* Contributors: Roni Kreinin

1.0.0 (2023-02-24)
------------------
* turtlebot4_setup tool
* RPI config updates
* Discovery server files
* Contributors: Roni Kreinin

0.1.3 (2022-09-27)
------------------
* Merge pull request `#2 <https://github.com/turtlebot/turtlebot4_setup/issues/2>`_ from turtlebot/roni-kreinin/domain_id
  v0.1.3
* Added webserver service
* Added argparser to install.py
  Removed namespacing for now
* Added 'ros_config' script for setting ROS_DOMAIN_ID, namespace, and RMW_IMPLEMENTATION
* Contributors: Roni Kreinin, roni-kreinin

0.1.2 (2022-06-14)
------------------
* Added chrony
  Updated wifi script
* Updated dependencies
  Move swap_on and swap_off to /usr/local/bin
* Fixed comment
* Updated Create 3 curl commands
  Move wifi and create update scripts to /usr/local/bin
* Updated oakd branch
* Update README.md
* Moved contents to root folder
  Updated oakd script to work for both pro and lite
  Updated turtlebot4_setup script
  Updated wifi script to allow the create 3 to be set up through the pi
  Added create 3 firmware flash scripts
* Update README.md
* Updated robot_upstart repo
* Added swap memory scripts when more RAM is needed to build packages
* Updated README
* Initial commit
* Contributors: Roni Kreinin, roni-kreinin
