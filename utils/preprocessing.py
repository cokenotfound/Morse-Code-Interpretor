import cv2

def prepare_frame(frame, width=640):
    # Resize for performance stability
    aspect_ratio = frame.shape[1] / frame.shape[0]
    height = int(width / aspect_ratio)
    frame = cv2.resize(frame, (width, height))
    
    # Optional: Denoising to help Light Detection stage
    # frame = cv2.GaussianBlur(frame, (5, 5), 0)
    
    return frame