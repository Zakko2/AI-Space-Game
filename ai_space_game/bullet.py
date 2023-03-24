import pygame
import random
from ai_space_game.settings import *
from ai_space_game.entity import *

class Bullet(Entity):
    def __init__(self, x, y, image, screen_width, screen_height):
        self.image = image
        super().__init__(image, x, y)        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speedy = -10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)