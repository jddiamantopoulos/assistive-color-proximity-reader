# Assistive Smart Glasses – Color & Proximity Feedback System

A Raspberry Pi–based wearable prototype that helps visually impaired users perceive their surroundings through real-time audio and proximity feedback.

The system detects dominant colors, converts them to speech, and provides obstacle alerts using ultrasonic sensing and audible cues.

---

## Features

- Real-time color detection using TCS34725 sensor  
- Weighted RGB classification for improved accuracy  
- Text-to-speech feedback via eSpeak  
- Ultrasonic distance sensing for obstacle detection  
- PWM buzzer for proximity alerts  
- Hardware button to toggle system on/off  
- Diagnostic tools for sensor testing  

---

## Technologies & Hardware

### Software
- Python 3  
- Raspberry Pi GPIO  
- Adafruit CircuitPython  
- eSpeak  

### Hardware
- Raspberry Pi  
- TCS34725 Color Sensor  
- Ultrasonic Sensor (HC-SR04 or similar)  
- Buzzer  
- Push Button  

---

## Project Structure

```
.
├── main.py
├── tools/
│   ├── test_color.py
│   └── test_ultrasonic.py
├── .gitignore
└── README.md
```

---

## Usage

Install dependencies:

```bash
pip install adafruit-circuitpython-tcs34725
sudo apt install espeak
```

Run the main application:

```bash
python main.py
```

Run diagnostic tools:

```bash
python tools/test_color.py
python tools/test_ultrasonic.py
```

---

## Project History

Originally developed in 2023 as an engineering prototype.  
Refactored and documented in 2026 to improve maintainability and system integration.

---

## Contributors

- **Jonathan Diamantopoulos (Primary Author & Maintainer)**  
  - Designed and implemented color detection and text-to-speech system  
  - Developed weighted RGB classification algorithm  
  - Finalized ultrasonic sensing and proximity feedback  
  - Led system integration, refactoring, and documentation  

- **Hai Tang**  
  - Initial GitHub setup and early commits  
  - Hardware wiring and configuration  

- **Matthew Binion**  
  - Hardware configuration  
  - Ultrasonic sensor prototyping  

---

## License

Provided for educational and portfolio purposes.
