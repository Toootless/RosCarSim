#!/bin/bash
# RosSim Startup Script

cd ~/RosSim_ws
source venv/bin/activate
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch rossim_core rossim_full.launch.py
