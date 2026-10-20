
from pathlib import Path
from collections import Counter
from PIL import Image

# Original image dimensions
width = 432
height = 475

# AES block size
block_size = 16

# Number of original image bytes
image_size = width * height

def investigate(filename, output_image):

    print("\nAnalyzing:", filename)

    # 1. Read the encrypted file
    data = Path(filename).read_bytes()

    print("File size:", len(data))

    # 2. Check OpenSSL signature
    if data[:8] != b"Salted__":
        raise ValueError("Invalid OpenSSL salted header")

    # 3. Remove the first 16 bytes
    ciphertext = data[16:]

    # 4. Exclude the final padding block
    image_ciphertext = ciphertext[:image_size]

    if len(image_ciphertext) != image_size:
        raise ValueError("Unexpected ciphertext size")

    # 5. Divide into 16-byte blocks
    blocks = []

    for i in range(0, len(image_ciphertext), block_size):
        block = image_ciphertext[i:i + block_size]
        blocks.append(block)

    # 6. Count the blocks
    counts = Counter(blocks)

    repeated_types = sum(
        1 for count in counts.values() if count > 1
    )

    repeated_occurrences = sum(
        count - 1 for count in counts.values() if count > 1
    )

    print("Total blocks:", len(blocks))
    print("Unique blocks:", len(counts))
    print("Repeated block types:", repeated_types)
    print("Extra repeated occurrences:", repeated_occurrences)

    # 7. Assign grayscale values to unique blocks
    sorted_blocks = sorted(
        counts,
        key=lambda block: (-counts[block], block)
    )

    shades = {}

    for index, block in enumerate(sorted_blocks):
        shades[block] = int(
            index * 255 / max(1, len(sorted_blocks) - 1)
        )

    # 8. Reconstruct the pattern
    pixels = []

    for block in blocks:
        shade = shades[block]
        pixels.extend([shade] * block_size)

    # 9. Save grayscale image
    image = Image.frombytes(
        "L",
        (width, height),
        bytes(pixels)
    )

    image.save(output_image)

    print("Saved:", output_image)

    return len(blocks), len(counts), repeated_types, repeated_occurrences


# Analyze ECB
ecb = investigate("classified.enc", "pattern_ecb.png")

# Analyze CBC
cbc = investigate("classified_cbc.enc", "pattern_cbc.png")

# Compare results
print("\n========== ECB vs CBC ==========")

print("Total blocks       : ECB =", ecb[0], "| CBC =", cbc[0])
print("Unique blocks      : ECB =", ecb[1], "| CBC =", cbc[1])
print("Repeated types     : ECB =", ecb[2], "| CBC =", cbc[2])
print("Extra repetitions  : ECB =", ecb[3], "| CBC =", cbc[3])
