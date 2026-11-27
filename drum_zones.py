
import cv2

DRUM_ZONES = {
    "CRASH": (50, 50, 250, 180),
    "HI-HAT": (300, 50, 500, 180),
    "RIDE": (550, 50, 750, 180),
    "SNARE": (50, 250, 250, 400),
    "TOM": (550, 250, 750, 400),
    "KICK": (300, 450, 500, 600)
}

def draw_zones(frame, active_hits=None):
    if active_hits is None:
        active_hits = set()

    for name, (x1, y1, x2, y2) in DRUM_ZONES.items():

        if name in active_hits:
            color = (0, 255, 0)  # Green flash
            thickness = -1       # Filled rectangle
        else:
            color = (255, 100, 0)
            thickness = 2

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            thickness
        )

        text_color = (0, 0, 0) if name in active_hits else color

        cv2.putText(
            frame,
            name,
            (x1 + 10, y1 + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            text_color,
            2
        )


def get_drum_zone(x, y):
    for name, (x1, y1, x2, y2) in DRUM_ZONES.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return name

    return None
