 Real-Time Hand Position Detection (MediaPipe + OpenCV)

A small computer-vision app that tracks your hand through the webcam and shows the **live X, Y and Z coordinates of your index fingertip**. It uses **MediaPipe Hands** for 21-point landmark detection and **OpenCV** for video capture and display.

## Features

- Real-time detection of one hand (confidence thresholds of 0.7)
- Highlights the **index fingertip** (landmark 8) with a green marker
- On-screen overlay of **X and Y in pixels** and **Z as relative depth**
- Draws the full hand skeleton (21 landmarks and connections)
- Prints the Z value to the console once per second
- Press **`q`** to quit

## How it works

1. Capture a frame from the webcam with OpenCV
2. Convert BGR to RGB and run `mp.solutions.hands`
3. Read landmark 8 (index fingertip), which MediaPipe gives as normalised coordinates
4. Convert X and Y to pixels with `x * width` and `y * height`
5. Draw the overlay and skeleton, then display the frame

> **About Z:** MediaPipe's `z` is a relative depth measured from the wrist, where smaller (more negative) values mean the point is closer to the camera. It is not a distance in centimetres.

## Tech stack

Python · OpenCV · MediaPipe

## Getting started

```bash
git clone https://github.com/<your-username>/MediaPipe_HandDetection.git
cd MediaPipe_HandDetection
pip install opencv-python mediapipe
python posDetection.py
```

A webcam is required. Show one hand to the camera and move it to see the values change.

## Project structure

```
MediaPipe_HandDetection/
└── posDetection.py
```

## Ideas for extension

- Track both hands (`max_num_hands=2`) and all fingertips
- Count raised fingers or recognise gestures
- Control the mouse cursor or a robot arm with the fingertip position
- Estimate approximate distance using the hand's pixel size

## License

Released under the MIT License. Add a `LICENSE` file to your repository to match.
