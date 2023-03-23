import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Intro screen settings
INTRO_SCREEN_DURATION = 5000  # in milliseconds
FADE_DURATION = 3000  # in milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font settings
FONT_PATH = "fonts/ARCADE_I.TTF"
FONT_SIZE = 36

# Image paths
PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, "images", "player.png")
ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, "images", "enemy.png")
BULLET_IMAGE_PATH = os.path.join(BASE_DIR, "images", "bullet.png")
BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "images", "background.png")
INTRO_SCREEN_IMAGE_PATH = os.path.join(BASE_DIR, "images", "Soale Stjas.png")

# Window Caption/Game Name
GAME_NAME = 'Soale Stjas (AI Space Game)'