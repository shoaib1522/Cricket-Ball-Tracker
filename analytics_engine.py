# analytics_engine.py
import numpy as np
import pandas as pd
import config
import os

class AnalyticsEngine:
    """Analyzes trajectory data to classify delivery type and logs results."""
    def __init__(self):
        self.delivery_type = "Undetermined"
        self.bounce_point_m = None

    def analyze_trajectory(self, trajectory_m):
        """Analyzes the full trajectory to find the bounce point and classify the delivery."""
        if len(trajectory_m) < 5:  # Need sufficient points to determine a bounce
            return

        # Simple bounce detection: Find the point with the maximum Y-coordinate (farthest down the pitch)
        # A more robust method would find where vertical velocity changes sign.
        world_coords_np = np.array(trajectory_m)
        bounce_index = np.argmax(world_coords_np[:, 1])
        
        # Ensure the bounce point is not the first or last point
        if 0 < bounce_index < len(world_coords_np) - 1:
            self.bounce_point_m = world_coords_np[bounce_index]
            bounce_y_m = self.bounce_point_m[1]

            if bounce_y_m <= config.FULL_LENGTH_THRESHOLD_M:
                self.delivery_type = "Full"
            elif config.FULL_LENGTH_THRESHOLD_M < bounce_y_m <= config.GOOD_LENGTH_THRESHOLD_M:
                self.delivery_type = "Good Length"
            else:
                self.delivery_type = "Short"

    def get_analytics_text(self):
        if self.bounce_point_m is not None:
            return f"{self.delivery_type} | Bounce Y: {self.bounce_point_m[1]:.2f}m"
        return "Analyzing..."

    def log_results(self):
        """Saves the final analytics to a CSV file."""
        if self.bounce_point_m is None:
            return
            
        data = {
            'video_file': [os.path.basename(config.INPUT_VIDEO_PATH)],
            'delivery_type': [self.delivery_type],
            'bounce_point_x_m': [round(self.bounce_point_m[0], 2)],
            'bounce_point_y_m': [round(self.bounce_point_m[1], 2)]
        }
        df = pd.DataFrame(data)

        # Append to CSV file, creating it if it doesn't exist
        if not os.path.isfile(config.ANALYTICS_CSV_PATH):
            df.to_csv(config.ANALYTICS_CSV_PATH, index=False)
        else:
            df.to_csv(config.ANALYTICS_CSV_PATH, mode='a', header=False, index=False)