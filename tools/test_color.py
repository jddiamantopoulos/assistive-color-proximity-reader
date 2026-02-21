"""
tools/test_color.py

Standalone diagnostic tool for testing the
TCS34725 color sensor and speech output.

Used during development to verify sensor accuracy
before integrating into the main system.
"""

import time
import math
import subprocess

import board
import adafruit_tcs34725


RED_W = 1.20
GREEN_W = 0.35
BLUE_W = 0.05


COLOR_MAP = [
    ("red",     (255, 0, 0)),
    ("orange",  (255, 128, 0)),
    ("yellow",  (255, 255, 0)),
    ("green",   (0, 255, 0)),
    ("blue",    (0, 0, 255)),
    ("indigo",  (127, 0, 255)),
    ("violet",  (255, 0, 255)),
    ("white",   (255, 255, 255)),
    ("black",   (0, 0, 0)),
]


i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)


def speak(text: str) -> None:
    subprocess.run(["espeak", text])


def closest_color(rgb: tuple[int, int, int]) -> str:

    r, g, b = rgb

    best = "unknown"
    best_dist = float("inf")

    for name, (rr, gg, bb) in COLOR_MAP:

        dr = (rr - r) * RED_W
        dg = (gg - g) * GREEN_W
        db = (bb - b) * BLUE_W

        dist = math.sqrt(dr**2 + dg**2 + db**2)

        if dist < best_dist:
            best_dist = dist
            best = name

    return best


def main() -> None:

    print("Color sensor diagnostic running...")

    while True:

        rgb = sensor.color_rgb_bytes
        name = closest_color(rgb)

        print(f"RGB={rgb} -> {name}")

        speak(name)

        time.sleep(1.5)


if __name__ == "__main__":
    main()