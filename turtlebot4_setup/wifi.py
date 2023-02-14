from turtlebot4_setup.menu import Menu, MenuEntry, OptionsMenu, Prompt, PreviewMenu

import subprocess, shlex

from turtlebot4_setup.conf import Conf, WifiOptions


class WifiSetup():
    title = """
 __      ___ ___ _   ___      _ 
 \ \    / (_) __(_) / __| ___| |_ _  _ _ __ 
  \ \/\/ /| | _|| | \__ \/ -_)  _| || | '_ \\
   \_/\_/ |_|_| |_| |___/\___|\__|\_,_| .__/
                                      |_|    
"""

    def __init__(self, configs: Conf) -> None:
        self.conf = configs

        self.conf.read()

        self.entries = [MenuEntry(entry=self.format_entry('Wi-Fi Mode', WifiOptions.WIFI_MODE),
                                  function=self.set_wifi_mode),
                        MenuEntry(entry=self.format_entry('SSID', WifiOptions.SSID),
                                  function=self.set_ssid),
                        MenuEntry(entry=self.format_entry('Password', WifiOptions.PASSWORD),
                                  function=self.set_password),
                        # TODO(rkreinin): Set Reg Domain in 22.04
                        # MenuEntry(entry=self.format_entry('Regulatory Domain', WifiOptions.REG_DOMAIN),
                        #           function=self.set_reg_domain),
                        MenuEntry(entry=self.format_entry('Band', WifiOptions.BAND),
                                  function=self.set_band),
                        MenuEntry(entry=self.format_entry('IP Address', WifiOptions.IP),
                                  function=self.set_ip_address),
                        MenuEntry(entry=self.format_entry('DHCP', WifiOptions.DHCP),
                                  function=self.set_dhcp),
                        MenuEntry('', None),
                        MenuEntry(entry='Apply Defaults', function=self.apply_defaults),
                        MenuEntry(entry='Save', function=self.save_settings),]

        self.menu = Menu(self.title, self.entries)

    def format_entry(self, name, opt: WifiOptions):
        return lambda: '{0}{1}[{2}]'.format(
            name,
            ' ' * (22 - len(name)),
            '' if self.conf.get(opt) is None else self.conf.get(opt))

    def run(self):
        self.conf.read()
        self.menu.show()

    def apply_defaults(self):
        self.conf.apply_default(self.conf.wifi_conf)

    def set_ssid(self):
        p = Prompt(prompt='SSID ({0}): '.format(self.conf.get(WifiOptions.SSID)),
                   default_response=self.conf.get(WifiOptions.SSID),
                   note='Wi-Fi Network SSID')
        self.conf.set(WifiOptions.SSID, p.show())

    def set_password(self):
        p = Prompt(prompt='Password ({0}): '.format(self.conf.get(WifiOptions.PASSWORD)),
                   default_response=self.conf.get(WifiOptions.PASSWORD),
                   note='Wi-Fi Network Password')
        self.conf.set(WifiOptions.PASSWORD, p.show())

    def set_reg_domain(self):
        p = Prompt(prompt='Regulatory Domain ({0}): '.format(self.conf.get(WifiOptions.REG_DOMAIN)),
                   default_response=self.conf.get(WifiOptions.REG_DOMAIN),
                   note='Wireless regulatory domain. \n' +
                        'Common options:\n' +
                        'USA: US\nCanada: CA\nUK: GB\n' +
                        'Germany: DE\nJapan: JP3\nSpain: ES')
        self.conf.set(WifiOptions.REG_DOMAIN, p.show())

    def set_wifi_mode(self):
        options = OptionsMenu(title='Wi-Fi Mode',
                              menu_entries=['Client', 'Access Point'],
                              default_option=self.conf.get(WifiOptions.WIFI_MODE))
        self.conf.set(WifiOptions.WIFI_MODE, options.show())

    def set_band(self):
        options = OptionsMenu(title='Band',
                              menu_entries=['5GHz', '2.4GHz', 'Any'],
                              default_option=self.conf.get(WifiOptions.BAND))
        self.conf.set(WifiOptions.BAND, options.show())

    def set_ip_address(self):
        p = Prompt(prompt='IP Address ({0}): '.format(self.conf.get(WifiOptions.IP)),
                   default_response=self.conf.get(WifiOptions.IP),
                   note='IP Address with CIDR. e.g. 192.168.0.12/24')
        self.conf.set(WifiOptions.IP, p.show())

    def set_dhcp(self):
        options = OptionsMenu(title='DHCP',
                              menu_entries=['True', 'False'],
                              default_option=self.conf.get(WifiOptions.DHCP))
        self.conf.set(WifiOptions.DHCP, options.show() == 'True')

    def save_settings(self):
        self.conf.write()
        self.menu.exit()
