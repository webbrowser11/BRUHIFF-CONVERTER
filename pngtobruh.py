from pathlib import Path
from PIL import Image
import struct
import argparse
import sys

def png_to_bruh(path: Path):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print("File not found!")
        sys.exit(1)

    img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()

    out_str = ""
    last_line = -1

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            hex_color = f"{r:02X}{g:02X}{b:02X}"
            if y != last_line:
                if last_line != -1:
                    out_str += "\n"
                last_line = y
            out_str += hex_color

    if path.suffix.lower() == ".png":
        path_to_bruh = path.with_suffix(".bruh")
    else:
        print("Input file must be a .png")
        sys.exit(1)

    with open(path_to_bruh, "wb") as file:
        file.write(struct.pack("<I", width))
        file.write(struct.pack("<I", height))
        file.write(out_str.encode("utf-8"))
        file.flush()

    print(f"Converted successfully: {path_to_bruh}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG to .bruh format.")
    parser.add_argument("path", type=Path, help="Path to the .png image")
    args = parser.parse_args()

    png_to_bruh(args.path)
