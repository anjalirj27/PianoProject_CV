# 🎹 Air-Piano: Play Chords with Hand Gestures

**Air-Piano** is a virtual MIDI piano that you can play using just your hands and a webcam — no keyboard or mouse needed! It detects your hand gestures in real-time and plays chords from the D scale accordingly. It’s a cool fusion of computer vision and music technology using Python.
---

## ✨ TL;DR

This project uses **computer vision** and **MIDI synthesis** to play D-scale chords based on hand gestures.  
It leverages:
- `OpenCV` for video feed
- `cvzone` (built on `MediaPipe`) for hand tracking
- `pygame.midi` for MIDI chord output

When you raise specific fingers, the program plays the corresponding chord and **automatically stops it after 2 seconds** — like magic ✨

---
## 🎯 Features

- 🎥 **Real-Time Hand Tracking** using OpenCV + cvzone
- 🎹 **MIDI Chord Output** using pygame.midi
- 🎶 **D Scale Chords** mapped to specific fingers (both hands)
- ⏱️ **Auto Sustain**: Chords sustain for 2 seconds and stop
- 🖐️ Control the piano just by lifting fingers in front of a webcam!

---

## 🖐️ How Chord Mapping Works

Different fingers on each hand are mapped to different chords from the **D major scale**.

| Hand  | Finger | Chord        | Notes Played     |
|-------|--------|--------------|------------------|
| Left  | Thumb  | D Major      | D, F#, A          |
| Left  | Index  | E Minor      | E, G, B           |
| Left  | Middle | G Major      | G, B, D           |
| Right | Thumb  | G Major      | G, B, D           |
| Right | Index  | A Major      | A, C#, E          |
| Right | Middle | B Minor      | B, D, F#          |
| Right | Pinky  | F# Minor     | F#, A, C#         |

You can view these mappings in detail in the `chordmaping.txt` file.

---

## 🛠️ How to Set It Up

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/air-piano.git
cd air-piano
