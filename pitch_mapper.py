# pitch_mapper.py
import numpy as np
import cv2

class PitchMapper:
    """Handles the homography transformation from pixel to real-world coordinates."""
    def __init__(self, src_points, dst_points_m):
        if len(src_points) != 4 or len(dst_points_m) != 4:
            raise ValueError("Exactly 4 source and destination points are required for homography.")

        src_pts = np.float32(src_points).reshape(-1, 1, 2)
        dst_pts = np.float32(dst_points_m).reshape(-1, 1, 2)
        
        self.homography_matrix, _ = cv2.findHomography(src_pts, dst_pts)

    def map_to_pitch(self, pixel_coords):
        """Converts a single (x, y) pixel coordinate to (X, Y) real-world meters."""
        pixel_pt = np.float32([pixel_coords]).reshape(-1, 1, 2)
        transformed_pt = cv2.perspectiveTransform(pixel_pt, self.homography_matrix)
        
        if transformed_pt is not None:
            return transformed_pt[0][0]
        return None