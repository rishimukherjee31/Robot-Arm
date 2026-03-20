# Gripper

ROS2 serial control node for the [Blue Robotics Newton Gripper](https://bluerobotics.com/store/rov/tools/newton-subsea-gripper/). Subscribes to `meco/joy` and sends open/close/stop commands to a Teensy microcontroller over USB serial.

---

## Hardware

- Teensy (connected via USB)
- Blue Robotics Newton Subsea Gripper
- Joystick / gamepad

---

## Building the Package

Clone the repo and build from the workspace root:

```bash
cd ~/ros2_ws_gripper
colcon build
source install/setup.bash
```

To permanently source the workspace, add it to your `.bashrc`:

```bash
echo "source ~/ros2_ws_gripper/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Running the Node

### With the alias (recommended)

Add the following alias to your `~/.bashrc`:

```bash
alias gripper='source ~/ros2_ws_gripper/install/setup.bash && ros2 run gripper gripper_serial_node'
```

Then apply and run:

```bash
source ~/.bashrc
gripper
```

### Without the alias

```bash
source ~/ros2_ws_gripper/install/setup.bash
ros2 run gripper gripper_serial_node
```

### Overriding the serial port or baud rate

```bash
ros2 run gripper gripper_serial_node --ros-args -p serial_port:=/dev/ttyACM1 -p baud_rate:=57600
```

---

## Running the Joystick

In a **separate terminal**, run:

```bash
joy
```

This launches the joystick node which publishes to `meco/joy`. The gripper node will respond to button presses once both nodes are running.

---

## Button Mapping

| Button Index | Action |
|---|---|
| `OPEN_BUTTON` (default: `0`) | Opens the gripper while held |
| `CLOSE_BUTTON` (default: `1`) | Closes the gripper while held |
| Neither pressed | Gripper stops (neutral) |

To find the correct indices for your controller, run:

```bash
ros2 topic echo meco/joy
```

Then press each button and note which index in the `buttons` array changes to `1`. Update `OPEN_BUTTON` and `CLOSE_BUTTON` in `gripper/gripper_serial_node.py` accordingly.

---

## Troubleshooting

**Serial port permission denied**
```bash
sudo usermod -aG dialout $USER
# Log out and back in for this to take effect
```

**Find the Teensy's port**
```bash
ls /dev/ttyACM*
# or
dmesg | tail
```

**Monitor serial commands being sent to the Teensy**
```bash
# Stop the gripper node first, then:
stty -F /dev/ttyACM0 57600 && cat /dev/ttyACM0
```
