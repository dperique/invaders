#!/usr/bin/env python3

"""
Creates sprite assets for the Space Invaders game with classic-style graphics.
Run this script once to generate the necessary image files.

How to run:
    python create_assets.py
"""

import pygame
from pathlib import Path
from typing import Tuple, List

def create_player_sprite(size: Tuple[int, int], color: Tuple[int, int, int],
                        filename: str) -> None:
    """
    Create a classic Space Invaders player ship sprite

    Arg(s):
        size (Tuple[int, int]): Width and height of the sprite
        color (Tuple[int, int, int]): RGB color tuple
        filename (str): Output filename
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)

    # Draw the cannon base
    width, height = size
    base_points = [
        (0, height),
        (width, height),
        (width - 5, height - 10),
        (5, height - 10)
    ]
    pygame.draw.polygon(surface, color, base_points)

    # Draw the cannon
    cannon_width = 6
    pygame.draw.rect(surface, color,
                    (width//2 - cannon_width//2, height - 25, cannon_width, 15))

    pygame.image.save(surface, filename)

def create_alien_sprite(size: Tuple[int, int], color: Tuple[int, int, int],
                       filename: str) -> None:
    """
    Create a classic Space Invaders alien sprite

    Arg(s):
        size (Tuple[int, int]): Width and height of the sprite
        color (Tuple[int, int, int]): RGB color tuple
        filename (str): Output filename
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    width, height = size

    # Draw alien body
    body_points = [
        (width//4, height//2),
        (width//4*3, height//2),
        (width//4*3, height//4*3),
        (width//4, height//4*3)
    ]
    pygame.draw.polygon(surface, color, body_points)

    # Draw alien head
    head_points = [
        (width//2 - 15, height//2),
        (width//2 + 15, height//2),
        (width//2 + 15, height//4),
        (width//2 - 15, height//4)
    ]
    pygame.draw.polygon(surface, color, head_points)

    # Draw antennae
    pygame.draw.line(surface, color, (width//2 - 15, height//4),
                    (width//2 - 20, height//8), 2)
    pygame.draw.line(surface, color, (width//2 + 15, height//4),
                    (width//2 + 20, height//8), 2)

    pygame.image.save(surface, filename)

def create_bullet_sprite(size: Tuple[int, int], color: Tuple[int, int, int],
                        filename: str) -> None:
    """
    Create a bullet sprite
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

    # Create player sprite (green)
    create_player_sprite((50, 40), (0, 255, 0), "assets/player.png")

    # Create alien sprite (red)
    create_alien_sprite((40, 40), (255, 50, 50), "assets/alien.png")

    # Create bullet sprite (white)
    create_bullet_sprite((4, 15), (255, 255, 255), "assets/bullet.png")

if __name__ == "__main__":
    main()
    print("[green]Assets created successfully![/green]")