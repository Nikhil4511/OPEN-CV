import cv2

img = cv2.imread(r"C:\Users\npal1\Pictures\har-2.jpg",cv2.IMREAD_GRAYSCALE)

ret, thresh_img = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

cv2.imshow("Original Image",img)
cv2.imshow("Thresholed image",thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()