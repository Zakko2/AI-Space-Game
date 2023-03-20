import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the fonts
font = pygame.font.Font(None, 36)

# Load images
player_image = pygame.image.load('player.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 38))

enemy_image = pygame.image.load('enemy.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 38))

bullet_image = pygame.image.load('bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (10, 20))


# Define the classes
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
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5
        self.score = 0
        self.lives = 3
        self.fire_timer = 0

    def update(self):
        self.rect.clamp_ip(screen.get_rect())

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def can_fire(self):
        time_since_last_fire = pygame.time.get_ticks() - self.fire_timer
        if time_since_last_fire >= 1000 / 3:  # 3 shots per second
            self.fire_timer = pygame.time.get_ticks()
            return True
        else:
            return False

    def shoot(self):
        if self.can_fire():
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(enemy_image, x, y)
        self.speedy = random.randint(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height:
            self.kill()

class Bullet(Entity):
    def __init__(self, x, y):
        super().__init__(bullet_image, x, y)
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Set up the sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Set up the player
player = Player()
all_sprites.add(player)

# Set up the clock
clock = pygame.time.Clock()

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.shoot()

    # Update the game state
    all_sprites.update()

    # Spawn enemies
    if len(enemies) < 10:
        enemy = Enemy(random.randint(0, screen_width - enemy_image.get_width()), random.randint(-100, -40))
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        player.score += 10

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.lives -= 1
        if player.lives == 0:
            running = False

    # Draw the screen
    screen.fill(black)
    all_sprites.draw(screen)
    score_text = font.render("Score: " + str(player.score), True, white)
    screen.blit(score_text, (10, 10))
    lives_text = font.render("Lives: " + str(player.lives), True, white)
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

def toggle_fullscreen():
    global fullscreen, screen, screen_width, screen_height

    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))

# Quit Pygame
pygame.quit()


# Delay to show the game window
pygame.time.wait(2000)