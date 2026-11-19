
import cv2
import mediapipe as mp
import time

# ==========================================
# GESTUREFLOW - HAND TRACKING SYSTEM
# ==========================================

# MediaPipe initialization
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# Camera initialization
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not access webcam. Check camera connection.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# FPS variables
previous_time = 0
fps = 0


# ==========================================
# FINGER COUNTING
# ==========================================

def count_fingers(hand, handedness):

    landmarks = hand.landmark
    fingers = []

    # Thumb detection
    # Assumes a mirrored selfie-view image
    if handedness == "Right":
        thumb = landmarks[4].x < landmarks[3].x
    else:
        thumb = landmarks[4].x > landmarks[3].x

    fingers.append(thumb)

    # Index, middle, ring and pinky
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        fingers.append(landmarks[tip].y < landmarks[pip].y)

    return fingers, sum(fingers)


# ==========================================
# GESTURE CLASSIFICATION
# ==========================================

def recognize_gesture(hand, handedness):

    fingers, count = count_fingers(hand, handedness)
    thumb, index, middle, ring, pinky = fingers

    if count == 5:
        gesture = "OPEN PALM"

    elif count == 0:
        gesture = "FIST"

    elif count == 2 and index and middle:
        gesture = "PEACE SIGN"

    elif count == 1 and index:
        gesture = "POINTING"

    elif count == 1 and thumb:
        if hand.landmark[4].y < hand.landmark[3].y:
            gesture = "THUMBS UP"
        else:
            gesture = "THUMB ONLY"

    else:
        gesture = f"{count} FINGERS"

    return gesture, count


# ==========================================
# MAIN APPLICATION
# ==========================================

try:

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                print("Unable to read webcam frame.")
                break

            # Mirror webcam for natural interaction
            frame = cv2.flip(frame, 1)

            height, width, _ = frame.shape

            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )

            # Process hand landmarks
            results = hands.process(rgb_frame)

            # ==================================
            # FPS CALCULATION
            # ==================================

            current_time = time.time()

            if previous_time != 0:
                current_fps = 1 / max(
                    current_time - previous_time, 1e-6
                )
                fps = 0.9 * fps + 0.1 * current_fps

            previous_time = current_time

            # ==================================
            # DISPLAY HEADER
            # ==================================

            cv2.rectangle(
                frame, (0, 0), (width, 55),
                (25, 25, 25), cv2.FILLED
            )

            cv2.putText(
                frame, "GESTUREFLOW",
                (20, 37),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0, 255, 180), 2
            )

            cv2.putText(
                frame, f"FPS: {fps:.1f}",
                (width - 170, 37),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )

            # ==================================
            # HAND DETECTION
            # ==================================

            if results.multi_hand_landmarks:

                for i, hand_landmarks in enumerate(
                    results.multi_hand_landmarks
                ):

                    # Identify handedness
                    handedness = (
                        results.multi_handedness[i]
                        .classification[0].label
                    )

                    # Classify gesture
                    gesture, finger_count = recognize_gesture(
                        hand_landmarks, handedness
                    )

                    # Index fingertip coordinates
                    index_tip = hand_landmarks.landmark[8]

                    cx = int(index_tip.x * width)
                    cy = int(index_tip.y * height)
                    z_value = index_tip.z

                    # Draw landmarks
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_styles.get_default_hand_landmarks_style(),
                        mp_styles.get_default_hand_connections_style()
                    )

                    # Highlight index fingertip
                    cv2.circle(
                        frame, (cx, cy),
                        12, (0, 255, 0), cv2.FILLED
                    )

                    cv2.circle(
                        frame, (cx, cy),
                        17, (255, 255, 255), 2
                    )

                    # Information panel position
                    panel_y = 85 + (i * 180)

                    cv2.rectangle(
                        frame,
                        (10, panel_y - 25),
                        (310, panel_y + 145),
                        (30, 30, 30),
                        cv2.FILLED
                    )

                    # Hand information
                    info = [
                        f"Hand: {handedness}",
                        f"Gesture: {gesture}",
                        f"Fingers: {finger_count}",
                        f"X: {cx} px",
                        f"Y: {cy} px",
                        f"Z: {z_value:.4f}"
                    ]

                    for j, text in enumerate(info):

                        cv2.putText(
                            frame,
                            text,
                            (25, panel_y + j * 27),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.58,
                            (0, 255, 180),
                            2
                        )

            else:

                cv2.putText(
                    frame,
                    "No hand detected",
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # Footer
            cv2.putText(
                frame,
                "Press Q to quit",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1
            )

            # Display application
            cv2.imshow("GestureFlow | Hand Intelligence", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("GestureFlow closed successfully.")
