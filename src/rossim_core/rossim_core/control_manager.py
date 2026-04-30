#!/usr/bin/env python3
"""
Control Manager Node

Routes commands from all GUI windows to the vehicle model.
Aggregates control inputs and manages communication.

Adapted from MicroROS-Car-Pi5 and ros-raspberry-pi patterns for ROS2 Jazzy
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist


class ControlManagerNode(Node):
    """Control command aggregation and routing"""
    
    def __init__(self):
        super().__init__('control_manager')
        
        # Create publishers to vehicle model
        self.command_pub = self.create_publisher(Twist, '/vehicle/commands', 10)
        self.state_broadcast_pub = self.create_publisher(String, '/gui/state', 10)
        
        # Create subscribers to GUI windows
        self.create_subscription(Float32, '/control/steering', self.steering_callback, 10)
        self.create_subscription(Float32, '/control/throttle', self.throttle_callback, 10)
        self.create_subscription(Float32, '/control/brake', self.brake_callback, 10)
        self.create_subscription(String, '/control/gear', self.gear_callback, 10)
        self.create_subscription(String, '/adas/settings', self.adas_callback, 10)
        self.create_subscription(String, '/vehicle/state', self.vehicle_state_callback, 10)
        
        # Store current commands
        self.current_steering = 0.0
        self.current_throttle = 0.0
        self.current_brake = 0.0
        self.current_gear = 'P'
        
        self.get_logger().info('Control Manager Node initialized')
    
    def steering_callback(self, msg):
        """Route steering command"""
        self.current_steering = msg.data
        self.publish_commands()
    
    def throttle_callback(self, msg):
        """Route throttle command"""
        self.current_throttle = msg.data
        self.publish_commands()
    
    def brake_callback(self, msg):
        """Route brake command"""
        self.current_brake = msg.data
        self.publish_commands()
    
    def gear_callback(self, msg):
        """Route gear selection"""
        self.current_gear = msg.data
        self.publish_commands()
    
    def adas_callback(self, msg):
        """Route ADAS settings to vehicle model"""
        settings_pub = self.create_publisher(String, '/adas/settings', 10)
        settings_pub.publish(msg)
    
    def vehicle_state_callback(self, msg):
        """Receive and rebroadcast vehicle state for all GUIs"""
        self.state_broadcast_pub.publish(msg)
    
    def publish_commands(self):
        """Publish aggregated commands to vehicle model"""
        cmd_msg = Twist()
        cmd_msg.linear.x = self.current_throttle
        cmd_msg.linear.y = self.current_brake
        cmd_msg.angular.z = self.current_steering
        
        self.command_pub.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ControlManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
