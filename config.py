# config.py
"""
Centralized configuration file for the Cricket Ball Tracking System.
Modify these values to tune the system for your specific video and setup.
"""

# --- Model Configuration ---
# Path to the local YOLOv5 model file.
YOLO_MODEL_PATH = 'models/yolov5s.pt'
# Confidence threshold for object detection. Detections below this score will be ignored.
CONFIDENCE_THRESHOLD = 0.3
# Class index for 'sports ball' in the COCO dataset, which YOLOv5 is trained on.
YOLO_CLASSES_TO_DETECT = [32]

# --- Video Configuration ---
# Path to the input video file.
INPUT_VIDEO_PATH = 'data/videos/cricket.mp4'
# Path to save the annotated output video.
OUTPUT_VIDEO_PATH = 'output/tracked_delivery.mp4'
# Path to save the analytics data.
ANALYTICS_CSV_PATH = 'output/analytics.csv'

# --- Tracking & Analytics Configuration ---
# Define pitch zones based on the ball's bouncing point (Y-coordinate in meters).
# The origin (0,0) is assumed to be the center of the popping crease at the bowler's end.
# These values are examples and MUST be tuned for accuracy.
FULL_LENGTH_THRESHOLD_M = 2.5  # A ball bouncing within 2.5m of the batsman's crease.
GOOD_LENGTH_THRESHOLD_M = 6.0  # A ball bouncing between 2.5m and 6.0m.
# Anything bouncing further than GOOD_LENGTH_THRESHOLD_M is considered 'Short'.

# --- Visuals Configuration ---
BBOX_COLOR = (0, 255, 0)      # Green for the bounding box
TRAIL_COLOR = (255, 0, 0)     # Blue for the trajectory trail
TEXT_COLOR_BG = (0, 0, 0)     # Black background for text
TEXT_COLOR_FG = (255, 255, 255) # White text
BBOX_THICKNESS = 2
TRAIL_THICKNESS = 2
FONT_SCALE = 0.8
FONT_FACE = 1 # cv2.FONT_HERSHEY_SIMPLEX