import pygame
import random
from ai_space_game.settings import *
from ai_space_game.entity import *

class Enemy(Entity):
    def __init__(self, x, y, image, screen_width, screen_height):
        self.image = image
        super().__init__(pygame.Surface.copy(image), x, y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speedy = random.uniform(1.0, 4.5)
        self.alpha = 0  # Start with transparency at 0
        self.image.set_alpha(self.alpha)  # Set the transparency of the image
        self.mask = pygame.mask.from_surface(image)
        self.dead = False
        self.angle = 0
        self.spin_speed = random.randint(2, 4)
        self.downward_speed = random.uniform(1, 3)        

    def die(self):
        self.dead = True

    def update(self, dt):
        self.rect.y += self.speedy
        if self.alpha < 255:  # Increase transparency gradually
            # Calculate alpha change based on elapsed time
            alpha_change = int(255 * (dt / 500.0))
            self.alpha += alpha_change
            if self.alpha > 255:
                self.alpha = 255
            # Set the transparency of the image
            self.image.set_alpha(self.alpha)

        if self.rect.top > self.screen_height:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)

        if self.dead:
            self.angle += self.spin_speed
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y += self.downward_speed

            self.alpha -= 255 / (2 * 1000) * dt
            if self.alpha < 0:
                self.kill()
            else:
                self.image.set_alpha(self.alpha)