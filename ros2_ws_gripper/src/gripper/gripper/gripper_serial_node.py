#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial

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

    def joy_callback(self, msg):
        if len(msg.buttons) <= max(OPEN_BUTTON, CLOSE_BUTTON):
            return

        if msg.buttons[OPEN_BUTTON]:
            cmd = 'O'
        elif msg.buttons[CLOSE_BUTTON]:
            cmd = 'C'
        else:
            cmd = 'L'

        if cmd != self.last_cmd:
            self.ser.write(cmd.encode())
            self.get_logger().info(f"Gripper → {cmd}")
            self.last_cmd = cmd

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
