import cv2
# image = cv2.imread(r"C:\Users\npal1\Pictures\harman-1.jpg")
image = cv2.imread(r"C:\Users\npal1\Pictures\harmann.jpg")


if image is None:
    print("Oops! your image is not working")

else:
    print("image loaded successfully!")
    # pt1 = (150,150)
    # pt2 = (250,250)

    # color = (0, 0, 255)
    # thickness = 3
    cv2.rectangle(image,pt1=(300,300),pt2=(150,150),color=(0,0,255),thickness=4)
    cv2.imshow("image focsing rectangle",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()