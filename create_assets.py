#!/usr/bin/env python3

"""
This script generates pixel art assets for the Space Invaders game.
It creates PNG files for the player, alien, and bullet sprites.
"""

from PIL import Image
import numpy as np
from pathlib import Path

def create_alien(size: tuple[int, int], color: tuple[int, int, int]) -> Image.Image:
    """
    Creates a classic Space Invaders alien sprite in the specified color.

    Arg(s):
        size (tuple[int, int]): Width and height of the sprite in pixels
        color (tuple[int, int, int]): RGB color tuple for the alien
    Return Value(s):
        Image.Image: PIL Image object containing the alien sprite
    """
    # Create a transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    pixels = img.load()

    # Classic Space Invaders alien pattern (1 represents colored pixel, 0 represents transparent)
    pattern = [
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,1,0,0,1,0,0],
        [0,1,0,1,1,0,1,0],
        [1,0,1,0,0,1,0,1]
    ]

    # Scale factor to match desired size
    scale_x = size[0] // len(pattern[0])
    scale_y = size[1] // len(pattern)

    # Draw the pattern
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            if pattern[y][x]:
                # Fill each scaled pixel
                for dx in range(scale_x):
                    for dy in range(scale_y):
                        pixels[x * scale_x + dx, y * scale_y + dy] = (*color, 255)

    return img

def main():
    """
    Creates all game assets and saves them to the assets directory.
    """
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)

    # Create red alien
    alien = create_alien((32, 32), (255, 0, 0))  # Pure red color
    alien.save(assets_dir / "alien.png")

    # Keep existing asset creation code...

if __name__ == "__main__":
    main()