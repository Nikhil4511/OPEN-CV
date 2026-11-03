""" It's Working
"""

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while True:
    success, img = cap.read()

    if not success:
        print("Camera frame nahi mila")
        break

    # Convert BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process image
    results = hands.process(imgRGB)

    # Detect hands
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                print(id, cx, cy)

                cv2.circle(img,(cx, cy),10,(255, 0, 255),
                    cv2.FILLED
                )

            # Draw hand connections
            mpDraw.draw_landmarks(img,handLms,
                mpHands.HAND_CONNECTIONS
            )

    # FPS
    cTime = time.time()

    if pTime != 0:
        fps = 1 / (cTime - pTime)
        cv2.putText(img,str(int(fps)),(15, 80),cv2.FONT_HERSHEY_PLAIN,3,(255, 0, 255),
            3
        )

    pTime = cTime

    cv2.imshow("Image", img)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()