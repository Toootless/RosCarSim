#!/usr/bin/env python3
"""Vehicle Model Node - Simple Physics Simulator"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist
import math

class VehicleModelNode(Node):
    def __init__(self):
        super().__init__('vehicle_model')
        
        # State variables
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.vx = 0.0
        self.steering = 0.0
        self.throttle = 0.0
        self.brake = 0.0
        self.gear = 'P'
        self.rpm = 0.0
        
        # Publishers
        self.state_pub = self.create_publisher(Twist, '/vehicle/state', 10)
        self.diag_pub = self.create_publisher(String, '/vehicle/diagnostics', 10)
        
        # Subscribers
        self.create_subscription(Float32, '/control/steering', self.steering_callback, 10)
        self.create_subscription(Float32, '/control/throttle', self.throttle_callback, 10)
        self.create_subscription(Float32, '/control/brake', self.brake_callback, 10)
        self.create_subscription(String, '/control/gear', self.gear_callback, 10)
        
        # Timer - 50 Hz update
        self.create_timer(0.02, self.update_and_publish)
        
        self.get_logger().info('Vehicle Model Node initialized')

    def steering_callback(self, msg):
        self.steering = max(-1.0, min(1.0, msg.data / 100.0))

    def throttle_callback(self, msg):
        self.throttle = max(0.0, min(1.0, msg.data))

    def brake_callback(self, msg):
        self.brake = max(0.0, min(1.0, msg.data))

    def gear_callback(self, msg):
        if msg.data in ['P', 'R', 'N', 'D', 'L']:
            self.gear = msg.data

    def update_and_publish(self):
        """Update physics and publish state"""
        dt = 0.02
        max_speed = 20.0  # m/s
        
        # Simple physics
        if self.gear == 'D':
            accel = self.throttle * 5.0
            decel = self.brake * 10.0
            self.vx += (accel - decel) * dt
            self.vx = min(max_speed, max(0.0, self.vx))
        elif self.gear == 'R':
            self.vx = -self.throttle * max_speed * 0.5
        elif self.gear in ['P', 'N']:
            self.vx *= 0.95  # Coast to stop
        
        # Update position
        if abs(self.vx) > 0.1:
            self.yaw += self.steering * self.vx * dt
            self.x += self.vx * math.cos(self.yaw) * dt
            self.y += self.vx * math.sin(self.yaw) * dt
        
        self.rpm = abs(self.vx) * 500.0 if self.vx != 0 else 0.0
        
        # Publish state
        state_msg = Twist()
        state_msg.linear.x = self.vx
        state_msg.linear.y = 0.0
        state_msg.linear.z = 0.0
        state_msg.angular.x = 0.0
        state_msg.angular.y = 0.0
        state_msg.angular.z = self.yaw
        self.state_pub.publish(state_msg)
        
        # Publish diagnostics
        diag_msg = String()
        diag_msg.data = f'x:{self.x:.1f},y:{self.y:.1f},speed:{self.vx:.2f},rpm:{self.rpm:.0f},gear:{self.gear}'
        self.diag_pub.publish(diag_msg)

def main(args=None):
    rclpy.init(args=args)
    node = VehicleModelNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
