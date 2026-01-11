import cv2
import numpy as np
from utils.config import LIGHT_THRESHOLD

class LightStage:
    def detect(self, frame):
        # Convert to grayscale to isolate intensity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Find the pixel with the maximum intensity
        _, max_val, _, _ = cv2.minMaxLoc(gray)
        
        # In this stage, duration determines Dot vs Dash
        # So we just return a Boolean 'Active' state
        if max_val >= LIGHT_THRESHOLD:
            return "ACTIVE" 
        return None