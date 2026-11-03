import cv2

image = cv2.imread(r"C:\Users\npal1\Pictures\WhatsApp Image 2026-07-03 at 10.18.09 PM (1).jpeg")

if image is None:
    print("Error: Image not found")
else:
    print("Image loaded successfully")

