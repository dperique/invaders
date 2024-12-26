#!/usr/bin/env python3

"""
Main game logic for Space Invaders.
"""

import pygame
import random
import json
from pathlib import Path
from typing import List, Optional
from rich import print

from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE,
    MAX_BULLETS, ALIEN_SHOOT_CHANCE, ALIEN_SPEED
)
from src.game_objects import Player, Alien, Bullet, AlienBullet
from src.options import GameOptions, OptionsMenu, load_options

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
        ALIEN_SPEED = 2
        ALIEN_SHOOT_CHANCE = 0.02

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
        self.lives: int = self.options.lives
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
                alien.update_rect()
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
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT]:
                self.player.move(1)
            if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
                self.shoot()
                self.shoot_timer = 10

            if self.shoot_timer > 0:
                self.shoot_timer -= 1

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

        # Update game objects
        self.update_bullets()
        self.update_aliens()
        self.check_collisions()

        # Check if all aliens are defeated
        if not self.aliens:
            self.level_complete()

    def update_bullets(self) -> None:
        """
        Update positions of all bullets and remove those off screen
        """
        # Update player bullets
        for bullet in self.bullets[:]:
            bullet.y -= self.options.missile_speed
            bullet.update_rect()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.move()
            if bullet.y > SCREEN_HEIGHT:
                self.alien_bullets.remove(bullet)

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

    def update_aliens(self) -> None:
        """
        Update alien positions and movement direction
        """
        move_down = False
        for alien in self.aliens:
            if ((alien.x >= SCREEN_WIDTH - self.alien_sprite.get_width() and self.alien_direction > 0) or
                (alien.x <= 0 and self.alien_direction < 0)):
                move_down = True
                break

        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.y += 20
                alien.update_rect()
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

        if not self.player_invulnerable:
            # Check alien collisions with player
            for alien in self.aliens:
                if (alien.y + alien.rect.height >= self.player.y or
                    alien.rect.colliderect(self.player.rect)):
                    self.player_hit()
                    break

            # Check alien bullet collisions with player
            for bullet in self.alien_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.alien_bullets.remove(bullet)
                    self.player_hit()
                    break

    def player_hit(self) -> None:
        """
        Handle player being hit by alien or bullet
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

    def level_complete(self) -> None:
        """
        Handle level completion by resetting aliens and increasing difficulty
        """
        global ALIEN_SPEED, ALIEN_SHOOT_CHANCE
        ALIEN_SPEED *= self.options.invader_speed_increment
        ALIEN_SHOOT_CHANCE += 0.002
        self.create_aliens()
        self.alien_direction = 1
        self.bullets.clear()
        self.alien_bullets.clear()

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

        if self.paused:
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
            # Store the current event for use in the options menu
            current_event = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_o and not self.in_options_menu:
                        self.in_options_menu = True
                
                current_event = event

            if self.in_options_menu:
                # Only process the options menu if we have an event
                if current_event:
                    if self.options_menu.handle_input(current_event):
                        self.in_options_menu = False
                self.options_menu.draw()
                pygame.display.flip()  # Make sure to update the display
            else:
                self.handle_input()
                self.update()
                self.draw()

            clock.tick(FPS)