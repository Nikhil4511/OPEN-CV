import cv2

path = input("Enter image path: ")

img = cv2.imread(r"C:\Users\npal1\Pictures\har-2.jpg")

if img is None:
    print("Image not found!")
else:
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()