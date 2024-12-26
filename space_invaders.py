#!/usr/bin/env python3

"""
A classic Space Invaders game implementation using Pygame.
Control your ship with arrow keys and shoot with spacebar.
The game keeps track of high scores in a local file.

Controls:
    Arrow Keys: Move ship left/right
    Spacebar: Shoot
    P: Pause game
    O: Open options menu
    Q: Quit game
    R: Restart (when game over)

How to run:
    python space_invaders.py
"""

import pygame
from src.game import Game

def main() -> None:
    """
    Initialize pygame and start the game
    """
    # Initialize Pygame and its mixer
    pygame.init()
    pygame.mixer.init()

    # Create and run game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()