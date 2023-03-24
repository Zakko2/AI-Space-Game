import unittest
import pygame
import os
import sys
from pathlib import Path

# Add the 'ai_space_game' package directory to sys.path
package_directory = Path(__file__).resolve().parent.parent
sys.path.append(str(package_directory))

from ai_space_game.player import Player
from ai_space_game.settings import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, "images", "player.png")
        BULLET_IMAGE_PATH = os.path.join(BASE_DIR, "images", "bullet.png")

        player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        bullet_image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.player = Player(player_image, 800, 600, bullet_image, self.all_sprites, self.bullets)

    def test_movement_horizontal(self):
        initial_x = self.player.rect.x
        self.player.move_left()
        self.assertEqual(self.player.rect.x, initial_x - self.player.speed)
        self.player.move_right()
        self.assertEqual(self.player.rect.x, initial_x)

    def test_movement_vertical(self):
        initial_y = self.player.rect.y
        self.player.move_up()
        self.assertEqual(self.player.rect.y, initial_y - self.player.speed)
        self.player.move_down()
        self.assertEqual(self.player.rect.y, initial_y)

    def test_shooting(self):
        self.player.shoot()
        self.assertEqual(len(self.bullets.sprites()), 1)

    def test_boundaries(self):
        self.player.rect.x = -100
        self.player.update()
        self.assertEqual(self.player.rect.x, 0)

        self.player.rect.y = -100
        self.player.update()
        self.assertEqual(self.player.rect.y, 0)

        self.player.rect.x = 900
        self.player.update()
        self.assertEqual(self.player.rect.x, self.screen.get_width() - self.player.rect.width)

        self.player.rect.y = 700
        self.player.update()
        self.assertEqual(self.player.rect.y, self.screen.get_height() - self.player.rect.height)

    def test_lives_decrementing(self):
        initial_lives = self.player.lives
        self.player.lives -= 1
        self.assertEqual(self.player.lives, initial_lives - 1)

    def test_score_incrementing(self):
        initial_score = self.player.score
        self.player.score += 100
        self.assertEqual(self.player.score, initial_score + 100)

    def test_shooting_rate_limiting(self):
        self.player.shoot()
        self.assertEqual(len(self.bullets.sprites()), 1)
        self.player.shoot()
        self.assertEqual(len(self.bullets.sprites()), 1)  # Should still be 1, because of rate limiting

        pygame.time.delay(350)  # Wait 350ms (a bit more than 1/3 of a second)
        self.player.shoot()
        self.assertEqual(len(self.bullets.sprites()), 2)

if __name__ == '__main__':
    unittest.main()