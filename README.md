# OpenCV & Computer Vision Practice|Projects

A collection of Python scripts and mini-projects I built while learning **OpenCV** and computer vision: basic image operations, drawing, edge detection, face detection, hand tracking, object classification, and an AI virtual keyboard.

> **Note:** The full folder is too large to upload to GitHub, so this README lists the structure of the project and what each file/folder is for. The virtual environment (`.venv`) and editor settings (`.vscode`) are not included.

---

## Project Structure

```
.
├── AI-Virtual-keyboard-project/   # Virtual keyboard controlled by hand gestures
├── edge detection/                # Edge detection experiments
├── face-detection/                # Face detection experiments
├── Hand-tracking-project/         # Hand tracking using MediaPipe
├── object-claasification/         # Object detection/classification using YOLO
├── video-webcam/                  # Webcam / video capture scripts
│
├── loading.py                     # Load an image
├── displaying.py                  # Display an image in a window
├── saving.py                      # Save an image to disk
├── dimensions.py                  # Get image height, width, channels
├── resize.py                      # Resize an image
├── cropped.py                     # Crop a region of an image
├── rotation.py                    # Rotate an image
├── drowing-line.py                # Draw a line on an image
├── rectangle.py                   # Draw a rectangle on an image
├── circle.py                      # Draw a circle on an image
├── text-image.py                  # Write text on an image
├── text.txt                       # Text notes
├── task-1.py                      # Practice task 1
├── task-2.py                      # Practice task 2
│
├── output-image.png               # Sample output image
├── grayscale output-image.png     # Grayscale version of the output
├── resized_output.png             # Output of the resize script
│
├── hand_landmarker.task           # MediaPipe hand landmark model
└── yolo11n.pt                     # YOLO11 nano pre-trained weights
```

---

## Basic OpenCV Scripts

| File | Description |
|------|-------------|
| `loading.py` | Reads an image from disk using `cv2.imread()` |
| `displaying.py` | Shows an image in a window using `cv2.imshow()` |
| `saving.py` | Saves an image using `cv2.imwrite()` |
| `dimensions.py` | Prints the image shape (height, width, channels) |
| `resize.py` | Resizes an image (output: `resized_output.png`) |
| `cropped.py` | Crops part of an image using array slicing |
| `rotation.py` | Rotates an image |
| `drowing-line.py` | Draws a line on an image |
| `rectangle.py` | Draws a rectangle on an image |
| `circle.py` | Draws a circle on an image |
| `text-image.py` | Puts text on an image using `cv2.putText()` |
| `task-1.py`, `task-2.py` | Practice exercises |

## Mini Projects

| Folder | Description |
|--------|-------------|
| `edge detection/` | Detecting edges in images (e.g., Canny edge detection) |
| `face-detection/` | Detecting faces in images / video |
| `Hand-tracking-project/` | Real-time hand tracking using `hand_landmarker.task` (MediaPipe) |
| `object-claasification/` | Object detection / classification using `yolo11n.pt` (Ultralytics YOLO11) |
| `video-webcam/` | Capturing and displaying live webcam video |
| `AI-Virtual-keyboard-project/` | An AI virtual keyboard you can type on using hand gestures |

## Model Files

- **`hand_landmarker.task`** – MediaPipe Hand Landmarker model used for hand tracking.
- **`yolo11n.pt`** – Pre-trained YOLO11 nano model from Ultralytics used for object detection.

---

## Tech Stack

- Python 3
- OpenCV (`opencv-python`)
- MediaPipe
- Ultralytics (YOLO11)
- NumPy

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install opencv-python numpy mediapipe ultralytics
```

## Usage

Run any script directly, for example:

```bash
python loading.py
python resize.py
```

For the mini projects, open the folder and run its main script:

```bash
cd Hand-tracking-project
python main.py
```



## License

This project is for learning purposes. Feel free to use and modify it.
