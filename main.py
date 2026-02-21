#!/usr/bin/env python3
"""
main.py

Assistive Glasses Prototype for Visually Impaired Users
-------------------------------------------------------

This program runs on a Raspberry Pi and provides real-time
environmental feedback by:

1. Detecting dominant colors using a TCS34725 color sensor
2. Converting detected colors to speech using eSpeak
3. Measuring distance using an ultrasonic sensor
4. Providing proximity alerts via a PWM buzzer
5. Allowing the user to toggle the system on/off with a button

This file serves as the main entry point for the device.

Primary Author: Jonathan Diamantopoulos
"""

import time
import math
import subprocess

import RPi.GPIO as GPIO
import board
import adafruit_tcs34725


# =========================================================
# GPIO Pin Configuration (BCM Numbering)
# =========================================================

TRIG = 17          # Ultrasonic trigger
ECHO = 13          # Ultrasonic echo
BUZZER_PIN = 27    # PWM buzzer output
BUTTON_PIN = 18    # Toggle button input


# =========================================================
# Color Classification Parameters
# =========================================================
# Weights were empirically tuned to improve classification
# accuracy under indoor lighting conditions.

RED_W = 1.20
GREEN_W = 0.35
BLUE_W = 0.05


# Reference colors for nearest-neighbor classification
COLOR_MAP = [
    ("red",     (255, 0, 0)),
    ("orange",  (255, 128, 0)),
    ("yellow",  (255, 255, 0)),
    ("green",   (0, 255, 0)),
    ("blue",    (0, 0, 255)),
    ("indigo",  (127, 0, 255)),
    ("violet",  (255, 0, 255)),
    ("white",   (255, 255, 255)),
]


# =========================================================
# Distance → Beep Timing Table
# =========================================================
# Closer objects produce more frequent feedback.

BEEP_TABLE = [
    (150, 1.25),
    (120, 1.00),
    (90,  0.75),
    (60,  0.50),
    (30,  0.25),
    (0,   0.07),
]


# =========================================================
# Global State
# =========================================================

active = True      # Toggled via hardware button
buzzer = None      # PWM object

# Initialize I2C color sensor
i2c = board.I2C()
color_sensor = adafruit_tcs34725.TCS34725(i2c)


# =========================================================
# Utility Functions
# =========================================================

def speak(text: str) -> None:
    """
    Converts text to speech using eSpeak.
    Output is suppressed to avoid terminal clutter.
    """
    subprocess.run(
        ["espeak", text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def closest_color(rgb: tuple[int, int, int]) -> str:
    """
    Classifies an RGB value using weighted Euclidean distance.

    Returns:
        Name of closest reference color
    """
    r, g, b = rgb

    best_name = "unknown"
    best_dist = float("inf")

    for name, (rr, gg, bb) in COLOR_MAP:

        dr = (rr - r) * RED_W
        dg = (gg - g) * GREEN_W
        db = (bb - b) * BLUE_W

        dist = math.sqrt(dr**2 + dg**2 + db**2)

        if dist < best_dist:
            best_dist = dist
            best_name = name

    return best_name


# =========================================================
# Hardware Setup
# =========================================================

def setup_gpio() -> None:
    """
    Configures GPIO pins and initializes PWM.
    """
    global buzzer

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    buzzer = GPIO.PWM(BUZZER_PIN, 440)

    GPIO.setup(
        BUTTON_PIN,
        GPIO.IN,
        pull_up_down=GPIO.PUD_UP
    )

    # Interrupt-based button handling
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=on_button,
        bouncetime=200
    )

    GPIO.output(TRIG, False)
    time.sleep(0.1)


def on_button(channel: int) -> None:
    """
    Interrupt callback for toggle button.
    """
    global active
    active = not active


# =========================================================
# Sensor Interfaces
# =========================================================

def distance_cm() -> float:
    """
    Measures distance using ultrasonic sensor.

    Returns:
        Distance in centimeters
    """
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start

    return duration * 17150.0


def beep_for_distance(dist: float) -> None:
    """
    Generates audible feedback based on distance.
    """
    wait_time = None

    for threshold, t in BEEP_TABLE:
        if dist >= threshold:
            wait_time = t
            break

    if wait_time is None:
        return

    time.sleep(wait_time)

    buzzer.start(10)
    time.sleep(0.1)
    buzzer.stop()


# =========================================================
# Main Control Loop
# =========================================================

def main() -> None:
    """
    Primary runtime loop.
    """
    setup_gpio()

    print("Assistive glasses system running...")

    try:
        while True:

            if not active:
                time.sleep(0.1)
                continue

            # --- Color Detection ---
            rgb = color_sensor.color_rgb_bytes
            color_name = closest_color(rgb)

            speak(color_name)

            # --- Proximity Feedback ---
            dist = distance_cm()
            beep_for_distance(dist)

    except KeyboardInterrupt:
        print("\nShutting down...")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()