# Morse Code Computer Vision Interpreter

A modular, real-time Morse code communication system that translates visual gestures, light pulses, and facial movements into text using **Computer Vision** and **State-Machine Logic**.

## 1. Abstract
This project bridges the gap between physical movement and digital communication. By monitoring a live video feed, the system detects "Active" states through three distinct input modes: Light Intensity, Hand Gestures, and Eye Blinks. 

Unlike standard binary codes, Morse code is not a "prefix-free" code. To resolve this, the system implements a **Temporal Analysis Engine** that uses time-based "Gaps" (silence) to distinguish between individual symbols, letters, and words.



## 2. Pipeline Architecture
The software follows a strictly modular pipeline to ensure high performance and low latency:

1.  **Video Capture:** Real-time frames are captured and inverted (mirrored) for an intuitive user experience.
2.  **Pre-processing:** Frames are resized and normalized to maintain a consistent Frame Rate (FPS), which is critical for accurate timing.
3.  **Stage Selector:** The user can toggle between three specialized detection modules:
    * **Stage 1 (Light):** Detects high-intensity pixel clusters (Flashlights).
    * **Stage 2 (Hand):** Tracks skeletal landmarks to differentiate between an **Open Palm (Dot)** and a **Closed Fist (Dash)**.
    * **Stage 3 (Eye):** Uses the **Eye Aspect Ratio (EAR)** to translate intentional blinks into Morse signals.
4.  **Temporal Analysis:** Converts "Signal ON/OFF" states into Morse symbols (`.` and `-`) and handles "Latch" logic to prevent duplicate entries.
5.  **Decoder:** A dictionary-based lookup that translates buffered symbols into alphanumeric characters.



## 3. Operational Logic

The system employs two distinct logic engines depending on the selected input stage. While Stage 2 is **Instantaneous (Shape-based)**, Stages 1 and 3 are **Temporal (Duration-based)**.

### Stage 1: Light Intensity (Flashlight)
* **Logic Type:** Duration-based.
* **Trigger:** Detects the brightest pixel cluster in the frame using `cv2.minMaxLoc`.
* **Dot (.):** Light is ON for less than 0.4 seconds.
* **Dash (-):** Light is ON for more than 0.4 seconds.

### Stage 2: Hand Gesture (Fist/Palm)
* **Logic Type:** Shape-based (Instantaneous).
* **Trigger:** Analyzes skeletal landmarks via MediaPipe.
* **Dot (.):** Detection of an **Open Palm** (at least 3 fingers extended).
* **Dash (-):** Detection of a **Closed Fist** (fingers curled into the palm).
* **Latch Mechanism:** To prevent repeated symbols from a single gesture, the system only registers a signal when the state changes from "None" to a gesture.



### Stage 3: Eye Tracking (Blink)
* **Logic Type:** Duration-based.
* **Trigger:** Calculates the **Eye Aspect Ratio (EAR)**.
* **Dot (.):** Eyes remain closed for a short duration (< 0.4s).
* **Dash (-):** Eyes remain closed for a long duration (> 0.4s).



### Global Spacing Logic
Regardless of the input stage, the engine uses "Gaps" (silence) to organize symbols:
* **Letter Gap (1.5s - 2.0s):** No signal detected; the current buffer is decoded into a character.
* **Word Gap (> 3.0s):** No signal detected; a space is added to the final text.

## 4. Technologies Used
* **Python:** Core logic and orchestration.
* **OpenCV:** Video acquisition, image mirroring, and intensity-based thresholding.
* **MediaPipe (v0.10.21):** Hand skeletal tracking and Face Mesh landmarking.
* **NumPy:** Euclidean distance and vector mathematics for EAR and gesture analysis.

## 5. Installation & Usage
1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install opencv-python mediapipe==0.10.21 numpy
