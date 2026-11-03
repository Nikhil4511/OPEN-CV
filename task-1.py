import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png",flags=0)

if image is not None:
    cv2.imshow("Showing image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    success = cv2.imwrite("grayscale output-image.png",image)
    if success:
        print("Successfully saved")
    else:
        print("Failed an image")