import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_mode_icons(frame, current_mode):
    h, w, _ = frame.shape
    padding, spacing = 60, 90
    active_col = (255, 255, 255)   # Pure White
    inactive_col = (60, 60, 60)    # Dim Gray

    # --- TORCH (Mode 1) ---
    is_active = (current_mode == 1)
    color = active_col if is_active else inactive_col
    x1 = w - (spacing * 3)
    # Stencil logic: Fill the box if active
    cv2.rectangle(frame, (x1, padding + 10), (x1 + 15, padding + 35), color, -1 if is_active else 2)
    cv2.rectangle(frame, (x1 - 5, padding), (x1 + 20, padding + 10), color, -1 if is_active else 2)

    # --- PALM (Mode 2) ---
    is_active = (current_mode == 2)
    color = active_col if is_active else inactive_col
    x2 = w - (spacing * 2)
    cv2.rectangle(frame, (x2, padding + 15), (x2 + 25, padding + 40), color, -1 if is_active else 2)
    for i in range(4):
        cv2.line(frame, (x2 + (i*7), padding + 15), (x2 + (i*7), padding - 5), color, 2)

    # --- EYE (Mode 3) ---
    is_active = (current_mode == 3)
    color = active_col if is_active else inactive_col
    x3 = w - spacing
    cv2.ellipse(frame, (x3, padding + 20), (25, 15), 0, 0, 360, color, -1 if is_active else 2)
    # Pupil: Black if icon is filled white, otherwise White
    pupil_color = (0, 0, 0) if is_active else (255, 255, 255)
    cv2.circle(frame, (x3, padding + 20), 5, pupil_color, -1)
    
    return frame

def draw_hud(frame, current_mode, morse_buffer, translated_text, show_help):
    h, w, _ = frame.shape
    hud_h = 140
    padding = 60
    
    # 1. Solid Black HUD Box (Bottom)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - hud_h), (w, h), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.9, frame, 0.1, 0)

    # 2. Vertical Divider
    divider_x = int(w * 0.45)
    cv2.line(frame, (divider_x, h - hud_h + 30), (divider_x, h - 30), (255, 255, 255), 1)

    # 3. Help Icon [H] (Top Left - Stencil Black/White Style)
    h_x, h_y = 40, padding
    # Solid White Background Box
    cv2.rectangle(frame, (h_x, h_y), (h_x + 35, h_y + 35), (255, 255, 255), -1)
    # Black "H" Text
    cv2.putText(frame, "H", (h_x + 6, h_y + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    if show_help:
        help_overlay = frame.copy()
        cv2.rectangle(help_overlay, (h_x, h_y + 45), (h_x + 300, h_y + 250), (0, 0, 0), -1)
        frame = cv2.addWeighted(help_overlay, 0.9, frame, 0.1, 0)
        
        cmds = [
            "Q: Quit Application", 
            "1-3: Switch Modes", 
            "C: Clear Screen", 
            "R: Reset System", 
            "N: New Line (Enter)", 
            "E: Export to TXT"
        ]
        for i, text in enumerate(cmds):
            cv2.putText(frame, text, (h_x + 15, h_y + 80 + (i * 25)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 4. Mode Icons (Top Right)
    frame = draw_mode_icons(frame, current_mode)

    # 5. Times New Roman Rendering via PIL (High Quality Typography)
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    try:
        # Standard Windows Path - Adjust if on Linux/Mac
        font_path = "C:/Windows/Fonts/times.ttf"
        font_large = ImageFont.truetype(font_path, 45)
        font_small = ImageFont.truetype(font_path, 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # White Labels
    draw.text((50, h - 125), "INPUT SEQUENCE", font=font_small, fill=(255, 255, 255))
    draw.text((divider_x + 50, h - 125), "TRANSLATION", font=font_small, fill=(255, 255, 255))
    
    # Morse Code Sequence
    draw.text((50, h - 90), morse_buffer, font=font_large, fill=(255, 255, 255))
    
    # Translated Text (Supports \n from 'N' key)
    # Dynamically adjust Y if text is multi-line to keep it inside the HUD
    text_y = h - 115 if "\n" in translated_text else h - 90
    draw.text((divider_x + 50, text_y), translated_text, font=font_large, fill=(255, 255, 255))

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)