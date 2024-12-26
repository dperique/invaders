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
from typing import List, Tuple, Optional, Dict, Any
from rich import print
from dataclasses import dataclass
import json
import random

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
PLAYER_SPEED: int = 8
BULLET_SPEED: int = 12
ALIEN_SPEED: int = 2
ALIEN_BULLET_SPEED: int = 5
ALIEN_SHOOT_CHANCE: float = 0.02  # 2% chance per alien per second
FPS: int = 60
MAX_BULLETS: int = 10  # Maximum number of bullets allowed on screen
STARTING_LIVES: int = 3
SHOOT_DELAY: int = 10  # Delay between shots when holding spacebar (in frames)

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

@dataclass
class GameOptions:
    """
    Stores game configuration options.

    Attributes:
        missile_speed: Speed of player missiles (pixels per frame)
        lives: Number of player lives
        invader_speed_increment: How much faster invaders get after each wave (multiplier)
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

        # Draw instructions
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

        if increase:
            new_value = min(current_value + step, max_val)
        else:
            new_value = max(current_value - step, min_val)

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

class Game:
    """
    Main game class handling game logic and state
    """
    def __init__(self) -> None:
        """
        Initialize the game
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        # Load assets
        self.player_sprite = pygame.image.load("assets/player.png").convert_alpha()
        self.alien_sprite = pygame.image.load("assets/alien.png").convert_alpha()
        self.bullet_sprite = pygame.image.load("assets/bullet.png").convert_alpha()

        # Initialize options first
        self.options = load_options()
        self.options_menu = OptionsMenu(self.screen, self.options)
        self.in_options_menu = False

        # Then load high score and reset game
        self.load_high_score()
        self.reset_game()

    def reset_game(self) -> None:
        """
        Reset the game state for a new game
        """
        # Reset global speed values
        global ALIEN_SPEED, ALIEN_SHOOT_CHANCE
        ALIEN_SPEED = 2  # Reset to initial value defined in constants
        ALIEN_SHOOT_CHANCE = 0.02  # Reset to initial value defined in constants

        self.player = Player(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 60,
            self.player_sprite,
            self.player_sprite.get_rect()
        )
        self.bullets: List[Bullet] = []
        self.alien_bullets: List[AlienBullet] = []
        self.aliens: List[Alien] = []
        self.create_aliens()
        self.score: int = 0
        self.lives: int = self.options.lives  # Use lives from options
        self.game_over: bool = False
        self.alien_direction: int = 1
        self.player_invulnerable: bool = False
        self.invulnerable_timer: int = 0
        self.paused: bool = False
        self.shoot_timer: int = 0

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
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_game()
            return

        if not self.paused:
            # Move this outside the event loop for smooth movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT]:
                self.player.move(1)
            if keys[pygame.K_SPACE]:
                if self.shoot_timer <= 0:
                    self.shoot()
                    self.shoot_timer = SHOOT_DELAY

            # Update shoot timer
            if self.shoot_timer > 0:
                self.shoot_timer -= 1

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
            bullet.update_rect()
            self.bullets.append(bullet)

    def update(self) -> None:
        """
        Update game state including bullets, aliens, and collisions
        """
        if self.game_over or self.paused:
            return

        # Update invulnerability
        if self.player_invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.player_invulnerable = False

        # Update bullets with custom speed
        for bullet in self.bullets[:]:
            bullet.y -= self.options.missile_speed  # Use missile speed from options
            bullet.update_rect()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.move()
            if bullet.y > SCREEN_HEIGHT:
                self.alien_bullets.remove(bullet)

        # Update aliens and their shooting
        self.update_aliens()
        self.alien_shoot()

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

    def alien_shoot(self) -> None:
        """
        Random chance for aliens to shoot
        """
        for alien in self.aliens:
            if random.random() < ALIEN_SHOOT_CHANCE / FPS:
                bullet = AlienBullet(
                    alien.x + self.alien_sprite.get_width() // 2,
                    alien.y + self.alien_sprite.get_height(),
                    self.bullet_sprite,
                    self.bullet_sprite.get_rect()
                )
                bullet.update_rect()
                self.alien_bullets.append(bullet)

    def check_collisions(self) -> None:
        """
        Check for collisions between bullets, aliens, and player
        """
        # Bullet-alien collisions
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

        # Check if aliens reached the player or collided with player
        if not self.player_invulnerable:
            # Check alien collisions
            for alien in self.aliens:
                if (alien.y + alien.rect.height >= self.player.y or
                    alien.rect.colliderect(self.player.rect)):
                    self.player_hit()
                    break

            # Check alien bullet collisions
            for bullet in self.alien_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.alien_bullets.remove(bullet)
                    self.player_hit()
                    break

    def player_hit(self) -> None:
        """
        Handle player being hit by alien
        """
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            # Reset player position and give temporary invulnerability
            self.player.x = SCREEN_WIDTH // 2
            self.player.update_rect()
            self.player_invulnerable = True
            self.invulnerable_timer = 120  # 2 seconds at 60 FPS

    def draw(self) -> None:
        """
        Draw all game objects and UI elements
        """
        self.screen.fill(BLACK)

        # Draw player (flashing if invulnerable)
        if not self.player_invulnerable or pygame.time.get_ticks() % 200 < 100:
            self.screen.blit(self.player_sprite, (self.player.x, self.player.y))

        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet_sprite, (bullet.x, bullet.y))

        # Draw alien bullets
        for bullet in self.alien_bullets:
            self.screen.blit(self.bullet_sprite, (bullet.x, bullet.y))

        # Draw aliens
        for alien in self.aliens:
            self.screen.blit(self.alien_sprite, (alien.x, alien.y))

        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        bullet_text = font.render(f"Bullets: {len(self.bullets)}/{MAX_BULLETS}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        self.screen.blit(bullet_text, (10, 100))

        if self.game_over:
            game_over_text = font.render("GAME OVER - Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text,
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                            SCREEN_HEIGHT // 2))

        # Add pause text if paused
        if self.paused:
            font = pygame.font.Font(None, 74)
            pause_text = font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text,
                           (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                            SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self) -> None:
        """
        Main game loop
        """
        clock = pygame.time.Clock()

        while True:
            # Handle window close and pause events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Add quit on 'Q' press
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_o and not self.in_options_menu:
                        self.in_options_menu = True

            if self.in_options_menu:
                if self.options_menu.handle_input(event):
                    self.in_options_menu = False

            # Handle continuous input (movement and shooting)
            if not self.in_options_menu:
                self.handle_input()

            if self.in_options_menu:
                self.options_menu.draw()
            else:
                # Regular game update and draw
                self.update()
                self.draw()

            pygame.display.flip()
            clock.tick(FPS)

    def level_complete(self) -> None:
        """
        Handle level completion by resetting aliens and increasing difficulty
        """
        global ALIEN_SPEED, ALIEN_SHOOT_CHANCE
        ALIEN_SPEED *= self.options.invader_speed_increment  # Use speed increment from options
        ALIEN_SHOOT_CHANCE += 0.002
        self.create_aliens()
        self.alien_direction = 1
        self.bullets.clear()
        self.alien_bullets.clear()

if __name__ == "__main__":
    game = Game()
    game.run()