import cv2
image = cv2.imread(r"C:\Users\npal1\Pictures\har-2.jpg")

blurred = cv2.GaussianBlur(image,(3,3),4)

cv2.imshow("Original image",image)
cv2.imshow("Blurred image",blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()