import pygame
import random

# Initialize Pygame
print("initializing pygame")
pygame.init()
print("pygame started")

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
INTRO_SCREEN_DURATION = 5000  # in milliseconds
FADE_DURATION = 3000  # in milliseconds

# Get the user's display size
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Calculate the aspect ratio
aspect_ratio = screen_width / screen_height

# Set up the display
screen_height = SCREEN_HEIGHT
screen_width = round(screen_height*aspect_ratio)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Soale Stjas (AI Space Game)")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the fonts
font_path = "fonts/ARCADE_I.TTF"
font = pygame.font.Font(font_path, 36)

# Load images
player_image = pygame.image.load('images/player.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 38))

enemy_image = pygame.image.load('images/enemy.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 38))

bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (10, 20))

background_image = pygame.image.load('images/background.png').convert()
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height))

# Load the intro screen image
intro_screen_image = pygame.image.load("images/Soale Stjas.png").convert()
intro_screen_alpha = 255  # Start with full opacity
intro_screen_image = pygame.transform.scale(
    intro_screen_image, (screen_width, screen_height))
# Set the opacity of the image
intro_screen_image.set_alpha(intro_screen_alpha)


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
        self.life_lost = False
        self.life_lost_timer = 0
        self.mask = pygame.mask.from_surface(player_image)

    def update(self):
        self.rect.clamp_ip(screen.get_rect())
        self.mask = pygame.mask.from_surface(player_image)

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
        super().__init__(pygame.Surface.copy(enemy_image), x, y)
        self.speedy = random.uniform(1.0, 4.5)
        self.alpha = 0  # Start with transparency at 0
        self.image.set_alpha(self.alpha)  # Set the transparency of the image
        self.mask = pygame.mask.from_surface(enemy_image)

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

        if self.rect.top > screen_height:
            self.kill()

        self.mask = pygame.mask.from_surface(enemy_image)


class Bullet(Entity):
    def __init__(self, x, y):
        super().__init__(bullet_image, x, y)
        self.speedy = -10
        self.mask = pygame.mask.from_surface(bullet_image)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(bullet_image)


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


def toggle_fullscreen():
    global fullscreen, screen, screen_width, screen_height

    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))


# Set up the sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
starfield1 = Starfield(screen_width, screen_height,
                       speed=random.uniform(0.5, 1.5))
starfield2 = Starfield(screen_width, screen_height,
                       speed=random.uniform(1.5, 2.5))
starfield3 = Starfield(screen_width, screen_height,
                       speed=random.uniform(2.5, 3.5))


# Set up the player
player = Player()
all_sprites.add(player)

# Set up the clock
clock = pygame.time.Clock()

# Set up the intro screen loop
intro_screen_alpha = 0  # Start with the intro screen image transparent
intro_screen_start_time = pygame.time.get_ticks()
intro_screen_running = True
show_press_any_key_text = False
while intro_screen_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_screen_running = False
        elif event.type == pygame.KEYDOWN:
            intro_screen_running = False

    # Update the intro screen
    dt = clock.tick(FPS)
    if intro_screen_alpha < 255:  # Fade in
        intro_screen_alpha += 255 / FADE_DURATION * dt
        if intro_screen_alpha > 255:
            intro_screen_alpha = 255
            show_press_any_key_text = True
    # Set the opacity of the image
    intro_screen_image.set_alpha(intro_screen_alpha)

    # Draw the intro screen
    screen.fill(black)
    screen.blit(intro_screen_image, (0, 0))
    if show_press_any_key_text:
        press_any_key_text = font.render("Press any key to start", True, white)
        press_any_key_text_rect = press_any_key_text.get_rect()
        # Centered horizontally and between lower third and fourth of screen
        press_any_key_text_rect.center = (
            screen_width // 2, (screen_height // 3) * 2 + (screen_height // 12))
        screen.blit(press_any_key_text, press_any_key_text_rect)
    pygame.display.flip()

# Fade out
while intro_screen_alpha > 0:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the intro screen
    dt = clock.tick(FPS)
    intro_screen_alpha -= 255 / FADE_DURATION * dt
    if intro_screen_alpha < 0:
        intro_screen_alpha = 0
    # Set the opacity of the image
    intro_screen_image.set_alpha(intro_screen_alpha)

    # Draw the intro screen
    screen.fill(black)
    screen.blit(intro_screen_image, (0, 0))
    pygame.display.flip()


# Set up the game loop
print("Starting game...")
running = True
fullscreen = False
lives_lost_timer = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            # elif event.key == pygame.K_f:
            #    toggle_fullscreen()

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Update the game state
    starfield1.update()
    starfield2.update()
    starfield3.update()

    dt = clock.tick(FPS)
    for sprite in all_sprites:
        if isinstance(sprite, Enemy):
            sprite.update(dt)
        else:
            sprite.update()

    # Spawn enemies
    if len(enemies) < 10:
        enemy = Enemy(random.randint(0, screen_width -
                      enemy_image.get_width()), random.randint(-100, -40))
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        player.score += 10

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.lives -= 1        
        lives_lost_timer = pygame.time.get_ticks()  # Update the timer when a life is lost
        if player.lives == 0:                       
            running = False

    # Draw the screen
    screen.blit(background_image, (0, 0))
    starfield1.draw(screen)
    starfield2.draw(screen)
    starfield3.draw(screen)
    all_sprites.draw(screen)

    score_text = font.render("Score: " + str(player.score), True, white)
    screen.blit(score_text, (10, 10))

    # Lives text flashing effect
    lives_text = font.render("Lives: " + str(player.lives), True, white)
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    # Show the "lives remaining" message if a life was lost in the last 2 seconds
    if pygame.time.get_ticks() - lives_lost_timer < 2000:
        lives_remaining_text = font.render("Lives remaining: " + str(player.lives), True, white)
        lives_remaining_text_rect = lives_remaining_text.get_rect()
        lives_remaining_text_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(lives_remaining_text, lives_remaining_text_rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
print("Game exited.")

# Delay to show the game window
pygame.time.wait(2000)