import copy
import os
import yaml
import subprocess
import shlex

from enum import Enum


class SystemOptions(str, Enum):
    MODEL = 'MODEL'
    VERSION = 'VERSION'
    ROS = 'ROS'
    HOSTNAME = 'HOSTNAME'
    IP = 'IP'


class WifiOptions(str, Enum):
    SSID = 'SSID'
    PASSWORD = 'PASSWORD'
    REG_DOMAIN = 'REG_DOMAIN'
    WIFI_MODE = 'WIFI_MODE'
    BAND = 'BAND'
    IP = 'IP'
    DHCP = 'DHCP'


class BashOptions(str, Enum):
    CYCLONEDDS_URI = 'CYCLONEDDS_URI'
    FASTRTPS_URI = 'FASTRTPS_DEFAULT_PROFILES_FILE'
    NAMESPACE = 'ROBOT_NAMESPACE'
    DOMAIN_ID = 'ROS_DOMAIN_ID'
    DISCOVERY_SERVER = 'ROS_DISCOVERY_SERVER'
    RMW = 'RMW_IMPLEMENTATION'
    DIAGNOSTICS = 'TURTLEBOT4_DIAGNOSTICS'
    WORKSPACE = 'WORKSPACE_SETUP'


class DiscoveryOptions(str, Enum):
    ENABLED = 'ENABLED'
    IP = 'IP'
    PORT = 'PORT'


class Conf():
    setup_dir = '/etc/turtlebot4/'
    netplan_dir = '/etc/netplan/'

    default_system_conf = {
        SystemOptions.MODEL: 'lite',
        SystemOptions.VERSION: '1.0.0',
        SystemOptions.ROS: 'Humble',
        SystemOptions.HOSTNAME: 'ubuntu',
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
        BashOptions.WORKSPACE: '/opt/ros/humble/setup.bash',
    }

    default_discovery_conf = {
        DiscoveryOptions.ENABLED: False,
        DiscoveryOptions.IP: '127.0.0.1',
        DiscoveryOptions.PORT: '11811',
    }

    def __init__(self) -> None:
        self.system_file = os.path.join(self.setup_dir, 'system')
        self.setup_bash_file = os.path.join(self.setup_dir, 'setup.bash')
        self.netplan_wifis_file = os.path.join(self.netplan_dir, '50-wifis.yaml')
        self.discovery_sh_file = os.path.join(self.setup_dir, 'discovery.sh')
        self.hostname_file = '/etc/hostname'

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

    def set(self, conf, value):
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
        self.read_system()
        self.read_wifi()
        self.read_bash()
        self.read_discovery()

    def write(self):
        self.write_system()
        self.write_wifi()
        self.write_discovery()
        self.write_bash()

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
                for k in [SystemOptions.MODEL, SystemOptions.VERSION, SystemOptions.ROS]:
                    if k in line:
                        system[i] = '{0}:{1}\n'.format(k, self.system_conf[k])
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

    def read_wifi(self):
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

    def write_wifi(self):
        ssid = self.get(WifiOptions.SSID)
        password = self.get(WifiOptions.PASSWORD)
        dhcp = self.get(WifiOptions.DHCP)
        wifi_mode = self.get(WifiOptions.WIFI_MODE)
        band = self.get(WifiOptions.BAND)
        ip = self.get(WifiOptions.IP)

        wlan0 = {
            'dhcp4': dhcp,
            'optional': True,
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
                'wifis': {
                    'renderer': 'NetworkManager',
                    'wlan0': wlan0,
                },
                'version': 2
            }
        }

        yaml.dump(netplan,
                  stream=open('/tmp' + self.netplan_wifis_file, 'w+'),
                  Dumper=yaml.SafeDumper,
                  indent=4,
                  default_flow_style=False,
                  default_style=None)

        subprocess.run(shlex.split('sudo mv /tmp' + self.netplan_wifis_file + ' ' + self.netplan_wifis_file))

    def read_bash(self):
        with open(self.setup_bash_file, 'r') as f:
            for line in f.readlines():
                for k in self.bash_conf.keys():
                    if 'export {0}'.format(k) in line:
                        try:
                            value = line.split('=')[1].strip()
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
            for i, line in enumerate(bash):
                is_conf = False
                for k, v in self.bash_conf.items():
                    if 'export {0}'.format(k) in line:
                        if v is None:
                            bash[i] = 'export {0}=\n'.format(k)
                        else:
                            bash[i] = 'export {0}={1}\n'.format(k, v)
                        is_conf = True
                if not is_conf:
                    bash[i] = line

        with open('/tmp' + self.setup_bash_file, 'w') as f:
            f.writelines(bash)
            subprocess.run(shlex.split('sudo mv /tmp' + self.setup_bash_file + ' ' + self.setup_bash_file))

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
                self.set(DiscoveryOptions.IP, discovery_server.split(':')[0].strip('"'))
                self.set(DiscoveryOptions.PORT, discovery_server.split(':')[1].strip('"'))
            except IndexError:
                self.discovery_conf = self.default_discovery_conf

    def write_discovery(self):
        if self.get(DiscoveryOptions.ENABLED) is True:
            self.set(BashOptions.DISCOVERY_SERVER, '{0}:{1}'.format(
                self.get(DiscoveryOptions.IP),
                self.get(DiscoveryOptions.PORT)))
            self.set(BashOptions.RMW, 'rmw_fastrtps_cpp')
            self.set(BashOptions.FASTRTPS_URI, self.setup_dir + 'fastdds_discovery_super_client.xml')

            # If Raspberry Pi is the discovery server, set the port in discovery.sh
            if self.get(DiscoveryOptions.IP) == '127.0.0.1':
                discovery_sh = []
                with open(self.discovery_sh_file, 'r') as f:
                    discovery_sh = f.readlines()
                    for i, line in enumerate(discovery_sh):
                        if 'fastdds' in line:
                            discovery_sh[i] = 'fastdds discovery -i 0 -p {0}'.format(
                                self.get(DiscoveryOptions.PORT))

                with open('/tmp' + self.discovery_sh_file, 'w') as f:
                    f.writelines(discovery_sh)
                    subprocess.run(shlex.split('sudo mv /tmp' + self.discovery_sh_file + ' ' + self.discovery_sh_file))
        else:
            self.set(BashOptions.DISCOVERY_SERVER, None)

        self.write_bash()
