#!/usr/bin/env python3
"""
Vehicle Control GUI

Provides interactive controls for:
- Steering wheel
- Accelerator pedal
- Brake pedal
- PRNDL transmission selector

ROS2 Jazzy compatible
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

try:
    import PySimpleGUI as sg
    GUI_FRAMEWORK = 'PySimpleGUI'
except ImportError:
    print("PySimpleGUI not found. Install with: pip install PySimpleGUI")
    GUI_FRAMEWORK = None


class ControlPanelNode(Node):
    """Vehicle Control GUI Node"""
    
    def __init__(self):
        super().__init__('control_panel')
        
        # Create publishers
        self.steering_pub = self.create_publisher(Float32, '/control/steering', 10)
        self.throttle_pub = self.create_publisher(Float32, '/control/throttle', 10)
        self.brake_pub = self.create_publisher(Float32, '/control/brake', 10)
        self.gear_pub = self.create_publisher(String, '/control/gear', 10)
        
        self.get_logger().info('Vehicle Control Panel Node initialized')
    
    def create_gui(self):
        """Create PySimpleGUI control panel"""
        if GUI_FRAMEWORK != 'PySimpleGUI':
            self.get_logger().error('PySimpleGUI not available')
            return None
        
        sg.theme('DarkBlue2')
        
        layout = [
            [sg.Text('VEHICLE CONTROL PANEL', font=('Arial', 16, 'bold'))],
            [sg.Separator()],
            [sg.Text('Steering Wheel (degrees):', font=('Arial', 12, 'bold'))],
            [sg.Slider(range=(-30, 30), default_value=0, size=(30, 15), 
                       orientation='h', key='steering', enable_events=True)],
            [sg.Text('Steering: 0°', key='steering_display', size=(20, 1))],
            [sg.Separator()],
            [sg.Text('Gas Pedal (%)', font=('Arial', 12, 'bold')),
             sg.Text('Brake Pedal (%)', font=('Arial', 12, 'bold'))],
            [sg.Slider(range=(0, 100), default_value=0, size=(15, 15),
                       orientation='v', key='throttle', enable_events=True),
             sg.Slider(range=(0, 100), default_value=0, size=(15, 15),
                       orientation='v', key='brake', enable_events=True)],
            [sg.Text('0%', key='throttle_display', size=(8, 1)),
             sg.Text('0%', key='brake_display', size=(8, 1))],
            [sg.Separator()],
            [sg.Text('Transmission:', font=('Arial', 12, 'bold'))],
            [sg.Button('P'), sg.Button('R'), sg.Button('N'), 
             sg.Button('D'), sg.Button('L')],
            [sg.Text('Current: P', key='gear_display', size=(15, 1))],
            [sg.Separator()],
            [sg.Button('Quit')],
        ]
        
        window = sg.Window('Vehicle Control', layout, finalize=True)
        return window
    
    def publish_controls(self, steering, throttle, brake, gear):
        """Publish control values"""
        # Convert steering angle to radians
        import math
        steering_rad = steering * math.pi / 180.0
        steering_msg = Float32()
        steering_msg.data = steering_rad
        self.steering_pub.publish(steering_msg)
        
        # Publish throttle (0-100 -> 0.0-1.0)
        throttle_msg = Float32()
        throttle_msg.data = throttle / 100.0
        self.throttle_pub.publish(throttle_msg)
        
        # Publish brake (0-100 -> 0.0-1.0)
        brake_msg = Float32()
        brake_msg.data = brake / 100.0
        self.brake_pub.publish(brake_msg)
        
        # Publish gear
        gear_msg = String()
        gear_msg.data = gear
        self.gear_pub.publish(gear_msg)
    
    def update_gui(self, window):
        """Update GUI and handle events"""
        if window is None:
            return False
        
        event, values = window.read(timeout=50)
        
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            return False
        
        # Get current values
        steering = int(values['steering'])
        throttle = int(values['throttle'])
        brake = int(values['brake'])
        
        # Determine current gear based on button press
        gear = 'P'  # Default
        if event in ['P', 'R', 'N', 'D', 'L']:
            gear = event
        
        # Update displays
        window['steering_display'].update(f'Steering: {steering}°')
        window['throttle_display'].update(f'{int(throttle)}%')
        window['brake_display'].update(f'{int(brake)}%')
        window['gear_display'].update(f'Current: {gear}')
        
        # Publish control values
        self.publish_controls(steering, throttle, brake, gear)
        
        return True
    
    def run(self):
        """Run control panel GUI"""
        if GUI_FRAMEWORK != 'PySimpleGUI':
            self.get_logger().error('PySimpleGUI framework not available')
            return
        
        window = self.create_gui()
        if window is None:
            return
        
        try:
            while self.update_gui(window):
                rclpy.spin_once(self, timeout_sec=0.01)
        except KeyboardInterrupt:
            pass
        finally:
            if window:
                window.close()


def main(args=None):
    rclpy.init(args=args)
    node = ControlPanelNode()
    
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
