import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png")
if image is None:
    print("Could not load image")
else:
    (h, w) = image.shape[:2]
    center = ((w//2),(h//2))
    M = cv2.getRotationMatrix2D(center,90,1.0)
    rotated = cv2.warpAffine(image,M,(w,h))

    cv2.imshow("Original",image)
    cv2.imshow("Rotated 90 degree",rotated)

    cv2.waitKey(0)
    cv2.destroyAllWindows()