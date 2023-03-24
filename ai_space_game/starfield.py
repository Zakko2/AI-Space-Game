import pygame
import random
from ai_space_game.settings import *
from ai_space_game.star import *

class Starfield:
    def __init__(self, screen_width, screen_height, speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.stars = pygame.sprite.Group()

        # Create the stars
        for i in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            star = Star(x, y)
            self.stars.add(star)

    def update(self):
        # Move the stars down
        for star in self.stars:
            star.rect.y += self.speed

            # If the star goes off the bottom of the screen, wrap it around to the top
            if star.rect.top > self.screen_height:
                star.rect.y = random.randint(-10, 0)

    def draw(self, screen):
        self.stars.draw(screen)