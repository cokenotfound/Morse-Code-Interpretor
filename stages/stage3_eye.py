import cv2
import mediapipe as mp
import numpy as np
from utils.config import EAR_THRESHOLD

class EyeStage:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)

    def calculate_ear(self, landmarks, eye_indices):
        # Vertical distances
        p2_p6 = np.linalg.norm(np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y]) - 
                               np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y]))
        p3_p5 = np.linalg.norm(np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y]) - 
                               np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y]))
        # Horizontal distance
        p1_p4 = np.linalg.norm(np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y]) - 
                               np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y]))
        
        return (p2_p6 + p3_p5) / (2.0 * p1_p4)

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return None

        # Standard MediaPipe indices for left eye
        LEFT_EYE = [33, 160, 158, 133, 153, 144]
        landmarks = results.multi_face_landmarks[0].landmark
        ear = self.calculate_ear(landmarks, LEFT_EYE)

        # If EAR is low, eyes are closed (Active Signal)
        if ear < EAR_THRESHOLD:
            return "ACTIVE"
        return None