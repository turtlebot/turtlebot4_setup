#!/usr/bin/env python3

# Copyright 2023 Clearpath Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from enum import Enum
import os
import re
import shlex
import subprocess
import sys

import yaml


__author__ = 'Roni Kreinin'
__email__ = 'rkreinin@clearpathrobotics.com'
__copyright__ = 'Copyright © 2023 Clearpath Robotics. All rights reserved.'
__license__ = 'Apache 2.0'


class SystemOptions(str, Enum):
    MODEL = 'MODEL'
    VERSION = 'VERSION'
    ROS = 'ROS'
    HOSTNAME = 'HOSTNAME'
    IP = 'IP'

    def __str__(self):
        return f'{self.value}'


class WifiOptions(str, Enum):
    SSID = 'SSID'
    PASSWORD = 'PASSWORD'
    REG_DOMAIN = 'REG_DOMAIN'
    WIFI_MODE = 'WIFI_MODE'
    BAND = 'BAND'
    IP = 'IP'
    DHCP = 'DHCP'

    def __str__(self):
        return f'{self.value}'


class BashOptions(str, Enum):
    CYCLONEDDS_URI = 'CYCLONEDDS_URI'
    FASTRTPS_URI = 'FASTRTPS_DEFAULT_PROFILES_FILE'
    NAMESPACE = 'ROBOT_NAMESPACE'
    DOMAIN_ID = 'ROS_DOMAIN_ID'
    DISCOVERY_SERVER = 'ROS_DISCOVERY_SERVER'
    RMW = 'RMW_IMPLEMENTATION'
    DIAGNOSTICS = 'TURTLEBOT4_DIAGNOSTICS'
    WORKSPACE = 'WORKSPACE_SETUP'
    SUPER_CLIENT = 'ROS_SUPER_CLIENT'

    def __str__(self):
        return f'{self.value}'


class DiscoveryOptions(str, Enum):
    ENABLED = 'ENABLED'
    PORT = 'PORT'
    SERVER_ID = 'SERVER_ID'
    OFFBOARD_IP = 'OFFBOARD_IP'
    OFFBOARD_PORT = 'OFFBOARD_PORT'
    OFFBOARD_ID = 'OFFBOARD_ID'

    def __str__(self):
        return f'{self.value}'


class Conf():
    setup_dir = '/etc/turtlebot4/'
    netplan_dir = '/etc/netplan/'

    default_system_conf = {
        SystemOptions.MODEL: 'lite',
        SystemOptions.VERSION: '2.0.2',
        SystemOptions.ROS: 'Jazzy',
        SystemOptions.HOSTNAME: 'turtlebot4',
    }

    default_wifi_conf = {
        WifiOptions.SSID: 'Turtlebot4',
        WifiOptions.PASSWORD: 'Turtlebot4',
        WifiOptions.REG_DOMAIN: 'CA',
        WifiOptions.WIFI_MODE: 'Access Point',
        WifiOptions.BAND: '5GHz',
        WifiOptions.IP: None,
        WifiOptions.DHCP: True,
    }

    default_bash_conf = {
        BashOptions.CYCLONEDDS_URI: setup_dir + 'cyclonedds_rpi.xml',
        BashOptions.FASTRTPS_URI: setup_dir + 'fastdds_rpi.xml',
        BashOptions.NAMESPACE: None,
        BashOptions.DOMAIN_ID: 0,
        BashOptions.DISCOVERY_SERVER: None,
        BashOptions.RMW: 'rmw_fastrtps_cpp',
        BashOptions.DIAGNOSTICS: '1',
        BashOptions.WORKSPACE: '/opt/ros/jazzy/setup.bash',
        BashOptions.SUPER_CLIENT: False
    }

    default_discovery_conf = {
        DiscoveryOptions.ENABLED: False,
        DiscoveryOptions.PORT: '11811',
        DiscoveryOptions.SERVER_ID: '0',
        DiscoveryOptions.OFFBOARD_IP: '',
        DiscoveryOptions.OFFBOARD_PORT: '11811',
        DiscoveryOptions.OFFBOARD_ID: '1',
    }

    def __init__(self) -> None:
        self.system_file = os.path.join(self.setup_dir, 'system')
        self.setup_bash_file = os.path.join(self.setup_dir, 'setup.bash')
        self.netplan_wifis_file = os.path.join(self.netplan_dir, '50-wifis.yaml')
        self.discovery_sh_file = os.path.join(self.setup_dir, 'discovery.sh')
        self.hostname_file = '/etc/hostname'
        self.fw_user_data_file = '/boot/firmware/user-data'

        self.system_conf = copy.deepcopy(self.default_system_conf)
        self.wifi_conf = copy.deepcopy(self.default_wifi_conf)
        self.bash_conf = copy.deepcopy(self.default_bash_conf)
        self.discovery_conf = copy.deepcopy(self.default_discovery_conf)

        subprocess.run(shlex.split('mkdir -p /tmp' + self.setup_dir))
        subprocess.run(shlex.split('mkdir -p /tmp' + self.netplan_dir))

        self.read()

    def get(self, conf):
        if isinstance(conf, SystemOptions):
            return self.system_conf.get(conf)
        elif isinstance(conf, WifiOptions):
            return self.wifi_conf.get(conf)
        elif isinstance(conf, BashOptions):
            return self.bash_conf.get(conf)
        elif isinstance(conf, DiscoveryOptions):
            return self.discovery_conf.get(conf)
        return None

    def set(self, conf, value):  # noqa: A003
        if isinstance(conf, SystemOptions):
            self.system_conf[conf] = value
        elif isinstance(conf, WifiOptions):
            self.wifi_conf[conf] = value
        elif isinstance(conf, BashOptions):
            self.bash_conf[conf] = value
        elif isinstance(conf, DiscoveryOptions):
            self.discovery_conf[conf] = value

    def apply_default(self, conf):
        if conf == self.system_conf:
            self.system_conf = copy.deepcopy(self.default_system_conf)
        elif conf == self.wifi_conf:
            self.wifi_conf = copy.deepcopy(self.default_wifi_conf)
        elif conf == self.bash_conf:
            self.bash_conf = copy.deepcopy(self.default_bash_conf)
        elif conf == self.discovery_conf:
            self.discovery_conf = copy.deepcopy(self.default_discovery_conf)

    def read(self):
        try:
            self.read_system()
            self.read_wifi()
            self.read_bash()
            # Must come after read_bash in order to have the discovery server envar
            self.read_discovery()
        except Exception as err:
            print(f'Error reading configuration: {err}. Terminating')
            sys.exit(1)

    def write(self):
        try:
            self.write_system()
            self.write_wifi()
            self.write_discovery()
            self.write_bash()
        except Exception as err:
            print(f'Error writing configuration: {err}. Configuration may be incomplete')
            sys.exit(1)

    def read_system(self):
        with open(self.system_file, 'r') as f:
            for line in f.readlines():
                for k in [SystemOptions.MODEL, SystemOptions.VERSION, SystemOptions.ROS]:
                    if k in line:
                        self.system_conf[k] = line.split(':')[1].strip()

        self.system_conf[SystemOptions.IP] = subprocess.run(
            shlex.split('hostname -I'),
            capture_output=True).stdout.decode('ascii').replace('192.168.186.3', '').strip()

        with open(self.hostname_file, 'r') as f:
            self.set(SystemOptions.HOSTNAME, f.readline().strip())

    def write_system(self):
        system = []
        with open(self.system_file, 'r') as f:
            system = f.readlines()
            for i, line in enumerate(system):
                is_conf = False
                for k in [
                    SystemOptions.MODEL,
                    SystemOptions.VERSION,
                    SystemOptions.ROS,
                    SystemOptions.HOSTNAME,
                ]:
                    if k in line:
                        system[i] = f'{k}:{self.system_conf[k]}\n'
                        is_conf = True
                        break

                if not is_conf:
                    system[i] = line

        with open('/tmp' + self.system_file, 'w') as f:
            f.writelines(system)
        subprocess.run(shlex.split('sudo mv /tmp' + self.system_file + ' ' + self.system_file))

        with open('/tmp' + self.hostname_file, 'w') as f:
            f.write(self.get(SystemOptions.HOSTNAME))
        subprocess.run(shlex.split('sudo mv /tmp' + self.hostname_file + ' ' + self.hostname_file))

        # update /boot/firmware/user-data with the new hostname
        subprocess.run(shlex.split(f'cp {self.fw_user_data_file} /tmp/user-data'))
        subprocess.run(shlex.split(f'sed -i -E "s/^hostname:.+/hostname: {self.get(SystemOptions.HOSTNAME)}/" /tmp/user-data'))  # noqa: E501
        subprocess.run(
            shlex.split(f'sudo mv /tmp/user-data {self.fw_user_data_file}'),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def read_wifi(self):
        try:
            # Try to open the existing wifi configuration, but if it doesn't exist we can carry on
            netplan = yaml.load(open(self.netplan_wifis_file, 'r'), yaml.SafeLoader)

            # wlan0 Config
            wlan0 = netplan['network']['wifis']['wlan0']

            # Get SSID
            self.set(WifiOptions.SSID, list(wlan0['access-points'])[0])
            # SSID settings
            ssid_settings = wlan0['access-points'][self.get(WifiOptions.SSID)]

            self.set(WifiOptions.PASSWORD, ssid_settings.get('password'))

            if wlan0.get('addresses'):
                self.set(WifiOptions.IP, wlan0['addresses'][0])
            else:
                self.set(WifiOptions.IP, None)

            if wlan0.get('dhcp4') is True:
                self.set(WifiOptions.DHCP, True)
            else:
                self.set(WifiOptions.DHCP, False)

            if ssid_settings.get('mode') == 'ap':
                self.set(WifiOptions.WIFI_MODE, 'Access Point')
            else:
                self.set(WifiOptions.WIFI_MODE, 'Client')

            if ssid_settings.get('band'):
                self.set(WifiOptions.BAND, ssid_settings.get('band'))
            else:
                self.set(WifiOptions.BAND, 'Any')
        except Exception:
            # If the wifi configuration doesn't have a wlan0 configuration, just skip this
            pass

    def write_wifi(self):
        ssid = self.get(WifiOptions.SSID)
        password = self.get(WifiOptions.PASSWORD)
        dhcp = self.get(WifiOptions.DHCP)
        wifi_mode = self.get(WifiOptions.WIFI_MODE)
        band = self.get(WifiOptions.BAND)
        ip = self.get(WifiOptions.IP)

        wlan0 = {
            'dhcp4': dhcp,
            'access-points': {
                ssid: {}
            }
        }

        if password is not None:
            wlan0['access-points'][ssid].update({'password': password})

        if ip is not None:
            wlan0.update({'addresses': [ip]})

        if wifi_mode == 'Access Point':
            wlan0['access-points'][ssid].update({'mode': 'ap'})

        if band is not None and band != 'Any':
            wlan0['access-points'][ssid].update({'band': band})

        netplan = {
            'network': {
                'version': 2,
                'wifis': {
                    'renderer': 'NetworkManager',
                    'wlan0': wlan0,
                },
            }
        }

        with open('/tmp' + self.netplan_wifis_file, 'w') as f:
            f.write('# This file was automatically created by the turtlebot4-setup tool and should not be manually modified\n\n')  # noqa: E501

        yaml.dump(netplan,
                  stream=open('/tmp' + self.netplan_wifis_file, 'a'),
                  Dumper=yaml.SafeDumper,
                  indent=4,
                  default_flow_style=False,
                  default_style=None)

        subprocess.run(shlex.split(
            'sudo mv /tmp' + self.netplan_wifis_file + ' ' + self.netplan_wifis_file))

    def read_bash(self):
        with open(self.setup_bash_file, 'r') as f:
            for line in f.readlines():
                for k in self.bash_conf.keys():
                    if f'export {k}' in line:
                        try:
                            value = line.split('=')[1].strip().strip('\'"')
                            if (k == BashOptions.SUPER_CLIENT):
                                value = value.split('||')[0].strip().strip('\'"')
                            if value == '':
                                self.set(k, None)
                            else:
                                self.set(k, value)
                        except IndexError:
                            self.set(k, None)
                        break

    def write_bash(self):
        bash = []
        with open(self.setup_bash_file, 'r') as f:
            bash = f.readlines()
            # Loop through every bash setting
            for k, v in self.bash_conf.items():
                # Check if the setting is currently in the setup.bash and update it
                found = False
                if v is None:
                    v = ''
                for i, line in enumerate(bash):
                    export_re = re.compile(rf'^\s*export\s+{k}=.*')
                    if export_re.match(line):
                        if (k == BashOptions.SUPER_CLIENT and str(v) == 'True'):
                            # Ensure super client is only applied on user terminals
                            bash[i] = f'[ -t 0 ] && export {k}={v} || export {k}=False\n'  # noqa: 501
                        else:
                            # Quotations required around v to handle multiple servers
                            # in discovery server
                            bash[i] = f'export {k}=\"{v}\"\n'
                        found = True

                # If the setting is missing from the setup.bash, add it to the beginning
                if not found:
                    if (k == BashOptions.SUPER_CLIENT and str(v) == 'True'):
                        # Ensure super client is only applied on user terminals
                        bash.insert(0, f'[ -t 0 ] && export {k}={v} || export {k}=False\n')  # noqa: 501
                    else:
                        # Quotations required around v to handle multiple servers
                        # in discovery server
                        bash.insert(0, f'export {k}=\"{v}\"\n')

        with open('/tmp' + self.setup_bash_file, 'w') as f:
            f.writelines(bash)
        subprocess.run(shlex.split(f'sudo mv /tmp{self.setup_bash_file} {self.setup_bash_file}'))

        for k, v in self.bash_conf.items():
            if v is None:
                os.environ[k] = ''
            else:
                os.environ[k] = str(v)

    def read_discovery(self):
        discovery_server = self.get(BashOptions.DISCOVERY_SERVER)
        if discovery_server is None or discovery_server == '':
            self.set(DiscoveryOptions.ENABLED, False)
        else:
            self.set(DiscoveryOptions.ENABLED, True)
            try:
                servers = discovery_server.split(';')
                for i, s in enumerate(servers):
                    s = s.strip()
                    if s:
                        server = s.split(':')
                        if (server[0].strip('"') == '127.0.0.1'):
                            self.set(DiscoveryOptions.SERVER_ID, i)
                            if len(server) > 1:
                                self.set(DiscoveryOptions.PORT, int(server[1].strip('\'"')))
                            else:
                                self.set(DiscoveryOptions.PORT, 11811)
                        else:
                            self.set(DiscoveryOptions.OFFBOARD_ID, i)
                            self.set(DiscoveryOptions.OFFBOARD_IP, server[0].strip('\'"'))
                            if len(server) > 1:
                                self.set(
                                    DiscoveryOptions.OFFBOARD_PORT, int(server[1].strip('\'"')))
                            else:
                                self.set(DiscoveryOptions.OFFBOARD_PORT, 11811)
            except Exception:
                self.discovery_conf = self.default_discovery_conf

    def write_discovery(self):
        if self.get(DiscoveryOptions.ENABLED) is True:
            self.set(BashOptions.DISCOVERY_SERVER, self.get_discovery_str())
            self.set(BashOptions.RMW, 'rmw_fastrtps_cpp')
            self.set(BashOptions.SUPER_CLIENT, True)

            with open('/tmp' + self.discovery_sh_file, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('# This file was automatically created by the turtlebot4-setup tool and should not be manually modified\n\n')  # noqa: E501
                f.write(f'source {self.get(BashOptions.WORKSPACE)}\n')
                f.write(f'fastdds discovery -i {self.get(DiscoveryOptions.SERVER_ID)} -p {self.get(DiscoveryOptions.PORT)}')  # noqa: E501
            subprocess.run(shlex.split(
                'sudo mv /tmp' + self.discovery_sh_file + ' ' + self.discovery_sh_file))
        else:
            self.set(BashOptions.DISCOVERY_SERVER, None)
            self.set(BashOptions.SUPER_CLIENT, False)

        self.write_bash()

    def get_discovery_str(self) -> str:
        discovery_str = ''
        servers = [{
            'id': self.get(DiscoveryOptions.SERVER_ID),
            'ip': '127.0.0.1',
            'port': self.get(DiscoveryOptions.PORT),
            }]
        offboard_ip = self.get(DiscoveryOptions.OFFBOARD_IP)
        if offboard_ip:
            servers.append({
                'id': self.get(DiscoveryOptions.OFFBOARD_ID),
                'ip': offboard_ip,
                'port': self.get(DiscoveryOptions.OFFBOARD_PORT)
                })

        servers.sort(key=lambda s: int(s['id']))

        i = 0
        for s in servers:
            while i < int(s['id']):
                discovery_str += ';'
                i += 1
            discovery_str += f"{s['ip']}:{s['port']};"
            i += 1
        return discovery_str

    def get_create3_server_str(self) -> str:
        # Create3 should only point at the local server on the pi
        discovery_str = ''
        for i in range(int(self.get(DiscoveryOptions.SERVER_ID))):
            discovery_str += ';'
        discovery_str += f'192.168.186.3:{self.get(DiscoveryOptions.PORT)}'
        return discovery_str
