#!/usr/bin/env python3
"""Vehicle Visualization GUI - PySimpleGUI 6.0 compatible"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import PySimpleGUI as sg

class VehicleVizNode(Node):
    def __init__(self):
        super().__init__('vehicle_viz')
        self.vehicle_state = {
            'x': 0.0, 'y': 0.0, 'vx': 0.0, 'vy': 0.0, 'yaw': 0.0,
            'speed_kmh': 0.0, 'rpm': 0.0, 'gear': 'P'
        }
        self.create_subscription(Twist, '/vehicle/state', self.state_callback, 10)
        self.create_subscription(String, '/vehicle/diagnostics', self.diagnostics_callback, 10)
        self.get_logger().info('Vehicle Visualization Node initialized')

    def state_callback(self, msg):
        self.vehicle_state['vx'] = msg.linear.x
        self.vehicle_state['vy'] = msg.linear.y
        self.vehicle_state['yaw'] = msg.angular.z
        self.vehicle_state['speed_kmh'] = abs(msg.linear.x) * 3.6

    def diagnostics_callback(self, msg):
        try:
            diag_data = dict(item.split(':') for item in msg.data.split(','))
            self.vehicle_state['x'] = float(diag_data.get('x', 0))
            self.vehicle_state['y'] = float(diag_data.get('y', 0))
            self.vehicle_state['speed_kmh'] = float(diag_data.get('speed', 0))
            self.vehicle_state['rpm'] = float(diag_data.get('rpm', 0))
            self.vehicle_state['gear'] = diag_data.get('gear', 'P')
        except:
            pass

    def create_gui(self):
        sg.theme('DarkBlue2')
        layout = [
            [sg.Text('VEHICLE VISUALIZATION', font=('Arial', 16, 'bold'))],
            [sg.Text('X: '), sg.Text('0.0', key='pos_x')],
            [sg.Text('Y: '), sg.Text('0.0', key='pos_y')],
            [sg.Text('Speed: '), sg.Text('0.0', key='speed'), sg.Text('km/h')],
            [sg.Text('RPM: '), sg.Text('0', key='rpm')],
            [sg.Text('Heading: '), sg.Text('0.0', key='heading'), sg.Text('°')],
            [sg.Text('Gear: '), sg.Text('P', key='gear')],
            [sg.Button('Exit')]
        ]
        return sg.Window('Vehicle Visualization', layout, finalize=True)

    def run(self):
        window = self.create_gui()
        if not window:
            return
        while True:
            event, values = window.read(timeout=100)
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            window['pos_x'].update(f"{self.vehicle_state['x']:.2f}")
            window['pos_y'].update(f"{self.vehicle_state['y']:.2f}")
            window['speed'].update(f"{self.vehicle_state['speed_kmh']:.1f}")
            window['rpm'].update(f"{self.vehicle_state['rpm']:.0f}")
            window['heading'].update(f"{self.vehicle_state['yaw']:.1f}")
            window['gear'].update(self.vehicle_state['gear'])
            rclpy.spin_once(self, timeout_sec=0.01)
        window.close()

def main():
    rclpy.init()
    node = VehicleVizNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
