import time
import os

def export_to_txt(text):
    # Create an 'exports' folder if it doesn't exist
    if not os.path.exists('exports'):
        os.makedirs('exports')
        
    # Generate a unique filename using a timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"exports/morse_session_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"--- Session Exported Successfully: {filename} ---")
        return True
    except Exception as e:
        print(f"--- Export Error: {e} ---")
        return False