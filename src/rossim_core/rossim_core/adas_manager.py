#!/usr/bin/env python3
"""
ADAS Manager Node

Manages Advanced Driver Assistance System features:
- Lane centering assist
- Adaptive Cruise Control (ACC)
- Backup camera
- Anti-lock braking (ABS) coordination

Adapted for ROS2 Jazzy
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32


class ADASManagerNode(Node):
    """ADAS features management"""
    
    def __init__(self):
        super().__init__('adas_manager')
        
        # ADAS State
        self.abs_enabled = False
        self.traction_control_enabled = False
        self.lane_center_enabled = False
        self.acc_enabled = False
        self.acc_target_speed = 0.0
        self.backup_camera_enabled = False
        
        # Create publishers
        self.status_pub = self.create_publisher(String, '/adas/status', 10)
        self.steering_assist_pub = self.create_publisher(Float32, '/adas/steering_assist', 10)
        
        # Create subscribers
        self.create_subscription(String, '/adas/settings', self.settings_callback, 10)
        self.create_subscription(String, '/vehicle/state', self.vehicle_state_callback, 10)
        
        # Timer for ADAS processing (10 Hz)
        self.create_timer(0.1, self.process_adas)
        
        self.get_logger().info('ADAS Manager Node initialized')
    
    def settings_callback(self, msg):
        """Receive ADAS configuration"""
        try:
            settings = dict(item.split(':') for item in msg.data.split(','))
            self.abs_enabled = settings.get('abs', 'false').lower() == 'true'
            self.traction_control_enabled = settings.get('tc', 'false').lower() == 'true'
            self.lane_center_enabled = settings.get('lane', 'false').lower() == 'true'
            self.acc_enabled = settings.get('acc', 'false').lower() == 'true'
            self.acc_target_speed = float(settings.get('acc_speed', '0'))
            self.backup_camera_enabled = settings.get('backup', 'false').lower() == 'true'
        except Exception as e:
            self.get_logger().warn(f'Error parsing ADAS settings: {e}')
    
    def vehicle_state_callback(self, msg):
        """Receive vehicle state for ADAS decisions"""
        # Vehicle state is available when needed by ADAS algorithms
        pass
    
    def process_adas(self):
        """Process ADAS logic"""
        # This is where ADAS algorithms run
        # For now, just publish status
        
        active_systems = []
        if self.abs_enabled:
            active_systems.append('ABS')
        if self.traction_control_enabled:
            active_systems.append('TC')
        if self.lane_center_enabled:
            active_systems.append('LaneCenter')
        if self.acc_enabled:
            active_systems.append(f'ACC@{self.acc_target_speed}')
        if self.backup_camera_enabled:
            active_systems.append('BackupCam')
        
        status_msg = String()
        status_msg.data = ','.join(active_systems) if active_systems else 'IDLE'
        self.status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ADASManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
