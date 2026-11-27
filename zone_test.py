
import cv2
import mediapipe as mp
from hit_detection import detect_hit
from sound_manager import play_sound
import time
from drum_zones import draw_zones, get_drum_zone

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
active_hits = {}
FLASH_DURATION = 0.15
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 600))

    h, w, _ = frame.shape

    # Draw all drum zones
    current_time = time.perf_counter()

    # Keep recently hit drums highlighted
    visible_hits = {
        drum for drum, hit_time in active_hits.items()
        if current_time - hit_time < FLASH_DURATION
    }

    draw_zones(frame, visible_hits)

    # Detect hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

            tip = hand_landmarks.landmark[8]

            x = int(tip.x * w)
            y = int(tip.y * h)

            zone = get_drum_zone(x, y)

            # Detect an actual downward strike
            hand_label = results.multi_handedness[i].classification[0].label

            hit = detect_hit(hand_label, x, y, zone)

            cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)

            if zone:
                cv2.putText(
                    frame, zone, (x + 15, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 255), 2
                )

            if hit:
                print("DRUM HIT:", hit)
                play_sound(hit)
                active_hits[hit] = time.perf_counter()
                cv2.putText(
                    frame, "HIT: " + hit,
                    (250, 300),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 0, 255), 3
                )


    cv2.imshow("Air Drum - Zone Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
