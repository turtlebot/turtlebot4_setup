^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package turtlebot4_setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.0.3 (2025-03-04)
------------------
* Update the hostname in `/boot/firmware/user-data` (`#19 <https://github.com/turtlebot/turtlebot4_setup/issues/19>`_)
  * Update the hostname in /boot/firmware/user-data as well as /etc/hostname to ensure it persists properly across reboots
  * Suppress error output about failure to preserve permissions across filesystems
  * Write the updated hostname to the turtlebot4/system file
* Fix/shm (`#21 <https://github.com/turtlebot/turtlebot4_setup/issues/21>`_)
  Turn off clearing of SHM on log out (interfered with services)
* Replace `User=ubuntu` with `User={os.getlogin()}` when generating the discovery server configuration file if necessary (`#20 <https://github.com/turtlebot/turtlebot4_setup/issues/20>`_)
* Fix tag order
* Update package maintainers
* Add an alias to reconnect to a previously-paired game controller
* Add a udev rule for the Logitech F710 family of controllers
* Contributors: Chris Iverach-Brereton, Hilary Luo

2.0.2 (2024-10-23)
------------------
* Add e2fsck to SD-flasher script
* Bump default version numbers
* Fix default hostname to match released SD card images
* Append `p2` for `mmcblk` devices, but just `2` for `sd*` devices when expanding the last partition
* Contributors: Chris Iverach-Brereton

2.0.1 (2024-10-04)
------------------
* Add a copy of the boot/firmware files to /etc/turtlebot for reference in case users modify these and want a clean, offline copy for reference
* Add ROBOT_SETUP to setup.bash
* Add growpart & resize2fs commands to the SD card-flashing script to expand the partition to use up the whole SD card
* Add socat as a package dependency instead of an ad-hoc post-install package
* Add MOTD file with the Turtlebot4 logotype
* Contributors: Chris Iverach-Brereton

2.0.0 (2024-09-28)
------------------
* Initial Jazzy implementation
  * Add a note about firmware compatibility to the readme
  * Add exception handling to the file i/o so the node doesn't just crash if we're missing a file
  * Add improved exception handling to the wifi settings parser
  * Update CI
  * Properly escape all `\` characters in stylized titles, add translation & link to generator page in comments
  * Add copyright & contribution notices, fix up code formatting, import ordering. Disable linting for some specific lines where appropriate
  * Add XML namespaces & version to cyclone DDS config
  * Omit XML linting (for now); it's consistently timing out and failing
  * Code formatting fixes
  * Add exception handling to the file preview
  * Add an option to force the Create3 settings to be reapplied, even if we haven't changed anything else. Always apply the _do_not_use namespace, as we're universally using the republisher now
  * Remove superfluous concatenation
  * Enable testing packages for CI
  * Disable checks on two lines with long format strings
  * Add exception handling for install & uninstall
  * Add an error prompt to show errors during installation
  * Handle KeyErrors separately
  * Add newline to end of file
  * Fix indentation
  * `''.format` -> `f''`
  * Update the default system file, print the keys instead of the enums
  * Add a `__str_\_` function to the relevant classes
* Disable DHCP4 on the built-in ethernet interface, make it non-optional
* Change the post-install chrony file command from mv to cp
* Only copy if the file exists
* Initial Jazzy implementation (`#15 <https://github.com/turtlebot/turtlebot4_setup/issues/15>`_)
* Contributors: Chris Iverach-Brereton

1.0.4 (2024-07-02)
------------------
* Multi-robot discovery server support (`#11 <https://github.com/turtlebot/turtlebot4_setup/issues/11>`)
  * Add discovery server ID
  * Switch from xml super client to envar
  * Don't look for an ntp server on create3
  * Adjust create3 discovery server envar for server_id
  * Get feedback from the curl command to abort the apply if the create3 is not accessible
  * Push ntp config to create3, pointing it at the pi
  * Write discovery.sh fresh each time for robustness
  * Insert missing exports when writing setup.bash
  * Update script for server ID
  * Enforce a local server in discovery server for the create3 and support an offboard server for pi only
  * Give the create3 a hidden namespace to prepare for republishing
  * Put environment variables in quotes to handle multiple discovery servers
  * Make  Super Client only apply to user terminals
  * Fix error when setting Offboard Discovery Server IP to blank
  * Remove IP Routing from script to set up discovery server on the user computer, no longer needed due to the republisher, includes file/service cleanup
  * Force compares as string to handle boolean settings correctly
  * Ensure that usb0 and wlan0 networks are up before either turtlebot4 service is started and use only NetworkManager to speed up boot
  * ipv4 forwarding is no longer required
  * Add create3 rmw profile for discovery server
  * git clone no longer necessary
  * Update discovery server user pc config script to accept any number of discovery servers
  * Added missing exec dependencies
  * Ensure that the chrony file always gets overwritten
* Update username for github issue asignment (`#10 <https://github.com/turtlebot/turtlebot4_setup/issues/10>`)
* Updated issue templates to forms and redirected troubleshooting to turtlebot4 repo (`#9 <https://github.com/turtlebot/turtlebot4_setup/issues/9>`)
* Contributors: Hilary Luo

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
