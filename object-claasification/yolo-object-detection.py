""" Working"""
import cv2
import torch
from ultralytics import YOLO
import time

# ─── Configuration (yahan se tune karo) ──────────────────────────────────────
MODEL_PATH  = "yolo11n.pt"
CONF_THRESH = 0.40          # 0.0 - 1.0 → zyada = strict detection
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
# ─────────────────────────────────────────────────────────────────────────────

# Load model + move to GPU/CPU
print(f"[INFO] Model load ho raha hai → {DEVICE.upper()} pe...")
model = YOLO(MODEL_PATH)
model.to(DEVICE)

# Open webcam
cap = cv2.VideoCapture(0)

# ✅ FIX 1: Camera open hua ya nahi, pehle check karo
if not cap.isOpened():
    print("[ERROR] Webcam nahi khuli! Camera connection check karo.")
    exit(1)

print("[INFO] Detection start. 'q' dabao exit karne ke liye.\n")

prev_time = time.time()

while True:
    success, frame = cap.read()

    if not success:
        # ✅ FIX 2: Break instead of silent exit — better error visibility
        print("[WARN] Frame nahi mila, retry kar raha hoon...")
        continue

    # ── YOLO Inference ────────────────────────────────────────────────────────
    # ✅ FIX 3: conf threshold + verbose=False (console spam band)
    results = model(frame, conf=CONF_THRESH, verbose=False)

    # ── Annotate frame ────────────────────────────────────────────────────────
    annotated_frame = results[0].plot()

    # ── FPS Calculation ───────────────────────────────────────────────────────
    curr_time = time.time()
    fps = 1.0 / (curr_time - prev_time + 1e-9)   # 1e-9 → div-by-zero se bachao
    prev_time = curr_time

    # ── Object count ──────────────────────────────────────────────────────────
    num_objects = len(results[0].boxes)

    # ── HUD Overlay ───────────────────────────────────────────────────────────
    # ✅ FIX 4: FPS, object count, device — sab screen pe dikhta hai
    cv2.putText(annotated_frame, f"FPS: {fps:.1f}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Objects: {num_objects}",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    cv2.putText(annotated_frame, f"Device: {DEVICE.upper()}",
                (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # ── Show Window ───────────────────────────────────────────────────────────
    cv2.imshow("YOLO11 – Live Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("[INFO] Detection band. Bye!")