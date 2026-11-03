import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\harman-1.jpg" )

if image is not None:
    cv2.imshow("Image showing",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Image not found")