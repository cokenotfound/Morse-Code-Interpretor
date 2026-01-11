import cv2
import numpy as np
import time

# Import Custom Modules
from stages.stage1_light import LightStage
from stages.stage2_hand import HandStage
from stages.stage3_eye import EyeStage
from morse.timing import TemporalAnalyzer
from morse.decoder import decode_sequence
from utils.preprocessing import prepare_frame
from utils.export import export_to_txt
from utils.ui import draw_hud

def main():
    # 1. Setup Window Properties
    win_name = "Morse CV Interpreter"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    # We set a starting size, but the prepare_frame logic will maintain the ratio
    cv2.resizeWindow(win_name, 1280, 720) 

    # 2. Initialize Hardware and Modules
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    stages = {1: LightStage(), 2: HandStage(), 3: EyeStage()}
    timer = TemporalAnalyzer()
    
    # Session State
    current_mode = 2  # Default to Hand Mode
    full_message = ""
    show_help = False

    print("System Started. Press 'H' for help menu.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 3. Pre-processing
        # Mirror the frame for intuitive movement
        frame = cv2.flip(frame, 1)
        # Fix Aspect Ratio to prevent stretching
        frame = prepare_frame(frame, target_width=1280)
        
        # 4. Core Logic: Detection & Morse Processing
        signal = stages[current_mode].detect(frame)
        event = timer.process(signal, current_mode)
        
        # Check if a letter is ready to be decoded
        if event == "DECODE_LETTER":
            buffer_code = timer.get_buffer()
            letter = decode_sequence(buffer_code)
            full_message += letter
            timer.clear_buffer()

        # 5. UI Rendering
        # Passes state to ui.py to draw the Black Theme HUD and Icons
        frame = draw_hud(
            frame, 
            current_mode, 
            timer.get_buffer(), 
            full_message, 
            show_help
        )

        # 6. Display
        cv2.imshow(win_name, frame)
        
        # 7. Keyboard Controller
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'): # Quit
            break
        elif key == ord('h'): # Toggle Help
            show_help = not show_help
        elif key == ord('n'): # New Line
            full_message += "\n"
        elif key == ord('e'): # Export to TXT
            export_to_txt(full_message)
        elif key == ord('r'): # Full Reset
            full_message = ""
            timer.clear_buffer()
        elif key == ord('c'): # Clear Translation Only
            full_message = ""
        elif key in [ord('1'), ord('2'), ord('3')]: # Mode Switching
            current_mode = int(chr(key))
            timer.clear_buffer() # Clear buffer when switching modes to prevent carryover

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()