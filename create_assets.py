#!/usr/bin/env python3

"""
This script creates all sprite assets for the Space Invaders game.
It generates PNG files for:
- Player ship (green pyramid shape)
- Alien (red classic space invader)
- Bullet (white rectangle)

Run this script before playing the game to ensure all assets are available.
"""

import pygame
import numpy as np
from pathlib import Path

def create_player_sprite(width: int = 60, height: int = 40) -> None:
    """
    Creates a pixelated player sprite that looks like a symmetrical pyramid shape.

    Arg(s):
        width (int): Width of the sprite in pixels
        height (int): Height of the sprite in pixels
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    pixel_width = width // 5
    pixel_height = height // 3

    shape = np.array([
        [0, 0, 1, 0, 0],  # Top pixel
        [0, 1, 1, 1, 0],  # Middle row
        [1, 1, 1, 1, 1],  # Base row
    ])

    for y in range(3):
        for x in range(5):
            if shape[y][x]:
                pygame.draw.rect(
                    surface,
                    (0, 255, 0),  # Bright green color
                    (x * pixel_width, y * pixel_height, pixel_width, pixel_height)
                )

    pygame.image.save(surface, "assets/player.png")

def create_alien_sprite(width: int = 32, height: int = 32) -> None:
    """
    Creates a classic Space Invaders alien sprite in red color.

    Arg(s):
        width (int): Width of the sprite in pixels
        height (int): Height of the sprite in pixels
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Classic Space Invaders alien pattern
    shape = np.array([
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,1,0,0,1,0,0],
        [0,1,0,1,1,0,1,0],
        [1,0,1,0,0,1,0,1]
    ])

    pixel_width = width // shape.shape[1]
    pixel_height = height // shape.shape[0]

    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y][x]:
                pygame.draw.rect(
                    surface,
                    (255, 0, 0),  # Red color
                    (x * pixel_width, y * pixel_height, pixel_width, pixel_height)
                )

    pygame.image.save(surface, "assets/alien.png")

def create_bullet_sprite(width: int = 4, height: int = 10) -> None:
    """
    Creates a simple bullet sprite as a white rectangle.

    Arg(s):
        width (int): Width of the sprite in pixels
        height (int): Height of the sprite in pixels
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(
        surface,
        (255, 255, 255),  # White color
        (0, 0, width, height)
    )
    pygame.image.save(surface, "assets/bullet.png")

def main() -> None:
    """
    Creates all game assets and saves them to the assets directory.
    """
    # Create assets directory if it doesn't exist
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)

    pygame.init()
    create_player_sprite()
    create_alien_sprite()
    create_bullet_sprite()
    pygame.quit()

if __name__ == "__main__":
    main()