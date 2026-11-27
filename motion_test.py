
import cv2
import mediapipe as mp
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# Store previous fingertip positions
previous_positions = {}

# Store last strike times
last_strike_times = {}

# Strike detection threshold
STRIKE_THRESHOLD = 900  # pixels per second
COOLDOWN = 0.25         # seconds

while True:
    success, frame = cap.read()

    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    current_time = time.perf_counter()

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

            # Identify the hand
            hand_label = results.multi_handedness[i].classification[0].label

            # Draw hand skeleton
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get index fingertip
            h, w, _ = frame.shape
            tip = hand_landmarks.landmark[8]

            x = int(tip.x * w)
            y = int(tip.y * h)

            velocity_y = 0

            # Calculate velocity if previous position exists
            if hand_label in previous_positions:

                previous_y, previous_time = previous_positions[hand_label]

                delta_y = y - previous_y
                delta_time = current_time - previous_time

                if delta_time > 0:
                    velocity_y = delta_y / delta_time

            # Update previous position
            previous_positions[hand_label] = (y, current_time)

            # Check for a drum strike
            if (
                velocity_y > STRIKE_THRESHOLD
                and current_time - last_strike_times.get(hand_label, 0) > COOLDOWN
            ):
                print(f"{hand_label} HAND - STRIKE DETECTED!")
                last_strike_times[hand_label] = current_time

            # Choose marker colour
            if velocity_y > STRIKE_THRESHOLD:
                colour = (0, 0, 255)
            elif velocity_y < -200:
                colour = (255, 165, 0)
            else:
                colour = (0, 255, 0)

            cv2.circle(frame, (x, y), 12, colour, -1)

            # Display information
            cv2.putText(
                frame,
                f"{hand_label}: {velocity_y:.0f} px/s",
                (x + 15, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                colour,
                2
            )

    cv2.imshow("AirDrum - Motion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
