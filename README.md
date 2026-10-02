ROS 2 micro-ROS Robot Controller

ROS 2 Jazzy controller for an ESP32-based robot using micro-ROS. The controller receives ultrasonic distance measurements from the ESP32 and publishes servo-angle commands based on the detected distance.

The current implementation communicates with the ESP32 through a USB serial micro-ROS Agent.

System Architecture

             USB Serial
ESP32 ─────────────────────> micro-ROS Agent
 │                              │
 │ /distance                    ▼
 │                           ROS 2
 │                              │
 │                       robot_controller
 │                              │
 │                         /servo_angle
 │                              │
 └──────────────────────────────┘

ROS 2 Package

The main package is:

robot_controller

The controller node is:

robot_controller

Run it with:

ros2 run robot_controller controller

Requirements

Ubuntu with ROS 2 Jazzy

micro-ROS Agent

Python 3

rclpy

std_msgs

ESP32 running the corresponding micro-ROS firmware

Topics

Subscribed

/distance

Type:

std_msgs/msg/Int32

The ESP32 publishes the distance measured by the HC-SR04.

Published

/servo_angle

Type:

std_msgs/msg/Int32

The controller publishes the desired servo angle.

Controller Behavior

The controller uses ultrasonic distance to determine whether an object is nearby.

Distance

Behavior

< 20 cm

Start servo sweeping

20–25 cm

Maintain the current detection state

> 25 cm

Stop sweeping and command 90°

When an object is detected, the servo sweeps between:

40° ↔ 140°

The 20 cm / 25 cm thresholds provide hysteresis and help prevent rapid state changes when the measured distance fluctuates around the detection threshold.

Creating the Package

cd ~/ROS_Projects/microros_ws/src

ros2 pkg create     --build-type ament_python     --license Apache-2.0     robot_controller     --dependencies rclpy std_msgs

Building

From the workspace root:

cd ~/ROS_Projects/microros_ws
colcon build --packages-select robot_controller
source install/local_setup.bash

Running

1. Source ROS 2

source /opt/ros/jazzy/setup.bash

2. Source the micro-ROS workspace

source ~/ROS_Projects/microros_ws/install/local_setup.bash

3. Start the micro-ROS Agent

With the ESP32 connected through USB:

ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0

The serial device may be different on another system.

4. Start the controller

Open another terminal:

source /opt/ros/jazzy/setup.bash
source ~/ROS_Projects/microros_ws/install/local_setup.bash

ros2 run robot_controller controller

Useful ROS 2 Commands

List nodes:

ros2 node list

List topics:

ros2 topic list

View distance measurements:

ros2 topic echo /distance

View servo commands:

ros2 topic echo /servo_angle

Manually send a servo command:

ros2 topic pub --once /servo_angle std_msgs/msg/Int32 "{data: 90}"

Development Workflow

There are two separate parts of the project.

ESP32 Firmware

The ESP32 firmware is developed and uploaded using PlatformIO.

PlatformIO
    │
    ▼
ESP32 firmware
    │
    ▼
micro-ROS client

Changes to main.cpp require rebuilding and uploading the ESP32 firmware:

pio run --target upload

ROS 2 Controller

The ROS 2 controller runs as a Python node on Ubuntu.

Changes to controller.py require rebuilding the ROS 2 package:

cd ~/ROS_Projects/microros_ws
colcon build --packages-select robot_controller
source install/local_setup.bash

Then:

ros2 run robot_controller controller

Git

The following generated directories should not be committed:

build/
install/
log/

The repository should contain the ROS 2 source package and its configuration files.

Learning Objectives

This project provides practical experience with:

ROS 2 Jazzy

Python ROS 2 nodes

rclpy

ROS 2 publishers

ROS 2 subscribers

ROS 2 topics

micro-ROS

micro-ROS Agent

ESP32 communication

Sensor-to-ROS communication

ROS-to-actuator communication

Basic robot control logic

Future Improvements

Wi-Fi micro-ROS transport

Robot motor control

Autonomous navigation behavior

Multiple ultrasonic sensors

Sensor filtering

Custom ROS 2 messages

ROS 2 parameters

Launch files

Improved servo control
