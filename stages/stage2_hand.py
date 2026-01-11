import cv2
import mediapipe as mp

class HandStage:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if not results.multi_hand_landmarks:
            return None # No hand in frame
            
        landmarks = results.multi_hand_landmarks[0].landmark
        
        # Check if Index (8) and Middle (12) are above their bases (5 and 9)
        # Note: In MediaPipe Y-axis, smaller values are higher on screen.
        fingers_extended = landmarks[8].y < landmarks[5].y and landmarks[12].y < landmarks[9].y
        
        if fingers_extended:
            return "DOT"   # Open Palm
        else:
            return "DASH"  # Closed Fist