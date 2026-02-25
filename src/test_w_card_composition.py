#   call .venv\Scripts\activate.bat
#   python src\test_w_card_composition.py

#import ReportLab

#import pypdf

#import fpdf2

#import wand

from PIL import Image, ImageDraw

# --- Sizes in millimeters ---
A4_W, A4_H = 210, 297
A6_W, A6_H = 105, 148

# --- Resolution ---
DPI = 300
MM_TO_INCH = 1 / 25.4

def mm_to_px(mm):
    return int(mm * MM_TO_INCH * DPI)

# Convert sizes to pixels
a4_px = (mm_to_px(A4_W), mm_to_px(A4_H))
a6_px = (mm_to_px(A6_W), mm_to_px(A6_H))

# Create white A4 canvas
canvas = Image.new("RGB", a4_px, "white")
draw = ImageDraw.Draw(canvas)

# Compute centered A6 rectangle
x0 = (a4_px[0] - a6_px[0]) // 2
y0 = (a4_px[1] - a6_px[1]) // 2
x1 = x0 + a6_px[0]
y1 = y0 + a6_px[1]

# Draw red A6 rectangle
draw.rectangle([x0, y0, x1, y1], fill="red")

# Save as PDF
canvas.save("a4_with_a6_centered.pdf", "PDF", resolution=DPI)
