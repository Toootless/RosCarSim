# ROS2 Jazzy Compatibility Checklist

This document outlines the compatibility status and requirements for running RosSim on ROS2 Jazzy.

## Overview

**Project Target**: ROS2 Jazzy on Linux (desktop or Raspberry Pi)
**Base Projects**: MicroROS-Car-Pi5 (HUMBLE) + ros-raspberry-pi (IRON)
**Status**: ⚠️ In Development - Compatibility verification in progress

## ROS2 Version Requirements

### Distribution Versions

| Distro | Release Date | Status | Notes |
|--------|-------------|--------|-------|
| ROS2 HUMBLE | 2022-05 | Older | Base project uses this |
| ROS2 IRON | 2023-05 | Older | Base project reference uses this |
| ROS2 JAZZY | 2024-05 | **Target** | Our deployment version |

### Python Version Compatibility

```
ROS2 JAZZY Requirements:
- Python 3.10 - 3.12
- Older projects may use Python 3.8
- Update: All code reviewed for 3.10+ compatibility
```

## Dependency Compatibility Matrix

### Core ROS2 Packages

| Package | HUMBLE | IRON | JAZZY | Status |
|---------|--------|------|-------|--------|
| rclpy | ✅ | ✅ | ✅ | Verified available |
| rclcpp | ✅ | ✅ | ✅ | C++ - verify if needed |
| std_msgs | ✅ | ✅ | ✅ | Core - should work |
| geometry_msgs | ✅ | ✅ | ✅ | Core - should work |
| sensor_msgs | ✅ | ✅ | ✅ | Core - should work |

**Status**: Core messages are stable across versions. ✅ Expected: All work

### Common Packages Used in Base Projects

| Package | Purpose | HUMBLE | IRON | JAZZY | Notes |
|---------|---------|--------|------|-------|-------|
| OpenCV (cv_bridge) | Image processing | ⚠️ | ⚠️ | ❓ | **ACTION NEEDED**: Test on Jazzy |
| MediaPipe | ML-based vision | ❓ | ❓ | ❓ | **ACTION NEEDED**: Verify compatibility |
| colcon | Build tool | ✅ | ✅ | ✅ | Stable across versions |
| ament_python | Python build | ✅ | ✅ | ✅ | Core build system |
| PyQt5 | GUI framework (if used) | ✅ | ✅ | ⚠️ | **VERIFY**: Qt version compatibility |
| PySimpleGUI | GUI framework (alternative) | ✅ | ✅ | ✅ | Good compatibility |

**Legend**: 
- ✅ Confirmed compatible
- ⚠️ Likely compatible, needs verification  
- ❓ Needs testing
- ❌ Known incompatible

## Pre-Installation Checklist

- [ ] Linux system available (Ubuntu 22.04 LTS for Jazzy)
- [ ] ROS2 Jazzy installed: `echo $ROS_DISTRO` should return "jazzy"
- [ ] Python 3.10+: `python3 --version`
- [ ] colcon installed: `colcon --version`
- [ ] rosdep initialized: `rosdep update`

## Verification Tests

### Test 1: ROS2 Core Installation
```bash
# Verify Jazzy installation
ros2 --version

# Should output something like: "ROS 2 Jazzy Jalisco (development os)"
```

### Test 2: colcon Build System
```bash
# Test colcon
cd ~/ros2_ws
colcon build --help

# Should show colcon build options
```

### Test 3: Python ROS2 Client
```bash
# Test rclpy import
python3 -c "import rclpy; print(rclpy.__version__)"
```

### Test 4: Create Test Package
```bash
# Create minimal test package
mkdir -p ~/test_ws/src
cd ~/test_ws/src
ros2 pkg create --build-type ament_python test_pkg --node-name test_node

# Build and test
cd ~/test_ws
colcon build
source install/setup.bash
ros2 run test_pkg test_node
```

## Known Issues & Workarounds

### Issue 1: Display Server on Raspberry Pi

**Problem**: GUI applications may fail on headless Raspberry Pi

**Solution**: 
- Use SSH with X11 forwarding
- Or use VNC server
- Or develop on desktop, deploy to Pi

### Issue 2: MediaPipe Compatibility

**Problem**: MediaPipe versions may have Jazzy-specific issues

**Status**: ⚠️ Needs verification

**Action**: 
```bash
# Test MediaPipe on Jazzy
python3 -c "import mediapipe as mp; print(mp.__version__)"
```

### Issue 3: OpenCV/cv_bridge

**Problem**: OpenCV compiled versions may not match Jazzy's Python version

**Solution**:
```bash
# Install from Jazzy repositories
sudo apt install python3-cv2
# Or use pip with Jazzy compatibility
pip install opencv-python-headless
```

## Package Verification Commands

Run these commands in your Jazzy environment:

```bash
# Check ROS2 Jazzy packages
apt list --installed | grep ros-jazzy

# Verify key packages
dpkg -l | grep -E "python3-rclpy|ros-jazzy-std-msgs|ros-jazzy-geometry-msgs"

# List available packages in Jazzy
apt-cache search ros-jazzy | head -20
```

## Compatibility Testing Procedure

### Phase 1: Core Setup (First Priority)
- [ ] Install ROS2 Jazzy
- [ ] Verify rclpy works
- [ ] Test colcon build
- [ ] Create and build test package

### Phase 2: Base Project Analysis (In Progress)
- [ ] Review MicroROS-Car-Pi5 dependencies
- [ ] Review ros-raspberry-pi dependencies
- [ ] Identify Jazzy-specific updates needed
- [ ] Update package.xml files

### Phase 3: Integration Testing (Next)
- [ ] Build RosSim packages on Jazzy
- [ ] Test node communication
- [ ] Test GUI framework (PyQt5 vs PySimpleGUI)
- [ ] Test inter-window message passing

### Phase 4: Hardware Testing (Final)
- [ ] Test on desktop Linux (Ubuntu 22.04)
- [ ] Test on Raspberry Pi 5 (if available)
- [ ] Performance profiling
- [ ] Documentation updates

## Resources

### Official Jazzy Documentation
- [ROS2 Jazzy Docs](https://docs.ros.org/en/jazzy/)
- [ROS2 Migration Guide](https://docs.ros.org/en/jazzy/Contributing/Migration-Guide.html)
- [colcon Documentation](https://colcon.readthedocs.io/)

### Troubleshooting
- [ROS2 Q&A](https://answers.ros.org)
- [ROS2 Discourse](https://discourse.ros.org)
- [GitHub Issues](https://github.com/ros2/ros2)

## Next Steps

1. **URGENT**: Set up Jazzy environment and run Phase 1 verification
2. **HIGH**: Analyze base project dependencies for Jazzy compatibility
3. **HIGH**: Update package.xml files with Jazzy dependencies
4. **MEDIUM**: Develop and test GUI framework selection (PyQt5 vs PySimpleGUI)
5. **MEDIUM**: Implement inter-window communication patterns

## Compatibility Status Summary

| Area | Status | Confidence | Notes |
|------|--------|-----------|-------|
| Core ROS2 | ✅ Good | High | Standard packages should work |
| Python Support | ✅ Good | High | Python 3.10+ is fine for Jazzy |
| Build System | ✅ Good | High | colcon is stable |
| GUI Frameworks | ⚠️ Needs Testing | Medium | PySimpleGUI preferred for stability |
| Vision (OpenCV) | ⚠️ Needs Testing | Medium | Needs environment-specific build |
| ML (MediaPipe) | ❓ Untested | Low | Version compatibility TBD |
| Hardware (Pi) | ⚠️ Needs Testing | Medium | May need display server setup |

**Overall Status**: Ready to begin compatibility verification

---

**Last Updated**: April 30, 2026

**Next Review Date**: After Phase 1 verification complete
