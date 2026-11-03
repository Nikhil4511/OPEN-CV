import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\Screenshots\Screenshot 2026-07-31 174640.png")

if image is not None:
    h, w, c = image.shape
    print(f"Image loaded:\nHeight: {h}\nWidth:{w}\nChannels:{c}")

else:
    print("Could not load image")