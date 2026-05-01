#!/usr/bin/env python3
"""RosSim Full System Launch File"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='rossim_core', executable='vehicle_model.py', name='vehicle_model', output='screen'),
        Node(package='vehicle_viz', executable='vehicle_display.py', name='vehicle_display', output='screen'),
        Node(package='vehicle_control_gui', executable='control_panel.py', name='vehicle_control_panel', output='screen'),
        Node(package='vehicle_options_gui', executable='options_panel.py', name='vehicle_options_panel', output='screen'),
    ])
