# RosSim - ROS2 Jazzy Vehicle Simulation with Multi-Window GUI

A comprehensive vehicle simulation system for ROS2 Jazzy designed for desktop Linux sandbox or Raspberry Pi deployment. Features interactive GUIs for vehicle visualization, control, and advanced options including ADAS capabilities.

## Project Overview

This project integrates multiple GUI windows for:
1. **Vehicle Visualization** - Real-time simulated vehicle state display
2. **Vehicle Controls** - Steering wheel, brake, accelerator (gas), and PRNDL (Park, Reverse, Neutral, Drive, Low) controls
3. **Vehicle Options** - Configuration for safety systems (ABS, traction control) and ADAS features (lane centering, adaptive cruise control, backup camera)

All windows communicate in real-time, updating based on user selections and vehicle state.

## Target Platform

- **Operating System**: ROS2 Jazzy on Linux
- **Supported Hardware**:
  - Desktop Linux sandbox/virtual machine
  - Raspberry Pi (5 recommended, Pi 4 with limitations)
- **Python Version**: 3.10+
- **Build System**: colcon + ament_cmake/ament_python

## Base Projects & Attribution

This project builds upon two excellent open-source educational resources:

### 1. MicroROS-Car-Pi5
- **Creator**: Yahboom Technology
- **Repository**: [MicroROS-Car-Pi5 on GitHub](https://github.com/YahboomTechnology/MicroROS-Car-Pi5)
- **License**: (See original repository)
- **Features Used**:
  - ROS2 vehicle control patterns
  - Python3 implementation examples
  - Hardware interface patterns
- **Original Target**: ROS2-HUMBLE, Raspberry Pi 5
- **Note**: Adapted for ROS2-JAZZY compatibility

### 2. ROS on Raspberry Pi
- **Repository**: ros-raspberry-pi
- **Features Used**:
  - ROS2 workspace structure and best practices
  - Docker-based development environment
  - Package creation patterns
- **Original Target**: ROS2-IRON
- **Note**: Adapted for ROS2-JAZZY compatibility

### Attribution in Code

All source files derived from or adapted from these projects include attribution headers:

```python
# Adapted from [Project Name]
# Original work by [Author/Organization]
# URL: [Original Repository URL]
# Licensed under [Original License]
```

## Project Structure

```
RosSim/
├── src/
│   └── rossim_core/
│       ├── rossim_core/
│       │   ├── __init__.py
│       │   ├── vehicle_model.py       # Vehicle state and physics
│       │   ├── control_manager.py     # Central control logic
│       │   └── adas_manager.py        # ADAS features (lane center, ACC, etc.)
│       ├── resource/
│       └── [setup files...]
│   ├── vehicle_viz/                   # Visualization GUI Window
│   │   ├── vehicle_viz/
│   │   │   └── vehicle_display.py    # Vehicle state visualization
│   │   └── [setup files...]
│   ├── vehicle_control_gui/           # Control GUI Window
│   │   ├── vehicle_control_gui/
│   │   │   └── control_panel.py      # Steering wheel, brake, gas, PRNDL
│   │   └── [setup files...]
│   └── vehicle_options_gui/           # Options GUI Window
│       ├── vehicle_options_gui/
│       │   └── options_panel.py      # ABS, traction control, ADAS settings
│       └── [setup files...]
├── docs/
│   ├── COMPATIBILITY.md               # ROS2 Jazzy compatibility notes
│   ├── INSTALLATION.md                # Setup and installation guide
│   ├── ARCHITECTURE.md                # System architecture
│   └── ATTRIBUTION.md                 # Detailed attribution
├── launch/
│   └── rossim_full.launch.py          # Launch all components
└── README.md                          # This file
```

## ROS2 Jazzy Compatibility Notes

⚠️ **Important**: The base projects use ROS2-HUMBLE and ROS2-IRON. Jazzy compatibility requires:

- [ ] Update all dependencies in `package.xml` files
- [ ] Test Python3 compatibility (Jazzy uses Python 3.10+)
- [ ] Verify all imported ROS2 packages support Jazzy
- [ ] Check display server compatibility (if using Raspberry Pi)

See [COMPATIBILITY.md](docs/COMPATIBILITY.md) for detailed compatibility checking.

## Installation

### Prerequisites
- ROS2 Jazzy installed and sourced
- Python 3.10 or higher
- colcon build tool

### Setup

```bash
# Clone/navigate to workspace
cd ~/your_ros2_workspace

# Create src directory if needed
mkdir -p src

# Copy RosSim into src
cp -r RosSim src/

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build all packages
colcon build

# Source the workspace
source install/setup.bash

# Launch the full system
ros2 launch rossim_core rossim_full.launch.py
```

## Key Features (In Development)

- **Real-time Vehicle Visualization**: Display vehicle orientation, speed, and status
- **Interactive Controls**: 
  - Steering wheel (±360° range)
  - Brake and acceleration pedals
  - PRNDL transmission selector
- **Safety Systems**:
  - ABS (Anti-lock Braking System) toggle
  - Traction control toggle
- **ADAS (Advanced Driver Assistance Systems)**:
  - Lane centering assist
  - Adaptive Cruise Control (ACC)
  - Backup camera view
- **Multi-Window Communication**: Real-time updates across all GUI windows

## Dependencies

See individual package `package.xml` files for complete dependency lists. Primary dependencies:
- rclpy (ROS2 Python client)
- PyQt5 or PySimpleGUI (GUI framework - TBD)
- std_msgs, geometry_msgs (ROS2 standard messages)
- sensor_msgs (for camera/sensor data)

## Development Notes

### Base Project References

When implementing features, refer to:
1. MicroROS-Car-Pi5 for vehicle control patterns
2. ros-raspberry-pi for ROS2 structure and best practices

### Future Enhancements

- Hardware integration (actual motor control, lidar, camera)
- 3D visualization (Gazebo simulation)
- Mobile app integration
- Multi-vehicle support
- Path planning and navigation

## License

This project integrates work from multiple sources with appropriate attribution. See [ATTRIBUTION.md](docs/ATTRIBUTION.md) for detailed licensing information.

## Support & Contact

For issues or questions about:
- **This integration**: Refer to project documentation
- **ROS2 Jazzy**: [ROS2 Jazzy Documentation](https://docs.ros.org)
- **Base Projects**: Contact original authors (see ATTRIBUTION.md)

## Change Log

- 2026-04-30: Project initialization, documentation structure created

---

**Last Updated**: April 30, 2026
