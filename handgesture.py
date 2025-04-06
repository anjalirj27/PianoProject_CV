import cv2 
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

# Initialize the Pygame MIDI module
pygame.midi.init()
player = pygame.midi.Output(0)
instruments = {
    0: "Acoustic Grand Piano",
    24: "Nylon Guitar",
    40: "Violin",
    81: "Lead 1 (Square)"
}
current_instrument = 0
player.set_instrument(current_instrument)

# Initialize camera and hand detector
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = HandDetector(detectionCon=0.8)  

# Chord mapping for fingers on each hand
chords = {
    "left": {
        "thumb": [62, 66, 69],
        "index": [64, 67, 71],
        "middle": [66, 69, 73],
        "ring": [67, 71, 74],
        "pinky": [69, 73, 76]
    },
    "right": {
        "thumb": [62, 66, 69],
        "index": [64, 67, 71],
        "middle": [67, 71, 74],
        "ring": [67, 71, 74],
        "pinky": [69, 73, 76]
    }
}

chord_names = {
    (62, 66, 69): "Dmin",
    (64, 67, 71): "Emin",
    (66, 69, 73): "F#min",
    (67, 71, 74): "Gmaj",
    (69, 73, 76): "Amaj"
}

# Sustain time (how long the note stays after finger goes down)
SUSTAIN_TIME = 2.0

# Track previous states of each finger (0 = down, 1 = up)
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}
active_chords = []

# Function to play a chord (MIDI notes)
def play_chord(chord_notes):
    for note in chord_notes:
        player.note_on(note, 127)
    active_chords.append(chord_notes)

# Function to stop a chord after a delay
def stop_chord_after_delay(chord_notes):
    time.sleep(SUSTAIN_TIME)
    for note in chord_notes:
        player.note_off(note, 127)
    if chord_notes in active_chords:
        active_chords.remove(chord_notes)

# Real-time loop
while True:
    success, img = cap.read()
    if not success:
        print("Camera not capturing frame.")
        continue

    hands, img = detector.findHands(img, draw=True)

    display_texts = []

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):  
                if finger in chords[hand_type]:
                    chord_notes = chords[hand_type][finger]
                    chord_tuple = tuple(chord_notes)
                    chord_name = chord_names.get(chord_tuple, "Chord")

                    # Finger is up now, but was previously down
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        play_chord(chord_notes)
                        display_texts.append(f"{hand_type.capitalize()} {finger}: {chord_name}")
                    # Finger is down now, but was previously up
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        threading.Thread(
                            target=stop_chord_after_delay,
                            args=(chord_notes,),
                            daemon=True  
                        ).start()
                    # Update the previous state
                    prev_states[hand_type][finger] = fingers[i]
    else:
        # If no hand is detected, stop all chords gracefully
        for hand in chords:
            for finger in chords[hand]:
                threading.Thread(
                    target=stop_chord_after_delay,
                    args=(chords[hand][finger],),
                    daemon=True
                ).start()
                prev_states[hand][finger] = 0  # Reset states properly

    # Show visual feedback: Chord names being played
    y_offset = 40
    for text in display_texts:
        cv2.putText(img, text, (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        y_offset += 40

    # Show current instrument
    cv2.putText(img, f"Instrument: {instruments[current_instrument]}", (800, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show the webcam feed
    cv2.imshow("Hand Tracking MIDI Chords", img)

    key = cv2.waitKey(1) & 0xFF
    # Exit if 'q' is pressed
    if key == ord('q'):
        break
    # Instrument switching
    elif key == ord('1'):
        current_instrument = 0
        player.set_instrument(current_instrument)
    elif key == ord('2'):
        current_instrument = 24
        player.set_instrument(current_instrument)
    elif key == ord('3'):
        current_instrument = 40
        player.set_instrument(current_instrument)
    elif key == ord('4'):
        current_instrument = 81
        player.set_instrument(current_instrument)

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.midi.quit()
