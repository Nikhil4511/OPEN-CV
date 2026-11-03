import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png")

if image is not None:
    cropped = image[200:400, 150:300]

    cv2.imshow("Original",image)
    cv2.imshow("Cropped image",cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()