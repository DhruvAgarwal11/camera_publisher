Inside the outer camera_publisher folder, run:
1) colcon build
2) source install/setup.bash
3) ros2 run camera_publisher camera_publisher

To modify the camera number, modify the camera_publisher.py device number
Sometimes, the frames might be distorted - modify the amount that the image is wrapped in the camera_publisher.py script
