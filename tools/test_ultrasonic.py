"""
tools/test_ultrasonic.py

Standalone diagnostic utility for ultrasonic sensor.

Used to validate distance measurements independently
from the main application logic.
"""

import time
import RPi.GPIO as GPIO


TRIG = 17
ECHO = 13


def setup() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.1)


def distance_cm() -> float:

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        end = time.time()

    return (end - start) * 17150.0


def main() -> None:

    setup()

    print("Ultrasonic diagnostic running...")

    try:
        while True:

            d = distance_cm()
            print(f"Distance: {d:.1f} cm")

            time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()