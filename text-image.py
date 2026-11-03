import cv2
image = cv2.imread(r"C:\Users\npal1\Pictures\har-2.jpg")


if image is None:
    print("Oops! your image is not working")

else:
    print("image loaded successfully!")
    cv2.putText(image,"Hello Harman!! G",(50,200),
                cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,255),2)
    cv2.imshow("Adding over text image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()