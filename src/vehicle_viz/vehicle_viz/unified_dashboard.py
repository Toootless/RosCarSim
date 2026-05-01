#!/usr/bin/env python3
"""Unified Vehicle Dashboard - Consolidated GUI for RosSim"""
import sys
import os
from pathlib import Path

# Ensure venv site-packages are in sys.path
venv_path = Path.home() / 'RosSim_ws' / 'venv' / 'lib' / 'python3.12' / 'site-packages'
if str(venv_path) not in sys.path and venv_path.exists():
    sys.path.insert(0, str(venv_path))

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, String
import PySimpleGUI as sg
import json
from datetime import datetime

class UnifiedDashboardNode(Node):
    def __init__(self):
        super().__init__('unified_dashboard')
        
        # Vehicle state
        self.position_x = 0.0
        self.position_y = 0.0
        self.velocity = 0.0
        self.heading = 0.0
        self.rpm = 0.0
        self.current_gear = 'P'
        
        # ADAS settings
        self.adas_settings = {
            'abs_enabled': False,
            'traction_control': False,
            'lane_centering': False,
            'adaptive_cruise': False,
            'backup_camera': False,
            'cruise_speed': 100
        }
        
        # CAN logging
        self.can_messages = []
        self.recorded_messages = []
        self.is_recording = False
        
        # Subscriptions
        self.state_sub = self.create_subscription(Twist, '/vehicle/state', self.state_callback, 10)
        self.diag_sub = self.create_subscription(String, '/vehicle/diagnostics', self.diagnostics_callback, 10)
        self.adas_sub = self.create_subscription(String, '/adas/settings', self.adas_callback, 10)
        
        # Publishers
        self.steering_pub = self.create_publisher(Float32, '/control/steering', 10)
        self.throttle_pub = self.create_publisher(Float32, '/control/throttle', 10)
        self.brake_pub = self.create_publisher(Float32, '/control/brake', 10)
        self.gear_pub = self.create_publisher(String, '/control/gear', 10)
        self.adas_pub = self.create_publisher(String, '/adas/settings', 10)
        
        # Timer for gear publishing (50ms)
        self.gear_timer = self.create_timer(0.05, self.publish_gear_timer)
        
        # Timer for CAN logging (100ms)
        self.can_timer = self.create_timer(0.1, self.log_can_message)
        
        self.get_logger().info('Unified Dashboard initialized')
    
    def state_callback(self, msg):
        """Update vehicle state from Twist message (position in angular fields)"""
        self.position_x = msg.angular.x
        self.position_y = msg.angular.y
        self.velocity = msg.linear.x
        self.heading = msg.angular.z
    
    def diagnostics_callback(self, msg):
        """Parse diagnostics string: x:50.0,y:0.0,speed:20.00,rpm:10000,gear:D"""
        try:
            parts = msg.data.split(',')
            for part in parts:
                key_val = part.strip().split(':')
                if len(key_val) == 2:
                    key, val = key_val
                    if key == 'rpm':
                        self.rpm = float(val)
                    elif key == 'gear':
                        self.current_gear = val.strip()
        except Exception as e:
            pass
    
    def adas_callback(self, msg):
        """Update ADAS settings from JSON message"""
        try:
            self.adas_settings.update(json.loads(msg.data))
        except:
            pass
    
    def publish_gear_timer(self):
        """Publish gear selection every 50ms"""
        gear_msg = String()
        gear_msg.data = self.current_gear
        self.gear_pub.publish(gear_msg)
    
    def log_can_message(self):
        """Log CAN message every 100ms"""
        msg = {
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'gear': self.current_gear,
            'speed': self.velocity,
            'rpm': self.rpm,
            'abs': self.adas_settings.get('abs_enabled', False),
            'traction': self.adas_settings.get('traction_control', False),
            'lane_center': self.adas_settings.get('lane_centering', False),
            'acc': self.adas_settings.get('adaptive_cruise', False),
            'backup_cam': self.adas_settings.get('backup_camera', False)
        }
        
        self.can_messages.append(msg)
        if len(self.can_messages) > 100:
            self.can_messages.pop(0)
        
        if self.is_recording:
            self.recorded_messages.append(msg)
    
    def draw_vehicle(self):
        """Create ASCII vehicle visualization based on state"""
        # Simple box with wheels
        gear_color_map = {'P': '#ffcc00', 'R': '#ff0000', 'N': '#0000ff', 'D': '#00cc00'}
        gear_color = gear_color_map.get(self.current_gear, '#666666')
        
        # Create a simple visual representation
        if self.velocity > 15:
            vehicle_char = '▶'  # Moving forward
        elif self.velocity < -5:
            vehicle_char = '◀'  # Reversing
        elif self.current_gear == 'R':
            vehicle_char = '◀'
        else:
            vehicle_char = '█'  # Stationary
        
        return vehicle_char, gear_color
    
    def run(self):
        sg.theme('Dark2')
        sg.set_options(font=('Arial', 12), element_padding=(5, 5))
        
        vehicle_char, _ = self.draw_vehicle()
        
        # Layout
        viz_column = [
            [sg.Text('Vehicle Status', font=('Arial', 14, 'bold'))],
            [sg.Multiline(size=(15, 8), key='vehicle_display', disabled=True, font=('Courier', 60))],
            [sg.Text(f'Position: ({self.position_x:.1f}, {self.position_y:.1f})', key='pos_text', font=('Arial', 11))],
            [sg.Text(f'Speed: {self.velocity:.1f} m/s', key='speed_text', font=('Arial', 11))],
            [sg.Text(f'RPM: {self.rpm:.0f}', key='rpm_text', font=('Arial', 11))],
            [sg.Text(f'Heading: {self.heading:.1f}°', key='heading_text', font=('Arial', 11))],
        ]
        
        control_column = [
            [sg.Text('Vehicle Control', font=('Arial', 14, 'bold'))],
            [sg.Text('Steering:'), sg.Slider(range=(-100, 100), default_value=0, orientation='h', size=(20, 15), key='steering_slider')],
            [sg.Text('Throttle:'), sg.Slider(range=(0, 100), default_value=0, orientation='h', size=(20, 15), key='throttle_slider')],
            [sg.Text('Brake:'), sg.Slider(range=(0, 100), default_value=0, orientation='h', size=(20, 15), key='brake_slider')],
            [sg.Button('P', size=(4, 1)), sg.Button('R', size=(4, 1)), sg.Button('N', size=(4, 1)), sg.Button('D', size=(4, 1))],
            [sg.Text('Gear: P', key='gear_display', font=('Arial', 12, 'bold'))],
        ]
        
        adas_column = [
            [sg.Text('ADAS Options', font=('Arial', 14, 'bold'))],
            [sg.Checkbox('ABS', key='abs_check'), sg.Text('🔴', text_color='red', key='status_abs')],
            [sg.Checkbox('Traction Control', key='traction_check'), sg.Text('🔴', text_color='red', key='status_traction')],
            [sg.Checkbox('Lane Centering', key='lane_check'), sg.Text('🔴', text_color='red', key='status_lane')],
            [sg.Checkbox('Adaptive Cruise', key='acc_check'), sg.Text('🔴', text_color='red', key='status_acc')],
            [sg.Checkbox('Backup Camera', key='backup_check'), sg.Text('🔴', text_color='red', key='status_backup')],
            [sg.Text('ACC Target Speed (km/h):'), sg.Slider(range=(20, 200), default_value=100, orientation='h', size=(15, 15), key='acc_speed_slider')],
        ]
        
        can_column = [
            [sg.Text('CAN Message Log', font=('Arial', 14, 'bold'))],
            [sg.Button('Record CAN', key='record_can'), sg.Button('Export CAN', key='export_can'), sg.Button('Clear Log', key='clear_log')],
            [sg.Multiline(size=(80, 8), key='can_log', disabled=True, font=('Courier', 9))],
        ]
        
        layout = [
            [sg.Column(viz_column, vertical_alignment='top'),
             sg.Column(control_column, vertical_alignment='top'),
             sg.Column(adas_column, vertical_alignment='top'),
             sg.Column(can_column, vertical_alignment='top')],
        ]
        
        window = sg.Window('RosSim Unified Dashboard', layout)
        
        while True:
            event, values = window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED:
                break
            
            # Draw vehicle visualization
            vehicle_char, _ = self.draw_vehicle()
            window['vehicle_display'].update(f'\n\n  {vehicle_char}', text_color='cyan')
            
            # Update display
            window['pos_text'].update(f'Position: ({self.position_x:.1f}, {self.position_y:.1f})')
            window['speed_text'].update(f'Speed: {self.velocity:.1f} m/s')
            window['rpm_text'].update(f'RPM: {self.rpm:.0f}')
            window['heading_text'].update(f'Heading: {self.heading:.1f}°')
            
            # Steering control
            steering_msg = Float32()
            steering_msg.data = float(values['steering_slider'])
            self.steering_pub.publish(steering_msg)
            
            # Throttle control
            throttle_msg = Float32()
            throttle_msg.data = float(values['throttle_slider'])
            self.throttle_pub.publish(throttle_msg)
            
            # Brake control
            brake_msg = Float32()
            brake_msg.data = float(values['brake_slider'])
            self.brake_pub.publish(brake_msg)
            
            # Gear selection
            for gear in ['P', 'R', 'N', 'D']:
                if event == gear:
                    self.current_gear = gear
                    window['gear_display'].update(f'Gear: {gear}')
            
            # ADAS settings update
            if event in ['abs_check', 'traction_check', 'lane_check', 'acc_check', 'backup_check', 'acc_speed_slider']:
                self.adas_settings['abs_enabled'] = values['abs_check']
                self.adas_settings['traction_control'] = values['traction_check']
                self.adas_settings['lane_centering'] = values['lane_check']
                self.adas_settings['adaptive_cruise'] = values['acc_check']
                self.adas_settings['backup_camera'] = values['backup_check']
                self.adas_settings['cruise_speed'] = int(values['acc_speed_slider'])
                
                adas_msg = String()
                adas_msg.data = json.dumps(self.adas_settings)
                self.adas_pub.publish(adas_msg)
            
            # CAN record button
            if event == 'record_can':
                self.is_recording = not self.is_recording
                window['record_can'].update('Stop Recording' if self.is_recording else 'Record CAN')
            
            # CAN export button
            if event == 'export_can':
                if self.recorded_messages:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filepath = Path(f'/tmp/can_log_{timestamp}.json')
                    with open(filepath, 'w') as f:
                        json.dump(self.recorded_messages, f, indent=2)
                    self.get_logger().info(f'CAN log exported to {filepath}')
            
            # Clear log button
            if event == 'clear_log':
                self.can_messages.clear()
            
            # ADAS status display with colors
            abs_color = 'green' if self.adas_settings.get('abs_enabled') else 'red'
            traction_color = 'green' if self.adas_settings.get('traction_control') else 'red'
            lane_color = 'green' if self.adas_settings.get('lane_centering') else 'red'
            acc_color = 'green' if self.adas_settings.get('adaptive_cruise') else 'red'
            backup_color = 'green' if (self.adas_settings.get('backup_camera') and self.current_gear == 'R') else 'red'
            
            window['status_abs'].update(('🟢' if abs_color == 'green' else '🔴'), text_color=abs_color)
            window['status_traction'].update(('🟢' if traction_color == 'green' else '🔴'), text_color=traction_color)
            window['status_lane'].update(('🟢' if lane_color == 'green' else '🔴'), text_color=lane_color)
            window['status_acc'].update(('🟢' if acc_color == 'green' else '🔴'), text_color=acc_color)
            window['status_backup'].update(('🟢' if backup_color == 'green' else '🔴'), text_color=backup_color)
            
            # CAN log display
            if self.can_messages:
                log_lines = []
                for msg in self.can_messages[-20:]:
                    line = f"{msg['timestamp']} | {msg['gear']} | {msg['speed']:6.1f} m/s | {msg['rpm']:6.0f} RPM | ABS:{'Y' if msg['abs'] else 'N'} TR:{'Y' if msg['traction'] else 'N'} LC:{'Y' if msg['lane_center'] else 'N'} ACC:{'Y' if msg['acc'] else 'N'} BC:{'Y' if msg['backup_cam'] else 'N'}"
                    log_lines.append(line)
                log_text = '\n'.join(log_lines)
                window['can_log'].update(log_text)
            
            # Process ROS2 callbacks
            rclpy.spin_once(self, timeout_sec=0)
        
        window.close()

def main(args=None):
    rclpy.init(args=args)
    node = UnifiedDashboardNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
