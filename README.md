# 🎹 Air-Piano: Play Chords with Hand Gestures

**Air-Piano** is a hands-free virtual MIDI instrument powered by your webcam and computer vision. By detecting finger gestures from both hands, it plays chords from the **D Major scale** in real-time — no physical keyboard required!

> A creative blend of music, machine vision, and MIDI technology — all in Python.

---

## ✨ In a Nutshell

This project uses **OpenCV**, **cvzone (MediaPipe)**, and **pygame.midi** to:
- Detect hand gestures via webcam
- Map each raised finger to a chord
- Play the chord for 2 seconds before releasing it

---

## 📆 Project Structure

```plaintext
PianoProject_CV/
│
├── handgesturecvpiano.py        # Original basic version: finger-chord mapping and auto-stop
├── handgesture.py               # Enhanced version with instrument switching + chord display
├── chordmaping.txt              # Lists chord mappings for reference
├── requirements.txt             # All required dependencies
└── README.md                    # 📘 You’re reading it!
```

---

## 👍 Chord Mapping (D Major Scale)

Each hand controls different chords. Raising a finger = triggering a chord.

| Hand  | Finger   | Chord     | Notes Played     |
|-------|----------|-----------|------------------|
| Left  | Thumb    | D Major   | D, F#, A         |
| Left  | Index    | E Minor   | E, G, B          |
| Left  | Middle   | G Major   | G, B, D          |
| Right | Thumb    | G Major   | G, B, D          |
| Right | Index    | A Major   | A, C#, E         |
| Right | Middle   | B Minor   | B, D, F#         |
| Right | Pinky    | F# Minor  | F#, A, C#        |

> Check full mapping in: `chordmaping.txt`

---

## 🛠️ Setup Instructions

### Step 1️⃣ – Clone the Repository

```bash
git clone https://github.com/anjalirj27/PianoProject_CV.git
cd PianoProject_CV
```

---

### Step 2️⃣ – Install Dependencies

Ensure you are in a Python environment (e.g., `tensorflowenv`). Then install all required packages:

```bash
pip install -r requirements.txt
```

**Dependencies List (from `requirements.txt`):**
- `opencv-python`
- `cvzone`
- `pygame`
- `mediapipe`
- `numpy`

---

### Step 3️⃣ – Run the Program

#### Option 1: Basic Version
To run the original hand-to-chord logic:

```bash
python handgesturecvpiano.py
```

#### Option 2: Enhanced Version 🎮
To use advanced features like **instrument switching** and **chord visual feedback**:

```bash
python handgesture.py
```

---

## 🌟 Features

- 🎥 **Real-Time Hand Tracking** using OpenCV + cvzone
- 🎹 **MIDI Chord Output** using pygame.midi
- 🎶 **D Scale Chords** mapped to specific fingers (both hands)
- ⏱️ **Auto Sustain**: Chords sustain for 2 seconds and stop
- 🖐️ Control the piano just by lifting fingers in front of a webcam!

---



