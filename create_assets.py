#!/usr/bin/env python3

"""
Creates basic sprite assets for the Space Invaders game.
Run this script once to generate the necessary image files.

How to run:
    python create_assets.py
"""

import pygame
from pathlib import Path
from typing import Tuple

def create_sprite(size: Tuple[int, int], color: Tuple[int, int, int], 
                 filename: str) -> None:
    """
    Create a simple sprite and save it to a file
    
    Arg(s):
        size (Tuple[int, int]): Width and height of the sprite
        color (Tuple[int, int, int]): RGB color tuple
        filename (str): Output filename
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
    pygame.image.save(surface, filename)

def main() -> None:
    """
    Create all necessary game assets
    """
    pygame.init()
    
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create player sprite (green rectangle)
    create_sprite((40, 30), (0, 255, 0), "assets/player.png")
    
    # Create alien sprite (red rectangle)
    create_sprite((30, 30), (255, 0, 0), "assets/alien.png")
    
    # Create bullet sprite (white rectangle)
    create_sprite((5, 10), (255, 255, 255), "assets/bullet.png")

if __name__ == "__main__":
    main()
    print("[green]Assets created successfully![/green]")