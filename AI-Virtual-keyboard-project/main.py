import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)

class Button():
    def __init__(self,pos,text,size=[100,100]):
        self.pos = pos
        self.size = size
        self.text = text

        def draw(self, img):
            cv2.rectangle(img,self.pos,self.size,(255,0,255),cv2,FILLED)
            cv2.putText(img,self.text,(self.pos[0]+25,self.pos[1]+25),cv2.FONT_HERSHEY_PLAIN,
                            5, (255,255,255),5)

        return img


myButton = Button([100,100],"Q")

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist,bboxInfo = detector.findHands(img)
# c:/Users/npal1/Desktop/Nikhil/coding/open-cv/AI-Virtual-keyboard-project/main.py
 
    cv2.rectangle(img,(100,100),(200,200),(255,0,255),cv2,FILLED)
    cv2.putText(img,"Q",(115,180),cv2.FONT_HERSHEY_PLAIN,
                5, (255,255,255),5)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)