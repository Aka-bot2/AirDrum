
import time

previous_positions = {}
last_hit_times = {}

HIT_THRESHOLD = 900
HIT_COOLDOWN = 0.35


def detect_hit(hand_label, x, y, zone):
    current_time = time.perf_counter()

    if hand_label not in previous_positions:
        previous_positions[hand_label] = (y, current_time)
        return None

    previous_y, previous_time = previous_positions[hand_label]

    dt = current_time - previous_time

    hit = None

    if dt > 0:
        velocity = (y - previous_y) / dt

        last_hit = last_hit_times.get(hand_label, 0)

        if (
            velocity > HIT_THRESHOLD
            and zone is not None
            and current_time - last_hit > HIT_COOLDOWN
        ):
            last_hit_times[hand_label] = current_time
            hit = zone

    previous_positions[hand_label] = (y, current_time)

    return hit
