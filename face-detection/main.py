# import cv2

# face_cascade = cv2.CascadeClassifier(r"C:\Users\npal1\Desktop\Nikhil\coding\open-cv\face-detection\haarcascade_frontalface_default.xml")

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = face_cascade.detectMultiScale(gray, 1.1,5)

#     for (x,y,w,h) in faces:
#         cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)

#         cv2.imshow("Webcam face detection",frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break


#     cap.release()
#     cv2.destroyAllWindows()



