import cv2
# image = cv2.imread(r"C:\Users\npal1\Pictures\harmann.jpg")
image = cv2.imread(r"C:\Users\npal1\Pictures\har-2.jpg")


if image is None:
    print("Oops! your image is not working")

else:
    print("image loaded successfully!")
    # pt1 = (150,150)
    # pt2 = (250,250)

    # color = (0, 0, 255)
    # thickness = 3
    
    # cv2.rectangle(image,pt1=(300,300),pt2=(150,150),color=(0,0,255),thickness=4)
    cv2.circle(image,(180,200),70,(255,0,0),3)

    cv2.imshow("Drawing Circle",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()