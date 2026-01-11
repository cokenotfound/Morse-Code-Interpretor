# Morse Code CV Interpreter

### A Minimalist, Multi-Modal Computer Vision Morse Decoder

A professional-grade real-time assistive tool that translates physical actions into digital communication using MediaPipe and OpenCV.

---

## Abstract
The **Morse Code CV Interpreter** is a computer vision application designed to bridge the gap between physical motion and digital text. By monitoring environmental inputs, the system translates light intensity, hand gestures, or eye blinks into Morse code, which is then decoded into text in real-time. Featuring a professional **Black Theme HUD** and high-contrast monochrome icons, the interface is built for maximum legibility in high-glare environments (such as when using the Flashlight mode).

---

## Key Features
* **Tri-Modal Input Switching:** * **Light Mode:** Detects high-intensity light (flashlights/phones).
    * **Hand Mode:** Detects palm states (Open Palm = Dot, Closed Fist = Dash).
    * **Eye Mode:** Tracks intentional blinks via Face Mesh landmarks.
* **Minimalist Black HUD:** A translucent, dark interface that prevents UI "washout" during light-based signaling.
* **High-Fidelity Typography:** Uses **Times New Roman** rendering via PIL for a clean, authoritative decoded output.
* **Session Management:** Dedicated controls for newlines, text clearing, and full system resets.
* **One-Key Export:** Instantly saves the current session to a timestamped `.txt` file in the `/exports` directory.

---

## Technologies Used
* **Python 3.x**
* **OpenCV:** Video stream handling and geometric UI drawing.
* **MediaPipe:** Hand landmark and Face Mesh tracking.
* **Pillow (PIL):** TrueType font rendering for HUD text.
* **NumPy:** Efficient frame manipulation.

---

## Controls & Instructions

### General Navigation
| Key | Action |
| :--- | :--- |
| **H** | **Toggle Help Menu** (Stencil-style icon in top-left) |
| **1** | Switch to **Light Mode** (Torch Icon) |
| **2** | Switch to **Hand Mode** (Palm Icon) |
| **3** | Switch to **Eye Mode** (Eye Icon) |
| **N** | **New Line**: Manually insert a line break in the translation |
| **E** | **Export**: Saves current text to `/exports/` folder |
| **C** | **Clear**: Wipes the current translated text box |
| **R** | **Reset**: Wipes translation and clears the Morse buffer |
| **Q** | **Quit**: Safely closes the application |

### Signaling Logic
1.  **Dot (`.`):** Short signal duration ( < 0.4s ).
2.  **Dash (`-`):** Long signal duration ( > 0.4s ).
3.  **Letter Gap:** Stop signaling for **2 seconds** to decode the current sequence.
4.  **Word Gap:** Stop signaling for **4 seconds** to insert a space.

---

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/cokenotfound/Morse-Code-Interpretor.git](https://github.com/cokenotfound/Morse-Code-Interpretor.git)
    cd Morse-Code-Interpretor
    ```

2.  **Install Dependencies:**
    ```bash
    pip install opencv-python mediapipe pillow numpy
    ```

3.  **Run the Application:**
    ```bash
    python main.py
    ```

---

## Project Structure
```text
├── main.py              # Application entry point & control loop
├── morse/               
│   ├── decoder.py       # Morse-to-Alpha dictionary
│   └── timing.py        # Temporal analysis for dots/dashes
├── stages/              
│   ├── stage1_light.py  # Light intensity detection
│   ├── stage2_hand.py   # MediaPipe Hand tracking
│   └── stage3_eye.py    # MediaPipe Face Mesh / EAR tracking
├── utils/               
│   ├── ui.py            # HUD and Stencil Icon rendering
│   ├── preprocessing.py # Proportional aspect ratio scaling
│   └── file_manager.py  # TXT export logic
└── exports/             # Directory for saved sessions
