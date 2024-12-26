#!/usr/bin/env python3

"""
Constants used throughout the Space Invaders game.
"""

from typing import Tuple

# Screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Game mechanics
PLAYER_SPEED: int = 8
BULLET_SPEED: int = 12
ALIEN_SPEED: int = 2
ALIEN_BULLET_SPEED: int = 5
ALIEN_SHOOT_CHANCE: float = 0.02
MAX_BULLETS: int = 10
STARTING_LIVES: int = 3
SHOOT_DELAY: int = 10

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)