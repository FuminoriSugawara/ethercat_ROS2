import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys
import tty
import termios

class VelocityControlPublisher(Node):
    def __init__(self):
        super().__init__('velocity_control_publisher')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 1)
        self.velocities = [0.0]  # デフォルト値

    def publish_velocity(self):
        msg = Float64MultiArray()
        msg.data = self.velocities
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing velocity: {self.velocities}')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main(args=None):
    rclpy.init(args=args)
    
    velocity_control_publisher = VelocityControlPublisher()
    
    print("Press 0-3 to change velocity, or 'q' to quit:")
    print("0: 0, 1: 100, 2: 200, 3: -100, 4: -200")
    
    while True:
        key = getch()
        if key == '0':
            velocity_control_publisher.velocities[0] = 0.0
        elif key == '1':
            velocity_control_publisher.velocities[0] = 100.0
        elif key == '2':
            velocity_control_publisher.velocities[0] = 200.0
        elif key == '3':
            velocity_control_publisher.velocities[0] = -100.0
        elif key == '4':
            velocity_control_publisher.velocities[0] = -200.0

        elif key.lower() == 'q':
            break
        else:
            continue
        
        velocity_control_publisher.publish_velocity()
    
    velocity_control_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()