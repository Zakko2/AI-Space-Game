import pygame
import random
import os
import sys
from pathlib import Path


# Add the 'ai_space_game' package directory to sys.path
package_directory = Path(__file__).resolve().parent.parent
sys.path.append(str(package_directory))


from ai_space_game.settings import *
from ai_space_game.player import *
from ai_space_game.enemy import *
from ai_space_game.bullet import *
from ai_space_game.star import *
from ai_space_game.starfield import *
from ai_space_game.music import *
from ai_space_game.sound import *
from ai_space_game.utils import toggle_fullscreen


# System setup, Initialize Pygame, Load images and fonts, etc...
#os.chdir("C:/Users/el_za/python_projects/AI Space Game/ai_space_game")
#sys.path.append('C:/Users/el_za/python_projects/AI Space Game/ai_space_game/images')

print("initializing pygame")
pygame.init()
pygame.mixer.init()
print("pygame started")

# Load and start the music
music = Music(MUSIC_PATH, volume=0.5)
music.play()

# Set up the display
# Get the user's display size
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Calculate the new screen dimensions
windowed_width = screen_width // 2
windowed_height = (screen_height * windowed_width) // screen_width

screen = pygame.display.set_mode((windowed_width, windowed_height))
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
background_image, (windowed_width, windowed_height))

# Load sounds
sound_explosion_001 = Sound(EXPLOSION_001_PATH, volume=0.25)
sound_explosion_002 = Sound(EXPLOSION_002_PATH, volume=0.25)
sound_shot_01 = Sound(SHOT_01_PATH, volume=0.25)
sound_shot_02 = Sound(SHOT_02_PATH, volume=0.25)
sound_shot_03 = Sound(SHOT_03_PATH, volume=0.25)
sound_shot_04 = Sound(SHOT_04_PATH, volume=0.25)

def play_random_explosion_sound():
    random_sound = random.choice([sound_explosion_001, sound_explosion_002])
    random_sound.play()

#def play_shot():
#    random_sound = random.choice([sound_explosion_001, sound_explosion_002])
#    random_sound.play()

# Set up the fonts
font_path = FONT_PATH
scaled_font_size = int(FONT_SIZE * windowed_width / windowed_width)
font = pygame.font.Font(FONT_PATH, scaled_font_size)

# Set up the sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
starfield1 = Starfield(windowed_width, windowed_height, speed=random.uniform(0.5, 1.5))
starfield2 = Starfield(windowed_width, windowed_height, speed=random.uniform(1.5, 2.5))
starfield3 = Starfield(windowed_width, windowed_height, speed=random.uniform(2.5, 3.5))

# Set up the player
player = Player(player_image, windowed_width, windowed_height, bullet_image, all_sprites, bullets)
all_sprites.add(player)

# Set up the clock
clock = pygame.time.Clock()

# Set up the intro screen loop
intro_screen_image = pygame.image.load(INTRO_SCREEN_IMAGE_PATH).convert_alpha()
intro_screen_image = pygame.transform.scale(intro_screen_image, (windowed_width, windowed_height))

# Calculate the new size of the intro screen image
intro_screen_original_width, intro_screen_original_height = intro_screen_image.get_size()
intro_screen_aspect_ratio = intro_screen_original_width / intro_screen_original_height
intro_screen_new_height = windowed_height
intro_screen_new_width = int(intro_screen_new_height * intro_screen_aspect_ratio)

# Resize the intro screen image
intro_screen_image = pygame.transform.scale(intro_screen_image, (intro_screen_new_width, intro_screen_new_height))





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
    
    # Center the intro screen image on the screen
    intro_screen_rect = intro_screen_image.get_rect()
    intro_screen_rect.center = (windowed_width // 2, windowed_height // 2)
    
    screen.blit(intro_screen_image, intro_screen_rect)
    if show_press_any_key_text:
        press_any_key_text = font.render("Press any key to start", True, WHITE)
        press_any_key_text_rect = press_any_key_text.get_rect()
        # Centered horizontally and between lower third and fourth of screen
        press_any_key_text_rect.center = (
            windowed_width // 2, (windowed_height // 3) * 2 + (windowed_height // 12))
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
    intro_screen_rect.center = (windowed_width // 2, windowed_height // 2)
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
                sound_shot_02.play()
            elif event.key == pygame.K_f:
                screen = toggle_fullscreen(screen, windowed_width, windowed_height)
            elif event.key == pygame.K_q:
                running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_UP]:
        player.move_up()
    if keys[pygame.K_DOWN]:
        player.move_down()

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
    def calculate_enemy_count(score):
        base_enemies = 10
        additional_enemies = score // 200
        return base_enemies + additional_enemies


    if len(enemies) < calculate_enemy_count(player.score):
        enemy = Enemy(
            random.randint(0, windowed_width - enemy_image.get_width()),
            random.randint(-100, -40),
            enemy_image,
            windowed_width,
            windowed_height
        )
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
    for hit in hits:
        if not hit.dead:
            hit.die() 
            player.score += 10
            play_random_explosion_sound()

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        if not hit.dead:
            player.lives -= 1        
            lives_lost_timer = pygame.time.get_ticks()  # Update the timer when a life is lost
            play_random_explosion_sound()
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
    screen.blit(lives_text, (windowed_width - lives_text.get_width() - 10, 10))

    # Show the "lives remaining" message if a life was lost in the last 2 seconds
    if pygame.time.get_ticks() - lives_lost_timer < 2000:
        lives_remaining_text = font.render("Lives remaining: " + str(player.lives), True, WHITE)
        lives_remaining_text_rect = lives_remaining_text.get_rect()
        lives_remaining_text_rect.center = (windowed_width // 2, windowed_height // 2)
        screen.blit(lives_remaining_text, lives_remaining_text_rect)

   # Draw enemy count text
    #enemy_count_text = font.render("Enemies: " + str(len(enemies)), True, WHITE)
    #enemy_count_text_rect = enemy_count_text.get_rect()
    #enemy_count_text_rect.topright = (windowed_width - 10, lives_text.get_height() + 20)
    #screen.blit(enemy_count_text, enemy_count_text_rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
print("Game exited.")