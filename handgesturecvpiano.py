import cv2 
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

#Initialize the Pygame MIDI module
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # 0 = Acoustic Grand Piano

#Initialize camera and hand detector
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = HandDetector(detectionCon=0.8)  

#Chord mapping for fingers on each hand
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

#Sustain time (how long the note stays after finger goes down)
SUSTAIN_TIME = 2.0

#Track previous states of each finger (0 = down, 1 = up)
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

#Function to play a chord (MIDI notes)
def play_chord(chord_notes):
    for note in chord_notes:
        player.note_on(note, 127)

#Function to stop a chord after a delay
def stop_chord_after_delay(chord_notes):
    time.sleep(SUSTAIN_TIME)
    for note in chord_notes:
        player.note_off(note, 127)

#Real-time loop
while True:
    success, img = cap.read()
    if not success:
        print("Camera not capturing frame.")
        continue

    hands, img = detector.findHands(img, draw=True)

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):  
                if finger in chords[hand_type]:
                    #Finger is up now, but was previously down
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        play_chord(chords[hand_type][finger])  
                    #Finger is down now, but was previously up
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        threading.Thread(
                            target=stop_chord_after_delay,
                            args=(chords[hand_type][finger],),
                            daemon=True  
                        ).start()
                    #Update the previous state
                    prev_states[hand_type][finger] = fingers[i]
    else:
        #If no hand is detected, stop all chords gracefully
        for hand in chords:
            for finger in chords[hand]:
                threading.Thread(
                    target=stop_chord_after_delay,
                    args=(chords[hand][finger],),  #Fixed: hand_type → hand
                    daemon=True
                ).start()
                prev_states[hand][finger] = 0  #Reset states properly

    #Show the webcam feed
    cv2.imshow("Hand Tracking MIDI Chords", img)

    #Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.midi.quit()
