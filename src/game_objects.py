#!/usr/bin/env python3

"""
Game object classes for Space Invaders including Player, Alien, and Bullets.
"""

from dataclasses import dataclass
import pygame
from src.constants import (
    SCREEN_WIDTH, PLAYER_SPEED, BULLET_SPEED,
    ALIEN_SPEED, ALIEN_BULLET_SPEED
)

@dataclass
class GameObject:
    """
    Base class for game objects with position and sprite management
    """
    x: float
    y: float
    sprite: pygame.Surface
    rect: pygame.Rect

    def update_rect(self) -> None:
        """
        Update rectangle position to match current x,y coordinates
        """
        self.rect.x = self.x
        self.rect.y = self.y

class Player(GameObject):
    """
    Player class representing the spaceship controlled by the user
    """
    def move(self, direction: int) -> None:
        """
        Move the player horizontally within screen bounds

        Arg(s):
            direction (int): Direction of movement (-1 for left, 1 for right)
        """
        new_x = self.x + (direction * PLAYER_SPEED)
        if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
            self.x = new_x
            self.update_rect()

class Bullet(GameObject):
    """
    Bullet class for projectiles fired by the player
    """
    def move(self) -> None:
        """
        Move the bullet upward
        """
        self.y -= BULLET_SPEED
        self.update_rect()

class AlienBullet(GameObject):
    """
    Bullet class for projectiles fired by aliens
    """
    def move(self) -> None:
        """
        Move the bullet downward
        """
        self.y += ALIEN_BULLET_SPEED
        self.update_rect()

class Alien(GameObject):
    """
    Alien class representing enemy ships
    """
    def move(self, direction: int) -> None:
        """
        Move the alien horizontally and vertically

        Arg(s):
            direction (int): Direction of movement (-1 for left, 1 for right)
        """
        self.x += direction * ALIEN_SPEED
        self.update_rect()