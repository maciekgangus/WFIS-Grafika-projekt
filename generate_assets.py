import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_road_texture():
    print("Generating road texture...")
    width, height = 2048, 2048
    data = np.random.randint(20, 35, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(data)
    draw = ImageDraw.Draw(img)

    img_spec = Image.new('RGB', (width, height), color=(10, 10, 10))
    draw_spec = ImageDraw.Draw(img_spec)

    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(30, 120)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(40, 40, 40), outline=None)
        draw_spec.ellipse((x-r, y-r, x+r, y+r), fill=(200, 200, 200), outline=None)

    line_width = 12

    center = width // 2
    gap = 16

    draw.rectangle((center - gap - line_width, 0, center - gap, height), fill=(220, 200, 100))
    draw_spec.rectangle((center - gap - line_width, 0, center - gap, height), fill=(0, 0, 0))

    draw.rectangle((center + gap, 0, center + gap + line_width, height), fill=(220, 200, 100))
    draw_spec.rectangle((center + gap, 0, center + gap + line_width, height), fill=(0, 0, 0))

    dash_len = 128
    gap_len = 128

    left_dash = width // 4
    right_dash = 3 * width // 4

    for y in range(0, height, dash_len + gap_len):
        draw.rectangle((left_dash - line_width//2, y, left_dash + line_width//2, y + dash_len), fill=(220, 220, 220))
        draw_spec.rectangle((left_dash - line_width//2, y, left_dash + line_width//2, y + dash_len), fill=(0, 0, 0))

        draw.rectangle((right_dash - line_width//2, y, right_dash + line_width//2, y + dash_len), fill=(220, 220, 220))
        draw_spec.rectangle((right_dash - line_width//2, y, right_dash + line_width//2, y + dash_len), fill=(0, 0, 0))

    img.save("textures/road.png")
    img_spec.save("textures/road_spec.png")



def generate_building_texture():
    print("Generating building texture...")
    width, height = 512, 512
    img = Image.new('RGB', (width, height), color=(10, 10, 15))
    draw = ImageDraw.Draw(img)
    
    img_emit = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw_emit = ImageDraw.Draw(img_emit)
    
    rows = 10
    cols = 8
    w_width = width // cols
    w_height = height // rows
    
    padding = 10
    
    for r in range(rows):
        for c in range(cols):
            if random.random() > 0.4:
                if random.random() > 0.5:
                    color = (255, 220 + random.randint(-20, 20), 100 + random.randint(-20, 20))
                else:
                    color = (200 + random.randint(-20, 20), 200 + random.randint(-20, 20), 255)
                
                x1 = c * w_width + padding
                y1 = r * w_height + padding
                x2 = (c + 1) * w_width - padding
                y2 = (r + 1) * w_height - padding
                
                draw.rectangle((x1, y1, x2, y2), fill=color)
                
                draw_emit.rectangle((x1, y1, x2, y2), fill=color)
                
    img.save("textures/building.png")
    img_emit.save("textures/building_emission.png")

def generate_sidewalk_texture():
    print("Generating sidewalk texture...")
    width, height = 512, 512
    data = np.random.randint(100, 120, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(data)
    draw = ImageDraw.Draw(img)
    
    tile_size = 64
    for x in range(0, width, tile_size):
        draw.line((x, 0, x, height), fill=(80, 80, 80), width=2)
    for y in range(0, height, tile_size):
        draw.line((0, y, width, y), fill=(80, 80, 80), width=2)
        
    img.save("textures/sidewalk.png")

def generate_black_texture():
    print("Generating black texture...")
    img = Image.new('RGB', (64, 64), color=(0, 0, 0))
    img.save("textures/black.png")

def generate_grass_texture():
    print("Generating grass texture...")
    width, height = 512, 512
    data = np.random.randint(40, 80, (height, width, 3), dtype=np.uint8)

    data[:, :, 0] = np.clip(data[:, :, 0] * 0.6, 20, 60).astype(np.uint8)
    data[:, :, 1] = np.clip(data[:, :, 1] * 1.4, 60, 140).astype(np.uint8)
    data[:, :, 2] = np.clip(data[:, :, 2] * 0.5, 15, 50).astype(np.uint8)

    img = Image.fromarray(data)
    draw = ImageDraw.Draw(img)

    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(10, 30)
        color = (random.randint(25, 40), random.randint(50, 80), random.randint(15, 35))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color, outline=None)

    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(5, 15)
        color = (random.randint(50, 70), random.randint(100, 130), random.randint(30, 50))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color, outline=None)

    img.save("textures/grass.png")

def generate_billboard_texture():
    print("Generating billboard texture...")
    width, height = 4096, 1024

    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img)

    img_emit = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw_emit = ImageDraw.Draw(img_emit)

    text = "PROSZE O 3.0"

    target_width = width * 0.8
    target_height = height * 0.8

    font = None
    font_size = 100

    font_paths = [
        "/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf",
        "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]

    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break

    if font_path:
        min_size = 50
        max_size = 2000
        best_size = 100

        for _ in range(20):
            test_size = (min_size + max_size) // 2
            test_font = ImageFont.truetype(font_path, test_size)
            bbox = draw.textbbox((0, 0), text, font=test_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width <= target_width and text_height <= target_height:
                best_size = test_size
                min_size = test_size
            else:
                max_size = test_size

        font_size = best_size
        font = ImageFont.truetype(font_path, font_size)
        print(f"Using font size: {font_size}")
    else:
        font = ImageFont.load_default()
        print("Using default font")

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    draw_emit.text((x, y), text, font=font, fill=(255, 255, 255))

    img.save("textures/billboard.png")
    img_emit.save("textures/billboard_emission.png")


def generate_car_body_texture():
    print("Generating car body texture...")
    img = Image.new('RGB', (64, 64), color=(100, 20, 20))
    img.save("textures/car_body.png")


def generate_headlight_texture():
    print("Generating headlight texture...")
    img = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 56, 56), fill=(255, 255, 220))
    img.save("textures/headlight.png")


def generate_taillight_texture():
    print("Generating taillight texture...")
    img = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((12, 24, 52, 40), fill=(255, 0, 0))
    img.save("textures/taillight.png")


def generate_windshield_texture():
    print("Generating windshield texture...")
    img = Image.new('RGB', (64, 64), color=(100, 120, 150))
    img.save("textures/windshield.png")


def main():
    ensure_dir("textures")
    generate_road_texture()
    generate_building_texture()
    generate_sidewalk_texture()
    generate_grass_texture()
    generate_billboard_texture()
    generate_black_texture()
    generate_car_body_texture()
    generate_headlight_texture()
    generate_taillight_texture()
    generate_windshield_texture()
    print("Assets generated.")

if __name__ == "__main__":
    main()