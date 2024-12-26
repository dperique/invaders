#!/usr/bin/env python3

"""
Game options management for Space Invaders.
"""

import json
import pygame
from dataclasses import dataclass
from typing import Tuple

@dataclass
class GameOptions:
    """
    Stores game configuration options.

    Attributes:
        missile_speed: Speed of player missiles (pixels per frame)
        lives: Number of player lives
        invader_speed_increment: How much faster invaders get after each wave
    """
    missile_speed: float = 10.0
    lives: int = 3
    invader_speed_increment: float = 1.2

class OptionsMenu:
    """
    Handles the options menu interface and settings.
    """
    def __init__(self, screen: pygame.Surface, options: GameOptions):
        """
        Initialize the options menu.

        Args:
            screen: Pygame surface to draw on
            options: Current game options
        """
        self.screen = screen
        self.options = options
        self.font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options_list = [
            ("Missile Speed", "missile_speed", 5.0, 20.0, 1.0),
            ("Lives", "lives", 1, 5, 1),
            ("Invader Speed Increment", "invader_speed_increment", 1.0, 2.0, 0.1)
        ]

    def draw(self) -> None:
        """
        Draw the options menu on the screen.
        """
        self.screen.fill((0, 0, 0))
        title = self.font.render("OPTIONS MENU", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        for i, (label, attr, min_val, max_val, step) in enumerate(self.options_list):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            value = getattr(self.options, attr)
            text = f"{label}: {value:.1f}" if isinstance(value, float) else f"{label}: {value}"
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text_surface, text_rect)

        instructions = self.font.render("↑↓: Select  ←→: Adjust  ESC: Save & Exit", True, (128, 128, 128))
        inst_rect = instructions.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(instructions, inst_rect)

    def handle_input(self, event: pygame.event) -> bool:
        """
        Handle input events for the options menu.

        Args:
            event: Pygame event to process

        Returns:
            bool: True if should exit options menu, False otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save_options()
                return True
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options_list)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options_list)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.adjust_value(event.key == pygame.K_RIGHT)
        return False

    def adjust_value(self, increase: bool) -> None:
        """
        Adjust the selected option value.

        Args:
            increase: True to increase value, False to decrease
        """
        label, attr, min_val, max_val, step = self.options_list[self.selected_option]
        current_value = getattr(self.options, attr)
        new_value = min(current_value + step, max_val) if increase else max(current_value - step, min_val)
        setattr(self.options, attr, new_value)

    def save_options(self) -> None:
        """
        Save the current options to a file.
        """
        options_dict = {
            "missile_speed": self.options.missile_speed,
            "lives": self.options.lives,
            "invader_speed_increment": self.options.invader_speed_increment
        }
        with open("game_options.json", "w") as f:
            json.dump(options_dict, f)

def load_options() -> GameOptions:
    """
    Load game options from file or return defaults if file doesn't exist.

    Returns:
        GameOptions: Loaded or default game options
    """
    try:
        with open("game_options.json", "r") as f:
            options_dict = json.load(f)
            return GameOptions(**options_dict)
    except (FileNotFoundError, json.JSONDecodeError):
        return GameOptions()