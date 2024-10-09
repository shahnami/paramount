from api.main import TuyaDeviceController
import cv2
import mediapipe as mp
import time
from dotenv import load_dotenv
import os

load_dotenv()

# MediaPipe hands initialization
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize device controller
device_controller = TuyaDeviceController(os.getenv("CLIENT_ID"), os.getenv("SECRET_KEY"))

# Webcam capture setup
cap = cv2.VideoCapture(0)

confirmation_needed = False
pending_action = None
confirmation_start_time = None
confirmation_cooldown = 0

# Function to count extended fingers
def count_extended_fingers(landmarks):
    fingers = []

    # Thumb
    if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers (Index, Middle, Ring, Pinky)
    for i in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
              mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
              mp_hands.HandLandmark.RING_FINGER_TIP,
              mp_hands.HandLandmark.PINKY_TIP]:
        if landmarks[i].y < landmarks[i - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image for easier control
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        current_time = time.time()

        if results.multi_hand_landmarks and not confirmation_needed and (current_time - confirmation_cooldown > 2):
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmarks for finger detection
                landmarks = hand_landmarks.landmark

                # Count fingers
                fingers = count_extended_fingers(landmarks)
                total_fingers = fingers.count(1)

                # Device Control Logic
                if total_fingers == 0:
                    # Fist Gesture - Turn off all devices
                    print("Turning off all devices. Show thumbs up to confirm.")
                    pending_action = ('all', False)
                    confirmation_needed = True
                    confirmation_start_time = current_time
                elif total_fingers == 5:
                    # Full Hand Gesture - Turn on all devices
                    print("Turning on all devices. Show thumbs up to confirm.")
                    pending_action = ('all', True)
                    confirmation_needed = True
                    confirmation_start_time = current_time
                elif 1 <= total_fingers <= len(device_controller.devices) and not (fingers[0] == 1 and total_fingers == 1):
                    # Finger Number Gesture - Control individual device (ignore thumbs up gesture)
                    print(f"Turning on Device {total_fingers}. Show thumbs up to confirm.")
                    pending_action = ('single', total_fingers - 1, True)
                    confirmation_needed = True
                    confirmation_start_time = current_time
        elif confirmation_needed:
            # Check if confirmation time has expired
            if current_time - confirmation_start_time > 2:
                print("Confirmation timeout. Action ignored.")
                confirmation_needed = False
                pending_action = None
            else:
                # Check for thumbs up confirmation
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        # Extract landmarks for finger detection
                        landmarks = hand_landmarks.landmark

                        # Count fingers
                        fingers = count_extended_fingers(landmarks)

                        # Check for thumbs up
                        thumb_up = (fingers[0] == 1 and all(f == 0 for f in fingers[1:]))
                        if thumb_up:
                            if pending_action:
                                if pending_action[0] == 'all':
                                    device_controller.control_all(pending_action[1])
                                elif pending_action[0] == 'single':
                                    device_controller.control_device(pending_action[1])
                            confirmation_needed = False
                            pending_action = None
                            confirmation_cooldown = current_time

        # Display the image
        cv2.imshow('Hand Gesture Control', frame)

        # Quit with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()