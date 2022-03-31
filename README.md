# Turtlebot4 Setup

Setup scripts for the TurtleBot 4 Raspberry Pi.

# Install or update pre-built image

Every Turtlebot4 comes with a SD card with a pre-installed Turtlebot4 image. If you wish to install an image on your own SD card or update to a newer image, follow these instructions. 

- Download the [latest turtlebot4 image](http://download.ros.org/downloads/turtlebot4/).

- Install the imaging tool dcfldd
```bash
sudo apt install dcfldd
```

- Insert your SD card into your PC and identify it:

```bash
sudo fdisk -l
```
- The SD card will have a name like `/dev/mmcblk0` or `/dev/sda`

- Get the SD flash script and flash the SD card
```bash
wget https://raw.githubusercontent.com/turtlebot/turtlebot4-images/galactic/turtlebot4_setup/scripts/sd_flash.sh
bash sd_flash.sh /path/to/image
```
- Follow the instructions and wait for the SD card to be flashed.

- Ensure your Raspberry Pi 4 is not powered before inserting the flashed SD card. 

- Follow [Wi-Fi Setup](https://github.com/turtlebot/turtlebot4_robot#rpi4-wifi-setup) to configure your Wi-Fi.

# Create an image manually

Follow these instructions if you wish to create a Turtlebot4 image manually.

## Create an Ubuntu Image

First install the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

- Insert your SD card into your PC and run the Raspberry Pi Imager. Follow the instructions and install Ubuntu 20.04 LTS onto the SD card.
- Ensure your Raspberry Pi 4 is not powered before inserting the flashed SD card. 
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

## Create your workspace

- Once logged in, create a workspace.
```bash
mkdir ~/turtlebot4_ws/src -p
```
- Clone this repository into the src folder
```bash
cd ~/turtlebot4_ws/src
git clone https://github.com/turtlebot/turtlebot4_setup.git
```

## Automatic Setup
- Run the `turtlebot4_setup.sh` script to automatically set up your turtlebot4.

### Turtlebot4 Standard
```bash
cd ~/turtlebot4_ws
bash src/turtlebot4_robot/turtlebot4_setup/scripts/turtlebot4_setup.sh -m standard
```

### Turtlebot4 Lite
```bash
cd ~/turtlebot4_ws
bash src/turtlebot4_robot/turtlebot4_setup/scripts/turtlebot4_setup.sh -m lite
```

- Run [Wi-Fi Setup](https://github.com/turtlebot/turtlebot4_robot#rpi4-wifi-setup) to enable the 5G Wi-Fi band.

## Manual Setup

If you wish to manually setup the workspace, follow these instructions.

### Install ROS2 Galactic

Follow https://docs.ros.org/en/galactic/Installation/Ubuntu-Install-Debians.html and install ros-galactic-ros-base

### Install ROS tools

```bash
sudo apt update && sudo apt install -y \
  build-essential \
  cmake \
  git \
  python3-colcon-common-extensions \
  python3-flake8 \
  python3-pip \
  python3-pytest-cov \
  python3-rosdep \
  python3-setuptools \
  python3-vcstool \
  wget
```

### Install additional packages

```bash
sudo apt install -y \
libgpiod-dev \
network-manager \
daemontools 
```

### Install bluetooth packages if needed
```bash
sudo apt install -y \
bluez \
bluez-tools \
pi-bluetooth
```

### Import source packages

```
cd ~/turtlebot4_ws
vcs import src < src/turtlebot4-images/turtlebot4_setup/turtlebot4_packages.repos
```

### Install OAK-D camera dependencies

Follow https://github.com/luxonis/depthai-ros/tree/main#install-dependencies

### Run rosdep

```
cd ~/turtlebot4_ws
sudo rosdep init
rosdep update
rosdep install -r --from-paths src -i -y --rosdistro galactic
```

### Build workspace
```
source /opt/ros/galactic/setup.bash
cd ~/turtlebot4_ws
colcon build
source install/setup.bash
```

### Apply udev rules

```bash
cd ~/turtlebot4_ws
sudo cp src/turtlebot4_setup/turtlebot4_setup/udev/turtlebot4.rules /etc/udev/rules.d/
```

### Enable usb0

```bash
echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/usercfg.txt
sudo sed -i '${s/$/ modules-load=dwc2,g_ether/}' /boot/firmware/cmdline.txt
```

### Enable i2c-3 bus

```bash
echo "dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=4,i2c_gpio_scl=5" | sudo tee -a /boot/firmware/usercfg.txt 
```

### Configure CycloneDDS

```bash
echo "export CYCLONEDDS_URI='<CycloneDDS><Domain><General><NetworkInterfaceAddress>wlan0,usb0</></></></>'" | sudo tee -a ~/.bashrc
```

### Create Turtlebot4 service to run on boot

#### Turtlebot4 Standard

```bash
ros2 run robot_upstart install turtlebot4_bringup/launch/standard.launch.py --job turtlebot4
```

#### Turtlebot4 Lite

```bash
ros2 run robot_upstart install turtlebot4_bringup/launch/lite.launch.py --job turtlebot4
```

### Set up Wi-Fi

Run [Wi-Fi Setup](https://github.com/turtlebot/turtlebot4_robot#rpi4-wifi-setup)

### Reboot the Raspberry Pi

```bash
sudo reboot
```
