#!/usr/bin/env python3
"""
Vehicle Visualization GUI

Displays real-time vehicle state including position, velocity, orientation,
steering angle, and current gear.

ROS2 Jazzy compatible
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

try:
    import PySimpleGUI as sg
    GUI_FRAMEWORK = 'PySimpleGUI'
except ImportError:
    print("PySimpleGUI not found. Install with: pip install PySimpleGUI")
    GUI_FRAMEWORK = None


class VehicleVizNode(Node):
    """Vehicle Visualization GUI Node"""
    
    def __init__(self):
        super().__init__('vehicle_viz')
        
        self.vehicle_state = {
            'x': 0.0,
            'y': 0.0,
            'vx': 0.0,
            'vy': 0.0,
            'yaw': 0.0,
            'steering': 0.0,
            'speed_kmh': 0.0,
            'rpm': 0.0,
            'gear': 'P'
        }
        
        # Create subscriber to vehicle state
        self.create_subscription(Twist, '/vehicle/state', self.state_callback, 10)
        self.create_subscription(String, '/vehicle/diagnostics', self.diagnostics_callback, 10)
        
        self.get_logger().info('Vehicle Visualization Node initialized')
    
    def state_callback(self, msg):
        """Update vehicle state from model"""
        self.vehicle_state['vx'] = msg.linear.x
        self.vehicle_state['vy'] = msg.linear.y
        self.vehicle_state['yaw'] = msg.angular.z
        self.vehicle_state['speed_kmh'] = abs(msg.linear.x) * 3.6  # m/s to km/h
    
    def diagnostics_callback(self, msg):
        """Update diagnostics from vehicle model"""
        try:
            diag_data = dict(item.split(':') for item in msg.data.split(','))
            self.vehicle_state['x'] = float(diag_data.get('x', 0))
            self.vehicle_state['y'] = float(diag_data.get('y', 0))
            self.vehicle_state['speed_kmh'] = float(diag_data.get('speed', 0))
            self.vehicle_state['rpm'] = float(diag_data.get('rpm', 0))
            self.vehicle_state['gear'] = diag_data.get('gear', 'P')
        except Exception as e:
            self.get_logger().warn(f'Error parsing diagnostics: {e}')
    
    def create_gui(self):
        """Create PySimpleGUI window"""
        if GUI_FRAMEWORK != 'PySimpleGUI':
            self.get_logger().error('PySimpleGUI not available')
            return None
        
        sg.theme('DarkBlue2')
        
        layout = [
            [sg.Text('VEHICLE VISUALIZATION', font=('Arial', 16, 'bold'))],
            [sg.Separator()],
            [sg.Text('Position: X=', width=15), sg.Text('0.0', key='pos_x', size=(10, 1))],
            [sg.Text('Position: Y=', width=15), sg.Text('0.0', key='pos_y', size=(10, 1))],
            [sg.Separator()],
            [sg.Text('Speed (km/h):', width=15), sg.Text('0.0', key='speed', size=(10, 1))],
            [sg.Text('RPM:', width=15), sg.Text('0', key='rpm', size=(10, 1))],
            [sg.Text('Heading (deg):', width=15), sg.Text('0.0', key='heading', size=(10, 1))],
            [sg.Separator()],
            [sg.Text('Current Gear:', width=15), sg.Text('P', key='gear', size=(10, 1))],
            [sg.Separator()],
            [sg.Button('Quit')],
        ]
        
        window = sg.Window('Vehicle Visualization', layout, finalize=True)
        return window
    
    def update_gui(self, window):
        """Update GUI with current vehicle state"""
        if window is None:
            return False
        
        event, values = window.read(timeout=100)
        
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            return False
        
        # Update displays
        window['pos_x'].update(f"{self.vehicle_state['x']:.1f}")
        window['pos_y'].update(f"{self.vehicle_state['y']:.1f}")
        window['speed'].update(f"{self.vehicle_state['speed_kmh']:.1f}")
        window['rpm'].update(f"{self.vehicle_state['rpm']:.0f}")
        window['heading'].update(f"{self.vehicle_state['yaw'] * 57.3:.1f}")  # rad to deg
        window['gear'].update(self.vehicle_state['gear'])
        
        return True
    
    def run(self):
        """Run visualization GUI"""
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
    node = VehicleVizNode()
    
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
