import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        # Subscribe to distance from ESP32
        self.distance_sub = self.create_subscription(
            Int32,
            '/distance',
            self.distance_callback,
            10
        )

        # Publish servo angle
        self.servo_pub = self.create_publisher(
            Int32,
            '/servo_angle',
            10
        )

        # Servo state
        self.angle = 40
        self.direction = 1

        # Whether an object is currently considered detected
        self.object_detected = False

        # Move servo every 100 ms
        self.timer = self.create_timer(
            0.1,
            self.servo_timer_callback
        )

    def distance_callback(self, msg):

        distance = msg.data

        # Start rotating when object is closer than 20 cm
        if distance < 20:
            self.object_detected = True

        # Stop rotating only after object is farther than 25 cm
        elif distance > 25:
            self.object_detected = False

        self.get_logger().info(
            f'Distance: {distance} cm'
        )

    def servo_timer_callback(self):

        if self.object_detected:

            # Move servo
            self.angle += 5 * self.direction

            # Reverse direction at 140°
            if self.angle >= 140:
                self.angle = 140
                self.direction = -1

            # Reverse direction at 40°
            elif self.angle <= 40:
                self.angle = 40
                self.direction = 1

            servo_msg = Int32()
            servo_msg.data = self.angle

            self.servo_pub.publish(servo_msg)

        else:

            # No object detected
            # Keep servo at center
            servo_msg = Int32()
            servo_msg.data = 90

            self.servo_pub.publish(servo_msg)


def main(args=None):

    rclpy.init(args=args)

    node = RobotController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
