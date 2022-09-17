import rclpy # Import the ROS client library for Python
from rclpy.node import Node # Enables the use of rclpy's Node class
from std_msgs.msg import Int32MultiArray # Enable use of the std_msgs/Float64MultiArray message type
import numpy as np # NumPy Python library
 
class PublishingSubscriber(Node):
  
  global arr2
  arr2 = []

  global Sortedarr2
  Sortedarr2 = Int32MultiArray()
  Sortedarr2.data = []

  def __init__(self):
   
    # Initiate the Node class's constructor and give it a name
    super().__init__('merge_arrays_node')
     
    # Create subscriber(s)    

    self.subscription_1 = self.create_subscription(Int32MultiArray, '/input/array1', self.sortArrays, 10)
    self.subscription_2 = self.create_subscription(Int32MultiArray, '/input/array2', self.sortArrays, 10)     
   
    # Create the publisher
    self.publisher1 = self.create_publisher(Int32MultiArray, '/output/array', 10)
    self.timer = self.create_timer(0.5, self.publish)

  def sortArrays(self, msg):
   
    i = 0
    for x in msg.data:
        if x not in arr2:
            arr2.append(msg.data[i])
        i += 1

    i = 0
    
    Sortedarr2.data = sorted(arr2)
       
  
  def publish(self):
    self.publisher1.publish(Sortedarr2)
    self.get_logger().info('Publishing: "%s"' % Sortedarr2.data)


def main(args=None):
 
  rclpy.init(args=args)
 
  # Create the node
  publishing_subscriber = PublishingSubscriber()
 
  # Spin the node so the callback function is called.
  # Pull messages from any topics this node is subscribed to.
  # Publish any pending messages to the topics.
  rclpy.spin(publishing_subscriber)
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  publishing_subscriber.destroy_node()
 
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
 
if __name__ == '__main__':
  main()
