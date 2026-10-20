
from pathlib import Path
from collections import Counter
from PIL import Image

# 1. Image dimensions
width = 432
height = 475
block_size = 16

# 2. Read encrypted file
data = Path("classified.enc").read_bytes()

print("Encrypted file size:", len(data))

# 3. Remove OpenSSL header
assert data[:8] == b"Salted__"
ciphertext = data[16:]

# 4. Exclude AES padding
image_size = width * height
image_ciphertext = ciphertext[:image_size]

# 5. Divide ciphertext into AES blocks
blocks = []

for i in range(0, len(image_ciphertext), block_size):
    block = image_ciphertext[i:i + block_size]
    blocks.append(block)

# 6. Count repeated blocks
counts = Counter(blocks)

print("Total image blocks:", len(blocks))
print("Unique blocks:", len(counts))
print("Repeated block types:",
      sum(1 for count in counts.values() if count > 1))

# 7. Sort blocks by frequency
sorted_blocks = sorted(
    counts,
    key=lambda block: (-counts[block], block)
)

# 8. High-contrast grayscale palette
palette = [
    0, 255, 190, 100, 230,
    140, 70, 210, 120, 245,
    160, 85, 200, 130, 50
]

shades = {}

for index, block in enumerate(sorted_blocks):
    if index == 0:
        shades[block] = 0
    else:
        shades[block] = palette[
            1 + (index - 1) % (len(palette) - 1)
        ]

# 9. Reconstruct pattern
pixels = []

for block in blocks:
    shade = shades[block]
    pixels.extend([shade] * block_size)

# 10. Create and replace pattern_ecb.png
image = Image.frombytes(
    "L",
    (width, height),
    bytes(pixels)
)

image.save("pattern_ecb.png")

print("SUCCESS: pattern_ecb.png replaced!")
