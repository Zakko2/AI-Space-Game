import pygame
import random
import os

from settings import *
from entities import Player, Enemy, Bullet, Star, Starfield
from utils import toggle_fullscreen


# System setup, Initialize Pygame, Load images and fonts, etc...
os.chdir("C:/Users/el_za/python_projects/AICastle/AI Space Game/ai_space_game")

print("initializing pygame")
pygame.init()
print("pygame started")

# Set up the display
# Get the user's display size
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Calculate the aspect ratio
aspect_ratio = screen_width / screen_height

scaled_height = SCREEN_HEIGHT
scaled_width = round(scaled_height * aspect_ratio)

scale_factor = min(screen_width / scaled_width, screen_height / scaled_height)

screen_width = round(scaled_width * scale_factor)
screen_height = round(scaled_height * scale_factor)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(GAME_NAME)

# Load images
player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 38))

enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 38))

bullet_image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (10, 20))

background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
background_image = pygame.transform.scale(
background_image, (screen_width, screen_height))

# Set up the fonts
font_path = FONT_PATH
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Set up the sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
starfield1 = Starfield(screen_width, screen_height, speed=random.uniform(0.5, 1.5))
starfield2 = Starfield(screen_width, screen_height, speed=random.uniform(1.5, 2.5))
starfield3 = Starfield(screen_width, screen_height, speed=random.uniform(2.5, 3.5))

# Set up the player
player = Player(player_image, screen_width, screen_height, bullet_image, all_sprites, bullets)
all_sprites.add(player)

# Set up the clock
clock = pygame.time.Clock()

# Set up the intro screen loop
intro_screen_image = pygame.image.load(INTRO_SCREEN_IMAGE_PATH).convert()
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
    screen.fill(BLACK)
    intro_screen_rect = intro_screen_image.get_rect()
    intro_screen_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(intro_screen_image, intro_screen_rect)
    if show_press_any_key_text:
        press_any_key_text = font.render("Press any key to start", True, WHITE)
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
    screen.fill(BLACK)
    intro_screen_rect = intro_screen_image.get_rect()
    intro_screen_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(intro_screen_image, intro_screen_rect)
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
        enemy = Enemy(random.randint(0, screen_width - enemy_image.get_width()), random.randint(-100, -40), enemy_image, screen_width, screen_height)
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

    score_text = font.render("Score: " + str(player.score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Lives text flashing effect
    lives_text = font.render("Lives: " + str(player.lives), True, WHITE)
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    # Show the "lives remaining" message if a life was lost in the last 2 seconds
    if pygame.time.get_ticks() - lives_lost_timer < 2000:
        lives_remaining_text = font.render("Lives remaining: " + str(player.lives), True, WHITE)
        lives_remaining_text_rect = lives_remaining_text.get_rect()
        lives_remaining_text_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(lives_remaining_text, lives_remaining_text_rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
print("Game exited.")