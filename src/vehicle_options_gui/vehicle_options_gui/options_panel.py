#!/usr/bin/env python3
"""
Vehicle Options GUI

Configuration panel for:
- Safety systems (ABS, traction control)
- ADAS features (lane centering, ACC, backup camera)

ROS2 Jazzy compatible
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    import PySimpleGUI as sg
    GUI_FRAMEWORK = 'PySimpleGUI'
except ImportError:
    print("PySimpleGUI not found. Install with: pip install PySimpleGUI")
    GUI_FRAMEWORK = None


class OptionsPanelNode(Node):
    """Vehicle Options GUI Node"""
    
    def __init__(self):
        super().__init__('options_panel')
        
        # Create publishers
        self.adas_settings_pub = self.create_publisher(String, '/adas/settings', 10)
        
        # Current settings
        self.abs_enabled = False
        self.tc_enabled = False
        self.lane_center_enabled = False
        self.acc_enabled = False
        self.acc_target_speed = 60.0
        self.backup_camera_enabled = False
        
        # Create subscriber to ADAS status
        self.create_subscription(String, '/adas/status', self.status_callback, 10)
        
        self.get_logger().info('Vehicle Options Panel Node initialized')
    
    def status_callback(self, msg):
        """Receive ADAS status updates"""
        self.get_logger().debug(f'ADAS Status: {msg.data}')
    
    def create_gui(self):
        """Create PySimpleGUI options panel"""
        if GUI_FRAMEWORK != 'PySimpleGUI':
            self.get_logger().error('PySimpleGUI not available')
            return None
        
        sg.theme('DarkBlue2')
        
        layout = [
            [sg.Text('VEHICLE OPTIONS', font=('Arial', 16, 'bold'))],
            [sg.Separator()],
            [sg.Text('SAFETY SYSTEMS', font=('Arial', 12, 'bold'))],
            [sg.Checkbox('ABS (Anti-Lock Braking)', default=False, key='abs', enable_events=True)],
            [sg.Checkbox('Traction Control', default=False, key='traction', enable_events=True)],
            [sg.Separator()],
            [sg.Text('ADAS FEATURES', font=('Arial', 12, 'bold'))],
            [sg.Checkbox('Lane Centering Assist', default=False, key='lane_center', enable_events=True)],
            [sg.Checkbox('Adaptive Cruise Control', default=False, key='acc', enable_events=True)],
            [sg.Text('ACC Target Speed (km/h):', size=(25, 1)),
             sg.Slider(range=(0, 200), default_value=60, size=(20, 15),
                       orientation='h', key='acc_speed', disabled=True, enable_events=True)],
            [sg.Checkbox('Backup Camera', default=False, key='backup_camera', enable_events=True)],
            [sg.Separator()],
            [sg.Text('ACTIVE SYSTEMS:', font=('Arial', 12, 'bold'))],
            [sg.Multiline(size=(40, 6), key='status_display', disabled=True)],
            [sg.Separator()],
            [sg.Button('Quit')],
        ]
        
        window = sg.Window('Vehicle Options', layout, finalize=True)
        return window
    
    def publish_settings(self):
        """Publish current settings"""
        settings_str = (
            f"abs:{'true' if self.abs_enabled else 'false'},"
            f"tc:{'true' if self.tc_enabled else 'false'},"
            f"lane:{'true' if self.lane_center_enabled else 'false'},"
            f"acc:{'true' if self.acc_enabled else 'false'},"
            f"acc_speed:{self.acc_target_speed},"
            f"backup:{'true' if self.backup_camera_enabled else 'false'}"
        )
        
        msg = String()
        msg.data = settings_str
        self.adas_settings_pub.publish(msg)
    
    def update_gui(self, window):
        """Update GUI and handle events"""
        if window is None:
            return False
        
        event, values = window.read(timeout=100)
        
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            return False
        
        # Update settings from GUI
        self.abs_enabled = values['abs']
        self.tc_enabled = values['traction']
        self.lane_center_enabled = values['lane_center']
        self.acc_enabled = values['acc']
        self.acc_target_speed = int(values['acc_speed'])
        self.backup_camera_enabled = values['backup_camera']
        
        # Update ACC speed slider disabled state
        window['acc_speed'].update(disabled=not self.acc_enabled)
        
        # Publish settings if anything changed
        if event in ['abs', 'traction', 'lane_center', 'acc', 'acc_speed', 'backup_camera']:
            self.publish_settings()
        
        # Update status display
        active_systems = []
        if self.abs_enabled:
            active_systems.append('✓ ABS')
        if self.tc_enabled:
            active_systems.append('✓ Traction Control')
        if self.lane_center_enabled:
            active_systems.append('✓ Lane Centering')
        if self.acc_enabled:
            active_systems.append(f'✓ ACC ({self.acc_target_speed} km/h)')
        if self.backup_camera_enabled:
            active_systems.append('✓ Backup Camera')
        
        status_text = '\n'.join(active_systems) if active_systems else 'No systems active'
        window['status_display'].update(status_text)
        
        return True
    
    def run(self):
        """Run options panel GUI"""
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
    node = OptionsPanelNode()
    
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
