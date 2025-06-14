# ball_detector.py
import torch
import config

class BallDetector:
    """Encapsulates the YOLOv5 model for ball detection."""
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=config.YOLO_MODEL_PATH)
        self.model.conf = config.CONFIDENCE_THRESHOLD
        self.model.classes = config.YOLO_CLASSES_TO_DETECT

    def detect_ball(self, frame):
        """
        Takes a single frame and returns the bounding box of the detected ball.
        Returns: [xmin, ymin, xmax, ymax] or None if no ball is detected.
        """
        results = self.model(frame, size=640)
        detections = results.xyxy[0]

        if len(detections) > 0:
            # Assume the most confident detection is the ball
            best_detection = detections[0].cpu().numpy()
            return best_detection[:4]
        return None