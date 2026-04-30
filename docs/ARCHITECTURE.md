# RosSim System Architecture

## Overview

RosSim is a multi-window GUI application for vehicle simulation on ROS2 Jazzy. Three independent GUI windows communicate through ROS2 pub/sub messaging and a central control node.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         ROS2 Jazzy Core                          │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                    ┌────────────┼────────────┐
                    │            │            │
        ┌───────────▼──┐  ┌──────▼─────┐  ┌──▼─────────────┐
        │ Vehicle Viz  │  │  Vehicle   │  │  Vehicle      │
        │ (Display)    │  │  Control   │  │  Options      │
        │              │  │  (Controls)│  │  (Config)     │
        └───────┬──────┘  └──────┬─────┘  └──┬─────────────┘
                │                │            │
                │ Subscribe      │            │ Publish
                │ (read-only)    │ Publish   │ Settings
                │                │ Commands  │
                └────────────────┼────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Control Manager       │
                    │  (Central Logic)       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Vehicle Model         │
                    │  (Physics & State)     │
                    └────────────────────────┘
```

## Nodes & Components

### 1. **Vehicle Model Node** (`vehicle_model.py`)
**Purpose**: Maintain vehicle state and physics simulation

**Responsibilities**:
- Track vehicle state (position, velocity, steering angle, etc.)
- Simulate vehicle physics (acceleration, deceleration, turning)
- Maintain ADAS system state (lane center assist, ACC, etc.)
- Simulate brake system (ABS if enabled)
- Simulate traction control if enabled

**Publishes**:
- `/vehicle/state` - Current vehicle state (position, velocity, orientation, etc.)
- `/vehicle/diagnostics` - Vehicle diagnostics (fuel, temperature, etc.)
- `/adas/status` - ADAS system status

**Subscribes**:
- `/vehicle/commands` - Steering, acceleration, braking commands
- `/adas/settings` - ADAS system configuration

**State Variables**:
```python
class VehicleState:
    # Motion
    position: (x, y, z)  # meters
    velocity: (vx, vy, vz)  # m/s
    orientation: (roll, pitch, yaw)  # radians
    steering_angle: float  # -π/6 to π/6 (±30°)
    
    # Engine & Transmission
    throttle: float  # 0.0 to 1.0
    brake: float  # 0.0 to 1.0
    gear: str  # 'P', 'R', 'N', 'D', 'L'
    rpm: float  # engine RPM
    
    # Systems
    abs_enabled: bool
    traction_control_enabled: bool
    
    # ADAS
    lane_center_enabled: bool
    acc_enabled: bool
    acc_target_speed: float
    backup_camera_active: bool
```

---

### 2. **Control Manager Node** (`control_manager.py`)
**Purpose**: Centralized control logic and command routing

**Responsibilities**:
- Receive commands from all GUI windows
- Validate and interpret commands
- Apply control constraints
- Forward validated commands to vehicle model
- Broadcast state updates to GUI windows

**Publishes**:
- `/vehicle/commands` - Processed control commands
- `/gui/state` - State information for all GUIs

**Subscribes**:
- `/control/steering` - Steering input from control GUI
- `/control/throttle` - Throttle input from control GUI
- `/control/brake` - Brake input from control GUI
- `/control/gear` - Gear selection from control GUI
- `/adas/config` - ADAS configuration from options GUI
- `/vehicle/state` - Vehicle state for broadcast

---

### 3. **Vehicle Visualization GUI** (`vehicle_viz/vehicle_display.py`)
**Purpose**: Display real-time vehicle state

**Window Type**: PySimpleGUI or PyQt5

**Displays**:
- Top-down vehicle view with current orientation
- Position and heading
- Velocity vector
- Steering angle indicator
- Current gear (P/R/N/D/L)
- Speed (mph or km/h)
- Engine RPM

**Publishes**: None (read-only)

**Subscribes**:
- `/vehicle/state` - Updates display with vehicle state
- `/vehicle/diagnostics` - Display additional info

**Example Layout**:
```
┌─────────────────────────────────┐
│     VEHICLE VISUALIZATION       │
├─────────────────────────────────┤
│                                 │
│         ┌─────────────┐         │
│         │     ◀  ▶    │         │
│         │  (Vehicle)  │  Spd: 45│
│         │             │  RPM: 2500
│         └─────────────┘         │
│                                 │
│  Position: (100, 50)            │
│  Heading: 45°                   │
│  Gear: D   Throttle: 60%        │
│                                 │
└─────────────────────────────────┘
```

---

### 4. **Vehicle Control GUI** (`vehicle_control_gui/control_panel.py`)
**Purpose**: Vehicle operation controls

**Window Type**: PySimpleGUI or PyQt5

**Controls**:
- **Steering Wheel**: ±30° range, visual feedback
- **Accelerator Pedal**: 0-100%, vertical slider
- **Brake Pedal**: 0-100%, vertical slider
- **PRNDL Selector**: Radio buttons or buttons (P/R/N/D/L)
- **Status Display**: Current gear, speed, throttle, brake

**Publishes**:
- `/control/steering` - Steering angle command (radians)
- `/control/throttle` - Throttle percentage (0.0-1.0)
- `/control/brake` - Brake percentage (0.0-1.0)
- `/control/gear` - Selected gear (string)

**Subscribes**:
- `/vehicle/state` - For feedback display

**Message Format**:
```python
class SteeringCommand:
    angle: float  # -π/6 to π/6 radians
    timestamp: float  # seconds

class ThrottleCommand:
    pedal_position: float  # 0.0 to 1.0
    timestamp: float

class BrakeCommand:
    pedal_position: float  # 0.0 to 1.0
    abs_active: bool  # Read from options
    timestamp: float

class GearCommand:
    gear: str  # 'P', 'R', 'N', 'D', 'L'
    timestamp: float
```

**Example Layout**:
```
┌─────────────────────────────────┐
│    VEHICLE CONTROL PANEL        │
├─────────────────────────────────┤
│                                 │
│         Steering Wheel:         │
│          ◜─────────◝            │
│         (Rotate dial)           │
│              0°                 │
│                                 │
│ ┌─────────────┐ ┌────────────┐ │
│ │   BRAKE     │ │    GAS     │ │
│ │     0%      │ │    0%      │ │
│ │  ▔▔▔▔▔▔▔  │ │  ▔▔▔▔▔▔▔  │ │
│ │  │      │  │ │  │      │  │ │
│ │  │  ▼   │  │ │  │  ▲   │  │ │
│ │  └──────┘  │ │  └──────┘  │ │
│ └─────────────┘ └────────────┘ │
│                                 │
│  [ P ]  [ R ]  [ N ]  [ D ]  [ L ] │
│         Current: D              │
│                                 │
└─────────────────────────────────┘
```

---

### 5. **Vehicle Options GUI** (`vehicle_options_gui/options_panel.py`)
**Purpose**: Vehicle system configuration

**Window Type**: PySimpleGUI or PyQt5

**Options**:
- **Safety Systems Section**:
  - [ ] ABS (Anti-lock Braking) - checkbox
  - [ ] Traction Control - checkbox
  
- **ADAS Section**:
  - [ ] Lane Centering - checkbox
  - [ ] Adaptive Cruise Control (ACC) - checkbox
    - ACC Target Speed: slider (0-200 km/h or 0-120 mph)
  - [ ] Backup Camera - checkbox

- **Status Display**: 
  - Active systems summary
  - ACC target speed (if enabled)
  - System health indicators

**Publishes**:
- `/adas/settings` - Configuration for ADAS systems
- `/adas/config` - Individual system enables/disables

**Subscribes**:
- `/adas/status` - For status feedback display

**Message Format**:
```python
class ADASSettings:
    lane_center_enabled: bool
    acc_enabled: bool
    acc_target_speed: float  # m/s
    backup_camera_enabled: bool
    timestamp: float

class SafetySettings:
    abs_enabled: bool
    traction_control_enabled: bool
    timestamp: float
```

**Example Layout**:
```
┌─────────────────────────────────┐
│     VEHICLE OPTIONS             │
├─────────────────────────────────┤
│                                 │
│   SAFETY SYSTEMS                │
│   ☐ ABS (Anti-Lock Braking)     │
│   ☑ Traction Control            │
│                                 │
│   ADAS FEATURES                 │
│   ☑ Lane Centering Assist       │
│   ☑ Adaptive Cruise Control     │
│      Target Speed: ◄────●────► 65 km/h │
│   ☐ Backup Camera               │
│                                 │
│   ACTIVE SYSTEMS:               │
│   • Traction Control: ACTIVE    │
│   • Lane Centering: ACTIVE      │
│   • ACC Target: 65 km/h         │
│                                 │
└─────────────────────────────────┘
```

---

## Message Types & Topics

### Topic Summary

| Topic | Type | Direction | Frequency |
|-------|------|-----------|-----------|
| `/vehicle/state` | Vehicle state | Publish | 50 Hz |
| `/vehicle/commands` | Control commands | Subscribe | As needed |
| `/control/steering` | Steering input | Subscribe | 10 Hz |
| `/control/throttle` | Throttle input | Subscribe | 10 Hz |
| `/control/brake` | Brake input | Subscribe | 10 Hz |
| `/control/gear` | Gear command | Subscribe | On change |
| `/adas/settings` | ADAS config | Subscribe | On change |
| `/adas/status` | ADAS feedback | Publish | 10 Hz |
| `/vehicle/diagnostics` | Vehicle info | Publish | 5 Hz |
| `/gui/state` | Broadcast state | Publish | 20 Hz |

### ROS2 Message Definition Examples

```yaml
# Vehicle State Message
header:
  stamp: Time
  frame_id: "vehicle"
position:
  x: float
  y: float
  z: float
velocity:
  x: float
  y: float
  z: float
orientation:
  x: float (quaternion)
  y: float
  z: float
  w: float
steering_angle: float  # radians
throttle_position: float  # 0.0-1.0
brake_position: float  # 0.0-1.0
current_gear: string  # P/R/N/D/L
speed_kmh: float
rpm: float

# ADAS Settings Message
abs_enabled: bool
traction_control_enabled: bool
lane_center_enabled: bool
acc_enabled: bool
acc_target_speed: float  # m/s
backup_camera_enabled: bool
```

---

## Data Flow Examples

### Example 1: User Accelerates Vehicle

```
1. User moves throttle slider in Control GUI
   ↓
2. Control GUI publishes to `/control/throttle` (0.6)
   ↓
3. Control Manager receives throttle command
   ↓
4. Control Manager publishes to `/vehicle/commands`
   ↓
5. Vehicle Model processes command
   ↓
6. Vehicle Model updates throttle_position = 0.6
   ↓
7. Vehicle Model calculates new velocity
   ↓
8. Vehicle Model publishes updated `/vehicle/state`
   ↓
9. Vehicle Viz subscribes, updates display (shows increased speed)
   ↓
10. Control GUI subscribes, updates throttle display feedback
```

### Example 2: User Enables Lane Centering (ACC)

```
1. User checks "Lane Centering" checkbox in Options GUI
   ↓
2. Options GUI publishes to `/adas/settings` (lane_center_enabled: true)
   ↓
3. Vehicle Model subscribes and receives setting
   ↓
4. Vehicle Model activates lane centering logic
   ↓
5. Vehicle Model publishes `/adas/status` (lane_center_active: true)
   ↓
6. Options GUI subscribes, shows "ACTIVE" status
   ↓
7. Vehicle Model calculates steering adjustments automatically
   ↓
8. Vehicle Model publishes updated steering in `/vehicle/state`
   ↓
9. Vehicle Viz shows adjusted vehicle heading
```

---

## Multi-Window Update Mechanism

All three GUI windows update simultaneously through ROS2 subscription:

```
Vehicle Visualization GUI (DISPLAY ONLY)
    ↓ subscribes to /vehicle/state
    ↓ updates 50 Hz
    └─→ Display updated immediately

Vehicle Control GUI (INPUT + FEEDBACK)
    ↓ publishes /control/steering|throttle|brake|gear
    ↓ subscribes to /vehicle/state for feedback
    └─→ Shows current vehicle state as feedback

Vehicle Options GUI (CONFIG + STATUS)
    ↓ publishes /adas/settings
    ↓ subscribes to /adas/status
    └─→ Shows current system configuration & status
```

## Design Principles

1. **Decoupled Windows**: Each GUI window is independent and can be run on different machines
2. **ROS2 Pub/Sub**: All communication through standard ROS2 messaging
3. **Real-time Updates**: 50 Hz vehicle state, 10 Hz GUI updates
4. **Fail-safe Design**: Loss of one GUI doesn't affect others
5. **Clear Responsibility**: Each component has one clear purpose
6. **Testable**: Each component can be tested independently

## Deployment Topologies

### Topology 1: Single Machine (Desktop)
```
Desktop Linux with ROS2 Jazzy
├── Vehicle Model Node
├── Control Manager Node
├── Vehicle Viz GUI Window
├── Vehicle Control GUI Window
└── Vehicle Options GUI Window
```

### Topology 2: Raspberry Pi + Desktop (Distributed)
```
Desktop Linux (Development)          Raspberry Pi (Deployment)
├── Vehicle Viz GUI Window (optional)    └── ROS2 Core + All nodes
├── Vehicle Control GUI Window (optional)   (headless or VNC)
└── Vehicle Options GUI Window (optional)
         ↓ ROS2 Network Bridge ↓
       Communicates via ROS2_DOMAIN_ID
```

---

## Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Vehicle Model Update Rate | 50 Hz | Smooth physics simulation |
| GUI Update Rate | 20-30 Hz | Smooth visual feedback |
| Network Latency | < 100 ms | Responsive controls |
| CPU Usage (Vehicle Model) | < 10% | Runs on Raspberry Pi |
| Memory Usage | < 200 MB | Runs on Raspberry Pi |

---

## Future Extensions

1. **Hardware Integration**: Replace model with actual vehicle hardware
2. **3D Visualization**: Gazebo simulation environment
3. **Sensor Integration**: Lidar, camera input from physical vehicle
4. **Multi-vehicle**: Support multiple vehicles simultaneously
5. **Recording/Playback**: Record and replay vehicle state sequences
6. **Network Remote Control**: Control from mobile app or web interface

---

**Last Updated**: April 30, 2026
