import unittest
import pygame
import os
import sys
from pathlib import Path

# Add the 'ai_space_game' package directory to sys.path
package_directory = Path(__file__).resolve().parent.parent
sys.path.append(str(package_directory))

from ai_space_game.entities import Player
from ai_space_game.settings import *

class TestPlayer(unittest.TestCase):
    def test_movement(self):
        # Set up the test environment
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        # Create a Player instance
        PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, "images", "player.png")
        ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, "images", "enemy.png")
        BULLET_IMAGE_PATH = os.path.join(BASE_DIR, "images", "bullet.png")
        BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "images", "background.png")
        INTRO_SCREEN_IMAGE_PATH = os.path.join(BASE_DIR, "images", "Soale Stjas.png")
        
        # Create a Player instance
        player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        bullet_image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        player = Player(player_image, 800, 600, bullet_image, all_sprites, bullets)

        

        # Test movement
        initial_x = player.rect.x
        player.move_left()
        self.assertEqual(player.rect.x, initial_x - player.speed)
        player.move_right()
        self.assertEqual(player.rect.x, initial_x)

if __name__ == '__main__':
    unittest.main()
