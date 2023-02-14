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
import os
import sys

import robot_upstart

parser = argparse.ArgumentParser()

parser.add_argument('model', type=str)

args = parser.parse_args()

if args.model != 'lite' and args.model != 'standard':
    print('Invalid model: {0}'.format(args.model))
    parser.print_help()
    sys.exit(1)

model = args.model
domain_id = os.environ['ROS_DOMAIN_ID'] or 0
rmw = os.environ['RMW_IMPLEMENTATION'] or 'rmw_fastrtps_cpp'
workspace = os.environ['ROBOT_SETUP'] or '/opt/ros/humble/setup.bash'

print('Installing TurtleBot 4 {0}. ROS_DOMAIN_ID={1}, RMW_IMPLEMENTATION={2}'.format(model, domain_id, rmw))

if rmw == 'rmw_cyclonedds_cpp':
    rmw_config = os.environ['CYCLONEDDS_URI']
else:
    rmw_config = os.environ['FASTRTPS_DEFAULT_PROFILES_FILE']

turtlebot4_job = robot_upstart.Job(name='turtlebot4',
                                   rmw=rmw,
                                   rmw_config=rmw_config,
                                   workspace_setup=workspace,
                                   ros_domain_id=domain_id)

turtlebot4_job.symlink = True
turtlebot4_job.add(package='turtlebot4_bringup', filename='launch/{0}.launch.py'.format(model))
turtlebot4_job.install()
