import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from nav2_msgs.action import FollowWaypoints
# from rclpy.duration import Duration # Handles time for ROS 2

class ClientFollowPoints(Node):

    def __init__(self):
        super().__init__('client_follow_points')
        self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')

    def send_points(self, points):
        msg = FollowWaypoints.Goal()
        msg.poses = points

        self._client.wait_for_server()
        self._send_goal_future = self._client.send_goal_async(msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.missed_waypoints))
        location=input("목적지 : ")

        if location == "a":
            ix=0.05
            iy=2.05
        elif location =="b":
            ix=2.1
            iy=1.98
        elif location =="c":
            ix=1.9
            iy=0.25
        else:
            ix=0.15
            iy=0.08

        rgoal = PoseStamped()
        rgoal.header.frame_id = "map"
        rgoal.header.stamp.sec = 0
        rgoal.header.stamp.nanosec = 0
        rgoal.pose.position.z = 0.0
        rgoal.pose.position.x = ix
        rgoal.pose.position.y = iy
        rgoal.pose.orientation.w = 1.0
        print(rgoal)
        mgoal = [rgoal]

        self.send_points(mgoal)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))

def main(args=None):
    rclpy.init(args=args)

    follow_points_client = ClientFollowPoints()
    print('client inited')

    location=input("목적지 : ")

    if location == "a":
        ix=0.05
        iy=2.05
    elif location =="b":
        ix=2.1
        iy=1.98
    elif location =="c":
        ix=1.9
        iy=0.25
    else:
        ix=0.15
        iy=0.08


    rgoal = PoseStamped()
    rgoal.header.frame_id = "map"
    rgoal.header.stamp.sec = 0
    rgoal.header.stamp.nanosec = 0
    rgoal.pose.position.z = 0.0
    rgoal.pose.position.x = ix
    rgoal.pose.position.y = iy
    rgoal.pose.orientation.w = 1.0
    print(rgoal)
    mgoal = [rgoal]

    follow_points_client.send_points(mgoal)

    rclpy.spin(follow_points_client)
