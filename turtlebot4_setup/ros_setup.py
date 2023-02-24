from turtlebot4_setup.menu import Menu, OptionsMenu, MenuEntry, Prompt
from turtlebot4_setup.conf import Conf, SystemOptions, BashOptions, DiscoveryOptions

import os

import subprocess, shlex

import robot_upstart


class RosSetup():

    title = """
  ___  ___  ___   ___      _  
 | _ \/ _ \/ __| / __| ___| |_ _  _ _ __ 
 |   / (_) \__ \ \__ \/ -_)  _| || | '_ \\
 |_|_\\\___/|___/ |___/\\___|\\__|\\_,_| .__/
                                   |_| 
"""

    setup_dir = '/etc/turtlebot4/'

    def __init__(self, conf: Conf) -> None:
        self.conf = conf

        self.discovery_server_menu = DiscoveryServer(self.conf)
        self.bash_setup_menu = BashSetup(self.conf)
        self.robot_upstart_menu = RobotUpstart(self.conf)

        self.entries = [MenuEntry('Bash Setup', self.bash_setup_menu.show),
                        MenuEntry('Discovery Server', function=self.discovery_server_menu.show),
                        MenuEntry('Robot Upstart', self.robot_upstart_menu.show)]

        self.menu = Menu(self.title, self.entries)

    def show(self):
        self.menu.show()


class BashSetup():

    title = """
  ___          _      ___      _             
 | _ ) __ _ __| |_   / __| ___| |_ _  _ _ __ 
 | _ \/ _` (_-< ' \  \__ \/ -_)  _| || | '_ \\
 |___/\__,_/__/_||_| |___/\___|\__|\_,_| .__/
                                       |_|       
"""

    def __init__(self, conf: Conf) -> None:
        self.conf = conf

        self.entries = [MenuEntry(entry=self.format_entry(BashOptions.NAMESPACE),
                                  function=self.set_robot_namespace),
                        MenuEntry(entry=self.format_entry(BashOptions.DOMAIN_ID),
                                  function=self.set_ros_domain_id),
                        MenuEntry(entry=self.format_entry(BashOptions.RMW),
                                  function=self.set_rmw_implementation),
                        MenuEntry(entry=self.format_entry(BashOptions.DIAGNOSTICS),
                                  function=self.set_turtlebot4_diagnostics),
                        MenuEntry(entry=self.format_entry(BashOptions.WORKSPACE),
                                  function=self.set_workspace_setup),
                        MenuEntry(entry=self.format_entry(BashOptions.CYCLONEDDS_URI),
                                  function=self.set_cyclonedds_uri),
                        MenuEntry(entry=self.format_entry(BashOptions.FASTRTPS_URI),
                                  function=self.set_fastrtps_default_profiles_file),
                        MenuEntry('', None),
                        MenuEntry(entry='Apply Defaults', function=self.apply_defaults),
                        MenuEntry(entry='Save', function=self.save_settings),]

        self.menu = Menu(self.title, self.entries)

    def format_entry(self, option: BashOptions):
        if option == BashOptions.DIAGNOSTICS:
            return lambda: '{0}{1}[{2}]'.format(
                option,
                ' ' * (35-len(option)),
                'Enabled' if self.conf.get(option) == '1' else 'Disabled')
        else:
            return lambda: '{0}{1}[{2}]'.format(
                option,
                ' ' * (35-len(option)),
                '' if self.conf.get(option) is None else self.conf.get(option))

    def show(self):
        self.conf.read()
        self.menu.show()

    def set_rmw_implementation(self):
        options = OptionsMenu(title=BashOptions.RMW,
                              menu_entries=['rmw_fastrtps_cpp', 'rmw_cyclonedds_cpp'],
                              default_option=self.conf.get(BashOptions.RMW))
        self.conf.set(BashOptions.RMW, options.show())

    def set_ros_domain_id(self):
        p = Prompt(prompt='{0} [{1}]: '.format(
                        BashOptions.DOMAIN_ID,
                        self.conf.get(BashOptions.DOMAIN_ID)),
                   default_response=self.conf.get(BashOptions.DOMAIN_ID),
                   response_type=int,
                   note='(0-101) or (215-232)')
        self.conf.set(BashOptions.DOMAIN_ID, p.show())

    def set_cyclonedds_uri(self):
        p = Prompt(prompt='{0} [{1}]: '.format(
                        BashOptions.CYCLONEDDS_URI,
                        self.conf.get(BashOptions.CYCLONEDDS_URI)),
                   default_response=self.conf.get(BashOptions.CYCLONEDDS_URI),
                   note='Full path to .xml file')
        self.conf.set(BashOptions.CYCLONEDDS_URI, p.show())

    def set_fastrtps_default_profiles_file(self):
        p = Prompt(prompt='{0} [{1}]: '.format(
                        BashOptions.FASTRTPS_URI,
                        self.conf.get(BashOptions.FASTRTPS_URI)),
                   default_response=self.conf.get(BashOptions.FASTRTPS_URI),
                   note='Full path to .xml file')
        self.conf.set(BashOptions.FASTRTPS_URI, p.show())

    def set_workspace_setup(self):
        p = Prompt(prompt='{0} [{1}]: '.format(
                    BashOptions.WORKSPACE,
                    self.conf.get(BashOptions.WORKSPACE)),
                   default_response=self.conf.get(BashOptions.WORKSPACE),
                   note='Full path to setup.bash file')
        self.conf.set(BashOptions.WORKSPACE, p.show())

    def set_robot_namespace(self):
        p = Prompt(prompt='{0} [{1}]: '.format(
                        BashOptions.NAMESPACE,
                        '' if self.conf.get(BashOptions.NAMESPACE) is None else
                        self.conf.get(BashOptions.NAMESPACE)),
                   default_response=self.conf.get(BashOptions.NAMESPACE),
                   note='ROS2 namespace')
        # Add '/' if needed
        ns = p.show()
        if ns != None and ns[0] != '/':
            ns = '/' + ns
        self.conf.set(BashOptions.NAMESPACE, ns)

    def set_turtlebot4_diagnostics(self):
        options = OptionsMenu(title=BashOptions.DIAGNOSTICS,
                              menu_entries=['Enabled', 'Disabled'],
                              default_option='Enabled' if self.conf.get(BashOptions.DIAGNOSTICS) == '1' else 'Disabled')
        self.conf.set(BashOptions.DIAGNOSTICS, '1' if options.show() == 'Enabled' else '0')

    def save_settings(self):
        self.conf.write()
        self.menu.exit()

    def apply_defaults(self):
        self.conf.apply_default(self.conf.bash_conf)


class DiscoveryServer():
    title = """
  ___  _                               ___       
 |   \(_)___ __ _____ _____ _ _ _  _  / __| ___ _ ___ _____ _ _
 | |) | (_-</ _/ _ \ V / -_) '_| || | \__ \/ -_) '_\ V / -_) '_|
 |___/|_/__/\__\___/\_/\___|_|  \_, | |___/\___|_|  \_/\___|_|
                                |__/                          
"""

    def __init__(self, configs: Conf) -> None:
        self.conf = configs

        self.entries = [MenuEntry(entry=self.format_entry('Enabled', DiscoveryOptions.ENABLED),
                                  function=self.set_enabled),
                        MenuEntry(entry=self.format_entry('IP', DiscoveryOptions.IP),
                                  function=self.set_ip),
                        MenuEntry(entry=self.format_entry('Port', DiscoveryOptions.PORT),
                                  function=self.set_port),
                        MenuEntry('', None),
                        MenuEntry(entry='Apply Defaults', function=self.apply_defaults),
                        MenuEntry(entry='Save', function=self.save_settings)]

        self.menu = Menu(title=self.title, menu_entries=self.entries)

    def format_entry(self, name, opt: DiscoveryOptions):
        return lambda: '{0}{1}[{2}]'.format(
            name,
            ' ' * (12 - len(name)),
            self.conf.get(opt))

    def show(self):
        self.menu.show()

    def set_enabled(self):
        options = OptionsMenu(title='Fast-DDS Discovery Server',
                              menu_entries=['True', 'False'],
                              default_option=self.conf.get(DiscoveryOptions.ENABLED))
        self.conf.set(DiscoveryOptions.ENABLED, options.show() == 'True')

    def set_ip(self):
        p = Prompt(prompt='IP [{0}]: '.format(self.conf.get(DiscoveryOptions.IP)),
                   default_response=self.conf.get(DiscoveryOptions.IP),
                   note='Discovery Server IP')
        self.conf.set(DiscoveryOptions.IP, p.show())

    def set_port(self):
        p = Prompt(prompt='Port [{0}]: '.format(self.conf.get(DiscoveryOptions.PORT)),
                   default_response=self.conf.get(DiscoveryOptions.PORT),
                   response_type=int,
                   note='Discovery Server Port')
        self.conf.set(DiscoveryOptions.PORT, p.show())

    def apply_defaults(self):
        self.conf.apply_default(self.conf.discovery_conf)

    def save_settings(self):
        self.conf.write_discovery()
        self.menu.exit()


class RobotUpstart():

    title = """
  ___     _         _     _   _         _            _   
 | _ \___| |__  ___| |_  | | | |_ __ __| |_ __ _ _ _| |_ 
 |   / _ \ '_ \/ _ \  _| | |_| | '_ (_-<  _/ _` | '_|  _|
 |_|_\___/_.__/\___/\__|  \___/| .__/__/\__\__,_|_|  \__|
                               |_|                      
"""

    def __init__(self, configs: Conf) -> None:
        self.conf = configs
        self.entries = [MenuEntry(entry='Restart',
                                  function=self.restart),
                        MenuEntry(entry='Start',
                                  function=self.start),
                        MenuEntry(entry='Stop',
                                  function=self.stop),
                        MenuEntry(entry='Install',
                                  function=self.install),
                        MenuEntry(entry='Uninstall',
                                  function=self.uninstall),
                        MenuEntry(entry='',function=None),
                        MenuEntry(entry='Status',
                                  function=self.view_service_status)]

        self.menu = Menu(self.title, self.entries)

    def show(self):
        self.menu.show()

    def view_service_status(self):
        try:
            subprocess.run(shlex.split('sudo systemctl status turtlebot4.service'))
        except KeyboardInterrupt:
            pass

    def stop(self):
        subprocess.run(shlex.split('sudo systemctl stop turtlebot4.service'))

    def start(self):
        subprocess.run(shlex.split('sudo systemctl start turtlebot4.service'))

    def restart(self):
        subprocess.run(shlex.split('sudo systemctl restart turtlebot4.service'))

    def daemon_reload(self):
        subprocess.run(shlex.split('sudo systemctl daemon-reload'))

    def install(self):
        self.uninstall()

        rmw = os.environ['RMW_IMPLEMENTATION']
        if rmw == 'rmw_fastrtps_cpp':
            rmw_config = os.environ['FASTRTPS_DEFAULT_PROFILES_FILE']
        else:
            rmw_config = os.environ['CYCLONEDDS_URI']

        turtlebot4_job = robot_upstart.Job(
            name='turtlebot4',
            workspace_setup=os.environ['ROBOT_SETUP'],
            rmw=rmw,
            rmw_config=rmw_config)

        turtlebot4_job.symlink = True
        turtlebot4_job.add(package='turtlebot4_bringup',
                           filename='launch/{0}.launch.py'.format(
                            self.conf.get(SystemOptions.MODEL)))
        turtlebot4_job.install()

        if self.conf.get(DiscoveryOptions.ENABLED) and self.conf.get(DiscoveryOptions.IP) == '127.0.0.1':
            discovery_job = robot_upstart.Job(workspace_setup=os.environ['ROBOT_SETUP'])
            discovery_job.install(Provider=TurtleBot4Extras)
            subprocess.run(shlex.split('sudo systemctl restart discovery.service'))

        self.daemon_reload()

    def uninstall(self):
        self.stop()

        turtlebot4_job = robot_upstart.Job(
            name='turtlebot4',
            workspace_setup=os.environ['ROBOT_SETUP'])

        turtlebot4_job.uninstall()

        self.daemon_reload()


class TurtleBot4Extras(robot_upstart.providers.Generic):
    def post_install(self):
        pass

    def generate_install(self):
        with open('/etc/turtlebot4/discovery.conf') as f:
            discovery_conf_contents = f.read()
        with open('/etc/turtlebot4/discovery.sh') as f:
            discovery_sh_contents = f.read()
        return {
            "/lib/systemd/system/discovery.service": {
                "content": discovery_conf_contents,
                "mode": 0o644
            },
            "/usr/sbin/discovery": {
                "content": discovery_sh_contents,
                "mode": 0o755
            },
            "/etc/systemd/system/multi-user.target.wants/discovery.service": {
                "symlink": "/lib/systemd/system/discovery.service"
            }}
