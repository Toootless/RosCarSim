# Development Roadmap & Progress Tracker

## Project Summary

**RosSim** - A vehicle simulation system for ROS2 Jazzy with three integrated GUI windows:
1. Vehicle Visualization (real-time display)
2. Vehicle Control Panel (steering wheel, pedals, PRNDL)
3. Vehicle Options Panel (ABS, traction control, ADAS)

**Target Platforms**: Desktop Linux (Ubuntu 22.04) or Raspberry Pi 5 running ROS2 Jazzy

---

## Phase 1: Project Setup & Documentation ✅ COMPLETE

### Completed Tasks
- ✅ Project directory structure created
- ✅ Comprehensive README created (PROJECT_README.md)
- ✅ Attribution documentation (docs/ATTRIBUTION.md)
- ✅ ROS2 Jazzy compatibility checklist (docs/COMPATIBILITY.md)
- ✅ System architecture documentation (docs/ARCHITECTURE.md)
- ✅ Installation guide (docs/INSTALLATION.md)
- ✅ This roadmap

### Documentation Checklist
- ✅ Original projects credited (Yahboom, ros-raspberry-pi)
- ✅ Attribution headers documented
- ✅ License compliance noted
- ✅ Compatibility requirements listed
- ✅ Architecture thoroughly explained
- ✅ Installation steps provided

---

## Phase 2: ROS2 Jazzy Compatibility Verification (NEXT)

### Task 2.1: Environment Setup
- [ ] Install ROS2 Jazzy on target machine (desktop Linux)
- [ ] Run Phase 1 compatibility tests:
  - [ ] Verify `ros2 --version`
  - [ ] Verify `colcon --version`
  - [ ] Verify `python3 -c "import rclpy"`
  - [ ] Create and build test ROS2 package
- [ ] Document any compatibility issues found
- [ ] Create workarounds if needed

**Estimated Time**: 1-2 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL - Blocking Phase 3

### Task 2.2: Base Project Dependency Analysis
- [ ] Extract dependency list from MicroROS-Car-Pi5
- [ ] Extract dependency list from ros-raspberry-pi
- [ ] Verify each dependency exists in ROS2 Jazzy:
  - [ ] rclpy, std_msgs, geometry_msgs, sensor_msgs (core - expect ✅)
  - [ ] cv_bridge / OpenCV (expect ⚠️)
  - [ ] MediaPipe (expect ❓)
  - [ ] GUI frameworks (PyQt5 vs PySimpleGUI - evaluate)
- [ ] Document compatibility results
- [ ] Update [COMPATIBILITY.md](docs/COMPATIBILITY.md) with findings

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL - Required for development

### Task 2.3: Create Baseline package.xml Files
- [ ] Create `src/rossim_core/package.xml` with verified dependencies
- [ ] Create `src/vehicle_viz/package.xml` with GUI framework dependencies
- [ ] Create `src/vehicle_control_gui/package.xml` with GUI framework dependencies
- [ ] Create `src/vehicle_options_gui/package.xml` with GUI framework dependencies
- [ ] Document dependency decisions (why PySimpleGUI or PyQt5)
- [ ] Successfully build with `colcon build`

**Estimated Time**: 1-2 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH - Required for Phase 3

---

## Phase 3: Core Vehicle Model (MVP)

### Task 3.1: Vehicle Model Node - Basic Structure
- [ ] Create `src/rossim_core/rossim_core/vehicle_model.py`
- [ ] Implement VehicleState dataclass:
  - [ ] Position (x, y, z)
  - [ ] Velocity (vx, vy, vz)
  - [ ] Orientation (roll, pitch, yaw)
  - [ ] Steering angle
  - [ ] Throttle, brake, gear
  - [ ] RPM, speed
- [ ] Implement basic ROS2 node lifecycle
- [ ] Create ROS2 custom messages for vehicle state
- [ ] Test node creation and startup

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL - Foundation

### Task 3.2: Vehicle Physics Simulation (Simple)
- [ ] Implement basic motion equations
- [ ] Steering → yaw rate calculation
- [ ] Throttle → acceleration calculation
- [ ] Brake → deceleration calculation
- [ ] Gear logic (P/R/N/D/L affects max speed)
- [ ] Update loop at 50 Hz
- [ ] Test with manual state changes

**Estimated Time**: 4-5 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL

### Task 3.3: Vehicle Model ROS2 Integration
- [ ] Publish `/vehicle/state` at 50 Hz
- [ ] Subscribe to `/vehicle/commands`
- [ ] Implement command validation
- [ ] Publish `/vehicle/diagnostics` at 5 Hz
- [ ] Add logging and debug output
- [ ] Test pub/sub with `ros2 topic echo`

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL

### Phase 3 Completion Gate
- [ ] Vehicle model node starts without errors
- [ ] `/vehicle/state` publishes valid messages
- [ ] Physics simulation runs smoothly
- [ ] 50 Hz publishing rate maintained

---

## Phase 4: Control Manager Node

### Task 4.1: Control Manager Structure
- [ ] Create `src/rossim_core/rossim_core/control_manager.py`
- [ ] Implement command aggregation from all GUIs
- [ ] Create command structures for steering/throttle/brake/gear
- [ ] Implement command validation logic
- [ ] Add rate limiting (prevents rapid changes)

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 4.2: Control Manager ROS2 Integration
- [ ] Subscribe to `/control/steering`, `/control/throttle`, `/control/brake`, `/control/gear`
- [ ] Publish to `/vehicle/commands`
- [ ] Republish vehicle state to `/gui/state` for GUIs
- [ ] Implement command history/buffering
- [ ] Test with manual message publishing

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Phase 5: Vehicle Visualization GUI

### Task 5.1: GUI Framework Selection
- [ ] Evaluate PySimpleGUI vs PyQt5
  - [ ] Complexity
  - [ ] Jazzy compatibility
  - [ ] Raspberry Pi support
- [ ] Make selection and document rationale
- [ ] Set up example GUI window

**Estimated Time**: 1-2 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 5.2: Vehicle Visualization Display
- [ ] Create main GUI window layout
- [ ] Implement top-down vehicle display
  - [ ] Draw vehicle rectangle
  - [ ] Show steering angle
  - [ ] Show heading/orientation
- [ ] Add text displays for:
  - [ ] Position (x, y)
  - [ ] Speed (km/h)
  - [ ] RPM
  - [ ] Current gear
  - [ ] Throttle/Brake status

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 5.3: Vehicle Visualization ROS2 Integration
- [ ] Create ROS2 node wrapper
- [ ] Subscribe to `/vehicle/state`
- [ ] Update display at 20 Hz
- [ ] Handle subscription errors gracefully
- [ ] Test with running vehicle model

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Phase 6: Vehicle Control GUI

### Task 6.1: Control Panel Layout
- [ ] Create main control window
- [ ] Implement steering wheel control (rotation dial)
- [ ] Implement accelerator pedal (vertical slider, 0-100%)
- [ ] Implement brake pedal (vertical slider, 0-100%)
- [ ] Implement PRNDL selector (5 buttons or radio buttons)
- [ ] Add status display section

**Estimated Time**: 4-5 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 6.2: Control Event Handling
- [ ] Steering wheel input → convert to angle (-π/6 to π/6)
- [ ] Pedal movements → convert to 0.0-1.0 range
- [ ] PRNDL button clicks → publish gear selection
- [ ] Implement dead zones (reduce noise)
- [ ] Add validation (prevent invalid combinations)

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 6.3: Control GUI ROS2 Integration
- [ ] Create ROS2 node wrapper
- [ ] Publish to `/control/steering`
- [ ] Publish to `/control/throttle`
- [ ] Publish to `/control/brake`
- [ ] Publish to `/control/gear`
- [ ] Subscribe to `/vehicle/state` for feedback display
- [ ] Test with running vehicle model

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Phase 7: Vehicle Options GUI

### Task 7.1: Options Panel Layout
- [ ] Create main options window
- [ ] Add Safety Systems section:
  - [ ] ABS checkbox
  - [ ] Traction Control checkbox
- [ ] Add ADAS section:
  - [ ] Lane Centering checkbox
  - [ ] ACC checkbox
  - [ ] ACC Target Speed slider (if ACC enabled)
  - [ ] Backup Camera checkbox
- [ ] Add active systems status display

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 7.2: Options Event Handling
- [ ] Checkbox state changes → boolean values
- [ ] ACC speed slider → convert to m/s
- [ ] Validate option combinations
- [ ] Show/hide dependent controls (e.g., ACC speed when ACC enabled)

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 7.3: Options GUI ROS2 Integration
- [ ] Create ROS2 node wrapper
- [ ] Publish to `/adas/settings`
- [ ] Publish to `/safety/settings`
- [ ] Subscribe to `/adas/status`
- [ ] Subscribe to `/safety/status`
- [ ] Update status displays in real-time
- [ ] Test with running vehicle model

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Phase 8: ADAS Implementation

### Task 8.1: Lane Centering System
- [ ] Implement steering adjustment logic
- [ ] Calculate steering correction based on lane deviation
- [ ] Smooth steering changes
- [ ] Publish lane centering status
- [ ] Test with vehicle model

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟠 MEDIUM

### Task 8.2: Adaptive Cruise Control (ACC)
- [ ] Implement speed maintenance logic
- [ ] Calculate throttle/brake adjustments
- [ ] Smooth acceleration/deceleration
- [ ] Handle edge cases (stopped, max speed)
- [ ] Publish ACC status
- [ ] Test with vehicle model

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟠 MEDIUM

### Task 8.3: Backup Camera
- [ ] Create backup camera view window
- [ ] Implement simple rear-view display
- [ ] Show distance grid overlay
- [ ] Display distance to objects (from simulation)
- [ ] Activate/deactivate with GUI checkbox

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟠 MEDIUM

### Task 8.4: ABS Implementation
- [ ] Implement ABS logic (prevent wheel lockup)
- [ ] Modify brake response when enabled
- [ ] Add ABS indicator in visualization
- [ ] Test emergency braking scenarios

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟠 MEDIUM

---

## Phase 9: Multi-Window Integration & Testing

### Task 9.1: Launch File
- [ ] Create `launch/rossim_full.launch.py`
- [ ] Launch all nodes: vehicle_model, control_manager, 3 GUI windows
- [ ] Add launch arguments (logging level, debug mode)
- [ ] Test launching full system
- [ ] Document launch procedure

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 9.2: Integration Testing
- [ ] All windows start without errors
- [ ] Steering input → vehicle rotation in viz
- [ ] Throttle input → vehicle speed in viz
- [ ] Brake input → vehicle deceleration
- [ ] PRNDL selection → gear display
- [ ] Options changes → system status updates
- [ ] All windows update in real-time

**Estimated Time**: 4-5 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🔴 CRITICAL

### Task 9.3: Performance Testing
- [ ] Monitor CPU usage
- [ ] Monitor memory usage
- [ ] Verify 50 Hz vehicle update rate
- [ ] Profile on Raspberry Pi (if available)
- [ ] Optimize if needed

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Phase 10: Documentation & Deployment

### Task 10.1: Code Documentation
- [ ] Add docstrings to all functions and classes
- [ ] Create API documentation
- [ ] Add inline comments for complex logic
- [ ] Create developer guide

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 10.2: User Documentation
- [ ] Create user guide for operating all three GUIs
- [ ] Add screenshots and examples
- [ ] Create troubleshooting guide
- [ ] Document ADAS features

**Estimated Time**: 2-3 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

### Task 10.3: Deployment Guide
- [ ] Create Raspberry Pi deployment guide
- [ ] Document network setup for distributed systems
- [ ] Create Docker configuration (optional)
- [ ] Create systemd service files (auto-start)

**Estimated Time**: 3-4 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟠 MEDIUM

### Task 10.4: Final Testing
- [ ] Run on desktop Linux
- [ ] Run on Raspberry Pi (if available)
- [ ] Test distributed setup (Pi + desktop)
- [ ] Document any platform-specific issues
- [ ] Create platform compatibility matrix

**Estimated Time**: 4-5 hours
**Owner**: [Assigned]
**Status**: 🔴 Not Started
**Priority**: 🟡 HIGH

---

## Timeline Summary

| Phase | Tasks | Est. Hours | Priority | Status |
|-------|-------|-----------|----------|--------|
| 1: Setup | 7 | 2 | 🔴 CRITICAL | ✅ DONE |
| 2: Jazzy Verification | 3 | 5-8 | 🔴 CRITICAL | 🔴 TODO |
| 3: Vehicle Model | 3 | 9-12 | 🔴 CRITICAL | 🔴 TODO |
| 4: Control Manager | 2 | 4-6 | 🟡 HIGH | 🔴 TODO |
| 5: Visualization GUI | 3 | 6-9 | 🟡 HIGH | 🔴 TODO |
| 6: Control GUI | 3 | 10-13 | 🟡 HIGH | 🔴 TODO |
| 7: Options GUI | 3 | 8-11 | 🟡 HIGH | 🔴 TODO |
| 8: ADAS | 4 | 10-14 | 🟠 MEDIUM | 🔴 TODO |
| 9: Integration | 3 | 8-11 | 🟡 HIGH | 🔴 TODO |
| 10: Deployment | 4 | 12-16 | 🟡 HIGH | 🔴 TODO |

**Total Estimated Time**: 80-120 hours over 8-12 weeks

---

## Next Immediate Actions

### Week 1 (High Priority)

1. **Verify ROS2 Jazzy Installation** (Phase 2.1)
   - Install on target machine
   - Run compatibility tests
   - Confirm environment is ready

2. **Analyze Base Project Dependencies** (Phase 2.2)
   - List all dependencies
   - Check Jazzy compatibility
   - Document findings

3. **Create Package Structure** (Phase 2.3)
   - Create package.xml files
   - Build basic packages
   - Confirm build system works

4. **Start Vehicle Model Development** (Phase 3.1-3.3)
   - Implement VehicleState
   - Add basic physics
   - Test ROS2 integration

### Success Criteria for Week 1
- ✅ Jazzy environment verified
- ✅ All packages build successfully
- ✅ Vehicle model node runs and publishes state
- ✅ Topics visible with `ros2 topic list`

---

## Dependencies & Blockers

- **Blocker 1**: ROS2 Jazzy installation (blocks Phase 2)
- **Blocker 2**: GUI framework selection (blocks Phases 5-7)
- **Blocker 3**: Vehicle model completion (blocks Phases 4-9)

---

## Notes & Decisions Log

### Decision 1: GUI Framework
- **Status**: 🟠 PENDING
- **Options**: PySimpleGUI vs PyQt5
- **Considerations**: Simplicity, Jazzy compatibility, Raspberry Pi support
- **Recommendation**: Evaluate both during Phase 5.1, lean toward PySimpleGUI for simplicity
- **Decision Maker**: [TBD]

### Decision 2: Vehicle Physics Complexity
- **Status**: ✅ DECIDED
- **Approach**: Start simple (Phase 3), enhance later
- **Rationale**: MVP focus, easier testing, can add complexity iteratively

### Decision 3: Message Format
- **Status**: ✅ DECIDED
- **Approach**: Custom messages defined in rossim_core package
- **Rationale**: Cleaner, self-contained, easier to maintain

---

## File Checklist

Documentation:
- ✅ PROJECT_README.md - Main project overview
- ✅ docs/ATTRIBUTION.md - Proper credit to base projects
- ✅ docs/COMPATIBILITY.md - ROS2 Jazzy verification checklist
- ✅ docs/ARCHITECTURE.md - System design and data flow
- ✅ docs/INSTALLATION.md - Setup and installation steps
- ✅ docs/ROADMAP.md - This file

Code (To be created):
- [ ] src/rossim_core/package.xml
- [ ] src/rossim_core/rossim_core/vehicle_model.py
- [ ] src/rossim_core/rossim_core/control_manager.py
- [ ] src/rossim_core/rossim_core/adas_manager.py
- [ ] src/vehicle_viz/package.xml
- [ ] src/vehicle_viz/vehicle_viz/vehicle_display.py
- [ ] src/vehicle_control_gui/package.xml
- [ ] src/vehicle_control_gui/vehicle_control_gui/control_panel.py
- [ ] src/vehicle_options_gui/package.xml
- [ ] src/vehicle_options_gui/vehicle_options_gui/options_panel.py
- [ ] launch/rossim_full.launch.py

---

**Last Updated**: April 30, 2026

**Project Status**: 🟡 In Planning Phase - Ready for Phase 2 (Jazzy Verification)

**Next Review**: After Phase 2 completion

---

## Contact & Questions

- **Project Lead**: [Your Name]
- **Base Project Credits**: Yahboom Technology (MicroROS-Car-Pi5), Open Robotics Community (ros-raspberry-pi)
- **Target Platforms**: Ubuntu 22.04 with ROS2 Jazzy, Raspberry Pi 5 with ROS2 Jazzy
