from PIL import Image
import os

# Create output directory
os.makedirs('patched_stopsigns', exist_ok=True)

# Load base stop sign (create a simple one if you don't have it)
# For now, we'll create a red octagon
base = Image.new('RGB', (512, 512), 'white')

# Simple red octagon stop sign
from PIL import ImageDraw
draw = ImageDraw.Draw(base)
octagon = [(128, 50), (384, 50), (462, 128), (462, 384), 
           (384, 462), (128, 462), (50, 384), (50, 128)]
draw.polygon(octagon, fill='red', outline='white')

# Add "STOP" text
try:
    from PIL import ImageFont
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
    draw.text((160, 200), "STOP", fill='white', font=font)
except:
    pass

# Save base stop sign
base.save('patched_stopsigns/stopsign_base.jpg')

# Apply each patch at center (310, 310)
patch_files = [
    'noise_patch.png',
    'checkerboard_patch.png',
    'gradient_patch.png',
    'edge_pattern_patch.png',
    'text_go_patch.png',
    'text_yield_patch.png'
]

for patch_file in patch_files:
    # Load patch
    patch = Image.open(f'adversarial_patches/{patch_file}')
    
    # Create new stop sign with patch
    stopsign = base.copy()
    
    # Paste patch at center (310, 310) - accounting for 200x200 size
    stopsign.paste(patch, (210, 210))
    
    # Save
    output_name = f'stopsign_with_{patch_file.replace("_patch.png", "")}.jpg'
    stopsign.save(f'patched_stopsigns/{output_name}')
    print(f"✅ Created: {output_name}")

print("\n✅ All patched stop signs created in 'patched_stopsigns/' folder")
