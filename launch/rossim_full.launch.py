#!/usr/bin/env python3
"""
RosSim Full Launch File

Launches all components of the RosSim system:
- Vehicle Model Node (physics simulation)
- Control Manager Node (command routing)
- ADAS Manager Node (advanced driver assistance)
- Vehicle Visualization GUI
- Vehicle Control GUI
- Vehicle Options GUI

ROS2 Jazzy
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """Generate launch description with all RosSim nodes"""
    
    # Launch arguments
    log_level = DeclareLaunchArgument(
        'log_level',
        default_value='info',
        description='Logging level for all nodes'
    )
    
    return LaunchDescription([
        log_level,
        
        # Core simulation nodes
        Node(
            package='rossim_core',
            executable='vehicle_model',
            name='vehicle_model',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
        
        Node(
            package='rossim_core',
            executable='control_manager',
            name='control_manager',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
        
        Node(
            package='rossim_core',
            executable='adas_manager',
            name='adas_manager',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
        
        # GUI nodes
        Node(
            package='vehicle_viz',
            executable='vehicle_display',
            name='vehicle_viz',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
        
        Node(
            package='vehicle_control_gui',
            executable='control_panel',
            name='control_panel',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
        
        Node(
            package='vehicle_options_gui',
            executable='options_panel',
            name='options_panel',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
            emulate_tty=True,
        ),
    ])


if __name__ == '__main__':
    generate_launch_description()
