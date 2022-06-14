#!/usr/bin/env python3
# Copyright 2022 Clearpath Robotics, Inc.
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
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

import sys

import robot_upstart


def help():
    print('TurtleBot 4 robot_upstart install script.')
    print('Usage: install.py [model] <ROS_DOMAIN_ID>')
    print('models: lite, standard')
    print('ROS_DOMAIN_ID: optional, defaults to 0')


argc = len(sys.argv)

if argc == 1:
    print('Model required.')
    help()
    sys.exit(1)

model = sys.argv[1]
if model != 'lite' and model != 'standard':
    print('Invalid model {0}'.format(model))
    help()
    sys.exit(2)

domain_id = 0
if argc == 3:
    try:
        domain_id = int(sys.argv[2])
    except ValueError:
        print('Invalid ROS_DOMAIN_ID {0}'.format(sys.argv[2]))
        help()
        sys.exit(3)

print('Installing TurtleBot 4 {0}. ROS_DOMAIN_ID={1}'.format(model, domain_id))

turtlebot4_job = robot_upstart.Job(name='turtlebot4',
                                   rmw='rmw_cyclonedds_cpp',
                                   rmw_config='/etc/cyclonedds_rpi.xml',
                                   workspace_setup='/opt/ros/galactic/setup.bash',
                                   ros_domain_id=domain_id)

turtlebot4_job.symlink = True
turtlebot4_job.add(package='turtlebot4_bringup', filename='launch/{0}.launch.py'.format(model))
turtlebot4_job.install()
