import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\harmann.jpg")

if image is None:
    print("Oops! your image is not working")
else:
    print("Image loaded successfully!")

    pt1 = (150,300)
    pt2 = (100,300)
    color = (0, 0, 255)
    thickness = 3

    cv2.line(image, pt1, pt2, color, thickness)
    cv2.imshow("line Drawing",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()