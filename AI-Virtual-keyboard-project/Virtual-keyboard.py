"""
AI Virtual Keyboard  ·  OpenCV + MediaPipe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gesture : Pinch index-finger + thumb together to press a key
Quit    : Press 'q' on physical keyboard  (or Ctrl-C in terminal)
"""

import cv2
import math
import time
import pynput
import numpy as np
import mediapipe as mp
from pynput.keyboard import Controller, Key as PKey

# ─────────────────────────── MediaPipe ──────────────────────────────────────
mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles  = mp.solutions.drawing_styles

hand_det = mp_hands.Hands(
    static_image_mode       = False,
    max_num_hands           = 1,
    min_detection_confidence= 0.75,
    min_tracking_confidence = 0.75,
)
kb = Controller()   # virtual OS keyboard

# ─────────────────────────── Layout constants ────────────────────────────────
ROWS = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",";"],
    ["Z","X","C","V","B","N","M",",",".","/"],
]

KW, KH, GAP   = 62, 58, 6          # key width, height, gap
START_X       = 32                  # keyboard left margin
START_Y       = 245                 # keyboard top margin

PINCH_THRESH  = 42                  # px – index/thumb distance = pinch
COOLDOWN_SEC  = 0.35                # s  – min time between key presses
FLASH_FRAMES  = 9                   # frames for green press-flash

# ─────────────────────────── Colour palette (BGR) ───────────────────────────
C = {
    "bg"      : (10,  10,  10),
    "key"     : (38,  38,  38),
    "hover"   : (90,  55, 185),
    "press"   : (30, 195,  90),
    "border"  : (160,160, 160),
    "text"    : (240,240, 240),
    "txtbox"  : (22,  22,  22),
    "accent"  : ( 0, 200, 255),     # index-finger dot
    "thumb"   : (30, 210, 210),
    "pinch"   : (30, 190,  90),
    "subtle"  : (110,110, 110),
}

# ─────────────────────────── Button class ───────────────────────────────────
class VKey:
    """One key on the virtual keyboard."""

    def __init__(self, label: str, x: int, y: int,
                 w: int = KW, h: int = KH):
        self.label = label
        self.x, self.y, self.w, self.h = x, y, w, h
        self._last_press = 0.0
        self._flash      = 0           # countdown flash frames

    # ── hit-test ──────────────────────────────────────────────────────────
    def contains(self, px: int, py: int) -> bool:
        return (self.x <= px <= self.x + self.w and
                self.y <= py <= self.y + self.h)

    # ── trigger ───────────────────────────────────────────────────────────
    def trigger(self, typed: str) -> str:
        """Fire the key action; respects cooldown. Returns updated typed str."""
        now = time.time()
        if now - self._last_press < COOLDOWN_SEC:
            return typed                    # still in cooldown

        self._last_press = now
        self._flash      = FLASH_FRAMES

        lbl = self.label
        if lbl == "BKSP":
            kb.press(PKey.backspace); kb.release(PKey.backspace)
            return typed[:-1]
        elif lbl == "SPACE":
            kb.press(PKey.space); kb.release(PKey.space)
            return typed + " "
        elif lbl == "ENTER":
            kb.press(PKey.enter); kb.release(PKey.enter)
            return typed + "\n"
        elif lbl == "CLEAR":
            return ""
        else:
            kb.press(lbl.lower()); kb.release(lbl.lower())
            return typed + lbl

    # ── draw ──────────────────────────────────────────────────────────────
    def draw(self, frame: np.ndarray, hover: bool = False):
        x, y, w, h = self.x, self.y, self.w, self.h
        col = (C["press"] if self._flash > 0
               else C["hover"] if hover
               else C["key"])

        # Semi-transparent fill via blend
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x+w, y+h), col, -1)
        cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)

        # Border (thicker on hover/press)
        bw  = 2 if (hover or self._flash) else 1
        bcl = C["accent"] if hover else C["border"]
        cv2.rectangle(frame, (x, y), (x+w, y+h), bcl, bw)

        # Label — scale down for longer strings
        fscale = 0.52 if len(self.label) <= 2 else 0.38
        tsz = cv2.getTextSize(self.label, cv2.FONT_HERSHEY_SIMPLEX, fscale, 2)[0]
        tx  = x + (w - tsz[0]) // 2
        ty  = y + (h + tsz[1]) // 2
        cv2.putText(frame, self.label, (tx, ty),
                    cv2.FONT_HERSHEY_SIMPLEX, fscale,
                    C["text"], 2, cv2.LINE_AA)

        if self._flash > 0:
            self._flash -= 1


# ─────────────────────────── Build button grid ───────────────────────────────
def build_buttons() -> list[VKey]:
    btns: list[VKey] = []

    for r, row in enumerate(ROWS):
        for c, lbl in enumerate(row):
            x = START_X + c * (KW + GAP)
            y = START_Y + r * (KH + GAP)
            btns.append(VKey(lbl, x, y))

    # Special bottom row  [BKSP | ────SPACE──── | ENTER | CLEAR]
    special = [("BKSP", 95), ("SPACE", 310), ("ENTER", 95), ("CLEAR", 95)]
    sx = START_X
    sy = START_Y + 3 * (KH + GAP)
    for lbl, w in special:
        btns.append(VKey(lbl, sx, sy, w, KH))
        sx += w + GAP

    return btns


# ─────────────────────────── Utility helpers ─────────────────────────────────
def dist(a, b) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])


def draw_textbox(frame, typed: str, W: int):
    """Draw the typed-text display at top of frame."""
    bx, by, bw, bh = 28, 18, W - 56, 78
    cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), C["txtbox"], -1)
    cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), C["accent"], 2)

    cv2.putText(frame, "OUTPUT", (bx+8, by-6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, C["accent"], 1, cv2.LINE_AA)

    # Scroll: keep last 55 chars
    show = (typed[-55:] if len(typed) > 55 else typed).replace("\n", "↵")
    cv2.putText(frame, show + "|", (bx+10, by+54),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, C["accent"], 2, cv2.LINE_AA)


def draw_hud(frame, pinching: bool, d_pinch: float, W: int):
    """HUD: title, gesture status, pinch distance bar."""
    # Title
    cv2.putText(frame, "AI Virtual Keyboard",
                (28, 130), cv2.FONT_HERSHEY_SIMPLEX,
                0.72, C["text"], 2, cv2.LINE_AA)

    # Status badge
    status_txt = "PINCH !" if pinching else "Pinch index+thumb to type"
    status_col = C["press"] if pinching else C["subtle"]
    cv2.putText(frame, status_txt, (28, 158),
                cv2.FONT_HERSHEY_SIMPLEX, 0.44, status_col, 1, cv2.LINE_AA)

    # Pinch distance bar (top-right corner)
    bar_max = 120
    bar_w   = min(int(d_pinch / PINCH_THRESH * bar_max), bar_max) if d_pinch else 0
    bx, by  = W - 140, 24
    cv2.rectangle(frame, (bx, by), (bx+bar_max, by+14), (50,50,50), -1)
    bar_col = C["press"] if pinching else C["hover"]
    cv2.rectangle(frame, (bx, by), (bx+bar_w, by+14), bar_col, -1)
    cv2.putText(frame, "PINCH", (bx, by-4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.36, C["subtle"], 1, cv2.LINE_AA)


def draw_finger_ui(frame, ix, iy, tx, ty, pinching: bool):
    """Visualise fingertips and pinch line."""
    cv2.circle(frame, (tx, ty), 9,  C["thumb"],  -1)
    cv2.circle(frame, (ix, iy), 12, C["accent"],  -1)
    cv2.circle(frame, (ix, iy), 14, C["accent"],   2)

    line_col = C["pinch"] if pinching else C["subtle"]
    cv2.line(frame, (ix, iy), (tx, ty), line_col, 2)

    # Small pinch-distance label
    mx, my = (ix+tx)//2, (iy+ty)//2
    d_text = f"{int(dist((ix,iy),(tx,ty)))}px"
    cv2.putText(frame, d_text, (mx+6, my),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, C["subtle"], 1, cv2.LINE_AA)


# ─────────────────────────── Main ────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  860)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)

    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    buttons = build_buttons()
    typed   = ""

    print("▶  AI Virtual Keyboard started — press 'q' to quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Camera read failed — exiting.")
            break

        frame = cv2.flip(frame, 1)          # mirror so it feels natural

        # ── Background tint ──────────────────────────────────────────────
        frame[:] = (frame * 0.55).astype(np.uint8)   # darken camera feed

        # ── Hand detection ───────────────────────────────────────────────
        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand_det.process(rgb)

        ix = iy = tx = ty = None
        d_pinch  = 0.0
        pinching = False

        if result.multi_hand_landmarks:
            lm   = result.multi_hand_landmarks[0].landmark
            fh, fw = frame.shape[:2]

            # Draw hand skeleton
            mp_drawing.draw_landmarks(
                frame,
                result.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(80,80,80), thickness=1, circle_radius=2),
                mp_drawing.DrawingSpec(color=(80,80,80), thickness=1),
            )

            ix, iy = int(lm[8].x * fw), int(lm[8].y * fh)   # index tip
            tx, ty = int(lm[4].x * fw), int(lm[4].y * fh)   # thumb tip

            d_pinch  = dist((ix,iy), (tx,ty))
            pinching = d_pinch < PINCH_THRESH

            draw_finger_ui(frame, ix, iy, tx, ty, pinching)

        # ── Draw UI layers ───────────────────────────────────────────────
        draw_textbox(frame, typed, W)
        draw_hud(frame, pinching, d_pinch, W)

        for btn in buttons:
            hover = (ix is not None) and btn.contains(ix, iy)
            if hover and pinching:
                typed = btn.trigger(typed)
            btn.draw(frame, hover=hover)

        # ── Footer ───────────────────────────────────────────────────────
        cv2.putText(frame,
                    "Index finger = cursor  |  Pinch (index+thumb) = press  |  q = quit",
                    (28, H - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.38, C["subtle"], 1, cv2.LINE_AA)

        cv2.imshow("AI Virtual Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Done. Typed text:\n", typed)


if __name__ == "__main__":
    main()