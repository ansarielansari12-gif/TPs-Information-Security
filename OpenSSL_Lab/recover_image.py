
from pathlib import Path
from PIL import Image

# Original image dimensions
width = 432
height = 475

# Read decrypted pixel data
data = Path("recovered.raw").read_bytes()

# Verify the size
print("Recovered bytes:", len(data))
print("Expected bytes:", width * height)

if len(data) != width * height:
    raise ValueError("Incorrect image size!")

# Create grayscale image
image = Image.frombytes("L", (width, height), data)

# Save as PNG
image.save("recovered.png")

print("SUCCESS: recovered.png created!")
