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

import argparse

import sys

import robot_upstart


parser = argparse.ArgumentParser()

parser.add_argument('model', type=str)
parser.add_argument('--domain', type=int, default=0)
parser.add_argument('--rmw', type=str, default='rmw_cyclonedds_cpp')

args = parser.parse_args()

if args.model != 'lite' and args.model != 'standard':
    print('Invalid model: {0}'.format(args.model))
    parser.print_help()
    sys.exit(1)

model = args.model

domain_id = 0
if (args.domain >= 0 and args.domain <= 101) or \
   (args.domain >= 215 and args.domain <= 232):
    domain_id = args.domain
else:
    print('Invalid ROS_DOMAIN_ID: {0}'.format(args.domain))
    parser.print_help()
    sys.exit(2)

rmw = 'rmw_cyclonedds_cpp'
if args.rmw == 'rmw_fastrtps_cpp' or args.rmw == 'rmw_cyclonedds_cpp':
    rmw = args.rmw
else:
    print('Invalid RMW {0}'.format(args.rmw))
    parser.print_help()
    sys.exit(3)

print('Installing TurtleBot 4 {0}. ROS_DOMAIN_ID={1}, RMW_IMPLEMENTATION={2}'.format(model, domain_id, rmw))

if rmw == 'rmw_cyclonedds_cpp':
    rmw_config = '/etc/cyclonedds_rpi.xml'
else:
    rmw_config = None

turtlebot4_job = robot_upstart.Job(name='turtlebot4',
                                   rmw=rmw,
                                   rmw_config=rmw_config,
                                   workspace_setup='/opt/ros/galactic/setup.bash',
                                   ros_domain_id=domain_id)

turtlebot4_job.symlink = True
turtlebot4_job.add(package='turtlebot4_bringup', filename='launch/{0}.launch.py'.format(model))
turtlebot4_job.install()
