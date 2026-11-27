
import pygame
from pathlib import Path

# Initialize audio
pygame.mixer.init()

SOUND_FOLDER = Path(__file__).parent / "sounds"

DRUM_SOUNDS = {
    "CRASH": "crash.mp3",
    "HI-HAT": "hihat.mp3",
    "RIDE": "ride.mp3",
    "SNARE": "snare.mp3",
    "TOM": "tom.mp3",
    "KICK": "kick.mp3"
}

# Load all sounds into memory
sounds = {}

for drum, filename in DRUM_SOUNDS.items():
    sounds[drum] = pygame.mixer.Sound(
        str(SOUND_FOLDER / filename)
    )


def play_sound(drum):
    if drum in sounds:
        sounds[drum].play()
