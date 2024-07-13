import cv2
import numpy as np
import glob
import yaml

# Define the chessboard size (number of inner corners per a chessboard row and column)
chessboard_size = (3, 3)  # Modify this to match your checkerboard pattern

# Define the size of the squares in your checkerboard (31.25 mm)
square_size = 31.25  # Replace with the actual size of squares in your checkerboard

# Termination criteria for corner subpixel accuracy
criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

# Prepare object points based on the actual size of squares
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all the images
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane

# Load all images
images = glob.glob('/home/dhruvagarwal/Desktop/ros2_ws/src/lidar_camera_calibration/calibration_data/camera_calibration/*.png')
# images = glob.glob('/home/dhruvagarwal/imgs/*.png')  # Adjust the path to your images
# print(images)
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Try to find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the camera calibration result
calibration_data = {
    "camera_matrix": mtx.tolist(),
    "dist_coeff": dist.tolist(),
    "rotation_vectors": [rvec.tolist() for rvec in rvecs],
    "translation_vectors": [tvec.tolist() for tvec in tvecs]
}

with open("calibration.yaml", "w") as f:
    yaml.dump(calibration_data, f)

print("Calibration completed successfully.")
