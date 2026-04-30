#!/usr/bin/env python3
"""
Vehicle Model Node

This node simulates the vehicle state and physics. It maintains all vehicle
parameters (position, velocity, steering angle, gear, etc.) and updates them
based on control commands received from the control manager.

Adapted from MicroROS-Car-Pi5 by Yahboom Technology for ROS2 Jazzy
https://github.com/YahboomTechnology/MicroROS-Car-Pi5
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist
import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class VehicleState:
    """Vehicle state representation"""
    # Position (meters)
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    # Velocity (m/s)
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    
    # Orientation (radians)
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    
    # Control inputs
    steering_angle: float = 0.0  # radians, -π/6 to π/6
    throttle: float = 0.0  # 0.0 to 1.0
    brake: float = 0.0  # 0.0 to 1.0
    gear: str = 'P'  # P, R, N, D, L
    
    # Engine
    rpm: float = 0.0
    
    # Systems
    abs_enabled: bool = False
    traction_control_enabled: bool = False
    
    # ADAS
    lane_center_enabled: bool = False
    acc_enabled: bool = False
    acc_target_speed: float = 0.0
    backup_camera_enabled: bool = False


class VehicleModelNode(Node):
    """Vehicle simulation and physics node"""
    
    def __init__(self):
        super().__init__('vehicle_model')
        
        # Vehicle state
        self.state = VehicleState()
        
        # Physics parameters
        self.max_speed = 50.0  # m/s
        self.max_acceleration = 5.0  # m/s²
        self.max_deceleration = 8.0  # m/s²
        self.wheelbase = 2.5  # meters
        self.mass = 1500.0  # kg
        
        # Create publishers
        self.state_pub = self.create_publisher(Twist, '/vehicle/state', 10)
        self.diagnostics_pub = self.create_publisher(String, '/vehicle/diagnostics', 10)
        self.adas_status_pub = self.create_publisher(String, '/adas/status', 10)
        
        # Create subscribers
        self.create_subscription(Twist, '/vehicle/commands', self.command_callback, 10)
        self.create_subscription(Float32, '/control/steering', self.steering_callback, 10)
        self.create_subscription(Float32, '/control/throttle', self.throttle_callback, 10)
        self.create_subscription(Float32, '/control/brake', self.brake_callback, 10)
        self.create_subscription(String, '/control/gear', self.gear_callback, 10)
        self.create_subscription(String, '/adas/settings', self.adas_callback, 10)
        
        # Create timer for simulation loop (50 Hz)
        self.create_timer(0.02, self.update_vehicle)
        
        self.get_logger().info('Vehicle Model Node initialized')
    
    def steering_callback(self, msg):
        """Handle steering input"""
        self.state.steering_angle = max(-math.pi/6, min(math.pi/6, msg.data))
    
    def throttle_callback(self, msg):
        """Handle throttle input"""
        self.state.throttle = max(0.0, min(1.0, msg.data))
    
    def brake_callback(self, msg):
        """Handle brake input"""
        self.state.brake = max(0.0, min(1.0, msg.data))
    
    def gear_callback(self, msg):
        """Handle gear selection"""
        if msg.data in ['P', 'R', 'N', 'D', 'L']:
            self.state.gear = msg.data
    
    def adas_callback(self, msg):
        """Handle ADAS settings"""
        # Parse ADAS settings message (format: "key1:val1,key2:val2")
        try:
            settings = dict(item.split(':') for item in msg.data.split(','))
            self.state.abs_enabled = settings.get('abs', 'false').lower() == 'true'
            self.state.traction_control_enabled = settings.get('tc', 'false').lower() == 'true'
            self.state.lane_center_enabled = settings.get('lane', 'false').lower() == 'true'
            self.state.acc_enabled = settings.get('acc', 'false').lower() == 'true'
            self.state.backup_camera_enabled = settings.get('backup', 'false').lower() == 'true'
        except Exception as e:
            self.get_logger().warn(f'Error parsing ADAS settings: {e}')
    
    def command_callback(self, msg):
        """Handle velocity commands (alternative interface)"""
        # For now, unused (using individual steering/throttle/brake topics)
        pass
    
    def update_vehicle(self):
        """Update vehicle physics and state"""
        dt = 0.02  # 50 Hz
        
        # Simple physics model
        if self.state.gear == 'P':
            # Park - no movement
            self.state.throttle = 0.0
            self.state.vx = 0.0
        elif self.state.gear == 'N':
            # Neutral - coast
            decel = 2.0 * dt
            if self.state.vx > 0:
                self.state.vx = max(0.0, self.state.vx - decel)
            elif self.state.vx < 0:
                self.state.vx = min(0.0, self.state.vx + decel)
        elif self.state.gear == 'D':
            # Drive forward
            accel = self.state.throttle * self.max_acceleration
            decel = self.state.brake * self.max_deceleration
            self.state.vx += (accel - decel) * dt
            self.state.vx = min(self.max_speed, self.state.vx)
            self.state.vx = max(0.0, self.state.vx)
        elif self.state.gear == 'R':
            # Reverse
            accel = self.state.throttle * self.max_acceleration
            decel = self.state.brake * self.max_deceleration
            self.state.vx = -min(self.max_speed * 0.5, accel * dt - decel * dt)
        elif self.state.gear == 'L':
            # Low gear (slower forward)
            accel = self.state.throttle * self.max_acceleration * 0.5
            decel = self.state.brake * self.max_deceleration
            self.state.vx += (accel - decel) * dt
            self.state.vx = min(self.max_speed * 0.5, self.state.vx)
        
        # Calculate RPM based on speed
        if self.state.vx != 0:
            self.state.rpm = abs(self.state.vx) * 500.0  # Simple RPM calculation
        else:
            self.state.rpm = 0.0
        
        # Update position based on velocity and steering
        if abs(self.state.vx) > 0.01:
            # Bicycle model for steering
            turning_radius = self.wheelbase / math.tan(self.state.steering_angle + 0.0001)
            angular_velocity = self.state.vx / turning_radius
            
            self.state.yaw += angular_velocity * dt
            self.state.x += self.state.vx * math.cos(self.state.yaw) * dt
            self.state.y += self.state.vx * math.sin(self.state.yaw) * dt
        
        # Apply ADAS adjustments
        if self.state.lane_center_enabled and abs(self.state.vx) > 0.1:
            # Simple lane centering: gentle steering correction
            self.state.steering_angle *= 0.95
        
        if self.state.acc_enabled and self.state.vx < self.state.acc_target_speed:
            # ACC: maintain target speed
            self.state.throttle = 0.5
        
        # Publish state
        self.publish_state()
    
    def publish_state(self):
        """Publish current vehicle state"""
        state_msg = Twist()
        state_msg.linear.x = self.state.vx
        state_msg.linear.y = self.state.vy
        state_msg.linear.z = self.state.vz
        state_msg.angular.x = self.state.roll
        state_msg.angular.y = self.state.pitch
        state_msg.angular.z = self.state.yaw
        
        self.state_pub.publish(state_msg)
        
        # Publish diagnostics periodically
        if int(self.get_clock().now().nanoseconds / 1e9) % 2 == 0:
            diag_msg = String()
            diag_msg.data = f'x:{self.state.x:.1f},y:{self.state.y:.1f},speed:{self.state.vx:.1f},rpm:{self.state.rpm:.0f},gear:{self.state.gear}'
            self.diagnostics_pub.publish(diag_msg)


def main(args=None):
    rclpy.init(args=args)
    node = VehicleModelNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
