# Morse Code Computer Vision Interpreter

A modular, real-time Morse code communication system that translates visual gestures and light signals into text using **Computer Vision** and **Temporal Analysis**.

## 1. Abstract
This project bridges the gap between physical movement and digital communication. By monitoring a live video feed, the system detects "Active" states through three distinct input modes: Light Intensity, Hand Gestures, and Eye Blinks. 

Unlike standard binary codes, Morse code is not a "prefix-free" code. To resolve this, the system implements a **State Machine** that uses time-based "Gaps" (silence) to distinguish between individual symbols, letters, and words.



## 2. Pipeline Architecture
The software follows a strictly modular pipeline to ensure high performance and low latency:

1.  **Video Capture:** Real-time frames are captured and inverted (mirrored) for an intuitive user experience.
2.  **Pre-processing:** Frames are resized and normalized to maintain a consistent Frame Rate (FPS), which is critical for accurate timing.
3.  **Stage Selector:** The user can toggle between three specialized detection modules:
    * **Stage 1 (Light):** Detects high-intensity pixel clusters (Flashlights).
    * **Stage 2 (Hand):** Tracks skeletal landmarks to differentiate between an **Open Palm (Dot)** and a **Closed Fist (Dash)**.
    * **Stage 3 (Eye):** Uses the **Eye Aspect Ratio (EAR)** to translate intentional blinks into Morse signals.
4.  **Temporal Analysis:** Converts "Signal ON/OFF" states into Morse symbols (`.` and `-`) and handles "Latch" logic to prevent duplicate entries.
5.  **Decoder:** A dictionary-based lookup that translates buffered symbols into alphanumeric characters once a "Letter Gap" is detected.



## 3. Technologies Used
* **Python:** The core logic orchestrator.
* **OpenCV:** Handles video stream acquisition, image flipping, and intensity-based light thresholding.
* **MediaPipe:** * **Hand Landmarks:** Tracks 21 3D coordinates on the hand to detect finger extension/contraction.
    * **Face Mesh:** Tracks 468+ landmarks to measure the precise distance between eyelids for blink detection.
* **NumPy:** Performs the Euclidean distance calculations required for the EAR formula and gesture vector analysis.



## 4. Operational Logic (Hand Stage)
In the Hand Gesture mode, the system bypasses standard timing for symbols. Instead, it "samples" the hand shape the moment it appears in the frame:

| Hand Shape | Morse Symbol | Gesture Requirement |
| :--- | :--- | :--- |
| **Open Palm** | Dot (.) | At least 3 fingers extended |
| **Closed Fist** | Dash (-) | All fingers curled into palm |

The system then waits for a **Letter Gap** (default 1.5s - 2.0s) of "neutral" or "no hand" state before finalizing the character and looking it up in the Morse dictionary.

## 5. Directory Structure
```text
MorseInterpreter/
├── main.py              # Orchestrator & UI
├── morse/
│   ├── decoder.py       # Dictionary translation
│   └── timing.py        # Temporal analysis logic
├── stages/
│   ├── stage1_light.py  # Intensity detection
│   ├── stage2_hand.py   # Landmark gesture detection
│   └── stage3_eye.py    # EAR blink detection
└── utils/
    ├── config.py        # Constants and Dict
    └── preprocessing.py # Frame optimization
