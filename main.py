import cv2
from stages.stage1_light import LightStage
from stages.stage2_hand import HandStage
from stages.stage3_eye import EyeStage
from morse.timing import TemporalAnalyzer
from morse.decoder import decode_sequence
from utils.preprocessing import prepare_frame

def main():
    cap = cv2.VideoCapture(0)
    
    # Initialize all modules
    stages = {
        1: LightStage(),
        2: HandStage(),
        3: EyeStage()
    }
    
    timer = TemporalAnalyzer()
    current_mode = 2  # Default to Hand Stage
    full_message = ""
    
    print("Controls: '1' for Light, '2' for Hand, '3' for Eye, 'c' to Clear, 'q' to Quit")

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1) # 1 flips horizontally, 0 would flip vertically
        
        # Step 1: Pre-processing
        frame = prepare_frame(frame)
        
        # Step 2: Stage Specific Detection
        detector = stages[current_mode]
        signal = detector.detect(frame)
        
        # Step 3: Timing and Decoding
        event = timer.process(signal, current_mode)
        
        if event == "DECODE_LETTER":
            code = timer.get_buffer()
            letter = decode_sequence(code)
            full_message += letter
            timer.clear_buffer()

        # UI Visuals
        mode_names = {1: "LIGHT", 2: "HAND (Fist/Palm)", 3: "EYE (Blink)"}
        cv2.putText(frame, f"MODE: {mode_names[current_mode]}", (10, 30), 1, 1.5, (255, 100, 0), 2)
        cv2.putText(frame, f"Symbols: {timer.get_buffer()}", (10, 70), 1, 1.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Text: {full_message}", (10, 110), 1, 1.5, (255, 255, 255), 2)
        
        cv2.imshow("Morse CV Interpreter", frame)
        
        # Handle Input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key in [ord('1'), ord('2'), ord('3')]:
            current_mode = int(chr(key))
            timer.clear_buffer() # Reset when switching modes
        elif key == ord('c'):
            full_message = ""

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()