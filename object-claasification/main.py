import cv2
import numpy as np
from pathlib import Path


# ==========================================
# 1. MODEL PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

prototxt = BASE_DIR / "MobileNetSSD_deploy.prototxt"
model = BASE_DIR / "MobileNetSSD_deploy.caffemodel"


# Check model files
if not prototxt.exists():
    print("ERROR: Prototxt file not found!")
    print(prototxt)
    exit()

if not model.exists():
    print("ERROR: Caffemodel file not found!")
    print(model)
    exit()


# ==========================================
# 2. LOAD MOBILE NET MODEL
# ==========================================

net = cv2.dnn.readNetFromCaffe(
    str(prototxt),
    str(model)
)

print("Model loaded successfully!")


# ==========================================
# 3. OBJECT CLASSES
# ==========================================

classes = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
    "Phone",
    "Book"
]


# ==========================================
# 4. OPEN WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened!")
    exit()


# ==========================================
# 5. REAL-TIME DETECTION
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        print("Camera frame nahi mila")
        break

    h, w = frame.shape[:2]


    # ======================================
    # 6. PREPROCESS IMAGE
    # ======================================

    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843,
        (300, 300),
        127.5
    )

    net.setInput(blob)


    # ======================================
    # 7. MODEL PREDICTION
    # ======================================

    detections = net.forward()


    # ======================================
    # 8. PROCESS DETECTIONS
    # ======================================

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]


        # Only show confident predictions
        if confidence > 0.5:

            class_id = int(detections[0, 0, i, 1])

            # Make sure class ID is valid
            if class_id >= len(classes):
                continue


            # ==================================
            # 9. GET BOUNDING BOX
            # ==================================

            box = detections[0, 0, i, 3:7] * np.array(
                [w, h, w, h]
            )

            startX, startY, endX, endY = box.astype(int)


            # Keep coordinates inside image
            startX = max(0, startX)
            startY = max(0, startY)
            endX = min(w - 1, endX)
            endY = min(h - 1, endY)


            # ==================================
            # 10. LABEL
            # ==================================

            label = classes[class_id]

            text = f"{label}: {confidence * 100:.1f}%"


            # ==================================
            # 11. DRAW BOUNDING BOX
            # ==================================

            cv2.rectangle(
                frame,
                (startX, startY),
                (endX, endY),
                (255, 0, 255),
                2
            )


            # ==================================
            # 12. DRAW LABEL
            # ==================================

            cv2.putText(
                frame,
                text,
                (startX, max(20, startY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 255),
                2
            )


    # ==========================================
    # 13. DISPLAY
    # ==========================================

    cv2.imshow("Object Detection", frame)


    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 14. RELEASE
# ==========================================

cap.release()
cv2.destroyAllWindows()


# #Import the neccesary libraries
# import numpy as np
# import argparse
# import cv2 

# # construct the argument parse 
# parser = argparse.ArgumentParser(
#     description='Script to run MobileNet-SSD object detection network ')
# parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
# parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
#                                   help='Path to text network file: '
#                                        'MobileNetSSD_deploy.prototxt for Caffe model or '
#                                        )
# parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
#                                  help='Path to weights: '
#                                       'MobileNetSSD_deploy.caffemodel for Caffe model or '
#                                       )
# parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
# args = parser.parse_args()

# # Labels of Network.
# classNames = { 0: 'background',
#     1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
#     5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
#     10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
#     14: 'motorbike', 15: 'person', 16: 'pottedplant',
#     17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

# # Open video file or capture device. 
# if args.video:
#     cap = cv2.VideoCapture(args.video)
# else:
#     cap = cv2.VideoCapture(0)

# #Load the Caffe model 
# net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

#     # MobileNet requires fixed dimensions for input image(s)
#     # so we have to ensure that it is resized to 300x300 pixels.
#     # set a scale factor to image because network the objects has differents size. 
#     # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
#     # after executing this command our "blob" now has the shape:
#     # (1, 3, 300, 300)
#     blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
#     #Set to network the input blob 
#     net.setInput(blob)
#     #Prediction of network
#     detections = net.forward()

#     #Size of frame resize (300x300)
#     cols = frame_resized.shape[1] 
#     rows = frame_resized.shape[0]

#     #For get the class and location of object detected, 
#     # There is a fix index for class, location and confidence
#     # value in @detections array .
#     for i in range(detections.shape[2]):
#         confidence = detections[0, 0, i, 2] #Confidence of prediction 
#         if confidence > args.thr: # Filter prediction 
#             class_id = int(detections[0, 0, i, 1]) # Class label

#             # Object location 
#             xLeftBottom = int(detections[0, 0, i, 3] * cols) 
#             yLeftBottom = int(detections[0, 0, i, 4] * rows)
#             xRightTop   = int(detections[0, 0, i, 5] * cols)
#             yRightTop   = int(detections[0, 0, i, 6] * rows)
            
#             # Factor for scale to original size of frame
#             heightFactor = frame.shape[0]/300.0  
#             widthFactor = frame.shape[1]/300.0 
#             # Scale object detection to frame
#             xLeftBottom = int(widthFactor * xLeftBottom) 
#             yLeftBottom = int(heightFactor * yLeftBottom)
#             xRightTop   = int(widthFactor * xRightTop)
#             yRightTop   = int(heightFactor * yRightTop)
#             # Draw location of object  
#             cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
#                           (0, 255, 0))

#             # Draw label and confidence of prediction in frame resized
#             if class_id in classNames:
#                 label = classNames[class_id] + ": " + str(confidence)
#                 labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

#                 yLeftBottom = max(yLeftBottom, labelSize[1])
#                 cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
#                                      (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
#                                      (255, 255, 255), cv2.FILLED)
#                 cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

#                 print(label) #print class and confidence

#     cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) >= 0:  # Break with ESC 
#         break