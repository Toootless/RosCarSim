# RosSim Quick Reference Guide

## Project Overview (30-Second Summary)

**RosSim** is a vehicle simulation system for ROS2 Jazzy with three interactive GUI windows:
- **Vehicle Visualization**: Real-time 3D-like display of vehicle state
- **Control Panel**: Steering wheel, pedals (gas/brake), PRNDL transmission
- **Options Panel**: Safety systems (ABS, traction control) and ADAS features

All windows communicate in real-time via ROS2 publish/subscribe messaging.

---

## Quick Links

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [PROJECT_README.md](PROJECT_README.md) | Project overview & features | 5 min |
| [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md) | Credit to base projects | 5 min |
| [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) | ROS2 Jazzy verification | 10 min |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & data flow | 15 min |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Setup & installation | 20 min |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Development plan & timeline | 15 min |

---

## Key Concepts

### Three GUI Windows

```
Vehicle Visualization          Vehicle Control GUI         Vehicle Options GUI
┌──────────────────┐          ┌──────────────────┐        ┌──────────────────┐
│  Display vehicle │          │  Input controls  │        │  Configure systems│
│  state in       │          │  • Steering      │        │  • ABS toggle    │
│  real-time      │          │  • Pedals        │        │  • Traction ctrl │
│                  │          │  • PRNDL         │        │  • Lane center   │
│  READ-ONLY      │          │  INPUT + FEEDBACK│        │  • ACC setup     │
│                  │          │                  │        │  • Backup camera │
└──────────────────┘          └──────────────────┘        └──────────────────┘
        ↓                              ↓                          ↓
   subscribes               publishes commands          publishes settings
     to state               reads vehicle state         reads system status
```

### ROS2 Communication

All windows talk through **ROS2 topics** (publish/subscribe):
- **Topics**: Named communication channels
- **Messages**: Data structures sent over topics
- **Nodes**: Programs that publish/subscribe to topics

**Example**: User moves steering wheel → Control GUI publishes to `/control/steering` → Vehicle Model subscribes and updates steering → Vehicle Model publishes new state to `/vehicle/state` → All GUIs subscribe and update display

### Core Components

| Component | Type | Role |
|-----------|------|------|
| Vehicle Model | Node | Simulates vehicle physics & state |
| Control Manager | Node | Routes commands from GUIs |
| Vehicle Viz | Node + GUI | Displays vehicle visualization |
| Control Panel | Node + GUI | Input steering, pedals, PRNDL |
| Options Panel | Node + GUI | Configure safety & ADAS systems |

---

## Getting Started Checklist

### 1️⃣ Before You Start
- [ ] Linux system (Ubuntu 22.04+ or Raspberry Pi OS)
- [ ] ROS2 Jazzy installed
- [ ] Python 3.10+
- [ ] ~2 GB free space

### 2️⃣ Installation (Follow docs/INSTALLATION.md)
```bash
# 1. Verify ROS2 Jazzy
echo $ROS_DISTRO  # Should be: jazzy

# 2. Create workspace
mkdir -p ~/RosSim_ws/src
cd ~/RosSim_ws

# 3. Copy RosSim into src directory
cp -r /path/to/RosSim/src/* ./src/

# 4. Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# 5. Build
colcon build

# 6. Source workspace
source install/setup.bash
```

### 3️⃣ Verify Installation
```bash
# Check packages built
ros2 pkg list | grep rossim

# Should see:
# - rossim_core
# - vehicle_control_gui
# - vehicle_options_gui
# - vehicle_viz
```

### 4️⃣ Launch Full System (When Ready)
```bash
ros2 launch rossim_core rossim_full.launch.py
```

---

## File Structure

```
RosSim/
├── PROJECT_README.md                 ← Start here
├── docs/
│   ├── ATTRIBUTION.md               ← Credit to base projects
│   ├── COMPATIBILITY.md             ← ROS2 Jazzy verification checklist
│   ├── ARCHITECTURE.md              ← System design deep-dive
│   ├── INSTALLATION.md              ← Setup instructions
│   ├── ROADMAP.md                   ← Development timeline & tasks
│   └── QUICK_REFERENCE.md           ← This file
├── src/                              ← ROS2 packages (to be created)
│   ├── rossim_core/
│   │   └── rossim_core/
│   │       ├── vehicle_model.py     ← Vehicle physics simulation
│   │       ├── control_manager.py   ← Command routing
│   │       └── adas_manager.py      ← ADAS logic
│   ├── vehicle_viz/
│   │   └── vehicle_viz/
│   │       └── vehicle_display.py   ← Visualization GUI
│   ├── vehicle_control_gui/
│   │   └── vehicle_control_gui/
│   │       └── control_panel.py     ← Control input GUI
│   └── vehicle_options_gui/
│       └── vehicle_options_gui/
│           └── options_panel.py     ← Options configuration GUI
├── launch/
│   └── rossim_full.launch.py        ← Launch all components
└── [Base project folders]
    ├── MicroROS-Car-Pi5-main/       ← Reference for vehicle control patterns
    └── ros-raspberry-pi-main/       ← Reference for ROS2 structure
```

---

## Common Commands

### Development

```bash
# Navigate to workspace
cd ~/RosSim_ws

# Build all packages
colcon build

# Build specific package
colcon build --packages-select vehicle_control_gui

# Build with verbose output
colcon build --event-handlers console_direct+

# Source workspace (after building)
source install/setup.bash

# Clean build
rm -rf build install log
colcon build
```

### Debugging & Monitoring

```bash
# List all ROS2 nodes running
ros2 node list

# List all published topics
ros2 topic list

# Echo topic messages in real-time
ros2 topic echo /vehicle/state

# Get info about a topic
ros2 topic info /vehicle/state

# Monitor system processes
top
htop  # if installed

# View ROS2 logs
ros2 run ros2 component list
```

### Troubleshooting

```bash
# Source ROS2 Jazzy (if not already sourced)
source /opt/ros/jazzy/setup.bash

# Source workspace (if built)
source ~/RosSim_ws/install/setup.bash

# Check installed packages
pip3 list | grep -E "rclpy|PyQt|PySimpleGUI|opencv"

# Reinstall Python dependencies
pip3 install --upgrade pip setuptools wheel
pip3 install rclpy pyqt5 opencv-python numpy

# Clean rebuild (slow but thorough)
cd ~/RosSim_ws
rm -rf build install log
colcon build --event-handlers console_direct+
```

---

## Architecture at a Glance

### Message Flow

```
User Input              Vehicle Simulation         Display Feedback
(GUI Windows)           (Model)                    (GUI Windows)

Steering Input  ──→  /control/steering  ──→  Vehicle Model  ──→  /vehicle/state  ──→  All GUIs Update
Throttle Input  ──→  /control/throttle  ──→  Physics Sim    ──→  Calculate State  ──→  Position Changes
Brake Input     ──→  /control/brake     ──→  Update Speed   ──→  Orientation Chng  ──→  Speed Display
PRNDL Input     ──→  /control/gear      ──→  Shift Gears    ──→  Publish State    ──→  Reflect Changes

ADAS Settings   ──→  /adas/settings     ──→  ADAS Manager   ──→  /adas/status     ──→  Options GUI Updates
```

### Key Topics

| Topic | Direction | Frequency | Content |
|-------|-----------|-----------|---------|
| `/vehicle/state` | Publish | 50 Hz | Position, velocity, orientation, gear, etc. |
| `/control/steering` | Subscribe | 10 Hz | Steering angle command |
| `/control/throttle` | Subscribe | 10 Hz | Gas pedal position |
| `/control/brake` | Subscribe | 10 Hz | Brake pedal position |
| `/control/gear` | Subscribe | On change | Gear selection (P/R/N/D/L) |
| `/adas/settings` | Subscribe | On change | System configuration |
| `/adas/status` | Publish | 10 Hz | System status feedback |
| `/vehicle/diagnostics` | Publish | 5 Hz | RPM, fuel, temperature, etc. |

---

## Development Tips

### Writing a New ROS2 Node

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.publisher_ = self.create_publisher(Float32, 'my_topic', 10)
        self.subscription = self.create_subscription(
            Float32, 'input_topic', self.listener_callback, 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

    def timer_callback(self):
        msg = Float32()
        msg.data = 42.0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### GUI Framework Quick Start

**PySimpleGUI Example:**
```python
import PySimpleGUI as sg

layout = [
    [sg.Text('Hello World')],
    [sg.Button('OK'), sg.Button('Cancel')]
]

window = sg.Window('My App', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    if event == 'OK':
        print('OK clicked')

window.close()
```

### Integrating ROS2 with PySimpleGUI

```python
import rclpy
import threading
import PySimpleGUI as sg
from rclpy.node import Node

class MyGUINode(Node):
    def __init__(self, window_queue):
        super().__init__('my_gui_node')
        self.window_queue = window_queue
        self.subscription = self.create_subscription(
            Float32, 'topic', self.callback, 10)

    def callback(self, msg):
        # Send update to GUI via queue
        self.window_queue.put(('update', msg.data))

# Run ROS2 in background thread
def ros_thread(window_queue):
    rclpy.init()
    node = MyGUINode(window_queue)
    rclpy.spin(node)

# Main GUI thread
import queue
q = queue.Queue()
threading.Thread(target=ros_thread, args=(q,), daemon=True).start()

# GUI window with periodic queue checks
window = sg.Window('App', [[sg.Text('Value: 0')]])
while True:
    event, values = window.read(timeout=100)
    
    try:
        msg_type, msg_data = q.get_nowait()
        if msg_type == 'update':
            # Update window with new data
            pass
    except queue.Empty:
        pass
    
    if event == sg.WINDOW_CLOSED:
        break
```

---

## Troubleshooting Guide

### Problem: "ros2: command not found"
**Solution**: Source ROS2 setup
```bash
source /opt/ros/jazzy/setup.bash
```

### Problem: "No module named 'rclpy'"
**Solution**: Rebuild workspace after ROS2 installation
```bash
cd ~/RosSim_ws
colcon build
source install/setup.bash
```

### Problem: GUI won't start
**Solution**: Check display and Python path
```bash
# Verify Python
python3 --version  # Should be 3.10+

# Check display (if using SSH)
echo $DISPLAY  # Should show :0 or :1

# Or use X11 forwarding
ssh -X user@host
```

### Problem: Topics not communicating
**Solution**: Verify ROS2_DOMAIN_ID and sourcing
```bash
# Check domain ID
echo $ROS2_DOMAIN_ID

# Verify node is running
ros2 node list

# Echo topic
ros2 topic echo /vehicle/state
```

### Problem: Slow performance on Raspberry Pi
**Solution**: Monitor and optimize
```bash
# Check CPU/memory usage
top

# Reduce publishing rates in code
self.create_timer(0.05, callback)  # Instead of 0.02

# Use lightweight GUI framework
# (PySimpleGUI preferred over PyQt5)
```

---

## Next Steps

1. **Read** [docs/INSTALLATION.md](docs/INSTALLATION.md) - Set up environment
2. **Review** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Understand system design
3. **Check** [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) - Verify ROS2 Jazzy
4. **Start** Phase 2 tasks from [docs/ROADMAP.md](docs/ROADMAP.md)

---

## Resources

- **ROS2 Documentation**: https://docs.ros.org/en/jazzy/
- **ROS2 Tutorials**: https://docs.ros.org/en/jazzy/Tutorials.html
- **colcon Build Tool**: https://colcon.readthedocs.io/
- **PySimpleGUI**: https://pysimplegui.readthedocs.io/
- **PyQt5**: https://www.riverbankcomputing.com/software/pyqt/

---

## Base Projects Attribution

This project integrates work from:
1. **Yahboom MicroROS-Car-Pi5** - Vehicle control patterns
2. **ros-raspberry-pi** - ROS2 structure and best practices

See [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md) for detailed credits.

---

**Quick Reference Last Updated**: April 30, 2026

**Status**: 🟡 Ready to begin Phase 2 (Jazzy Verification)

**Questions?** See [PROJECT_README.md](PROJECT_README.md) or individual docs for detailed info.
