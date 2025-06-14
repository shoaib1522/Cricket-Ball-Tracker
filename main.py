# main.py
import cv2
from collections import deque
import config
import drawing_utils
from ball_detector import BallDetector
from ball_tracker import KalmanFilterTracker
from pitch_mapper import PitchMapper
from analytics_engine import AnalyticsEngine

def main():
    # --- 1. INITIALIZATION ---
    print("Initializing system components...")
    detector = BallDetector()
    tracker = KalmanFilterTracker()
    analytics = AnalyticsEngine()
    
    # ========================== IMPORTANT CALIBRATION STEP ==========================
    # YOU MUST PROVIDE THESE POINTS FOR YOUR SPECIFIC CAMERA ANGLE.
    # To get these points, open your video, pause on a clear frame of the pitch,
    # and use a tool (like Paint or GIMP) to find the pixel coordinates (x, y)
    # of four corners of a known rectangle on the pitch (e.g., the batting crease).

    # Example pixel coordinates from the video frame (top-left, top-right, bottom-left, bottom-right of the crease)
    # UPDATE THESE VALUES
    src_points_px = [(667,547), (1310, 549), (664, 583), (1311, 586)]

    # Corresponding real-world coordinates in meters.
    # Assume (0,0) is the center of the bowling crease line.
    # The batting crease is 1.22m wide and its line is at Y=17.68m from the bowling crease.
    # We will define our origin (0,0) as the center of the *batting* crease for simplicity here.
    crease_width_m = 2.64 # Standard crease width
    dst_points_m = [
        (-crease_width_m / 2, 0),  # Top-left
        (crease_width_m / 2, 0),   # Top-right
        (-crease_width_m / 2, 1.22), # Bottom-left (1.22m is width of return crease)
        (crease_width_m / 2, 1.22)  # Bottom-right
    ]
    # =================================================================================
    
    mapper = PitchMapper(src_points_px, dst_points_m)
    
    # --- 2. VIDEO I/O SETUP ---
    cap = cv2.VideoCapture(config.INPUT_VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Could not open video file {config.INPUT_VIDEO_PATH}")
        return
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(config.OUTPUT_VIDEO_PATH, fourcc, fps, (width, height))
    
    # --- 3. DATA STORAGE & PROCESSING LOOP ---
    pixel_trail = deque(maxlen=30)
    world_trajectory = []

    print(f"Processing video: {config.INPUT_VIDEO_PATH}")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # a. Detect the ball
        bbox = detector.detect_ball(frame)
        
        # b. Track the ball using the Kalman Filter
        if bbox is not None:
            center_pixel = drawing_utils.get_bbox_center(bbox)
            tracked_pixel = tracker.update(center_pixel)
        else:
            if tracker.is_initialized:
                tracked_pixel = tracker.predict()
            else:
                tracked_pixel = None
        
        # c. Map, Analyze, and Visualize
        if tracked_pixel is not None:
            pixel_trail.append(tracked_pixel.astype(int))
            
            world_coords = mapper.map_to_pitch(tracked_pixel)
            if world_coords is not None:
                world_trajectory.append(world_coords)

        analytics.analyze_trajectory(world_trajectory)
        analytics_text = analytics.get_analytics_text()
        
        # d. Draw visuals on the frame
        output_frame = drawing_utils.draw_visuals(frame.copy(), bbox, list(pixel_trail), analytics_text)
        
        # e. Display and save the frame
        cv2.imshow('Cricket Ball Tracker', output_frame)
        out.write(output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- 4. CLEANUP & FINALIZATION ---
    print("Video processing finished.")
    analytics.log_results()
    print(f"Analytics saved to {config.ANALYTICS_CSV_PATH}")
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Annotated video saved to {config.OUTPUT_VIDEO_PATH}")

if __name__ == '__main__':
    main()