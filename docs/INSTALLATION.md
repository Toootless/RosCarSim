# RosSim Installation & Setup Guide

## Prerequisites Checklist

Before you start, verify you have:

- [ ] Linux system (Ubuntu 22.04 LTS recommended, Raspberry Pi OS optional)
- [ ] ROS2 Jazzy installed
- [ ] Python 3.10 or higher
- [ ] colcon build system
- [ ] Git (for version control)
- [ ] ~2 GB free disk space

## Step 1: Verify ROS2 Jazzy Installation

### Check ROS2 Distro

```bash
echo $ROS_DISTRO
# Should output: jazzy
```

If empty, source your ROS2 installation:

```bash
source /opt/ros/jazzy/setup.bash
```

To make this permanent, add to `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Key Commands

```bash
# Check ROS2 version
ros2 --version

# Check colcon
colcon --version

# Check Python version
python3 --version
# Should be 3.10 or higher
```

## Step 2: Prepare Workspace

### Create ROS2 Workspace

```bash
# Navigate to your projects directory
cd ~/Documents/VS_projects

# Create workspace structure
mkdir -p RosSim_ws/src

# Navigate into workspace
cd RosSim_ws
```

### Copy RosSim Packages

```bash
# Copy the RosSim project into src
# Option A: If RosSim is already in a folder
cp -r ../RosSim/* ./

# Option B: If cloning from git (future)
# git clone <repository-url> ./src/rossim
```

### Verify Structure

```bash
ls -la src/
# Should see documentation and (eventually) ROS2 packages
```

## Step 3: Install System Dependencies

### Update Package Manager

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Required Tools

```bash
# ROS2 development tools
sudo apt install -y \
  python3-dev \
  python3-pip \
  build-essential

# GUI Framework dependencies (for PySimpleGUI or PyQt5)
sudo apt install -y \
  python3-tk

# Optional: For PyQt5 support
sudo apt install -y \
  python3-pyqt5
```

### Install ROS2 Dependencies

```bash
# Install rosdep if not already installed
sudo apt install -y python3-rosdep

# Initialize rosdep (if not already done)
sudo rosdep init
rosdep update
```

## Step 4: Create ROS2 Packages

Navigate to your workspace and create the necessary packages:

```bash
cd ~/Documents/VS_projects/RosSim_ws

# Make sure source directory exists
mkdir -p src

# Create core package (if not already existing)
cd src

# Create packages
ros2 pkg create --build-type ament_python rossim_core
ros2 pkg create --build-type ament_python vehicle_viz
ros2 pkg create --build-type ament_python vehicle_control_gui
ros2 pkg create --build-type ament_python vehicle_options_gui

# Return to workspace root
cd ..
```

### Verify Package Structure

```bash
ls -la src/
# Should see:
# - vehicle_control_gui/
# - vehicle_options_gui/
# - vehicle_viz/
# - rossim_core/
```

## Step 5: Install Python Dependencies

### Install Python Packages

**Note**: Modern Ubuntu/Debian (Python 3.12+) restricts system-wide pip installs (PEP 668). Use one of these approaches:

**Option A: Use System Packages (Recommended - No PEP 668 Issues)**

```bash
# Install via apt package manager
sudo apt install -y \
  python3-pysimplegui \
  python3-opencv \
  python3-numpy

# Or if using PyQt5 instead
sudo apt install -y python3-pyqt5
```

**Option B: Use Virtual Environment (If you need pip)**

```bash
# Create virtual environment in your workspace
cd ~/Documents/VS_projects/RosSim_ws
python3 -m venv venv

# Activate it
source venv/bin/activate

# Now pip works without restrictions
pip3 install --upgrade pip setuptools wheel
pip3 install PySimpleGUI opencv-python numpy

# Remember to activate before working:
# source venv/bin/activate
```

**Option C: Override PEP 668 (Not Recommended)**

```bash
# Only if absolutely necessary (risk breaking system packages)
pip3 install --break-system-packages PySimpleGUI numpy opencv-python
```

### Alternative: Using rosdep

For each package that has a `package.xml`, rosdep can install dependencies:

```bash
cd ~/Documents/VS_projects/RosSim_ws

# Install all dependencies from package.xml files
rosdep install --from-paths src --ignore-src -r -y
```

## Step 6: Build the Packages

### Build All Packages

```bash
# From workspace root
cd ~/Documents/VS_projects/RosSim_ws

# Build
colcon build

# Or with verbose output for debugging
colcon build --event-handlers console_direct+
```

### Expected Output

```
Starting >>> rossim_core
Finished <<< rossim_core [0.50s]
Starting >>> vehicle_viz
Finished <<< vehicle_viz [0.45s]
Starting >>> vehicle_control_gui
Finished <<< vehicle_control_gui [0.42s]
Starting >>> vehicle_options_gui
Finished <<< vehicle_options_gui [0.48s]

Summary: 4 packages built in 2.0s
```

### Troubleshooting Build Errors

**Error**: `ModuleNotFoundError: No module named 'rclpy'`
```bash
# Make sure ROS2 Jazzy is sourced
source /opt/ros/jazzy/setup.bash

# Try building again
colcon build
```

**Error**: `Could not find ament_cmake`
```bash
# Install build dependencies
sudo apt install -y python3-ament-cmake python3-ament-python

# Try building again
colcon build
```

## Step 7: Source Your Workspace

After successful build, source the workspace:

```bash
# Source the workspace
source ~/Documents/VS_projects/RosSim_ws/install/setup.bash

# Verify it worked (should see our package)
ros2 pkg list | grep rossim
# Should output: rossim_core, vehicle_control_gui, vehicle_options_gui, vehicle_viz
```

### Make Permanent

Add to `~/.bashrc`:

```bash
echo "source ~/Documents/VS_projects/RosSim_ws/install/setup.bash" >> ~/.bashrc
```

## Step 8: Verify Installation

### Check ROS2 Nodes

```bash
# List available nodes
ros2 pkg list | grep rossim

# List available topics (once nodes are running)
ros2 topic list
```

### Run a Test Package

```bash
# After sourcing workspace, try running a node (once created)
ros2 run rossim_core vehicle_model
# Should start the vehicle model node
```

## Step 9: Set Up Development Environment

### VS Code Setup

1. Install ROS2 extension in VS Code:
   - Press `Ctrl+Shift+X` (Extensions)
   - Search for "ROS2" 
   - Install recommended ROS2 extension

2. Open your workspace in VS Code:
   ```bash
   code ~/Documents/VS_projects/RosSim_ws
   ```

### Python Path Configuration

Create `.vscode/settings.json` in workspace root:

```json
{
  "python.defaultInterpreterPath": "/usr/bin/python3",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "autopep8",
  "[python]": {
    "editor.formatOnSave": true
  }
}
```

## Raspberry Pi Specific Setup

If deploying to Raspberry Pi 5:

### 1. Install ROS2 Jazzy on Pi

```bash
# Add ROS2 repository (if not already done)
sudo apt-add-repository universe

# Install ROS2 Jazzy
sudo apt install -y ros-jazzy-desktop

# Or minimal install
sudo apt install -y ros-jazzy-ros-core
```

### 2. Increase Swap Space (if needed)

```bash
# Check current swap
free -h

# Temporarily increase
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
sudo dphys-swapfile swapon
```

### 3. Set Up Display Server (for GUI)

**Option A: SSH with X11 forwarding**
```bash
# From desktop Linux:
ssh -X pi@raspberrypi.local

# Then run GUI applications
```

**Option B: VNC Server**
```bash
# Install on Pi
sudo apt install -y tightvncserver

# Start VNC server
tightvncserver :1 -geometry 1024x768 -depth 24

# Connect from desktop using VNC client
```

**Option C: Headless operation**
```bash
# Run without display, control via desktop ROS2 network
# Requires ROS2_DOMAIN_ID setup (see Network section)
```

## Network Setup (Optional: For Distributed Systems)

If running nodes on multiple machines:

### Set ROS2_DOMAIN_ID

```bash
# On both machines
export ROS2_DOMAIN_ID=0

# Make permanent
echo "export ROS2_DOMAIN_ID=0" >> ~/.bashrc
```

### Configure Firewall (if needed)

```bash
# Allow ROS2 ports (DDS typically uses UDP 7400-7409)
sudo ufw allow 7400:7409/udp

# Reload firewall
sudo ufw reload
```

## Troubleshooting Installation

### Issue: "ros2: command not found"
**Solution**: Source ROS2 setup file
```bash
source /opt/ros/jazzy/setup.bash
```

### Issue: "colcon: command not found"
**Solution**: Install colcon
```bash
sudo apt install -y python3-colcon-common-extensions
```

### Issue: "ModuleNotFoundError" during build
**Solution**: Install missing Python package
```bash
pip3 install <package_name>
```

### Issue: Build hangs or runs very slowly
**Solution**: Check system resources on Raspberry Pi
```bash
# Monitor system
top
# Press 'h' for help

# Check disk space
df -h

# Check memory
free -h
```

## Verify Installation Checklist

- [ ] ROS2 Jazzy sourced (`echo $ROS_DISTRO` shows "jazzy")
- [ ] colcon installed and working
- [ ] Python 3.10+ available
- [ ] Workspace created at `~/Documents/VS_projects/RosSim_ws`
- [ ] Packages created in `src/` directory
- [ ] All packages built successfully
- [ ] Workspace sourced in `.bashrc`
- [ ] ROS2 nodes and topics visible with `ros2 pkg list`
- [ ] Python dependencies installed
- [ ] VS Code configured (if using)

## Next Steps

1. ✅ Installation complete
2. → Proceed to [ARCHITECTURE.md](ARCHITECTURE.md) to understand system design
3. → Check [COMPATIBILITY.md](COMPATIBILITY.md) for version verification
4. → Start implementing nodes in `src/` packages

## Getting Help

**Error messages not covered here?**
- Check [ROS2 Troubleshooting](https://docs.ros.org/en/jazzy/Troubleshooting.html)
- Search [ROS Answers](https://answers.ros.org)
- Check VS Code terminal for detailed error output

**Need to rebuild?**

```bash
# Clean build
cd ~/Documents/VS_projects/RosSim_ws
rm -rf build install log
colcon build
```

---

**Last Updated**: April 30, 2026

**Installation Time**: ~30-60 minutes (depending on system)
