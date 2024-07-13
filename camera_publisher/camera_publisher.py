import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.image_publisher = self.create_publisher(Image, '/sensors/camera/image_color', 10)
        self.info_publisher = self.create_publisher(CameraInfo, '/sensors/camera/camera_info', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            height, width, _ = frame.shape
            shift_amount = 128
            frame = np.roll(frame, shift_amount, axis=1)
            #frame[:, -shift_amount:] = 0
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.image_publisher.publish(img_msg)

            # Create and publish CameraInfo message
            camera_info = CameraInfo()
            camera_info.header.stamp = self.get_clock().now().to_msg()
            camera_info.header.frame_id = "camera_frame"
            # Add more CameraInfo details if available
            self.info_publisher.publish(camera_info)

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
