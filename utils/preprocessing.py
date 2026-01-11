import cv2

def prepare_frame(frame, target_width=1280):
    # 1. Get the actual dimensions of your camera's raw feed
    h, w = frame.shape[:2]
    
    # 2. Calculate the aspect ratio (Width / Height)
    aspect_ratio = w / h
    
    # 3. Determine the new height based on the ratio to prevent stretching
    target_height = int(target_width / aspect_ratio)
    
    # 4. Resize using INTER_AREA (best for downscaling/maintaining quality)
    resized_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
    
    return resized_frame