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
FONT_PATH = os.path.join(BASE_DIR, "fonts", "ARCADE_I.TTF")
FONT_SIZE = 36

# Image paths
PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, "images", "player.png")
ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, "images", "enemy.png")
BULLET_IMAGE_PATH = os.path.join(BASE_DIR, "images", "bullet.png")
BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "images", "background.png")
INTRO_SCREEN_IMAGE_PATH = os.path.join(BASE_DIR, "images", "Soale Stjas.png")
PILOT_PORTRAIT_PATH = os.path.join(BASE_DIR, "images\pilot_female\character2", "sad_0.33_10_f38545eb643f41d29f8943456cb4ce6d.png")

# Music
MUSIC_PATH = os.path.join(BASE_DIR, "sounds", "Aries_Beats_-_Neon_Lights.ogg")

# Sounds
EXPLOSION_001_PATH = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0244_explosion_003_01.wav")
EXPLOSION_002_PATH = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0288_combat_drone_jet_texture_sonic_boom_003.wav")
SHOT_01_PATH       = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0284_soundwave_weapon_scifi_shot_low_001.wav")
SHOT_02_PATH       = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0286_invader_weapon_scifi_shot_002.wav")
SHOT_03_PATH       = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0286_invader_weapon_scifi_shot_007.wav")
SHOT_04_PATH       = os.path.join(BASE_DIR, "sounds", "Bluezone_BC0288_combat_drone_weapon_scifi_shot_001.wav")

# Window Caption/Game Name
GAME_NAME = 'Soale Stjas (AI Space Game)'