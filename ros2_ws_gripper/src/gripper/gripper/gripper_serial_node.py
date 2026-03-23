#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial
import time

# Debouncer
DOUBLE_PRESS_MIN_MS = 200   # ignore if same command seen within this window
DOUBLE_PRESS_MAX_MS = 500   # only count as double press within this window

OPEN_BUTTON  = 11   # Right stick button
CLOSE_BUTTON = 10   # Left stick button


class GripperSerialNode(Node):
    def __init__(self):
        super().__init__('gripper_serial_node')

        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 57600)

        port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value

        self.ser = serial.Serial(port, baud, timeout=1)
        self.get_logger().info(f"Opened serial port {port} at {baud} baud")

        self.last_cmd = None

        self.create_subscription(Joy, 'meco/joy', self.joy_callback, 10)
        self.get_logger().info("Gripper serial node ready")

        self.last_cmd = None
        self.prev_command = None
        self.last_cmd_time = 0.

    def joy_callback(self, msg):
        if len(msg.buttons) <= max(OPEN_BUTTON, CLOSE_BUTTON):
            return

        if msg.buttons[OPEN_BUTTON]:
            cmd = 'O'
        elif msg.buttons[CLOSE_BUTTON]:
            cmd = 'C'
        else:
            return
            
        now = time.time() * 1000  # ms
        elapsed = now - self.last_cmd_time
        
        if elapsed < DOUBLE_PRESS_MIN_MS:
            return

        if cmd == self.prev_command and elapsed < DOUBLE_PRESS_MAX_MS:
            # Confirmed double press — stop and reset
            self.ser.write(b'S')
            self.get_logger().info("Gripper → S (double press stop)")
            self.prev_command = None
            self.last_cmd = 'S'
            self.last_cmd_time = now
            return

        if cmd != self.last_cmd:
            self.ser.write(cmd.encode())
            self.get_logger().info(f"Gripper → {cmd}")
            self.last_cmd = cmd

        self.prev_command = cmd
        self.last_cmd_time = now

    def destroy_node(self):
        self.ser.write(b'S')
        self.ser.close()
        self.get_logger().info("Serial port closed")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GripperSerialNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
