#!/usr/bin/env python3

"""
A classic Space Invaders game implementation using Pygame.
Control your ship with arrow keys and shoot with spacebar.
The game keeps track of high scores in a local file.

How to run:
    python space_invaders.py
"""

import pygame
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from rich import print
from dataclasses import dataclass
import json

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
PLAYER_SPEED: int = 5
BULLET_SPEED: int = 7
ALIEN_SPEED: int = 2
FPS: int = 60
MAX_BULLETS: int = 10  # Maximum number of bullets allowed on screen

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)

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

class Game:
    """
    Main game class handling game logic and state
    """
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        # Load assets
        self.player_sprite = pygame.image.load("assets/player.png").convert_alpha()
        self.alien_sprite = pygame.image.load("assets/alien.png").convert_alpha()
        self.bullet_sprite = pygame.image.load("assets/bullet.png").convert_alpha()

        self.reset_game()
        self.load_high_score()

    def reset_game(self) -> None:
        """
        Reset the game state for a new game
        """
        self.player = Player(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 60,
            self.player_sprite,
            self.player_sprite.get_rect()
        )
        self.bullets: List[Bullet] = []
        self.aliens: List[Alien] = []
        self.create_aliens()
        self.score: int = 0
        self.game_over: bool = False
        self.alien_direction: int = 1

    def load_high_score(self) -> None:
        """
        Load the high score from file
        """
        self.high_score_file = Path("high_score.json")
        if self.high_score_file.exists():
            with open(self.high_score_file, "r") as f:
                self.high_score = json.load(f)["high_score"]
        else:
            self.high_score = 0

    def save_high_score(self) -> None:
        """
        Save the high score to file
        """
        with open(self.high_score_file, "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def create_aliens(self) -> None:
        """
        Create the initial formation of aliens
        """
        for row in range(5):
            for col in range(10):
                alien = Alien(
                    50 + col * 70,
                    50 + row * 50,
                    self.alien_sprite,
                    self.alien_sprite.get_rect()
                )
                alien.update_rect()  # Initialize alien rectangle position
                self.aliens.append(alien)

    def handle_input(self) -> None:
        """
        Handle player input for movement and shooting
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.shoot()

    def shoot(self) -> None:
        """
        Create a new bullet if under the maximum limit
        """
        if len(self.bullets) < MAX_BULLETS:
            bullet = Bullet(
                self.player.x + self.player_sprite.get_width() // 2 - self.bullet_sprite.get_width() // 2,
                self.player.y,
                self.bullet_sprite,
                self.bullet_sprite.get_rect()
            )
            bullet.update_rect()  # Initialize bullet rectangle position
            self.bullets.append(bullet)

    def update(self) -> None:
        """
        Update game state including bullets, aliens, and collisions
        """
        if self.game_over:
            return

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Update aliens
        self.update_aliens()

        # Check collisions
        self.check_collisions()

        # Check if all aliens are defeated
        if not self.aliens:
            self.level_complete()

    def update_aliens(self) -> None:
        """
        Update alien positions and movement direction
        """
        move_down = False
        for alien in self.aliens:
            if (alien.x >= SCREEN_WIDTH - self.alien_sprite.get_width() and
                self.alien_direction > 0) or (alien.x <= 0 and self.alien_direction < 0):
                move_down = True
                break

        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.y += 20
                alien.rect.y = alien.y
        else:
            for alien in self.aliens:
                alien.move(self.alien_direction)

    def check_collisions(self) -> None:
        """
        Check for collisions between bullets and aliens
        """
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.aliens.remove(alien)
                    self.bullets.remove(bullet)
                    self.score += 100
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                    break

        # Check if aliens reached the player
        for alien in self.aliens:
            if alien.y + alien.rect.height >= self.player.y:
                self.game_over = True

    def draw(self) -> None:
        """
        Draw all game objects and UI elements
        """
        self.screen.fill(BLACK)

        # Draw player
        self.screen.blit(self.player_sprite, (self.player.x, self.player.y))

        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet_sprite, (bullet.x, bullet.y))

        # Draw aliens
        for alien in self.aliens:
            self.screen.blit(self.alien_sprite, (alien.x, alien.y))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))

        # Add bullet count display
        bullet_text = font.render(f"Bullets: {len(self.bullets)}/{MAX_BULLETS}", True, WHITE)
        self.screen.blit(bullet_text, (10, 70))

        if self.game_over:
            game_over_text = font.render("GAME OVER - Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text,
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                            SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self) -> None:
        """
        Main game loop
        """
        clock = pygame.time.Clock()

        while True:
            self.handle_input()

            keys = pygame.key.get_pressed()
            if self.game_over and keys[pygame.K_r]:
                self.reset_game()

            self.update()
            self.draw()
            clock.tick(FPS)

    def level_complete(self) -> None:
        """
        Handle level completion by resetting aliens and increasing difficulty
        """
        global ALIEN_SPEED
        ALIEN_SPEED += 0.1  # Make aliens move faster in next level
        self.create_aliens()
        self.alien_direction = 1
        self.bullets.clear()  # Clear any remaining bullets

if __name__ == "__main__":
    game = Game()
    game.run()