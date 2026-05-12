import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
os.makedirs('adversarial_patches', exist_ok=True)

# 1. NOISE PATCH
noise = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
Image.fromarray(noise).save('adversarial_patches/noise_patch.png')

# 2. CHECKERBOARD PATCH
checker = np.zeros((200, 200, 3), dtype=np.uint8)
square_size = 25
for i in range(0, 200, square_size):
    for j in range(0, 200, square_size):
        if (i // square_size + j // square_size) % 2 == 0:
            checker[i:i+square_size, j:j+square_size] = [255, 255, 255]
Image.fromarray(checker).save('adversarial_patches/checkerboard_patch.png')

# 3. GRADIENT PATCH
gradient = np.zeros((200, 200, 3), dtype=np.uint8)
for i in range(200):
    for j in range(200):
        gradient[i, j] = [int(255 * i / 200), int(255 * j / 200), 128]
Image.fromarray(gradient).save('adversarial_patches/gradient_patch.png')

# 4. EDGE PATTERN (Concentric circles)
edge = Image.new('RGB', (200, 200), 'yellow')
draw = ImageDraw.Draw(edge)
colors = ['red', 'blue', 'yellow', 'red']
for i in range(10):
    draw.ellipse([i*10, i*10, 200-i*10, 200-i*10], 
                 outline=colors[i%4], width=3)
edge.save('adversarial_patches/edge_pattern_patch.png')

# 5. TEXT "GO" PATCH
text_go = Image.new('RGB', (200, 200), 'green')
draw = ImageDraw.Draw(text_go)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
except:
    font = ImageFont.load_default()
draw.text((50, 60), "GO", fill='white', font=font)
text_go.save('adversarial_patches/text_go_patch.png')

# 6. TEXT "YIELD" PATCH
text_yield = Image.new('RGB', (200, 200), 'green')
draw = ImageDraw.Draw(text_yield)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
except:
    font = ImageFont.load_default()
draw.text((20, 75), "YIELD", fill='white', font=font)
text_yield.save('adversarial_patches/text_yield_patch.png')

print("✅ All 6 patches generated in 'adversarial_patches/' folder")
print("\nGenerated patches:")
print("  1. noise_patch.png")
print("  2. checkerboard_patch.png")
print("  3. gradient_patch.png")
print("  4. edge_pattern_patch.png")
print("  5. text_go_patch.png")
print("  6. text_yield_patch.png")
