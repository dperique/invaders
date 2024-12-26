<p align="center">
  <img src="logo/invaders_logo1.png" alt="Space Invaders Logo" width="400"/>
</p>

# Space Invaders

## Description

This is a simple implementation of the classic arcade game "Space Invaders".

When I used to play games, I noticed that I could think about problems in the background. I also noticed that I could train my ability to stay calm and focused to solve a problem in realtime (e.g., get out of a sticky situation vs. panicing and giving up). This skill applies well to motorcycling and driving in rush hour traffic or even fixing a problem at work where I made an error and need to correct it quickly to recover.

I'll design more things into the game like using different keys that can help me train my hands for faster trills in piano.

## Installation

1. Clone the repository
2. Run `python -m venv .venv`
3. Run `source .venv/bin/activate`
4. Run `pip install -r requirements.txt`
5. Run `python create_assets.py` to create the assets
6. Run `python space_invaders.py` to start the game

## Controls

- Left/Right: Move the player left or right
- Space: Shoot a bullet
- P: Pause the game
- O: Open options menu
- Q: Quit game
- In options menu:
  - ↑/↓: Select option
  - ←/→: Adjust value
  - ESC: Save and exit options

## Gameplay

- The player can move left and right to avoid incoming alien bullets.
- The player can shoot bullets to destroy aliens.
- The game ends when the player is hit by an alien bullet or runs out of lives.
- The game can be paused by pressing P.

## Notes