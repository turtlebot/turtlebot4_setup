# Turtlebot4 Setup

Setup scripts and tools for the TurtleBot 4 Raspberry Pi.

Visit the [TurtleBot 4 User Manual](https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_setup.html) for more details.

Prior to starting make sure your Create® 3 is updated to the `I.*.*` firmware; older versions of the firmware are not compatible with ROS 2 Jazzy. 
You can find [firmware updates and instructions on the iRobot website](https://edu.irobot.com/create3-update). 

To access the RaspberryPi on the TurtleBot4 you will need a 2.5mm hex key to remove the top bolts.
The RaspberryPi SD card can be difficult to find. It is located on the side of the RaspberryPi facing the Create3 on the side opposite the USB and Ethernet ports. 

# Create an image manually

Follow these instructions if you wish to create a Turtlebot4 image manually.

## Create an Ubuntu Image

First install the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) from the website or using the Ubuntu Snap store.

- Ensure your Raspberry Pi 4 is not powered before removing the flashed SD card.
- Insert your SD card into your PC and run the Raspberry Pi Imager. Follow the instructions to install Ubuntu 24.04 Server (64-bit) onto the SD card.
- If you use this method **you must configure the operating system customizations prior to imaging the SD card.** Please use the following settings:
  - Set the default login and password to `ubuntu` / `ubuntu`
  - Enable SSH 
  - Set the default wifi network, password, and country to your home network
- You can set up the Raspberry Pi by either connecting it to your network via Ethernet or by using a keyboard and HDMI monitor via a micro HDMI cable.

### Ethernet Setup

- Connect the Raspberry Pi to your Network with an Ethernet cable.
- Boot the Raspberry Pi.
- Find the Raspberry Pi's IP using your router's portal.
- SSH into the Raspberry Pi using the IP address.
```bash
ssh ubuntu@xxx.xxx.xxx.xxx
```
- The default login is `ubuntu` and password is `ubuntu`. You will be prompted to change your password.

### HDMI Setup

- Connect a keyboard to the Raspberry Pi via USB.
- Connect a monitor to the Raspberry Pi via the HDMI0 port.
- Boot the Raspberry Pi.
- The default login is `ubuntu` and password is `ubuntu`. You will be prompted to change your password.

## Manually configure Wi-Fi

Once you are logged into the Raspberry Pi, configure the Wi-Fi:

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```
Add the following lines:
```bash
wifis:
    wlan0:
        optional: true
        access-points:
            "YOUR_WIFI_SSID":
                password: "YOUR_WIFI_PASSWORD"
        dhcp4: true
```
Note: Ensure that `wifis:` is aligned with the existing `ethernets:` line. All indentations should be 4 spaces. Do not use tabs.
- Reboot the Raspberry Pi. It should now be connected to your Wi-Fi.
- Find the Raspberry Pi's IP using your router's portal.
- SSH into the Raspberry Pi using the IP address.
```bash
ssh ubuntu@xxx.xxx.xxx.xxx
```

## Download and run the setup script

```
wget -qO - https://raw.githubusercontent.com/turtlebot/turtlebot4_setup/jazzy/scripts/turtlebot4_setup.sh | bash
```

The script will automatically install ROS 2 Jazzy, TurtleBot 4 packages, and other important apt packages. It will also configure the RPi4 to work in a TurtleBot 4. Once complete, the RPi4 should be rebooted with `sudo reboot`. Then, run `turtlebot4-setup` to configure the robot with the setup tool.
