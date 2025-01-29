from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math

# Setup
WIDTH, HEIGHT = 1200, 1800
BG_COLOR = (240, 240, 240)  # Light gray
cover = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(cover)

# ===== FRONT COVER =====

# Gradient background
for y in range(HEIGHT):
    gradient = tuple(int(c * (1 - y/HEIGHT*0.5)) for c in (0, 0, 128))  # Navy gradient
    draw.line([(0, y), (WIDTH, y)], fill=gradient)

# Title
title_font = ImageFont.truetype("fonts/BebasNeue-Regular.ttf", 100)  # Download font from Google Fonts
draw.text((100, 100), "SUDOKU MASTERMIND", fill=(0, 0, 64), font=title_font)

# Subtitle
sub_font = ImageFont.truetype("fonts/Lora-Regular.ttf", 24)
sub_text = "74 Challenging Puzzles • 5 Levels of Difficulty • 16x16 Grids • Includes Solutions"
draw.text((100, 220), sub_text, fill=(255, 200, 0), font=sub_font)

# Sudoku Grid Background
def draw_grid(x, y, size, cells, line_width=2):
    cell_size = size // cells
    for i in range(cells + 1):
        width = line_width * 2 if i % 4 == 0 else line_width
        draw.line([(x, y + i*cell_size), (x + size, y + i*cell_size)], fill=(0, 0, 0), width=width)
        draw.line([(x + i*cell_size, y), (x + i*cell_size, y + size)], fill=(0, 0, 0), width=width)

# 16x16 grid (background)
draw_grid(200, 400, 800, 16, line_width=1)

# 9x9 grid overlay (foreground)
draw_grid(500, 600, 300, 9, line_width=2)

# Difficulty color bands
difficulty_colors = [(166, 232, 200), (255, 255, 153), (255, 178, 102), (255, 102, 102), (178, 102, 255)]
for i, color in enumerate(difficulty_colors):
    draw.rectangle([
        (100 + i*180, HEIGHT-300),
        (250 + i*180, HEIGHT-200)
    ], fill=color)

# Tagline
tag_font = ImageFont.truetype("fonts/Lora-Bold.ttf", 32)
draw.text((100, HEIGHT-150), "From Beginner to Expert – Conquer Every Grid!", 
          fill=(0, 0, 64), font=tag_font)

# ===== BACK COVER =====
# (For simplicity, we'll create a separate image)
back_cover = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
back_draw = ImageDraw.Draw(back_cover)

# Description
desc_font = ImageFont.truetype("fonts/Lora-Regular.ttf", 24)
description = """Dive into 74 expertly crafted Sudoku puzzles, including five sprawling 16x16 challenges! With 5 difficulty levels—Starter, Intermediate, Advanced, Expert, and Mastermind—this book is perfect for sharpening your logic at any skill level. Solutions included for every puzzle!"""
back_draw.multiline_text((100, 100), description, fill=(0, 0, 64), font=desc_font, spacing=20)

# Features list
features = [
    "✔️ 74 Pages of Brain-Teasing Fun",
    "✔️ 5 Difficulty Levels (Color-Coded)",
    "✔️ 5 Giant 16x16 Sudoku Grids",
    "✔️ Full Solutions Provided",
    "✔️ Clear, Easy-to-Read Layout"
]
back_draw.multiline_text((100, 400), "\n".join(features), fill=(0, 0, 128), font=desc_font, spacing=25)

# Solved grid snippet
draw_grid(800, 400, 200, 16, line_width=1)
back_draw.text((850, 450), "SOLVED", fill=(0, 128, 0), font=desc_font)

# Barcode placeholder
back_draw.rectangle([(WIDTH-250, HEIGHT-150), (WIDTH-50, HEIGHT-50)], fill=(0, 0, 0))
back_draw.text((WIDTH-230, HEIGHT-140), "ISBN Barcode Area", fill=(255, 255, 255), font=desc_font)

# ===== SAVE RESULTS =====
cover.save("book/sudoku_front_cover.png")
back_cover.save("book/sudoku_back_cover.png")