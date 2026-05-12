from PIL import Image
import os

# Create output directories
os.makedirs('size_variations', exist_ok=True)
os.makedirs('rotation_variations', exist_ok=True)

# Load your best patch (use noise patch for consistency)
# First create a simple noise patch if needed
import numpy as np
noise = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
patch = Image.fromarray(noise)

# Create base stop sign
base = Image.new('RGB', (512, 512), 'white')
from PIL import ImageDraw
draw = ImageDraw.Draw(base)
octagon = [(128, 50), (384, 50), (462, 128), (462, 384), 
           (384, 462), (128, 462), (50, 384), (50, 128)]
draw.polygon(octagon, fill='red', outline='white')

# Add STOP text
try:
    from PIL import ImageFont
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
    draw.text((160, 200), "STOP", fill='white', font=font)
except:
    pass

print("Generating SIZE variations...")
# SIZE VARIATIONS: 0.5x, 0.75x, 1.0x, 1.5x, 2.0x
sizes = [0.5, 0.75, 1.0, 1.5, 2.0]
for scale in sizes:
    stopsign = base.copy()
    new_size = int(200 * scale)
    resized_patch = patch.resize((new_size, new_size))
    
    # Center position
    x = (512 - new_size) // 2
    y = (512 - new_size) // 2
    
    stopsign.paste(resized_patch, (x, y))
    stopsign.save(f'size_variations/stopsign_size_{scale}x.jpg')
    print(f"  ✅ Created size {scale}x")

print("\nGenerating ROTATION variations...")
# ROTATION VARIATIONS: 0°, 45°, 90°, 135°, 180°
angles = [0, 45, 90, 135, 180]
for angle in angles:
    stopsign = base.copy()
    rotated_patch = patch.rotate(angle, expand=False)
    
    # Center position (210, 210) for 200x200 patch on 512x512 image
    stopsign.paste(rotated_patch, (210, 210))
    stopsign.save(f'rotation_variations/stopsign_rotation_{angle}deg.jpg')
    print(f"  ✅ Created rotation {angle}°")

print("\n✅ All transformations generated!")
print(f"  Size variations: {len(sizes)} files")
print(f"  Rotation variations: {len(angles)} files")
