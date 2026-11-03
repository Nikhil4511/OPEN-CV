import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png")

if image is None:
    print("Image not found")
else:
    print("Image loaded")

    resized = cv2.resize(image,(400,400))

    cv2.imshow("Original image",image)
    cv2.imshow("resized image",resized)

    cv2.imwrite("resized_output.png",resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()