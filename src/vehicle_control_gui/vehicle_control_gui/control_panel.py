#!/usr/bin/env python3
"""Vehicle Control GUI"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
import PySimpleGUI as sg

class ControlPanelNode(Node):
    def __init__(self):
        super().__init__('vehicle_control_gui')
        self.steering_pub = self.create_publisher(Float32, '/control/steering', 10)
        self.throttle_pub = self.create_publisher(Float32, '/control/throttle', 10)
        self.brake_pub = self.create_publisher(Float32, '/control/brake', 10)
        self.gear_pub = self.create_publisher(String, '/control/gear', 10)
        self.current_gear = 'P'
        self.create_timer(0.05, self.publish_gear_timer)
        self.get_logger().info('Vehicle Control Panel initialized')

    def publish_gear_timer(self):
        msg = String()
        msg.data = self.current_gear
        self.gear_pub.publish(msg)

    def create_gui(self):
        sg.theme('DarkBlue2')
        layout = [
            [sg.Text('VEHICLE CONTROL PANEL', font=('Arial', 14, 'bold'))],
            [sg.Text('Steering:')],
            [sg.Slider(range=(-100, 100), default_value=0, size=(40, 15), orientation='h', key='steering', enable_events=True)],
            [sg.Text('Steering: 0°', key='steering_val')],
            [sg.Text('Throttle:')],
            [sg.Slider(range=(0, 100), default_value=0, size=(40, 15), orientation='h', key='throttle', enable_events=True)],
            [sg.Text('Throttle: 0%', key='throttle_val')],
            [sg.Text('Brake:')],
            [sg.Slider(range=(0, 100), default_value=0, size=(40, 15), orientation='h', key='brake', enable_events=True)],
            [sg.Text('Brake: 0%', key='brake_val')],
            [sg.Text('Transmission:')],
            [sg.Button('P', key='gear_P', size=(6, 2)), sg.Button('R', key='gear_R', size=(6, 2)), sg.Button('N', key='gear_N', size=(6, 2)), sg.Button('D', key='gear_D', size=(6, 2))],
            [sg.Text('Current Gear: P', key='gear_display')],
            [sg.Button('Exit')]
        ]
        return sg.Window('Vehicle Control Panel', layout, finalize=True)

    def run(self):
        window = self.create_gui()
        gear_buttons = {'gear_P': 'P', 'gear_R': 'R', 'gear_N': 'N', 'gear_D': 'D'}
        
        while True:
            event, values = window.read(timeout=100)
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            
            if event == 'steering':
                val = values['steering']
                window['steering_val'].update(f'Steering: {val:.0f}°')
                msg = Float32()
                msg.data = float(val)
                self.steering_pub.publish(msg)
            
            if event == 'throttle':
                val = values['throttle']
                window['throttle_val'].update(f'Throttle: {val:.0f}%')
                msg = Float32()
                msg.data = float(val)
                self.throttle_pub.publish(msg)
            
            if event == 'brake':
                val = values['brake']
                window['brake_val'].update(f'Brake: {val:.0f}%')
                msg = Float32()
                msg.data = float(val)
                self.brake_pub.publish(msg)
            
            if event in gear_buttons:
                self.current_gear = gear_buttons[event]
                window['gear_display'].update(f'Current Gear: {self.current_gear}')
                self.get_logger().info(f'Gear: {self.current_gear}')
            
            rclpy.spin_once(self, timeout_sec=0.01)
        window.close()

def main():
    rclpy.init()
    node = ControlPanelNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
