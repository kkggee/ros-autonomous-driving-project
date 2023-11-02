import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile


class M_pubsub(Node):
    def __init__(self):
        pass



def main (args=None):
    rclpy.init(args=args)
    node=M_pubsub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('keyboard interrupt')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
