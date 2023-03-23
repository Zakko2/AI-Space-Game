import sys
sys.path.append('C:/Users/el_za/python_projects/AICastle/AI Space Game/ai_space_game/tests')

import unittest
import pygame

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
        player_image = pygame.image.load("../images/player.png").convert_alpha()
        bullet_image = pygame.image.load("../images/bullet.png").convert_alpha()
        player = Player(player_image, 800, 600, bullet_image, all_sprites, bullets)

        # Test movement
        initial_x = player.rect.x
        player.move_left()
        self.assertEqual(player.rect.x, initial_x - player.speed)
        player.move_right()
        self.assertEqual(player.rect.x, initial_x)

if __name__ == '__main__':
    unittest.main()
