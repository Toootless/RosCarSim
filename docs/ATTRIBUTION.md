# Attribution & Licensing

This project incorporates work from open-source projects. We are committed to giving proper credit to the original authors and maintaining compliance with their licenses.

## Base Projects

### 1. Yahboom MicroROS-Car-Pi5

**Project Name**: Raspberry Pi 5 ROS2 Robot Car (MicroROS-Car-Pi5)

**Creator**: Yahboom Technology

**Repository**: https://github.com/YahboomTechnology/MicroROS-Car-Pi5

**Description**: Educational ROS2 robot car platform for Raspberry Pi 5, featuring:
- ROS2-HUMBLE + Python3 programming
- Vehicle motion control
- AI visual interaction with MediaPipe
- SLAM mapping and navigation
- Multi-machine control
- OpenCV image processing

**Components Used In RosSim**:
- Vehicle control patterns and message structures
- Motor control implementation examples
- ROS2 node architecture patterns
- Python3 package structure

**License**: [Check original repository for license details]

**Website**: https://category.yahboom.net/products/microros-pi5

**Contact**: 
- Technical Support: support@yahboom.com
- WhatsApp: +86 18682378128

**Attribution in Our Code**:
```python
# Adapted from MicroROS-Car-Pi5 by Yahboom Technology
# Original: https://github.com/YahboomTechnology/MicroROS-Car-Pi5
# Used for vehicle control patterns and ROS2 architecture
```

---

### 2. ROS on Raspberry Pi

**Repository**: ros-raspberry-pi (from GitHub educational resources)

**Description**: Beginner-friendly guide to ROS on Raspberry Pi, featuring:
- Docker-based ROS development environment
- ROS2 workspace creation and management
- Publisher-subscriber pattern examples
- Package structure best practices
- colcon build system usage

**Components Used In RosSim**:
- ROS2 workspace structure
- Package organization best practices
- colcon build configuration templates
- Docker integration patterns
- Launch file examples

**Attribution in Our Code**:
```python
# Adapted from ros-raspberry-pi educational materials
# Used for ROS2 workspace structure and build system patterns
```

---

## ROS2 Jazzy Compatibility Notes

The base projects target ROS2-HUMBLE and ROS2-IRON respectively. This project updates components for **ROS2-Jazzy** compatibility:

| Component | Original | Updated For |
|-----------|----------|-------------|
| ROS2 Version | HUMBLE / IRON | JAZZY |
| Python Version | 3.8+ | 3.10+ |
| Build System | colcon | colcon (updated) |
| Key Packages | See package.xml | Updated for Jazzy |

See [COMPATIBILITY.md](COMPATIBILITY.md) for detailed compatibility information.

---

## Licensing

### Our Project

This RosSim project is developed as an integration and educational tool. All original code includes appropriate attribution to source projects.

### Base Project Licenses

- **MicroROS-Car-Pi5**: [Check original repository - typically educational/open-source]
- **ros-raspberry-pi**: [Check original repository]

Users should review the original project licenses before use.

---

## Code Attribution Headers

All files adapted from or derived from the base projects include headers like:

```python
"""
[Module Description]

Adapted from: [Original Project Name]
Original Author: [Author/Organization]
Original Repository: [URL]
Changes: [What was adapted/modified]
ROS2 Version: Jazzy
"""
```

---

## Acknowledgments

We thank:
- **Yahboom Technology** for comprehensive ROS2 robot car educational materials
- **ROS Community** for excellent documentation and examples
- **Open Robotics** for ROS2 framework
- All contributors to the base projects

---

## How to Contribute

When contributing to RosSim:

1. If using code patterns from base projects, include attribution
2. If adding new dependencies, verify they support ROS2 Jazzy
3. Update compatibility matrix when adding new components
4. Follow existing attribution patterns in code

---

## Questions or Issues?

For questions about:
- **Attribution & Licensing**: Review this document and original repositories
- **ROS2 Jazzy Compatibility**: See COMPATIBILITY.md
- **Original Project Features**: Contact original authors (see contacts above)

---

**Last Updated**: April 30, 2026
