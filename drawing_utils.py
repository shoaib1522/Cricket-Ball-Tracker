# utils.py
"""Utility functions for the project."""
import cv2
import numpy as np
import config

def get_bbox_center(bbox):
    """Calculates the center point (x, y) of a bounding box [xmin, ymin, xmax, ymax]."""
    return np.array([(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2])

def draw_visuals(frame, bbox, trail, analytics_text):
    """Draws all tracking and analytics information onto the frame."""
    # Draw the trajectory trail
    if len(trail) > 1:
        for i in range(1, len(trail)):
            cv2.line(frame, tuple(trail[i-1]), tuple(trail[i]), config.TRAIL_COLOR, config.TRAIL_THICKNESS)

    # Draw the bounding box
    if bbox is not None:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[2]), int(bbox[3]))
        cv2.rectangle(frame, p1, p2, config.BBOX_COLOR, config.BBOX_THICKNESS, 1)

    # Draw the analytics text with a background
    if analytics_text:
        (text_width, text_height), baseline = cv2.getTextSize(analytics_text, config.FONT_FACE, config.FONT_SCALE, 2)
        text_bg_rect_p1 = (10, 10)
        text_bg_rect_p2 = (10 + text_width + 10, 10 + text_height + 10)
        cv2.rectangle(frame, text_bg_rect_p1, text_bg_rect_p2, config.TEXT_COLOR_BG, -1)
        cv2.putText(frame, analytics_text, (20, 15 + text_height), config.FONT_FACE, config.FONT_SCALE, config.TEXT_COLOR_FG, 2)

    return frame