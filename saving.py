import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png")

if image is not None:
    success = cv2.imwrite("output-image.png",image)
    if success:
        print("Successfully saved")
    else:
        print("Failed an image")

else:
    print("Error")