import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\median-blur.jpg")

blurred = cv2.medianBlur(image,15)

cv2.imshow("Original",image)
cv2.imshow("Clean image",blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()