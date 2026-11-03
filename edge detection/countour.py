import cv2

img = cv2.imread()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)

# find countours
contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2)

cv2.drawContours(img,contours,-1,(0,200,0),3)

cv2.imshow("Contours",img)
cv2.waitKey(0)
cv2.destroyAllWindows()