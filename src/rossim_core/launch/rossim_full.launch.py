#!/usr/bin/env python3
"""RosSim Full System Launch - Unified Dashboard"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='rossim_core', executable='vehicle_model.py', name='vehicle_model', output='screen'),
        Node(package='vehicle_viz', executable='unified_dashboard.py', name='unified_dashboard', output='screen'),
    ])
