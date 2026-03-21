# Gripper - ROS2 Package

Serial control node for the [Blue Robotics Newton Subsea Gripper](https://bluerobotics.com/store/rov/tools/newton-subsea-gripper/). Subscribes to `meco/joy` and sends open/close/stop commands to a Teensy microcontroller over USB serial.

---

## Hardware

<table>
  <tr>
    <td align="center" width="25%">
      <a href="[LINK_TO_GRIPPER_PAGE](https://bluerobotics.com/store/thrusters/grippers/newton-gripper-asm-r2-rp/)">
        <img src="images/gripper_bluerobotics.png" alt="Newton Gripper"/>
      </a>
      <br/><em>Blue Robotics Newton Subsea Gripper</em>
    </td>
    <td align="center" width="25%">
      <a href="[LINK_TO_TEENSY_PAGE](https://www.adafruit.com/product/4622?gad_source=1&gad_campaignid=23438252138&gbraid=0AAAAADx9JvTZZ7gwLZCzYd8QUhY5R7cGz&gclid=Cj0KCQjw4PPNBhD8ARIsAMo-icxPHWb_9d_0uVnq1ScXd9T21jGUxf40RBOnBfyuICJ9U_wETMItf4IaAiNBEALw_wcB)">
        <img src="images/teensy.png" alt="Teensy"/>
      </a>
      <br/><em>Teensy — outputs PWM to the gripper</em>
    </td>
    <td align="center" width="25%">
      <a href="[LINK_TO_JETSON_PAGE](https://www.seeedstudio.com/NVIDIAr-Jetson-Orintm-Nano-Developer-Kit-p-5617.html?gad_source=1&gad_campaignid=12740460396&gbraid=0AAAAACiAB46QW1SzoVzo1UtJA9xO5rX2P&gclid=Cj0KCQjw4PPNBhD8ARIsAMo-icwXl3e9NurcGByQ_XoXVKZpOYZagCgubZqKdcpjKv-6ngYbDYGzkAQaAg3zEALw_wcB)">
        <img src="images/jetson.png" alt="Jetson"/>
      </a>
      <br/><em>Jetson — runs the ROS2 gripper node</em>
    </td>
    <td align="center" width="25%">
      <a href="LINK_TO_LAPTOP_PAGE">
        <img src="images/laptop.jpg" alt="Laptop"/>
      </a>
      <br/><em>Laptop — runs the joystick node</em>
    </td>
  </tr>
</table>


<p align="center"><em>Harware used.</em></p>

![System Schematic](images/schematic.png)

<p align="center"><em>System schematic showign wiring between devices.</em></p>

---

## Package Structure

```
ros2_ws_gripper/
└── src/
    └── gripper/
        ├── gripper/
        │   ├── __init__.py
        │   └── gripper_serial_node.py
        ├── resource/
        │   └── gripper
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```

---

## Dependencies

### System Dependencies
- ROS2 (Humble)
- Python 3
- python3-serial

```bash
sudo apt install python3-serial
```

### ROS2 Dependencies
- rclpy
- sensor_msgs

---

## Building the Package

### First Time Setup

```bash
# Navigate to workspace
cd ~/ros2_ws_gripper

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Source ROS2
source /opt/ros/humble/setup.bash

# Build the package
colcon build --packages-select gripper

# Source the workspace
source install/setup.bash
```

### Rebuilding After Changes

```bash
cd ~/ros2_ws_gripper

# Clean build (recommended after major changes)
rm -rf build/ install/ log/
colcon build --packages-select gripper

# Or incremental build
colcon build --packages-select gripper

# Source the workspace
source install/setup.bash
```

### Permanently Source the Workspace

```bash
echo "source ~/ros2_ws_gripper/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Running the Nodes

### Set Up the Alias (Recommended)

Add the following to your `~/.bashrc`:

```bash
alias gripper='source ~/ros2_ws_gripper/install/setup.bash && ros2 run gripper gripper_serial_node'
```

Apply it:

```bash
source ~/.bashrc
```

### Step 1 — Launch the Joystick Node

In a **separate terminal** on the laptop, run:

```bash
joy
```

![Joy Terminal](images/joy.png)

<p align="center"><em>Joystick node publishing to <code>meco/joy</code>.</em></p>

### Step 2 — Launch the Gripper Node

#### With the alias

```bash
gripper
```

#### Without the alias

```bash
source ~/ros2_ws_gripper/install/setup.bash
ros2 run gripper gripper_serial_node
```

![Gripper Terminal](images/gripper.png)

<p align="center"><em>Gripper node connected to the Teensy over serial.</em></p>

### Overriding Serial Port or Baud Rate

```bash
ros2 run gripper gripper_serial_node --ros-args -p serial_port:=/dev/ttyACM1 -p baud_rate:=57600
```

---

## Button Mapping

| Button Index | Action |
|---|---|
| `OPEN_BUTTON` (default: `0`) | Opens the gripper while held |
| `CLOSE_BUTTON` (default: `1`) | Closes the gripper while held |
| Neither pressed | Gripper stops (neutral / 1500µs) |

To find the correct indices for your controller:

```bash
ros2 topic echo meco/joy
```

Press each button and note which index in the `buttons` array changes to `1`. Update `OPEN_BUTTON` and `CLOSE_BUTTON` in `gripper/gripper_serial_node.py` accordingly.

---

## Teensy Serial Protocol

The Teensy listens for single-character commands over USB serial at 57600 baud:

| Command | Action |
|---|---|
| `O` | Open gripper (1100µs PWM) |
| `C` | Close gripper (1900µs PWM) |
| `S` | Stop / neutral (1500µs PWM) |

---

## Troubleshooting

### Serial port permission denied
```bash
sudo usermod -aG dialout $USER
# Log out and back in for this to take effect
```

### Find the Teensy's port
```bash
ls /dev/ttyACM*
# or
dmesg | tail
```

### Monitor serial commands being sent to the Teensy
```bash
# Stop the gripper node first, then:
stty -F /dev/ttyACM0 57600 && cat /dev/ttyACM0
```

### Package not found
```bash
# Make sure you sourced the workspace
source ~/ros2_ws_gripper/install/setup.bash

# Check if package is built
ros2 pkg list | grep gripper
```

### Node is running but gripper is not responding
```bash
# Confirm joy messages are flowing and check button indices
ros2 topic echo meco/joy

# Check the node is subscribed
ros2 node info /gripper_serial_node
```

---

## License

MIT
