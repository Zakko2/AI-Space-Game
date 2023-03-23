import pygame
import random
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Player(pygame.sprite.Sprite):
    """
    The Player class represents the player's spaceship in the game. It is responsible for
    managing the player's position, movement, shooting, and collision detection. The player
    can move left and right, shoot bullets, and collide with other game objects.

    Attributes:
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        bullet_image (Surface): The image used for the player's bullets.
        all_sprites (Group): The sprite group containing all game sprites.
        bullets (Group): The sprite group containing the player's bullets.
        image (Surface): The image used for the player's spaceship.
        rect (Rect): The rectangular area representing the player's spaceship.
        speed (int): The player's movement speed.
        score (int): The player's current score.
        lives (int): The player's current lives.
        fire_timer (int): A timer used to control the player's shooting rate.
        life_lost (bool): A flag indicating if the player has just lost a life.
        life_lost_timer (int): A timer used to handle the player's respawn delay.
        mask (Mask): A mask used for precise collision detection.
    """
    def __init__(self, image, screen_width, screen_height, bullet_image, all_sprites, bullets):
        super().__init__()
        self.screen_width = screen_width        # Store screen width
        self.screen_height = screen_height      # Store screen height
        self.bullet_image = bullet_image        # Store bullet image
        self.all_sprites = all_sprites          # Store all sprite groups
        self.bullets = bullets                  # Store bullet sprite group
        self.image = image                      # Set player image
        self.rect = self.image.get_rect()       # Get player image's rectangle
        self.rect.centerx = screen_width // 2   # Set player's horizontal starting position
        self.rect.bottom = screen_height - 10   # Set player's vertical starting position
        self.speed = 8                          # Set player's speed
        self.score = 0                          # Initialize player's score
        self.lives = 3                          # Initialize player's lives
        self.fire_timer = 0                     # Initialize fire timer
        self.life_lost = False                  # Initialize life lost flag
        self.life_lost_timer = 0                # Initialize life lost timer
        self.mask = pygame.mask.from_surface(image)  # Create a mask for collision detection

    def update(self):
        # Keep the player inside the screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))
        # Update the player's mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def move_left(self):
        # Move the player to the left by the defined speed
        self.rect.x -= self.speed

    def move_right(self):
        # Move the player to the right by the defined speed
        self.rect.x += self.speed

    def can_fire(self):
        # Check if enough time has passed since the last shot
        time_since_last_fire = pygame.time.get_ticks() - self.fire_timer
        if time_since_last_fire >= 1000 / 3:  # 3 shots per second
            self.fire_timer = pygame.time.get_ticks()
            return True
        else:
            return False

    def shoot(self):
        # If the player is allowed to fire, create a bullet and add it to the sprite groups
        if self.can_fire():
            bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_image, self.screen_width, self.screen_height)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

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

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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