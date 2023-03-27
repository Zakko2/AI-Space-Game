import pygame
from ai_space_game.settings import *
from ai_space_game.entity import *
from ai_space_game.bullet import *

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

    def move_up(self):
        # Move the player up by the defined speed
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self):
        # Move the player down by the defined speed
        self.rect.y += self.speed
        if self.rect.y > self.screen_height - self.rect.height:
            self.rect.y = self.screen_height - self.rect.height

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